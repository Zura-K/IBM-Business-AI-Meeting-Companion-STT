import os
import time
import requests

class SpeechDownloader:
    def __init__(self, url):
        self.url = url
        self.download_folder = "downloads"
        self.audio_file_path = os.path.join(self.download_folder, f"downloaded_audio_{int(time.time())}.mp3")
        os.makedirs(self.download_folder, exist_ok=True)

    def download_audio(self):
        try:
            response = requests.get(self.url, stream=True)  # Stream to avoid memory overload

            if response.status_code == 200:
                with open(self.audio_file_path, "wb") as file:
                    for chunk in response.iter_content(chunk_size=8192):  # Download in chunks
                        file.write(chunk)

                print("File downloaded successfully:", self.audio_file_path)
                return self.audio_file_path
            else:
                print(f"Failed to download the file. HTTP Status Code: {response.status_code}")
                return None
        except requests.RequestException as e:
            print(f"Error downloading file: {e}")
            return None
