
from pathlib import Path

from google_drive import connect_google_drive
from googleapiclient.http import MediaFileUpload


# Existing Google Drive test folder
TEST_FOLDER_ID = "1FLdb5-b0m-3-AQUFXn0xmGLKOg1_DfrS"

# Create a sample file inside the project folder
BASE_DIR = Path(__file__).resolve().parent
SAMPLE_FILE = BASE_DIR / "drive_upload_sample.txt"


def upload_test_file():

    # Create sample content
    SAMPLE_FILE.write_text(
        "Hello! This is a CloudCacheOptimizer Google Drive test file.",
        encoding="utf-8"
    )

    # Connect to Google Drive
    service = connect_google_drive()

    # Prepare file details
    file_metadata = {
        "name": SAMPLE_FILE.name,
        "parents": [TEST_FOLDER_ID]
    }

    # Upload the sample file
    media = MediaFileUpload(
        str(SAMPLE_FILE),
        mimetype="text/plain"
    )

    uploaded_file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id, name, parents"
    ).execute()

    print("\nFile uploaded successfully!")
    print("File name:", uploaded_file["name"])
    print("File ID:", uploaded_file["id"])


if __name__ == "__main__":
    upload_test_file()
