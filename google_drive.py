
import os

from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# Google Drive permission: access only files created or selected by this app
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Project paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CREDENTIALS_FILE = os.path.join(
    BASE_DIR,
    "credentials",
    "client_secret_191045384051-u518mjg6ieesjlho7kismsr39j3c9i8k.apps.googleusercontent.com.json"
)

TOKEN_FILE = os.path.join(
    BASE_DIR,
    "credentials",
    "token.json"
)

# App-owned test folder name
TEST_FOLDER_NAME = "CloudCacheOptimizer_AppTest"


def connect_google_drive():
    """Authenticate and connect to Google Drive."""

    creds = None

    # Load saved authentication token
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(
            TOKEN_FILE, SCOPES
        )

    # Authenticate if necessary
    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    "Google OAuth credentials file was not found. "
                    "Check the credentials folder."
                )

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        # Save token securely
        os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)

        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # Build Google Drive service
    service = build(
        "drive",
        "v3",
        credentials=creds
    )

    print("Google Drive connected successfully!")

    return service


def find_app_test_folder(service):
    """Find the test folder previously created by this app."""

    results = service.files().list(
        q=(
            f"name = '{TEST_FOLDER_NAME}' "
            "and mimeType = 'application/vnd.google-apps.folder' "
            "and trashed = false"
        ),
        spaces="drive",
        fields="files(id, name)"
    ).execute()

    folders = results.get("files", [])

    if folders:
        folder = folders[0]

        print("Test folder already exists:", folder["name"])
        print("Folder ID:", folder["id"])

        return folder["id"]

    return None


def create_app_test_folder(service):
    """Create a test folder owned by this application."""

    folder_metadata = {
        "name": TEST_FOLDER_NAME,
        "mimeType": "application/vnd.google-apps.folder"
    }

    folder = service.files().create(
        body=folder_metadata,
        fields="id, name"
    ).execute()

    print("Test folder created successfully!")
    print("Folder name:", folder["name"])
    print("Folder ID:", folder["id"])

    return folder["id"]


def get_or_create_test_folder(service):
    """Find the app test folder or create it if missing."""

    folder_id = find_app_test_folder(service)

    if folder_id:
        return folder_id

    return create_app_test_folder(service)


if __name__ == "__main__":

    try:
        drive = connect_google_drive()

        folder_id = get_or_create_test_folder(drive)

        print("\nGoogle Drive setup completed!")
        print("Test folder ID:", folder_id)

    except Exception as error:
        print("\nGoogle Drive setup failed.")
        print("Error:", error)
