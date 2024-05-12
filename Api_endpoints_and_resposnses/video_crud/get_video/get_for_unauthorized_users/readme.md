# This directory contains the following api endpoint and response:

### These api endpoints are for unauthorized users therefore no access token is required


## 1. get video by name api endpoint and response


### api endpoint:

   ```url
    http://127.0.0.1:8000/video/get_video_title/?video_title=otp
   ```
### query parameters:

   ```json
    {
        "video_title": "otp"
    }
   ```

### response:

   ```json
    [
    {
        "message": "your searched video is",
        "otp": {
            "video_id": "ec5e5ff284f346979b2cb1e24907b6e1",
            "title": "otp",
            "description": "otp checking",
            "creation_date": "2024-05-12T01:35:53",
            "duration": 30.51,
            "resolution": "1920x1052",
            "owner": "avyay"
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

## 2. get all video api endpoint and response

### api endpoint:

   ```url
    http://127.0.0.1:8000/video/get_all_details
   ```

### response:

   ```json
    {
    "All videos details :": [
        {
            "video_id": "ec5e5ff284f346979b2cb1e24907b6e1",
            "title": "otp",
            "description": "otp checking",
            "creation_date": "2024-05-12T01:35:53",
            "duration": 30.51,
            "resolution": "1920x1052",
            "owner": "avyay"
        }
    ]
}
   ``` 