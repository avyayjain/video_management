# This directory contains the following files:

## 1. add_thumbnail endpoint and response

### api endpoint:

   ```url
    http://127.0.0.1:8000/video_edit/thumbnail/ec5e5ff284f346979b2cb1e24907b6e1
   ```

### In the body, the video file should be uploaded as a form-data with the key as "thumbnail"

### token should be included in the header as Authorization

### query parameter:

   ```url
    video_id: {video_id}    
   ```

### response:

   ```json
    {
    "message": "Thumbnail updated successfully"
    }
   ```