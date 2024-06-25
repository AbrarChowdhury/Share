#!/usr/bin/env python3

import requests
import os
from urllib.parse import urlparse
from tqdm import tqdm

def download_file(url):
    try:
        # Send a GET request to download the file
        response = requests.get(url, stream=True)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract filename from the URL or Content-Disposition header
            filename = get_filename(response)
            
            # Determine the current working directory
            current_directory = os.getcwd()
            
            # Create the full path to save the file
            file_path = os.path.join(current_directory, filename)
            
            # Save the file with the determined filename
            with open(file_path, 'wb') as f:
                for chunk in tqdm(response.iter_content(chunk_size=1024), desc=filename, unit='KB', unit_scale=True):
                    if chunk:  # Filter out keep-alive new chunks
                        f.write(chunk)
            
            print(f"\nFile downloaded successfully as '{file_path}'")
        else:
            print(f"Failed to download file: HTTP status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

def get_filename(response):
    # Try to get filename from Content-Disposition header
    content_disposition = response.headers.get('content-disposition')
    if content_disposition and 'filename=' in content_disposition:
        filename = content_disposition.split('filename=')[1].strip('"\'')
    else:
        # If filename not found in headers, extract from URL
        parsed_url = urlparse(response.url)
        filename = os.path.basename(parsed_url.path)
    
    return filename

# Example usage:
if __name__ == "__main__":
    file_url = input("Enter the URL of the file you want to download: ").strip()
    download_file(file_url)
