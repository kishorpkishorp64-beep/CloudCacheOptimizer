
from collections import OrderedDict
from pathlib import Path


class FIFOCache:
    def __init__(self, cache_dir, max_size_mb=1):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.cache = OrderedDict()

        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def current_size(self):
        return sum(
            (self.cache_dir / name).stat().st_size
            for name in self.cache
            if (self.cache_dir / name).is_file()
        )

    def get(self, filename):
        if filename not in self.cache:
            self.misses += 1
            print(f"FIFO CACHE MISS: {filename}")
            return None

        path = self.cache_dir / filename

        if not path.is_file():
            del self.cache[filename]
            self.misses += 1
            print(f"FIFO CACHE MISS: {filename} (file missing)")
            return None

        # FIFO does not change insertion order on access.
        self.hits += 1
        print(f"FIFO CACHE HIT: {filename}")
        return path.read_bytes()

    def put(self, filename, content):
        if not filename or Path(filename).name != filename:
            raise ValueError("Use a simple filename without folder paths.")

        if not isinstance(content, bytes):
            raise TypeError("Content must be bytes.")

        if len(content) > self.max_size_bytes:
            print(f"NOT CACHED: {filename} exceeds the cache limit.")
            return False

        if filename in self.cache:
            (self.cache_dir / filename).unlink(missing_ok=True)
            del self.cache[filename]

        while (
            self.current_size() + len(content) > self.max_size_bytes
            and self.cache
        ):
            oldest, _ = self.cache.popitem(last=False)
            (self.cache_dir / oldest).unlink(missing_ok=True)
            self.evictions += 1
            print(f"FIFO EVICTION: {oldest}")

        path = self.cache_dir / filename
        path.write_bytes(content)
        self.cache[filename] = True

        print(f"FIFO CACHED: {filename} ({len(content)} bytes)")
        return True

    def show_stats(self):
        print("\n--- FIFO CACHE STATISTICS ---")
        print(f"Cache hits: {self.hits}")
        print(f"Cache misses: {self.misses}")
        print(f"Evictions: {self.evictions}")
        print(f"Cached objects: {len(self.cache)}")
        print(f"Cache size: {self.current_size()} bytes")
