from src.common.utils.constants import DB_CONNECTION_LINK
from src.db.database import Users
from src.db.errors import (
    DatabaseErrors,
    DatabaseConnectionError,
    DataInjectionError,
    ItemNotFound,
)
from src.db.utils import DBConnection


def user_login(user_email: str):
    """

    :param user_email: User Email
    :return: None
    """
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                data = (
                    db.session.query(Users).filter(Users.email_id == user_email).first()
                )
                if not data:
                    raise ItemNotFound
                data.logout = False
                db.session.commit()
            except:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError


def user_logout(user_email: str):
    """

    :param user_email: User Email
    :return: None
    """
    try:
        with DBConnection(DB_CONNECTION_LINK, False) as db:
            try:
                data = (
                    db.session.query(Users).filter(Users.email_id == user_email).first()
                )
                if not data:
                    raise ItemNotFound
                data.logout = True
                db.session.delete(data)
                db.session.commit()

            except:
                raise DataInjectionError
            finally:
                db.session.close()
    except DatabaseErrors:
        raise
    except Exception:
        raise DatabaseConnectionError
