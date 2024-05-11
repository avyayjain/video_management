import os
from tempfile import NamedTemporaryFile
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import FileResponse
from pydantic import BaseModel
from src.common.utils.generate_error_details import generate_details
from src.common.utils.generate_logs import logging
from src.common.utils.user_defined_errors import UserErrors
from src.db.functions.video_crud import upload_video_detail, get_video_detail, get_video_detail_by_id, \
    get_videos_detail, delete_video, update_video_detail, get_video_detail_by_name
from src.db.functions.video_functions import extract_video_metadata, store_video
from src.resources.token import UserBase, get_current_active_user

video_router = APIRouter()


class VideoInfo(BaseModel):
    title: str
    description: str

    @classmethod
    def as_form(cls, title: str = Form(...), description: str = Form(...)) -> 'VideoInfo':
        return cls(title=title, description=description)


class UpdateItem(BaseModel):
    title: str
    description: str


@video_router.post("/video_upload")
async def video_upload(data: VideoInfo = Depends(VideoInfo.as_form), video: UploadFile = File(...),
                       current_user: UserBase = Depends(get_current_active_user)):
    try:
        with NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(await video.read())
            file_path = tmp_file.name

        duration, resolution, format = extract_video_metadata(file_path)

        filename, thumbnail_path = store_video(video, title=data.title)
        os.unlink(file_path)

        user_id = current_user.user_id

        video_det = upload_video_detail(data.title, data.description, duration, resolution, format,
                                        user_id, filename, thumbnail_path)

    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(data.title)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "Item" + str(data.title) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": "You have successfully uploaded the video ", "video details": [video_det]}, \
           FileResponse(f"uploads/{filename}", media_type="video/mp4")


@video_router.put("/update_item_details/{video_id}")
async def update_item_details(
        video_id, data: UpdateItem, current_user: UserBase = Depends(get_current_active_user)
):
    try:
        filename = update_video_detail(video_id, data.title, data.description, current_user.user_id)

    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(video_id)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)
    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(video_id)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "Item" + str(video_id) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": "video details updated successfully", "item_id": video_id}, \
           FileResponse(f"uploads/{filename}", media_type="video/mp4")


@video_router.get("/get_all_details")
async def get_all_video_details():
    try:
        video_det = get_video_detail()
    except Exception as e:
        error_msg = (
            f"error +  + {e.message}"
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    return {
        "All videos details :": video_det
    }


@video_router.get("/get_video_detail_by_id/{video_id}")
async def get_video_details_id(
        video_id, current_user: UserBase = Depends(get_current_active_user)
):
    try:
        try:
            video, filename = get_video_detail_by_id(video_id, current_user.user_id)
        except UserErrors as e:
            error_msg = (
                    "\n item  {} \n ".format(str(video_id)) + "\n" + e.message
            )
            logging.warning(error_msg, exc_info=True)
            with open("error.log", "a") as f:
                f.write(
                    "================================================================== \n"
                )
            details = generate_details(e.message, e.type)
            raise HTTPException(status_code=e.response_code, detail=details)
    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(video_id)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "Item" + str(video_id) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": "your searched video is", video_id: video}, \
           FileResponse(f"uploads/{filename}", media_type="video/mp4")


@video_router.get("/get_video_detail_for_user/")
async def get_video_details_user(current_user: UserBase = Depends(get_current_active_user)):
    try:
        try:
            video = get_videos_detail(current_user.user_id)
        except UserErrors as e:
            error_msg = (
                    "\n video  {} \n ".format(str(current_user.user_id)) + "\n" + e.message
            )

            logging.warning(error_msg, exc_info=True)
            with open("error.log", "a") as f:
                f.write(
                    "================================================================== \n"
                )
            details = generate_details(e.message, e.type)
            raise HTTPException(status_code=e.response_code, detail=details)
    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(current_user.user_id)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "Item" + str(current_user.user_id) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": "your videos are", "video": video}


@video_router.get("/get_video_title/")
async def get_video_name(video_title):
    try:
        try:
            video, filename = get_video_detail_by_name(video_title)
        except UserErrors as e:
            error_msg = (
                    "\n item  {} \n ".format(str(video_title)) + "\n" + e.message
            )
            logging.warning(error_msg, exc_info=True)
            with open("error.log", "a") as f:
                f.write(
                    "================================================================== \n"
                )
            details = generate_details(e.message, e.type)
            raise HTTPException(status_code=e.response_code, detail=details)
    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(video_title)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "Item" + str(video_title) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": "your searched video is", video_title: video}, \
           FileResponse(f"uploads/{filename}", media_type="video/mp4")


@video_router.delete("/delete_item_details/{video_id}")
async def delete_item_details(
        video_id, current_user: UserBase = Depends(get_current_active_user)
):
    try:
        try:
            delete_video(video_id, current_user.user_id)
        except UserErrors as e:
            error_msg = (
                    "\n item  {} \n ".format(str(video_id)) + "\n" + e.message
            )
            logging.warning(error_msg, exc_info=True)
            with open("error.log", "a") as f:
                f.write(
                    "================================================================== \n"
                )
            details = generate_details(e.message, e.type)
            raise HTTPException(status_code=e.response_code, detail=details)
    except UserErrors as e:
        error_msg = (
                "\n item  {} \n ".format(str(video_id)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "Item" + str(video_id) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)
    return {"message": f"{video_id} is deleted successfully"}
