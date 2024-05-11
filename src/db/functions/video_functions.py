import os
import shutil
from fastapi import UploadFile, HTTPException
from moviepy.editor import VideoFileClip
from src.common.utils.constants import UPLOAD_FOLDER, DB_CONNECTION_LINK
import cv2

from src.db.database import VideoInfo
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError
from src.db.utils import DBConnection


def extract_video_metadata(file_path: UploadFile):
    try:
        # Open the video file
        video = VideoFileClip(file_path)

        # Extract metadata
        duration = video.duration  # Duration of the video in seconds
        resolution = f"{video.size[0]}x{video.size[1]}"
        print(resolution)  # Resolution of the video
        format = video.fps  # Format of the video

        # Close the video file
        video.close()

        return duration, resolution, format

    except Exception as e:
        print("Error extracting metadata:", e)
        raise e


def store_video(file, title):
    try:
        upload_dir = UPLOAD_FOLDER

        # Create the upload directory if it doesn't exist
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        file_path = os.path.join(upload_dir, title, file.filename)
        with open(file_path, "wb") as video_file:
            # Iterate over the file chunks and write them to the new file
            shutil.copyfileobj(file.file, video_file)

        thumbnail_path = os.path.join(upload_dir, "thumbnail_" + file.filename + ".jpg")

        # Create thumbnail
        create_thumbnail(video_path=file_path, thumbnail_path=thumbnail_path)

    except Exception as e:
        print(f"Error storing video: {e}")
        return None

    return file.filename, thumbnail_path


def create_thumbnail(video_path: str, thumbnail_path: str):
    cap = cv2.VideoCapture(video_path)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(thumbnail_path, frame)
    cap.release()


def find_video(video_id, user_id):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                video = db.session.query(VideoInfo).filter(VideoInfo.video_id == video_id).first()

                if not video:
                    raise HTTPException(status_code=404, detail="Video not found")

                if video.owner_id != user_id:
                    raise HTTPException(status_code=403,
                                        detail="Permission denied: You are not the owner of this video")

                return video.filename, video.title, video.thumbnail_filename
            except Exception as e:
                print(e)
                raise DataInjectionError
            finally:
                db.session.close()

    except DatabaseErrors:
        raise
    except Exception as e:
        print(e)
        raise DatabaseConnectionError


def remove_thumbnail(thumbnail_path):
    try:
        if os.path.exists(thumbnail_path):
            os.remove(thumbnail_path)
    except Exception as e:
        print(f"Error removing thumbnail: {e}")
