import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from src.resources.video import video_router
from src.resources.sign_up import add_user_router
from src.resources.token import token_router
from src.resources.video_editing import video_editing_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(add_user_router, prefix="/user/sign-up")
app.include_router(token_router, prefix="/token")
app.include_router(video_router, prefix="/video")
app.include_router(video_editing_router, prefix="/video_edit")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000,reload=True)
