from pathlib import Path

from flask import Flask, jsonify, request, Response, send_from_directory

from cache_engine.ai_cache import AICache

PROJECT_DIR = Path(__file__).resolve().parent.parent
ORIGIN_DIR = PROJECT_DIR / "origin_storage"
CACHE_DIR = PROJECT_DIR / "cache_storage"

ORIGIN_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

app = Flask(__name__)

cache = AICache(CACHE_DIR, max_size_mb=1)
DASHBOARD_DIR = PROJECT_DIR / "dashboard"


@app.route("/dashboard", methods=["GET"])
def dashboard():
    return send_from_directory(DASHBOARD_DIR, "index.html")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "Cloud Computing Cache Optimizer",
        "status": "running",
        "cache_strategy": "AI",
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

    # Check the AI cache first.
    content = cache.get(filename)

    if content is not None:
        return Response(content, mimetype="application/octet-stream")

    # On a cache miss, retrieve the original object.
    original_file = ORIGIN_DIR / filename

    if not original_file.is_file():
        return jsonify({"error": "Object not found"}), 404

    content = original_file.read_bytes()

    # Ask the AI cache to store the object if it fits.
    cache.put(filename, content)

    return Response(content, mimetype="application/octet-stream")


@app.route("/objects/<filename>", methods=["PUT"])
def upload_object(filename):
    if not filename or Path(filename).name != filename:
        return jsonify({"error": "Invalid filename"}), 400

    content = request.get_data(cache=False)

    if len(content) > 1024 * 1024:
        return jsonify({"error": "Upload limit is 1 MB"}), 413

    original_file = ORIGIN_DIR / filename
    original_file.write_bytes(content)

    # Remove any stale cached copy after an upload or update.
    cache.remove(filename)

    return jsonify({
        "message": "Object saved to original storage",
        "filename": filename,
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