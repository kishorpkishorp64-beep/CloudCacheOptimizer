
from pathlib import Path

from storage.storage_manager import StorageManager

PROJECT_DIR = Path(__file__).resolve().parent.parent
ORIGIN_DIR = PROJECT_DIR / "origin_storage"

ORIGIN_DIR.mkdir(parents=True, exist_ok=True)

# Create a sample object in original storage
sample = ORIGIN_DIR / "welcome.txt"
sample.write_text(
    "Welcome to the Cloud Computing Cache Optimizer!",
    encoding="utf-8"
)

storage = StorageManager(PROJECT_DIR, max_cache_size_mb=1)

print("\n--- FIRST REQUEST ---")
data = storage.get_object("welcome.txt")
if data is not None:
    print("Returned:", data.decode("utf-8"))

print("\n--- SECOND REQUEST ---")
data = storage.get_object("welcome.txt")
if data is not None:
    print("Returned:", data.decode("utf-8"))

print("\n--- CACHE STATISTICS ---")
storage.show_stats()
