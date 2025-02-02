from x_uploader import XUploader
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()
    API_KEY = os.getenv("X_API_KEY")
    API_SECRET = os.getenv("X_API_SECRET")
    ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
    ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
    
    if not all([API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET]):
        raise ValueError("Missing X API credentials in .env file")
    
    uploader = XUploader(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    
    video_id = uploader.upload_video(
        video_path="videos/test.mp4",
        caption="Check out this awesome video! #coding #python"
    )
    
    if video_id:
        print(f"Video uploaded successfully! Tweet ID: {video_id}")
    else:
        print("Failed to upload video")
