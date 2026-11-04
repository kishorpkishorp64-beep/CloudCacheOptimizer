
from pathlib import Path

from cache_engine.cache_manager import CacheManager

PROJECT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_DIR / "cache_storage"

cache = CacheManager(CACHE_DIR, max_size_mb=1)

# Add objects to the cache
cache.put("object_A.txt", b"This is object A")
cache.put("object_B.txt", b"This is object B")

# Access an object that is cached
result = cache.get("object_A.txt")
if result is not None:
    print("DATA:", result.decode("utf-8"))

# Access an object that is not cached
cache.get("object_C.txt")

# Display statistics
cache.show_stats()
