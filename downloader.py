import yt_dlp
import os
import re

class YouTubeDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = download_path
        if not os.path.exists(download_path):
            os.makedirs(download_path)

    def download_video(self, url):
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            'outtmpl': os.path.join(self.download_path, '%(title)s.%(ext)s'),
            'noplaylist': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            video_path = ydl.prepare_filename(info)
            
            # Extract metadata
            metadata = {
                'title': info.get('title', ''),
                'description': info.get('description', ''),
                'hashtags': self._extract_hashtags(info.get('description', '')),
                'video_path': video_path
            }
            return metadata

    def _extract_hashtags(self, description):
        if not description:
            return []
        # Find all hashtags in the description
        hashtags = re.findall(r'#(\w+)', description)
        return list(set(hashtags)) # Unique hashtags

if __name__ == "__main__":
    # Quick test
    downloader = YouTubeDownloader()
    # Replace with a valid short for testing if needed
    # test_url = "https://www.youtube.com/shorts/..." 
    # print(downloader.download_video(test_url))
