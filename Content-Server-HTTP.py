import sys
import os
import argparse

from flask import Flask, send_from_directory

from auxiliary_functions import get_ip, get_pwd, is_path_valid

def port_range(value):
    if not value.isdigit():
        raise argparse.ArgumentTypeError(f"Provided argument is not digit")
    value = int(value)
    if 49152 <= value <= 65535:
        return value
    raise argparse.ArgumentTypeError(f"Port number must be in the range 49152-65535. Provided: {value}")

# argument parser
parser = argparse.ArgumentParser(description='Local HTTP content server for Windows machines')
parser.add_argument('-ph', '--path',
                    required=False,
                    default="Current",
                    type=str,
                    help='Set path with content or use current working directory')
parser.add_argument('-ip', '--interface',
                    required=False,
                    default="all",
                    type=str,
                    # hostIP issue, it is possible that it will select the ip address of a non-connected network interface
                    choices=['hostIP', 'localhost', 'all'],
                    help='On which network interface should the server be available?')
parser.add_argument('-p', '--port',
                    required=False,
                    default=55443,
                    type=port_range,
                    help='Which port for the service? Port range - (49152–65535)')
args = parser.parse_args()

# set arguments
# path
if args.path == 'Current':
    set_path = get_pwd()
elif is_path_valid(args.path):
    set_path = args.path
else:
    print('Invalid path')
    sys.exit(1)

# network interface
match args.interface:
    case 'hostIP':
        host = get_ip()
    case 'localhost':
        host = '127.0.0.1'
    case 'all':
        host = '0.0.0.0'
    case _:
        print('Invalid interface')
        sys.exit(1)

# port
port = args.port

app = Flask(__name__)

# Path to video files folder
VIDEO_FOLDER = set_path

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
    print(f'Server is running on IP: {host}, port: {port}')
    print(f'Serves path: {set_path}')
    # Make server accessible on the local network
    app.run(host=host, port=port)
