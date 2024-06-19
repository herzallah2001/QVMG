# quran_downloader.py
import os
import requests
import urllib.request
from moviepy.editor import AudioFileClip

class QuranVerseDownloader:
    def __init__(self):
        self.save_path_audios = "./audios"
        self.save_path_texts = "./texts"
        self.db_filename = "db.txt"
        
        # Clear directories if they exist
        
        # Create directories if they do not exist
        self.create_directory(self.save_path_audios)
        self.create_directory(self.save_path_texts)
    
    def clear_directory(self, directory_path):
        if os.path.exists(directory_path):
            for file in os.listdir(directory_path):
                file_path = os.path.join(directory_path, file)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        os.rmdir(file_path)
                except Exception as e:
                    print(f"Failed to delete {file_path}. Reason: {e}")
    
    def create_directory(self, directory_path):
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            print(f"Created folder: {directory_path}")
    
    def write_to_db(self, ayah_number, surah_number):
        try:
            with open(self.db_filename, 'w', encoding='utf-8') as file:
                file.write(f"{ayah_number}\n")
                file.write(f"{surah_number}\n")
            print("Lines written successfully to db.txt.")
        except Exception as e:
            print(f"An error occurred while writing to db.txt: {e}")
    
    def read_from_db(self):
        try:
            with open(self.db_filename, 'r') as file:
                ayah_number = int(file.readline().strip())
                surah_number = int(file.readline().strip())
            return ayah_number, surah_number
        except FileNotFoundError:
            print(f"File {self.db_filename} not found.")
            return None, None
        except ValueError:
            print("Invalid data format in the file.")
            return None, None
    
    def download_quran_verse_data(self, ayah_number, surah_number, total_length):
        try:
            # Fixed API endpoint URL with {ayah_number} placeholder
            api_url = f"https://api.alquran.cloud/v1/ayah/{ayah_number}/ar.alafasy"

            # Send GET request to the API endpoint
            response = requests.get(api_url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Parse JSON response
                data = response.json()['data']  # Access the 'data' object
                
                # Extract surah number from the 'surah' object under 'data'
                surah_number_actual = data['surah']['number']
                print(f"Surah Number: {surah_number_actual}")
                
                # Check if the retrieved surah number matches the expected surah number
                if surah_number_actual != surah_number:
                    self.write_to_db(ayah_number, surah_number_actual)
                    return False, 0
                
                # Extract audio URL and text
                audio_url = data['audio']
                text = data['text']
                
                # Download .mp3 audio file
                audio_filename = os.path.join(self.save_path_audios, f"{ayah_number}.mp3")
                urllib.request.urlretrieve(audio_url, audio_filename)
                
                # Get audio length using MoviePy
                audio_clip = AudioFileClip(audio_filename)
                audio_length = audio_clip.duration
                audio_clip.close()
                
                # Increment total length
                total_length += audio_length + 1
                
                if total_length > 60:
                    # Delete the audio file if total length exceeds 60 seconds
                    os.remove(audio_filename)
                    return False, 0
                
                # Save text to a text file
                text_filename = os.path.join(self.save_path_texts, f"{ayah_number}.txt")
                with open(text_filename, "w", encoding='utf-8') as text_file:
                    text_file.write(text)
                
                # Update database with new ayah number
                ayah_number += 1
                self.write_to_db(ayah_number, surah_number)
                
                return True, total_length
            else:
                print(f"Failed to retrieve data from the API. Status code: {response.status_code}")
                return False, 0
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False, 0
    
    def iterate(self):
        self.clear_directory(self.save_path_audios)
        self.clear_directory(self.save_path_texts)
        
        total_length = 0
        continue_iteration = True
        
        while continue_iteration:
            ayah_number, surah_number = self.read_from_db()
            
            if ayah_number == 6237:
                self.write_to_db(1, 1)
            
            continue_iteration, total_length = self.download_quran_verse_data(ayah_number, surah_number, total_length)
            print(f"Continue iteration: {continue_iteration}")
