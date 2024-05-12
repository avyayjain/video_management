# This is the readme file for the sign_up_and_login directory

## The sign_up_and_login directory contains the following files:


## 1. sign up api endpoint and response
### api endpoint:

   ```url
    http://localhost:8000/user/sign-up/
   ```
### body:

   ```json
    {
          "email": "avyay2@gmail.com",
          "password": "avyay",
          "name": "avyay"
    }
   ```
### response:

   ```json
    {
        "detail": "User Added ,please login to continue"
    }
   ```

## 2. login api endpoint and response
### api endpoint:

   ```url
    http://localhost:8000/user/login/
   ```
### body:
   ```json
    {
       "email_id": "avyay@gmail.com",
       "password": "avyay123"
    }
   ```
### response:
   ```json
    {
        "access_token": "{access_token}",
        "token_type": "bearer"
    }
   ```  