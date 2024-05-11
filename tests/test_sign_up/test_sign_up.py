from unittest import TestCase
from src.common.utils.constants import DB_CONNECTION_LINK
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import app
from starlette.testclient import TestClient


class TestSignUp(TestCase):

    def setUp(self):
        app.testing = True
        engine = create_engine(DB_CONNECTION_LINK)
        self.app = TestClient(app)
        Session = sessionmaker(engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    #
    def test_sign_up(self):
        data = {
            "detail": "User Added ,please login to continue"
        }

        sign_up = self.app.post(
            f"/user/sign-up/",
            json={
                "email": "avyay2@gmail.com",
                "password": "avyay123",
                "name": "avyay"
            }
        )

        expected_code = 200

        self.assertEqual(sign_up.status_code,
                         expected_code,
                         f"Status Code didn't match..Received {sign_up.status_code}, expected {expected_code}.")

        sign_up_data = sign_up.json()

        self.assertEqual(
            sign_up_data["detail"],
            data["detail"],
            "Status Code didn't match..Received {}, expected {}.".format(
                sign_up.json(), data
            ),
        )

    # test case for user exists
    def test_sign_up_2(self):
        data = {
            "detail": [
                {
                    "msg": "Can't Insert Data in Database. Try Again",
                    "type": "DataInjectionError"
                }
            ]
        }

        sign_up = self.app.post(
            f"/user/sign-up/",
            json={
                "email": "avyay4@gmail.com",
                "password": "avyay123",
                "name": "avyay"
            }
        )

        expected_code = 503

        self.assertEqual(sign_up.status_code,
                         expected_code,
                         f"Status Code didn't match..Received {sign_up.status_code}, expected {expected_code}.")

        sign_up_data = sign_up.json()

        self.assertEqual(
            sign_up_data["detail"],
            data["detail"],
            "Status Code didn't match..Received {}, expected {}.".format(
                sign_up.json(), data
            ),
        )
