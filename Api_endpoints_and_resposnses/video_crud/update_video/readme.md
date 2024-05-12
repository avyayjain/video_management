# This directory contains the following api endpoint and response:

## 1. update video by id api endpoint and response

### api endpoint:

   ```url
    http://127.0.0.1:8000/video/update_item_details/ec5e5ff284f346979b2cb1e24907b6e1
   ```
### query parameters:

   ```json
    {
        "video_id": "{video_id}"
    }
   ```

### body:

   ```json
    {
  "title": "otp",
  "description": "changed des of the otp video"
    }
   ```

token should be passed in the header as Authorization: Bearer {access_token}

### response:

   ```json
    [
    {
        "message": "video details updated successfully",
        "item_id": "ec5e5ff284f346979b2cb1e24907b6e1"
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