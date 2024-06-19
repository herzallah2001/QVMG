from pytube import YouTube
import os

class YouTubeDownloader:
    def __init__(self, save_path='.'):
        self.save_path = save_path

    def download_video(self, url, resolution='720p'):
        try:
            yt = YouTube(url)
            print(f'Title: {yt.title}')
            print(f'Views: {yt.views}')
            
            # Filter streams by resolution
            ys = yt.streams.filter(res=resolution).first()
            
            if ys is None:
                print(f"No stream available with resolution: {resolution}")
                return
            
            print(f"Downloading video at {resolution} resolution...")
            downloaded_file_path = ys.download(self.save_path)
            print("Download completed!!")
            
            # Rename the downloaded file to 'your_video'
            new_file_path = os.path.join(self.save_path, 'your_video' + os.path.splitext(downloaded_file_path)[1])
            os.rename(downloaded_file_path, new_file_path)
            print(f"File renamed to: {new_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")

