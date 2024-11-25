import socket
import os

def get_ip():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    return ip_addr

def get_pwd():
    # get the current working directory
    current_working_directory = os.getcwd()
    return current_working_directory

def is_path_valid(path):
    try:
        # Check if path exist
        if os.path.exists(path):
            return True
        else:
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False