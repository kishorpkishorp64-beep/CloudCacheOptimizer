
from pathlib import Path

from cache_engine.fifo_cache import FIFOCache

PROJECT_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = PROJECT_DIR / "data" / "fifo_cache"

cache = FIFOCache(CACHE_DIR, max_size_mb=1)

# Insert two objects
cache.put("object_A.txt", b"Object A data")
cache.put("object_B.txt", b"Object B data")

# Read A. FIFO keeps its original insertion position.
cache.get("object_A.txt")

# Insert C; the cache has room, so nothing is evicted yet.
cache.put("object_C.txt", b"Object C data")

# Show results
cache.show_stats()
