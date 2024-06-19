import os
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize
from PIL import Image
from moviepy.video.fx import all as vfx

if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

class VideoSplitter:
    def __init__(self, video_path, save_path, segment_duration=60, output_resolution=(1080, 1920)):
        self.video_path = video_path
        self.save_path = save_path
        self.segment_duration = segment_duration
        self.output_resolution = output_resolution

    def split_video_into_segments(self):
        try:
            # Load the original video
            original_video = VideoFileClip(self.video_path)
            total_duration = original_video.duration

            if total_duration < self.segment_duration:
                print("Video is less than the segment duration. No action will be taken.")
                return

            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)
                print(f"Created folder: {self.save_path}")

            video_no_audio = original_video.without_audio()

            # Resize the video to the specified resolution
            resized_video = resize(video_no_audio, newsize=self.output_resolution)
            
            darkened_clip = resized_video.fx(vfx.colorx, 0.5)  # This will darken the video by 50%

            # Calculate the number of segments
            num_segments = int(total_duration // self.segment_duration)

            # Iterate and save each segment
            for i in range(num_segments):
                start_time = i * self.segment_duration
                end_time = start_time + self.segment_duration
                segment = darkened_clip.subclip(start_time, end_time)

                # Define the output filename
                output_filename = os.path.join(self.save_path, f"segment_{i+1}.mp4")

                # Export the segment
                segment.write_videofile(output_filename, codec="libx264", audio_codec="aac")
                print(f"Saved: {output_filename}")

            print("All segments saved successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
