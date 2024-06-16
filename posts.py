from fastapi import  HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse

import main
import security
from schemas import CreatePost, UpdatePost

post_router = APIRouter(tags=["posts"])


@post_router.post("/create_post")
def create_post(create_post_data: CreatePost, current_user=Depends(security.get_current_user)):
    user_id = dict(current_user).get("user_id")
    main.cursor.execute("""INSERT INTO posts (title, content, user_id)
    VALUES (%s, %s, %s)""",
                        (create_post_data.title, create_post_data.content, user_id))
    main.conn.commit()

    return JSONResponse(content={"message": "OK"})


@post_router.delete("/delete_post/{post_id}")
def delete_post(post_id: int, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")

    main.cursor.execute("""DELETE FROM posts WHERE post_id = %s AND user_id = %s""",
                        (post_id,
                         user_id))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Your post successfully deleted"})


@post_router.put("/update_post/{post_id}")
def update_post(post_id: int, update_post_data: UpdatePost, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")

    main.cursor.execute("""SELECT * FROM posts WHERE post_id = %s AND user_id = %s""", (post_id, user_id))
    post = main.cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Post not found or you don't have permission")

    main.cursor.execute("""UPDATE posts SET title = %s, content = %s WHERE post_id = %s AND user_id = %s""",
                        (update_post_data.title,
                         update_post_data.content,
                         post_id, user_id))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Post updated successfully"})


@post_router.get("/get_post/{post_id}")
def get_post(post_id: int, current_user=Depends(security.get_current_user)):
    current_user = dict(current_user)
    user_id = current_user.get("user_id")

    main.cursor.execute("""SELECT * FROM posts WHERE post_id = %s AND user_id = %s""",
                        (post_id,
                         user_id))

    post = main.cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found or you don't have permission")

    return post



