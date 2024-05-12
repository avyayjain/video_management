# This directory contains the following api endpoint and response:

## 1. get video by id api endpoint and response

### api endpoint:

   ```url
    http://127.0.0.1:8000/video/get_video_detail_by_id/ec5e5ff284f346979b2cb1e24907b6e1
   ```
### query parameters:

   ```json
    {
        "video_id": "{video_id}"
    }
   ```
token should be passed in the header as Authorization: Bearer {access_token}

### response:

   ```json
    [
    {
        "message": "your searched video is",
        "ec5e5ff284f346979b2cb1e24907b6e1": {
            "video_id": "ec5e5ff284f346979b2cb1e24907b6e1",
            "title": "otp",
            "description": "otp checking",
            "creation_date": "2024-05-12T01:35:53",
            "duration": 30.51,
            "status": "active",
            "resolution": "1920x1052",
            "format": "29.97002997002997",
            "owner": "avyay",
            "filename": "OTP-Checker 2023-06-09 10-08-29.mp4",
            "thumbnail_filename": "./uploads\\otp\\thumbnail_OTP-Checker 2023-06-09 10-08-29.mp4.jpg"
        }
    },
    {
        "path": "uploads/OTP-Checker 2023-06-09 10-08-29.mp4",
        "status_code": 200,
        "filename": null,
        "send_header_only": false,
        "media_type": "video/mp4",
        "background": null,
        "raw_headers": [
            [
                "content-type",
                "video/mp4"
            ]
        ],
        "stat_result": null
    }
]
   ```

## 2. get video by id api endpoint and response

### api endpoint:

   ```url
    http://127.0.0.1:8000/video/get_video_detail_for_user/
   ```

token should be passed in the header as Authorization: Bearer {access_token}


### response:

   ```json
    {
    "message": "your videos are",
    "video": [
        {
            "video_id": "ec5e5ff284f346979b2cb1e24907b6e1",
            "title": "otp",
            "description": "otp checking",
            "creation_date": "2024-05-12T01:35:53",
            "duration": 30.51,
            "status": "active",
            "resolution": "1920x1052",
            "format": "29.97002997002997",
            "owner": "avyay",
            "filename": "OTP-Checker 2023-06-09 10-08-29.mp4",
            "thumbnail_filename": "./uploads\\otp\\thumbnail_OTP-Checker 2023-06-09 10-08-29.mp4.jpg"
        }
    ]
}
   ``` 