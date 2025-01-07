from flask import Flask, render_template, request, jsonify
from pytube import YouTube
import os

app = Flask(__name__)

def download_video(url, resolution):
    folder = os.path.expanduser("~/Downloads")  # Save to Downloads directory
    try:
        yt = YouTube(url)
        if resolution == "Low":
            stream = yt.streams.filter(res="144p").first()
        elif resolution == "Medium":
            stream = yt.streams.filter(res="360p").first()
        else:
            stream = yt.streams.get_highest_resolution()

        if stream:
            stream.download(folder)
            return True, folder
        else:
            return False, "Selected resolution is not available."
    except Exception as e:
        return False, str(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    url = data.get('url')
    resolution = data.get('resolution')

    if not url:
        return jsonify({"success": False, "message": "Please provide a YouTube URL."})

    success, message = download_video(url, resolution)
    if success:
        return jsonify({"success": True, "message": f"Video downloaded successfully to {message}"})
    else:
        return jsonify({"success": False, "message": message})

if __name__ == '__main__':
    app.run(debug=True)
