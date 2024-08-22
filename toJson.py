import os
import json
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from datetime import datetime, timezone
import coverpy

# Initialize CoverPy
coverpy = coverpy.CoverPy()

def get_mp3_metadata(file_path):
    audio = MP3(file_path, ID3=ID3)
    
    # Extract song name and artist
    title = str(audio.get('TIT2', ['Unknown Title'])[0])
    author = str(audio.get('TPE1', ['Unknown Artist'])[0])
    
    # Fetch cover image URL

    try:
        result = coverpy.get_cover(title + ' ' + author, 1)  # Assuming title as the query for cover
        image_url = result.artwork(1000) if result else None
    except:
        image_url = 'https://upload.wikimedia.org/wikipedia/commons/1/1d/Invisible_Pink_Unicorn_High_Resolution.png'
    metadata = [{
        "title": title,
        "author": author,
        "image": image_url,  # Use coverpy URL directly
        "time": datetime.now(timezone.utc).isoformat().replace(" ", "_"),
        "mp3_path": os.path.abspath(file_path)  # Absolute path to MP3 file
    }]
    
    return metadata

def save_to_json(metadata, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=4)

def process_mp3_files(folder_path, output_folder):
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp3"):
            file_path = os.path.join(folder_path, filename)
            metadata = get_mp3_metadata(file_path)
            
            if metadata:
                json_filename = f"{os.path.splitext(filename)[0].replace(' ', '_')}.json"
                json_path = os.path.join(output_folder, json_filename)
                save_to_json(metadata, json_path)
                print(f"Metadata for {filename} saved to {json_path}")

def main():
    folder_path = "mp3files"
    output_folder = "songs"
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    process_mp3_files(folder_path, output_folder)
    
    print(f"Processing complete. JSON files saved to {output_folder}")

if __name__ == "__main__":
    main()
