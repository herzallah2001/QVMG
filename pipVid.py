from youtDowload import YouTubeDownloader
from rassemble import VideoAudioMerger
from vidNormal import VideoSplitter

class VideoProcessingPipeline:
    def __init__(self, video_url, resolution):
        self.video_url = video_url
        self.resolution = resolution

    def run_pipeline(self):
        try:
            # Download YouTube video
            downloader = YouTubeDownloader(save_path="./")
            downloader.download_video(url=self.video_url, resolution=self.resolution)

            # Split downloaded video into segments
            splitter = VideoSplitter(video_path="./your_video.mp4", save_path="./fragments")
            splitter.split_video_into_segments()

            # Merge video segments
            merger = VideoAudioMerger()
            merger.process_videos()

        except Exception as e:
            print(f"An error occurred: {e}")

"""
# Example usage
if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=IUN664s7N-c'
    resolution = '360p'
    pipeline = VideoProcessingPipeline(video_url, resolution)
    pipeline.run_pipeline()
"""