import requests
import os
from typing import Optional
from datetime import datetime

class XUploader:
    def __init__(self, api_key: str, api_secret: str, access_token: str, access_token_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret
        self.base_url = "https://api.twitter.com/2"

    def upload_video(self, 
                    video_path: str, 
                    caption: str) -> Optional[str]:
        
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")

        # Step 1: Upload media
        upload_url = "https://upload.twitter.com/1.1/media/upload.json"
        headers = {
            "Authorization": f"OAuth oauth_consumer_key=\"{self.api_key}\", "
                           f"oauth_token=\"{self.access_token}\", "
                           f"oauth_signature_method=\"HMAC-SHA1\""
        }

        # Initialize upload
        with open(video_path, 'rb') as video_file:
            total_bytes = os.path.getsize(video_path)
            
            init_data = {
                'command': 'INIT',
                'total_bytes': total_bytes,
                'media_type': 'video/mp4'
            }
            
            try:
                init_response = requests.post(upload_url, headers=headers, data=init_data)
                init_response.raise_for_status()
                media_id = init_response.json()['media_id_string']

                # Upload chunks
                chunk_size = 1024 * 1024  # 1MB chunks
                segment_index = 0
                
                video_file.seek(0)
                while True:
                    chunk = video_file.read(chunk_size)
                    if not chunk:
                        break
                        
                    append_data = {
                        'command': 'APPEND',
                        'media_id': media_id,
                        'segment_index': segment_index,
                        'media': chunk
                    }
                    
                    append_response = requests.post(upload_url, headers=headers, data=append_data)
                    append_response.raise_for_status()
                    segment_index += 1

                # Finalize upload
                finalize_data = {
                    'command': 'FINALIZE',
                    'media_id': media_id
                }
                
                finalize_response = requests.post(upload_url, headers=headers, data=finalize_data)
                finalize_response.raise_for_status()

                # Create tweet with media
                tweet_url = f"{self.base_url}/tweets"
                tweet_data = {
                    "text": caption,
                    "media": {"media_ids": [media_id]}
                }
                
                tweet_response = requests.post(tweet_url, headers=headers, json=tweet_data)
                tweet_response.raise_for_status()
                
                return tweet_response.json().get('data', {}).get('id')
                
            except requests.exceptions.RequestException as e:
                print(f"Error uploading to X: {str(e)}")
                return None 