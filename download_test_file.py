
from pathlib import Path

from google_drive import connect_google_drive
from googleapiclient.http import MediaIoBaseDownload
import io


# Google Drive file ID
FILE_ID = "19acjbbnOe87B4kJVvMZv42QfAN-a_Leq"

# Local download location
BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_FILE = BASE_DIR / "drive_download_sample.txt"


def download_test_file():

    # Connect to Google Drive
    service = connect_google_drive()

    # Request the file from Google Drive
    request = service.files().get_media(
        fileId=FILE_ID
    )

    # Download the file
    with open(DOWNLOAD_FILE, "wb") as file:
        downloader = MediaIoBaseDownload(
            file, request
        )

        done = False

        while not done:
            status, done = downloader.next_chunk()
            print(f"Download progress: {int(status.progress() * 100)}%")

    print("\nFile downloaded successfully!")
    print("Downloaded file:", DOWNLOAD_FILE)


if __name__ == "__main__":
    download_test_file()
