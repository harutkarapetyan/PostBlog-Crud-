from fastapi import HTTPException, status, Depends, APIRouter
from fastapi.responses import JSONResponse
from schemas import UpdateSettings
import main
import security


setting_router = APIRouter(tags=["settings"])


@setting_router.get("/get-possible-settings")
def get_possible_settings(current_user=Depends(security.get_current_user)):
    main.cursor.execute("""SELECT * FROM possible_settings""")

    possible_settings = main.cursor.fetchall()

    return possible_settings


@setting_router.put("/update_settings")
def make_settings(setting_data: UpdateSettings, current_user=Depends(security.get_current_user)):
    user_id = dict(current_user).get("user_id")
    main.cursor.execute("""UPDATE user_settings SET language=%s, background_color=%s, font_size=%s WHERE user_id=%s """,
                        (setting_data.language, setting_data.background_color, setting_data.font_size, user_id))

    main.conn.commit()

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": "Your settings successfully updated"})






