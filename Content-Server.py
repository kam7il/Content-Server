from flask import Flask, send_from_directory
import os

app = Flask(__name__)

# Path to video files folder
VIDEO_FOLDER = "SET PATH"

@app.route('/')
def list_videos():
    """
    Displays a list of video files available in the folder.
    """
    try:
        files = os.listdir(VIDEO_FOLDER)
        video_files = [file for file in files if file.endswith(('.mp4', '.mkv', '.avi', '.mov'))]
        response = "<h1>Video available:</h1><ul>"
        for video in video_files:
            response += f'<li><a href="/video/{video}">{video}</a></li>'
        response += "</ul>"
        return response
    except FileNotFoundError:
        return "The video folder does not exist!", 404

@app.route('/video/<filename>')
def stream_video(filename):
    """
    Allows video streaming.
    """
    try:
        return send_from_directory(VIDEO_FOLDER, filename, as_attachment=False)
    except FileNotFoundError:
        return "File not found!", 404

if __name__ == '__main__':
    # Set the host to '0.0.0.0' to make the server accessible on the local network
    app.run(host='0.0.0.0', port=5421)
