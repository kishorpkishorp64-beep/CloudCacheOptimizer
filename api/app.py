
from pathlib import Path
from io import BytesIO

from flask import Flask, jsonify, request, Response, send_from_directory

from cache_engine.ai_cache import AICache
from google_drive import connect_google_drive
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload


PROJECT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_DIR / "cache_storage"
DASHBOARD_DIR = PROJECT_DIR / "dashboard"

CACHE_DIR.mkdir(parents=True, exist_ok=True)

# Only use this dedicated Google Drive test folder.
TEST_FOLDER_ID = "1FLdb5-b0m-3-AQUFXn0xmGLKOg1_DfrS"

app = Flask(__name__)

cache = AICache(CACHE_DIR, max_size_mb=1)

# Connect only when a Drive operation is requested.
drive_service = None


def get_drive_service():
    global drive_service

    if drive_service is None:
        drive_service = connect_google_drive()

    return drive_service


def find_drive_file(service, filename):
    """Find a file and verify its test-folder location."""

    safe_name = filename.replace("\\", "\\\\").replace("'", "\\'")

    results = service.files().list(
        q=f"name = '{safe_name}' and trashed = false",
        pageSize=100,
        fields="files(id, name, parents)"
    ).execute()

    files = results.get("files", [])

    # Keep only files inside our dedicated test folder.
    matching_files = [
        file for file in files
        if TEST_FOLDER_ID in file.get("parents", [])
    ]

    if len(matching_files) > 1:
        raise ValueError(
            "Multiple files with this name exist in the test folder."
        )

    return matching_files[0] if matching_files else None


def download_from_drive(service, file_id):
    """Download a file from Google Drive into memory."""

    request_file = service.files().get_media(fileId=file_id)

    buffer = BytesIO()
    downloader = MediaIoBaseDownload(buffer, request_file)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        if status:
            print(f"Google Drive download: {int(status.progress() * 100)}%")

    return buffer.getvalue()


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return send_from_directory(DASHBOARD_DIR, "index.html")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Cloud Computing Cache Optimizer",
        "status": "running",
        "cache_strategy": "AI",
        "storage": "Google Drive",
        "endpoints": {
            "health": "/health",
            "get_object": "/objects/<filename>",
            "upload_object": "/objects/<filename> (PUT)",
            "statistics": "/stats",
        },
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"})


@app.route("/objects/<filename>", methods=["GET"])
def get_object(filename):
    if not filename or Path(filename).name != filename:
        return jsonify({"error": "Invalid filename"}), 400

    # 1. Check the AI cache first.
    content = cache.get(filename)

    if content is not None:
        return Response(content, mimetype="application/octet-stream")

    # 2. On a cache miss, retrieve the file from Google Drive.
    try:
        service = get_drive_service()
        drive_file = find_drive_file(service, filename)

        if drive_file is None:
            return jsonify({
                "error": "Object not found in Google Drive test folder"
            }), 404

        content = download_from_drive(service, drive_file["id"])

    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    except Exception:
        app.logger.exception("Google Drive retrieval failed")
        return jsonify({"error": "Google Drive retrieval failed"}), 502

    # 3. Store the downloaded file in the AI cache if it fits.
    cache.put(filename, content)

    # 4. Return the file.
    return Response(content, mimetype="application/octet-stream")


@app.route("/objects/<filename>", methods=["PUT"])
def upload_object(filename):
    if not filename or Path(filename).name != filename:
        return jsonify({"error": "Invalid filename"}), 400

    content = request.get_data(cache=False)

    if len(content) > 1024 * 1024:
        return jsonify({"error": "Upload limit is 1 MB"}), 413

    try:
        service = get_drive_service()

        # Search only inside the dedicated test folder.
        existing_file = find_drive_file(service, filename)

        file_metadata = {
            "name": filename,
            "parents": [TEST_FOLDER_ID]
        }

        media = MediaIoBaseUpload(
            BytesIO(content),
            mimetype="application/octet-stream",
            resumable=False
        )

        if existing_file:
            uploaded_file = service.files().update(
                fileId=existing_file["id"],
                media_body=media,
                fields="id, name"
            ).execute()
        else:
            uploaded_file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, name, parents"
            ).execute()

    except ValueError as error:
        return jsonify({"error": str(error)}), 409

    except Exception:
        app.logger.exception("Google Drive upload failed")
        return jsonify({"error": "Google Drive upload failed"}), 502

    # Remove an old cached copy after a successful upload.
    cache.remove(filename)

    return jsonify({
        "message": "Object saved to Google Drive test folder",
        "filename": uploaded_file["name"],
        "file_id": uploaded_file["id"],
        "size_bytes": len(content),
    }), 201


@app.route("/stats", methods=["GET"])
def stats():
    total = cache.hits + cache.misses

    return jsonify({
        "cache_strategy": "AI",
        "cache_hits": cache.hits,
        "cache_misses": cache.misses,
        "evictions": cache.evictions,
        "cached_objects": len(cache.entries),
        "cache_size_bytes": cache.current_size(),
        "hit_rate_percent": round(
            cache.hits / total * 100, 2
        ) if total else 0,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
