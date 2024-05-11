from unittest import TestCase
from src.common.utils.constants import DB_CONNECTION_LINK
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import app
from starlette.testclient import TestClient


class TestLogin(TestCase):

    def setUp(self):
        app.testing = True
        engine = create_engine(DB_CONNECTION_LINK)
        self.app = TestClient(app)
        Session = sessionmaker(engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()

    # Test cases for correct login
    def test_login(self):
        token_response = self.app.post(
            f"/token",
            json={"email_id": "avyay@gmail.com",
                  "password": "avyay123"}
        )
        expected_code = 200

        self.assertEqual(token_response.status_code,
                         expected_code,
                         f"Status Code didn't match..Received {token_response.status_code}, expected {expected_code}.")

    # Test cases for incorrect login
    # Test case for incorrect email
    def test_login_2(self):
        data = {
            "detail": [
                {
                    "msg": "Incorrect Email or password",
                    "type": "PermissionDeniedError"
                }
            ]
        }
        token_response = self.app.post(
            f"/token",
            json={"email_id": "avyay2@gmail.com",
                  "password": "avyay123"}
        )
        expected_code = 401

        self.assertEqual(token_response.status_code,
                         expected_code,
                         "Status Code didn't match..Received {}, expected {}.".format(
                             token_response.status_code, expected_code
                         ))

        token_response_data = token_response.json()

        self.assertEqual(
            token_response_data["detail"],
            data["detail"],
            "Status Code didn't match..Received {}, expected {}.".format(
                token_response.json(), data
            ),
        )

    # Test case for incorrect password
    def test_login_3(self):
        data = {
            "detail": [
                {
                    "msg": "Incorrect Email or password",
                    "type": "PermissionDeniedError"
                }
            ]
        }
        token_response = self.app.post(
            f"/token",
            json={"email_id": "avyay@gmail.com",
                  "password": "avyay1234"}
        )
        expected_code = 401

        self.assertEqual(token_response.status_code,
                         expected_code,
                         "Status Code didn't match..Received {}, expected {}.".format(
                             token_response.status_code, expected_code
                         ))

        token_response_data = token_response.json()

        self.assertEqual(
            token_response_data["detail"],
            data["detail"],
            "Status Code didn't match..Received {}, expected {}.".format(
                token_response.json(), data
            ),
        )

    # Test case for empty email
    def test_login_4(self):
        data = {
            "detail": [
                {
                    "loc": [
                        "body",
                        "email_id"
                    ],
                    "msg": "value is not a valid email address",
                    "type": "value_error.email"
                }
            ]
        }
        token_response = self.app.post(
            f"/token",
            json={"email_id": "",
                  "password": "avyay123"}
        )
        expected_code = 422

        self.assertEqual(token_response.status_code,
                         expected_code,
                         "Status Code didn't match..Received {}, expected {}.".format(
                             token_response.status_code, expected_code
                         ))

        token_response_data = token_response.json()

        self.assertEqual(
            token_response_data["detail"],
            data["detail"],
            "Status Code didn't match..Received {}, expected {}.".format(
                token_response.json(), data
            ),
        )

    # Test case for empty password
    def test_login_5(self):
        data = {
            "detail": [
                {
                    "msg": "Incorrect Email or password",
                    "type": "PermissionDeniedError"
                }
            ]
        }
        token_response = self.app.post(
            f"/token",
            json={"email_id": "avyay@gmail.com",
                  "password": " "}
        )
        expected_code = 401
        self.assertEqual(token_response.status_code,
                         expected_code,
                         "Status Code didn't match..Received {}, expected {}.".format(
                             token_response.status_code, expected_code
                         ))

        token_response_data = token_response.json()

        self.assertEqual(
            token_response_data["detail"],
            data["detail"],
            "Status Code didn't match..Received {}, expected {}.".format(
                token_response.json(), data
            ),
        )
