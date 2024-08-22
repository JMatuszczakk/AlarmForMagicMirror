import time
import requests
import json
import pygame
from pathlib import Path

# Initialize pygame mixer for playing audio
pygame.mixer.init()

def play_mp3(mp3_path):
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(mp3_path)
        pygame.mixer.music.play()

def stop_mp3():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()

def watch_url(url, poll_interval=1):
    last_data = None

    while True:
        try:
            # Fetch the data from the URL
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for bad responses
            data = response.json()

            if data != last_data:
                if data:
                    # New data available, play the mp3
                    mp3_path = data[0]['mp3_path']
                    if Path(mp3_path).exists():
                        play_mp3(mp3_path)
                    else:
                        print(f"File {mp3_path} does not exist.")
                else:
                    # Data has disappeared, stop playing
                    stop_mp3()

                # Update the last data state
                last_data = data

        except requests.RequestException as e:
            stop_mp3()
        
        except json.JSONDecodeError:
            print("Error decoding JSON from response.")

        # Wait for the next polling interval
        time.sleep(poll_interval)

if __name__ == "__main__":
    # Replace with the URL you want to monitor
    url = "http://127.0.0.1:5001/json"
    watch_url(url)
