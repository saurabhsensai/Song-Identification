import requests
import os

def recognize_local_song(file_path):
    url = "https://shazam-song-recognition-api.p.rapidapi.com/recognize/file"
    
    headers = {
        "x-rapidapi-key": "b7f26d018fmshf859091b39a13c3p1cfd14jsnd9d2996a991d",  # Replace with your API key
        "x-rapidapi-host": "shazam-song-recognition-api.p.rapidapi.com"
    }
    
    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        files = {
            'file': (os.path.basename(file_path), file, 'audio/mpeg')  # for MP3 files
        }
        
        response = requests.post(url, headers=headers, files=files)
        return response.json()

# Usage example
try:
    result = recognize_local_song("downloads/reel_audio_20241119_175808.mp3")  # Replace with your actual file path
    # Song name
    song_name = result['track']['title']

# Artist name
    artist_name = result['track']['subtitle']

# Full details
    print(f"Song: {song_name}")
    print(f"Artist: {artist_name}")
except FileNotFoundError:
    print("File not found! Please check the file path.")
except Exception as e:
    print(f"An error occurred: {str(e)}")