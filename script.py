import yt_dlp
import logging
import os
from datetime import datetime

class InstagramAudioExtractor:
    def __init__(self, output_dir="downloads"):
        self.output_dir = output_dir
        self.setup_logging()
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('audio_extractor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_safe_filename(self, url):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"reel_audio_{timestamp}"
    
    def download_audio(self, url):
        try:
            output_path = os.path.join(self.output_dir, self.get_safe_filename(url))
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': output_path,
                'quiet': True,
                'no_warnings': True
            }
            
            self.logger.info(f"Starting download for URL: {url}")
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if os.path.exists(output_path):
                self.logger.info(f"Successfully downloaded audio to: {output_path}")
                return {
                    "success": True,
                    "file_path": output_path,
                    "message": "Audio extracted successfully"
                }
            else:
                raise Exception("Output file not found after download")
                
        except Exception as e:
            error_message = f"Error downloading audio: {str(e)}"
            self.logger.error(error_message)
            return {
                "success": False,
                "error": error_message
            }
    
    def cleanup_old_files(self, max_age_hours=24):
        """Clean up files older than max_age_hours"""
        try:
            current_time = datetime.now()
            for filename in os.listdir(self.output_dir):
                file_path = os.path.join(self.output_dir, filename)
                file_age = datetime.fromtimestamp(os.path.getctime(file_path))
                age_hours = (current_time - file_age).total_seconds() / 3600
                
                if age_hours > max_age_hours:
                    os.remove(file_path)
                    self.logger.info(f"Cleaned up old file: {filename}")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

# Usage example
if __name__ == "__main__":
    extractor = InstagramAudioExtractor()
    
    # Example URL - replace with actual Instagram reel URL
    reel_url = "https://www.instagram.com/reel/DB3laidy9Ia/"
    
    # Download audio
    result = extractor.download_audio(reel_url)
    
    if result["success"]:
        print(f"Audio downloaded to: {result['file_path']}")
        
    else:
        print(f"Error: {result['error']}")
    
    # Clean up old files
    extractor.cleanup_old_files()