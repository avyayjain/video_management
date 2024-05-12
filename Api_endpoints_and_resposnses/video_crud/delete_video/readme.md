# This directory contains the following api endpoint and response:

## 1. delete video by id api endpoint and response

### api endpoint:

   ```url
    http://127.0.0.1:8000/video/delete_item_details/ec5e5ff284f346979b2cb1e24907b6e1
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
    {"message": "ec5e5ff284f346979b2cb1e24907b6e1 is deleted successfully"}
   ```