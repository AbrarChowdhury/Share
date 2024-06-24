import os
import subprocess
import json
import pyperclip


def get_path():
    current_path = os.getcwd()
    file_name = input("Name the file: ")
    current_path = os.path.join(current_path, file_name)
    print(current_path)
    return current_path


def run_curl(path):
    curl_command = ["curl", "-F", f"path=@{path}", "https://file.io"]
    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        response = result.stdout
        try:
            response_json = json.loads(response)
            link = response_json.get("link")
            if link:
                print("Link:", link)
                pyperclip.copy(link)
                print("Link has been copied to the clipboard.")
            else:
                print("Link not found in the response.")
        except json.JSONDecodeError:
            print("Failed to parse JSON response.")
    else:
        print("Curl command failed.")
        if result.stderr:
            print("Error:", result.stderr)


path = get_path()
run_curl(path)
