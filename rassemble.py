import os
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, TextClip, CompositeVideoClip
from QuraanGet import QuranVerseDownloader

class VideoAudioMerger:
    def __init__(self, seg_dir="./fragments/", audio_dir="./audios/", output_dir="./output/"):
        self.seg_dir = seg_dir
        self.audio_dir = audio_dir
        self.output_dir = output_dir
        self.downloader = QuranVerseDownloader()
        
    @staticmethod
    def change_extension(filepath, new_extension=".txt"):
        base, _ = os.path.splitext(filepath)
        base = base.replace('./audios/', './texts/')
        new_filepath = base + new_extension
        return new_filepath

    def process_videos(self):
        for video_file in os.listdir(self.seg_dir):
            self.downloader.iterate()
            video_path = os.path.join(self.seg_dir, video_file)
            self.process_single_video(video_path, video_file)

    def process_single_video(self, video_path, video_file):
        video = VideoFileClip(video_path)
        start_time = 0
        new_audio = video.audio

        for audio_file in os.listdir(self.audio_dir):
            audio_path = os.path.join(self.audio_dir, audio_file)
            text_path = self.change_extension(audio_path)
            audio, text_content = self.load_audio_and_text(audio_path, text_path)
            text_clip = self.create_text_clip(text_content, video.w, audio.duration, start_time)
            video = CompositeVideoClip([video, text_clip])
            new_audio = self.combine_audio_clips(new_audio, audio, start_time)
            start_time += 1 + audio.duration

        video_with_new_audio = video.set_audio(new_audio)
        self.save_video(video_with_new_audio, video_file)

    @staticmethod
    def load_audio_and_text(audio_path, text_path):
        audio = AudioFileClip(audio_path)
        with open(text_path, 'r', encoding='utf-8') as file:
            text_content = file.read().strip()
        return audio, text_content

    @staticmethod
    def create_text_clip(text_content, video_width, duration, start_time):
        text = TextClip(text_content, fontsize=100, color='white', align='center', method='caption',
                        size=(video_width, None), font='Scheherazade')
        return text.set_duration(duration).set_start(start_time).set_position(('center', 'center'))

    @staticmethod
    def combine_audio_clips(new_audio, audio, start_time):
        if new_audio is None:
            return audio.set_start(start_time)
        return CompositeAudioClip([new_audio, audio.set_start(start_time)])

    def save_video(self, video_with_new_audio, video_file):
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created folder: {self.output_dir}")
        output_filename = os.path.splitext(video_file)[0] + "_with_audio.mp4"
        output_path = os.path.join(self.output_dir, output_filename)
        video_with_new_audio.write_videofile(output_path, codec="libx264", audio_codec="aac")


