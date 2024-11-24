import os

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

if __name__ == '__main__':
    # raw string
    print(is_path_valid(r'D:\Video'))