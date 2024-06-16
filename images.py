# import os
# import shutil
# import datetime
# from fastapi import File, UploadFile, APIRouter, HTTPException, status, Depends
# from fastapi.responses import JSONResponse
# import psycopg2
# import main
# import security
#
#
# image_router = APIRouter(tags=["image"], prefix="/image")
#
#
# @image_router.post("/upload_profile_photo")
# def upload_main_photo(image: UploadFile = File(...), current_user=Depends(security.get_current_user)):
#     time = (datetime.datetime.utcnow().strftime('%B %d %Y - %H_%M_%S'))
#     image_url = f"{os.getcwd()}/static/images/{time}{image.filename}"
#
#     user_id = dict(current_user).get("user_id")
#     try:
#         main.cursor.execute("""SELECT user_id FROM users WHERE user_id = %s""",
#                             (user_id,))
#         user_id_checked = main.cursor.fetchone()
#
#     except Exception as error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail={"ERROR:": error})
#
#     if user_id_checked is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User by {user_id} id not found")
#
#     try:
#
#         main.cursor.execute("""UPDATE users SET profile_photo = %s WHERE user_id = %s""",
#                             (image_url, user_id))
#
#         main.conn.commit()
#     except Exception as error:
#         main.conn.rollback()
#         return HTTPException(status_code=500,
#                              detail={"ERROR": error})
#
#     with open(image_url, "wb") as file_object:
#
#         shutil.copyfileobj(image.file, file_object)
#
#     return JSONResponse(status_code=status.HTTP_200_OK,
#                         content={"message": "Image uploaded successfully"})
#
#
# @image_router.delete("/delete_profile_image/")
# def delete_profile_image(current_user=Depends(security.get_current_user)):
#     user_id = dict(current_user).get("user_id")
#     try:
#         main.cursor.execute("""SELECT user_id FROM users WHERE user_id = %s""",
#                             (user_id,))
#
#         user_checked = main.conn.fileno()
#     except Exception as error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail={"error:": {error}})
#
#     if user_checked is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail={"message": f"User by {user_id} id not found"})
#
#     try:
#         main.cursor.execute("""UPDATE users SET profile_photo = %s WHERE user_id = %s""",
#                             (image_url, user_id))
#
#     except Exception:
#         pass
#
#
# @image_router.post("/upload_image")
# def upload_images(image: UploadFile = File(...), current_user=Depends(security.get_current_user)):
#     user_id = dict(current_user).get("user_id")
#     try:
#         image_data = image.file.read()
#
#         main.cursor.execute("""INSERT INTO users_images (image, user_id)
#                             VALUES (%s,%s)""",
#                             (psycopg2.Binary(image_data), user_id))
#
#         main.conn.commit()
#
#     except Exception as error:
#         main.conn.rollback()
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail={"error:": error})
#
#     return JSONResponse(status_code=status.HTTP_200_OK,
#                         content={"message": "Image uploaded successfully"})
#
#
# @image_router.delete("/delete_image/{image_id}")
# def delete_image(image_id: int, current_user=Depends(security.get_current_user)):
#     user_id = dict(current_user).get("user_id")
#     try:
#         main.cursor.execute("""SELECT image_id FROM users_images WHERE image_id =%s AND user_id=%s""",
#                             (image_id, user_id))
#     except Exception as error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail={"error:": error})
#
#     target_image = main.cursor.fetchone()
#     if target_image is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail={"message": f"Image by {image_id} id not found"})
#
#     try:
#         main.cursor.execute("""DELETE FROM users_images WHERE image_id=%s AND user_id=%s""",
#                             (image_id, user_id))
#
#         main.conn.commit()
#
#     except Exception as error:
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#                             detail={"error:": error})
#
#     return JSONResponse(status_code=status.HTTP_200_OK,
#                         content={"message": "Image successfully deleted"})
#
#
#
