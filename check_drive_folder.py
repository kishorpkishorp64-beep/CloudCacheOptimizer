
from google_drive import connect_google_drive

service = connect_google_drive()

results = service.files().list(
    q="name = 'drive_upload_sample.txt' and trashed = false",
    pageSize=100,
    fields="files(id, name, parents)"
).execute()

print("\nFiles returned by Google Drive search:")

for file in results.get("files", []):
    print(file)

if not results.get("files"):
    print("No files found by search.")
