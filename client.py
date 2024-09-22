import sys
import requests
import os

# Define constants
UPLOAD_URL = 'http://localhost:5000/upload'
STATUS_URL = 'http://localhost:5000/status'
SUPPORTED_EXTENSIONS = {'.pptx'}

def is_supported_file(filepath):
    """Check if the file has a supported extension."""
    _, ext = os.path.splitext(filepath)
    return ext in SUPPORTED_EXTENSIONS

<<<<<<< HEAD
def upload_file(filepath, email=None):
    url = 'http://localhost:5000/upload'
    try:
        files = {'file': open(filepath, 'rb')}
        data = {'email': email} if email else {}
        response = requests.post(url, files=files, data=data)
=======
def upload_file(filepath):
    """
    Upload a file to the server and print the response.
>>>>>>> main

    Parameters:
    filepath (str): The path to the file to be uploaded.
    """
    if not is_supported_file(filepath):
        print(f"Unsupported file type: {filepath}. Supported types: {SUPPORTED_EXTENSIONS}")
        return

    try:
        with open(filepath, 'rb') as file:
            files = {'file': file}
            response = requests.post(UPLOAD_URL, files=files)

            if response.status_code == 200:
                try:
                    result = response.json()
                    if 'uid' in result:
                        print(f"File uploaded successfully. UID: {result['uid']}")
                    else:
                        print("File uploaded successfully.")
                        print("Server Response:", result)  # Print the entire response for debugging
                except ValueError:
                    print("Invalid JSON received from server.")
                    print("Server Response:", response.text)  # Print the entire response for debugging
            else:
                print(f"Failed to upload file. Status Code: {response.status_code}")
    except IOError as e:
        print(f"Error opening file: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

def check_status(uid):
    """
    Check the status of a file upload.

    Parameters:
    uid (str): The unique identifier of the file upload.
    """
    url = f'{STATUS_URL}?uid={uid}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Status: {result['status']}")
                if result['status'] == 'done':
                    print(f"Explanation: {result['explanation']}")
                else:
                    print("File is still pending explanation.")
            except ValueError:
                print("Invalid JSON received from server.")
                print("Server Response:", response.text)
        elif response.status_code == 404:
            print("UID not found.")
        else:
            print(f"Failed to get status. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

def get_history(email):
    url = f'http://localhost:5000/history?email={email}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            history = response.json()
            for record in history:
                print(f"UID: {record['uid']}, Filename: {record['filename']}, Status: {record['status']}, Upload Time: {record['upload_time']}, Finish Time: {record['finish_time']}, Error Message: {record['error_message']}")
        else:
            print(f"Failed to get history. Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python client.py <upload|status|history> <file_path|uid|email>")
        sys.exit(1)

    command = sys.argv[1]

    if command == "upload" and len(sys.argv) in [3, 4]:
        filepath = sys.argv[2]
        email = sys.argv[3] if len(sys.argv) == 4 else None
        upload_file(filepath, email)
    elif command == "status" and len(sys.argv) == 3:
        uid = sys.argv[2]
        check_status(uid)
    elif command == "history" and len(sys.argv) == 3:
        email = sys.argv[2]
        get_history(email)
    else:
        print("Invalid command or missing arguments.")
        print("Usage: python client.py <upload|status|history> <file_path|uid|email>")
