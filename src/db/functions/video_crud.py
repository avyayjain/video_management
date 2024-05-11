import os
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import joinedload
from datetime import datetime
from src.common.utils.constants import DB_CONNECTION_LINK, UPLOAD_FOLDER
from src.db.database import VideoInfo, Users
from src.db.errors import DataInjectionError, DatabaseErrors, DatabaseConnectionError
from src.db.utils import DBConnection


def upload_video_detail(title, des, duration, resolution, format, user, filename, thumbnail_filename):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = db.session.query(Users).filter(Users.user_id == user).first()
            try:
                video = VideoInfo(
                    video_id=uuid.uuid4().hex,
                    title=title,
                    description=des,
                    creation_date=current_time,
                    duration=duration,
                    status="active",
                    resolution=resolution,
                    format=format,
                    owner=user,
                    filename=filename,
                    thumbnail_filename=thumbnail_filename,
                )
                db.session.add(video)
                db.session.commit()
                return video.video_id
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


def get_videos_detail(user):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                # video = db.session.query(VideoInfo).filter(VideoInfo.owner_id == user).all()
                video_info = (
                    db.session.query(VideoInfo)
                    .join(Users, VideoInfo.owner_id == Users.user_id)
                    .options(joinedload(VideoInfo.owner))
                    .filter(Users.user_id == user)
                    .all()
                )

                output = []
                if video_info:
                    for video in video_info:
                        output.append({
                            "video_id": video.video_id,
                            "title": video.title,
                            "description": video.description,
                            "creation_date": video.creation_date,
                            "duration": video.duration,
                            "status": video.status,
                            "resolution": video.resolution,
                            "format": video.format,
                            "owner": video.owner.name,
                            "filename": video.filename,
                            "thumbnail_filename": video.thumbnail_filename,
                        })

                else:
                    return {
                        "message": "No video found"
                    }

                return output
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


def get_video_detail():
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                video = db.session.query(VideoInfo).all()
                output = []
                if video:
                    for video in video:
                        if video.status == "active":
                            output.append({
                                "video_id": video.video_id,
                                "title": video.title,
                                "description": video.description,
                                "creation_date": video.creation_date,
                                "duration": video.duration,
                                "resolution": video.resolution,
                                "owner": video.owner.name,
                            })
                else:
                    return {
                        "message": "No video found"
                    }

                return output
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


def get_video_detail_by_id(video_id, user_id):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                video = db.session.query(VideoInfo).filter(VideoInfo.video_id == video_id).first()

                if not video:
                    raise HTTPException(status_code=404, detail="Video not found")

                if video.owner_id != user_id:
                    raise HTTPException(status_code=403,
                                        detail="Permission denied: You are not the owner of this video")

                if video:
                    return {
                               "video_id": video.video_id,
                               "title": video.title,
                               "description": video.description,
                               "creation_date": video.creation_date,
                               "duration": video.duration,
                               "status": video.status,
                               "resolution": video.resolution,
                               "format": video.format,
                               "owner": video.owner.name,
                               "filename": video.filename,
                               "thumbnail_filename": video.thumbnail_filename,
                           }, video.filename

                else:
                    return {
                        "message": "No video found"
                    }

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


def get_video_detail_by_name(video_title):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                video = db.session.query(VideoInfo).filter(VideoInfo.title == video_title).first()

                if not video:
                    raise HTTPException(status_code=404, detail="Video not found")

                if video:
                    return {
                               "video_id": video.video_id,
                               "title": video.title,
                               "description": video.description,
                               "creation_date": video.creation_date,
                               "duration": video.duration,
                               "resolution": video.resolution,
                               "owner": video.owner.name,
                           }, video.filename

                else:
                    return {
                        "message": "No video found"
                    }

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


def update_video_detail(video_id, title, des, user_id):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                video = db.session.query(VideoInfo).filter(VideoInfo.video_id == video_id).first()

                if not video:
                    raise HTTPException(status_code=404, detail="Video not found")

                if video.owner_id != user_id:
                    raise HTTPException(status_code=403,
                                        detail="Permission denied: You are not the owner of this video")

                video.title = title
                video.description = des
                db.session.commit()
                return video.filename
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


def delete_video(video_id, user_id):
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                video = db.session.query(VideoInfo).filter(VideoInfo.video_id == video_id).first()

                if not video:
                    raise HTTPException(status_code=404, detail="Video not found")

                if video.owner_id != user_id:
                    raise HTTPException(status_code=403,
                                        detail="Permission denied: You are not the owner of this video")

                if os.path.exists(os.path.join(UPLOAD_FOLDER, video.filename)):
                    os.remove(os.path.join(UPLOAD_FOLDER, video.filename))

                db.session.delete(video)
                db.session.commit()

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
