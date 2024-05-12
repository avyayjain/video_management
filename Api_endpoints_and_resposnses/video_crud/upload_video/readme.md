# This is the readme file for the video crud directory

## The post directory contains the following files:


## 1. video upload endpoint and response
### api endpoint:

   ```url
    http://localhost:8000/video/upload/
   ```
### body:

   ```json
    {
          "title": "OTP-Checker",
          "description": "This is a video on how to use OTP-Checker",
    }
   ```
In the body, the video file should be uploaded as a form-data with the key as "video"    

### response:

   ```json
    [
    {
        "message": "You have successfully uploaded the video ",
        "video details": [
            "ec5e5ff284f346979b2cb1e24907b6e1"
        ]
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
