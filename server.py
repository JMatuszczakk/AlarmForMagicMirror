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

@app.route('/serve_image/<filename>')
def serve_image(filename):
    return send_from_directory(images_folder, filename)

@app.route('/serve_current_image')
def serve_current_image():
    try:
        with open('current_image.json', 'r') as f:
            current_image = json.load(f)
        filename = current_image.get("image", "")
        if filename:
            image_path = os.path.join(images_folder, filename)
            if os.path.exists(image_path):
                print(f"Serving image: {filename}")
                return send_from_directory(images_folder, filename)
            else:
                print(f"Image file does not exist: {image_path}")
                return abort(404)  # Return a 404 if the file does not exist
        else:
            print("No image filename found in JSON.")
            return 'No image set', 403
    except FileNotFoundError:
        print("current_image.json file not found.")
        return 'File not found', 404
@app.route('/set_time', methods=['POST'])
def set_time():
    x = request.form
    json_string = list(x.keys())[0]
    jsoned = json.loads(json_string)
    times = jsoned['time']
    #HH:MM

    with open('time.json', 'w') as f:
        json.dump({'time': times}, f)

    return 'OK'

@app.route('/form', methods=['GET'])
def time_form():
    html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Set Time</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 500px; margin: 0 auto; padding: 20px; }
            form { display: flex; flex-direction: column; gap: 10px; }
            input[type="time"], input[type="submit"] { padding: 10px; }
            input[type="submit"] { background-color: #4CAF50; color: white; border: none; cursor: pointer; }
            input[type="submit"]:hover { background-color: #45a049; }
        </style>
    </head>
    <body>
        <h1>Set Time for Adding Songs</h1>
        <form action="/set_time" method="post">
            <label for="time">Select Time:</label>
            <input type="time" id="time" name="time" required>
            <input type="submit" value="Set Time">
        </form>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/clear')
def clear():
    with open('data.json', 'w') as f:
        json.dump({}, f)
    with open('time.json', 'w') as f:
        json.dump({}, f)
    with open('current_image.json', 'w') as f:
        json.dump({"image": ""}, f)
    return 'OK'

if __name__ == '__main__':
    app.run(debug=True, port=5001, host='0.0.0.0')
