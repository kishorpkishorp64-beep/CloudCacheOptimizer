
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

ORIGIN_DIR = PROJECT_DIR / "origin_storage"
CACHE_DIR = PROJECT_DIR / "cache_storage"

ORIGIN_DIR.mkdir(exist_ok=True)
CACHE_DIR.mkdir(exist_ok=True)

# Create a sample object in the original storage
sample_file = ORIGIN_DIR / "welcome.txt"
sample_file.write_text(
    "Welcome to the Cloud Computing Cache Optimizer!",
    encoding="utf-8"
)

print("ORIGINAL STORAGE:", ORIGIN_DIR)
print("CACHE STORAGE:", CACHE_DIR)
print("SAMPLE OBJECT CREATED:", sample_file.name)
print("CONTENT:", sample_file.read_text(encoding="utf-8"))
print("\nSTEP 2 COMPLETED SUCCESSFULLY!")
