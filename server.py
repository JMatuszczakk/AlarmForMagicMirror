from flask import Flask, jsonify, request, render_template_string, send_from_directory, url_for
import json
import os
import random
from datetime import datetime, time, timedelta

app = Flask(__name__)
global times 
times = time(0, 0)
songs_folder = 'songs'
images_folder = 'songImages'

if not os.path.exists(songs_folder):
    os.mkdir(songs_folder)

if not os.path.exists(images_folder):
    os.mkdir(images_folder)

# Create data.json if it doesn't exist
if not os.path.exists('data.json'):
    with open('data.json', 'w') as f:
        json.dump({}, f)

# Create time.json if it doesn't exist
if not os.path.exists('time.json'):
    with open('time.json', 'w') as f:
        json.dump({}, f)

# Create current_image.json if it doesn't exist
if not os.path.exists('current_image.json'):
    with open('current_image.json', 'w') as f:
        json.dump({"image": ""}, f)

@app.route('/json')
def json_data():
    # Read set time from file
    try:
        with open('time.json') as f:
            times = json.load(f)
    except:
        return 'error'
    
    times = times["time"]
    

    times = times.split(':')
    times = time(int(times[0]), int(times[1]))

    # Make times have today's date
    if datetime.now().time() > times:
        # Get all files in songs_folder
        files = os.listdir(songs_folder)
        # If files is not empty
        with open('data.json', 'r') as f16:
            data16 = json.load(f16)
            print(data16)
        
        if files and data16 == {}:
            # Get random file from files
            random_file = random.choice(files)

            with open(f'{songs_folder}/{random_file}', 'r') as f:
                data = json.load(f)

            # # Update image URL
            # if 'image' in data[0]:
            #     image_filename = data[0]['image']
            #     with open('current_image.json', 'w') as f:
            #         json.dump({"image": image_filename}, f)
            #     image_url = url_for('serve_current_image', _external=True)
            #     data[0]['image'] = image_url

            with open('data.json', 'w') as f2:
                json.dump(data, f2)
    else:
        with open('data.json', 'w') as f:
            json.dump({}, f)

    with open('data.json', 'r') as f:
        data = json.load(f)
    return jsonify(data)
