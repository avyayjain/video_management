import logging

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr

from src.common.utils.generate_error_details import generate_details
from src.common.utils.user_defined_errors import UserErrors
from src.db.functions.add_user import create_user
from src.db.functions.logout import user_logout
from src.resources.token import UserBase, get_current_active_user

add_user_router = APIRouter()


class AuthAddUser(BaseModel):
    email: EmailStr
    password: str
    name: str


@add_user_router.post("/")
async def sign_up(
        form_data: AuthAddUser
):
    """
    API to ADD Users

    """
    try:
        create_user(
            user_email=form_data.email,
            password=form_data.password,
            user_name=form_data.name,
        )
        return {"detail": "User Added ,please login to continue"}

    except UserErrors as e:
        error_msg = (
                "\n email  {} \n ".format(str(form_data.email)) + "\n" + e.message
        )
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details(e.message, e.type)
        raise HTTPException(status_code=e.response_code, detail=details)

    except Exception:
        error_msg = "email :" + str(form_data.email) + "\n"
        logging.warning(error_msg, exc_info=True)
        with open("error.log", "a") as f:
            f.write(
                "================================================================== \n"
            )
        details = generate_details("Internal Server Error", "InternalServerError")
        raise HTTPException(status_code=500, detail=details)


@add_user_router.delete("/delete_user")
async def delete_user(current_user: UserBase = Depends(get_current_active_user)
                      ):
    """
    API to ADD Users
    """
    try:
        try:
            user_logout(current_user.email_id)
        except Exception as e:
            print(e)
        return {"detail": "User Delete"}

    except Exception as e:
        print(e)
