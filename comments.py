from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from schemas import CreateComment, UpdateComment
import main
import security

comment_router = APIRouter(tags=["comments"])


@comment_router.post("/create_comment/{post_id}")
def create_comment(post_id: int, comment_data: CreateComment,  current_user=Depends(security.get_current_user)):
    main.cursor.execute("""SELECT post_id FROM posts WHERE post_id=%s""",
                        (post_id,))

    post_id_checked = main.cursor.fetchone()

    if post_id_checked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail={"message": "Post not found!"})

    user_id = dict(current_user).get("user_id")

    main.cursor.execute("""INSERT INTO comments (text, user_id, post_id) VALUES (%s, %s, %s)""",
                        (comment_data.text, user_id, post_id))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Your comment successfully created"})


@comment_router.delete("/delete_comment/{comment_id}")
def delete_comment(comment_id: int, current_user=Depends(security.get_current_user)):
    main.cursor.execute("""SELECT comment_id FROM comments WHERE comment_id=%s""",
                        (comment_id,))

    comment_id_checked = main.cursor.fetchone()

    if comment_id_checked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No comment with {comment_id} ids found")

    user_id = dict(current_user).get("user_id")
    main.cursor.execute("""SELECT user_id FROM comments WHERE comment=%s AND user_id=%s""",
                        (comment_id, user_id))

    user_id_checked = main.cursor.fetchone()
    if user_id_checked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"You cannot delete a comment because you did not write it")

    main.cursor.execute("""DELETE FROM comments WHERE comment_id = %s AND user_id = %s""",
                        (comment_id,
                            user_id))
    main.conn.commit()
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Your comment has been successfully deleted"})


@comment_router.get("/all_comments_for_one_post/{post_id}")
def get_all_comments_for_one_post(post_id: int, current_user=Depends(security.get_current_user)):
    main.cursor.execute("""SELECT post_id FROM posts WHERE post_id = %s""",
                        (post_id,))

    post_id_checked = main.cursor.fetchone()
    if post_id_checked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with {post_id} ids found")

    main.cursor.execute("""SELECT * FROM comments WHERE post_id = %s""",
                        (post_id,))

    comments_data = main.cursor.fetchall()

    return comments_data


@comment_router.put("/update_comment/{comment_id}")
def update_comment(comment_id: int, comment_data: UpdateComment, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")

    main.cursor.execute("""SELECT * FROM comments WHERE comment_id= %s AND user_id = %s""",
                        (comment_id, user_id))

    target_comment = main.cursor.fetchone()

    if target_comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Comment not found")

    main.cursor.execute("""UPDATE comments SET  text = %s WHERE comment_id = %s AND user_id = %s""",
                        (comment_data.text,
                         comment_id, user_id))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Comment updated successfully"})













