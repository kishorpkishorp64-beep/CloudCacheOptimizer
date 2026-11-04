
import time
from pathlib import Path

from ml_model.predict_reuse import predict_reuse


class AICache:
    def __init__(self, cache_dir, max_size_mb=1):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.entries = {}

        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def current_size(self):
        total = 0
        for entry in self.entries.values():
            path = self.cache_dir / entry["filename"]
            if path.is_file():
                total += path.stat().st_size
        return total

    def get(self, filename):
        entry = self.entries.get(filename)

        if entry is None:
            self.misses += 1
            print(f"AI CACHE MISS: {filename}")
            return None

        path = self.cache_dir / entry["filename"]

        if not path.is_file():
            del self.entries[filename]
            self.misses += 1
            print(f"AI CACHE MISS: {filename} (file missing)")
            return None

        entry["access_count"] += 1
        entry["last_access"] = time.time()
        self.hits += 1

        print(f"AI CACHE HIT: {filename}")
        return path.read_bytes()

    def remove(self, filename):
        """Remove a cached object, if it exists."""
        entry = self.entries.pop(filename, None)

        if entry is not None:
            path = self.cache_dir / entry["filename"]
            path.unlink(missing_ok=True)

    def _value(self, entry):
        age = max(0, int(time.time() - entry["last_access"]))
        size_kb = max(1, entry["size_bytes"] / 1024)

        _, probability = predict_reuse(
            size_kb=size_kb,
            access_count=entry["access_count"],
            seconds_since_last_access=age,
        )

        # Give higher value to frequently accessed, recently used objects.
        frequency_score = entry["access_count"]
        recency_score = 1 / (1 + age / 60)

        return (
                probability
                * frequency_score
                * recency_score
                / size_kb
        )

        # Prefer likely-to-be-reused objects that use less space.
        return probability / size_kb
    def put(self, filename, content):
        if not filename or Path(filename).name != filename:
            raise ValueError("Use a simple filename without folder paths.")

        if not isinstance(content, bytes):
            raise TypeError("Content must be bytes.")

        if len(content) > self.max_size_bytes:
            print(f"NOT CACHED: {filename} exceeds the cache limit.")
            return False

        if filename in self.entries:
            (self.cache_dir / filename).unlink(missing_ok=True)
            del self.entries[filename]

        while (
            self.current_size() + len(content) > self.max_size_bytes
            and self.entries
        ):
            # Evict the object with the lowest predicted value.
            victim = min(
                self.entries,
                key=lambda name: self._value(self.entries[name]),
            )

            (self.cache_dir / victim).unlink(missing_ok=True)
            del self.entries[victim]
            self.evictions += 1
            print(f"AI EVICTION: {victim}")

        path = self.cache_dir / filename
        path.write_bytes(content)

        self.entries[filename] = {
            "filename": filename,
            "size_bytes": len(content),
            "access_count": 1,
            "last_access": time.time(),
        }

        print(f"AI CACHED: {filename} ({len(content)} bytes)")
        return True

    def show_stats(self):
        total = self.hits + self.misses
        hit_rate = self.hits / total * 100 if total else 0

        print("\n--- AI CACHE STATISTICS ---")
        print(f"Hits: {self.hits}")
        print(f"Misses: {self.misses}")
        print(f"Evictions: {self.evictions}")
        print(f"Cached objects: {len(self.entries)}")
        print(f"Cache size: {self.current_size()} bytes")
        print(f"Hit rate: {hit_rate:.2f}%")
