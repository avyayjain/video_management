import logging
import os
import shutil

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File

from src.common.utils.constants import UPLOAD_FOLDER
from src.common.utils.generate_error_details import generate_details
from src.common.utils.user_defined_errors import UserErrors
from src.db.functions.video_functions import find_video, remove_thumbnail
from src.resources.token import UserBase, get_current_active_user

video_editing_router = APIRouter()


@video_editing_router.post("/thumbnail/{video_id}")
async def upload_thumbnail(
        video_id: str, thumbnail: UploadFile = File(...), current_user: UserBase = Depends(get_current_active_user)
):
    try:
        filename, title, thumbnail_name = find_video(video_id, current_user.user_id)

        if filename is None:
            raise UserErrors("Video not found", "VideoNotFound", 404)

        else:
            remove_thumbnail(thumbnail_name)
            thumbnail_path = os.path.join(UPLOAD_FOLDER, title, "thumbnail_" + thumbnail.filename + ".jpg")
            with open(thumbnail_path, "wb") as buffer:
                shutil.copyfileobj(thumbnail.file, buffer)

    except UserErrors as e:
        error_msg = (
                "\n video  {} \n ".format(str(video_id)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "video" + str(video_id) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": "Thumbnail updated successfully"}
