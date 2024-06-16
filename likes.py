from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse

import main
import security


like_router = APIRouter(tags=["likes"])


@like_router.post("/like/{post_id}")
def like(post_id: int, current_user=Depends(security.get_current_user)):
    main.cursor.execute("""SELECT post_id FROM posts WHERE post_id=%s""",
                        (str(post_id),))

    post_id_checked = main.cursor.fetchone()

    if post_id_checked is not None:
        user_id = dict(current_user).get("user_id")

        main.cursor.execute("""SELECT user_id FROM likes WHERE post_id=%s AND user_id=%s""",
                            (str(post_id), str(user_id)))
        user_id_checked = main.cursor.fetchone()

        if user_id_checked is None:
            main.cursor.execute("""INSERT INTO likes (post_id, user_id)
                                VALUES (%s, %s)""",
                                (str(post_id), str(user_id)))
            main.conn.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "OK"})

        else:
            main.cursor.execute("""DELETE FROM likes WHERE post_id = %s AND user_id = %s""",
                                (post_id,
                                 user_id))
            main.conn.commit()
            return JSONResponse(status_code=status.HTTP_200_OK,
                                content={"message": "Your like has been removed"})

    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id {post_id} not found!")


@like_router.get("/all_likes_for_one_post/{post_id}")
def all_likes_for_one_post(post_id: int, current_user=Depends(security.get_current_user)):
    main.cursor.execute("""SELECT post_id FROM posts WHERE post_id=%s""",
                        (str(post_id),))

    post_id_checked = main.cursor.fetchone()

    if post_id_checked is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post in id {post_id} not found ")

    main.cursor.execute("""SELECT * FROM likes WHERE post_id=%s""",
                        (post_id,))

    likes_data = main.cursor.fetchall()

    return likes_data





