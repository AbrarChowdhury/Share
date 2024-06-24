import os
import json
import pyperclip
import requests
from tqdm import tqdm

def get_path():
    current_path = os.getcwd()
    file_name = input("Name the file: ")
    full_path = os.path.join(current_path, file_name)
    print(f"File path: {full_path}")
    return full_path

def upload_file_with_progress(path):
    url = "https://file.io"
    file_size = os.path.getsize(path)
    file_name = os.path.basename(path)

    with open(path, 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name, ncols=80) as progress_bar:
            response = requests.post(
                url,
                files={"file": (file_name, f)},
                stream=True
            )
            response.raise_for_status()
            progress_bar.update(file_size)
    
    return response.json()

def run_curl(path):
    try:
        response_json = upload_file_with_progress(path)
        link = response_json.get("link")
        if link:
            print("Link:", link)
            pyperclip.copy(link)
            print("Link has been copied to the clipboard.")
        else:
            print("Link not found in the response.")
    except requests.RequestException as e:
        print("File upload failed.")
        print("Error:", str(e))
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")

if __name__ == "__main__":
    path = get_path()
    run_curl(path)
