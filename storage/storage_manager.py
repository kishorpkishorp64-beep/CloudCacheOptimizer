
from pathlib import Path

from cache_engine.cache_manager import CacheManager


class StorageManager:
    def __init__(self, project_dir, max_cache_size_mb=1):
        self.project_dir = Path(project_dir)
        self.origin_dir = self.project_dir / "origin_storage"
        self.cache_dir = self.project_dir / "cache_storage"

        self.origin_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache = CacheManager(
            self.cache_dir,
            max_size_mb=max_cache_size_mb
        )

    def get_object(self, filename):
        # Try the cache first
        cached_content = self.cache.get(filename)

        if cached_content is not None:
            return cached_content

        # If not cached, retrieve from original storage
        if not filename or Path(filename).name != filename:
            raise ValueError("Use a simple filename without folder paths.")

        original_file = self.origin_dir / filename

        if not original_file.is_file():
            print(f"OBJECT NOT FOUND: {filename}")
            return None

        content = original_file.read_bytes()
        print(f"ORIGIN STORAGE READ: {filename}")

        # Save a copy in the cache
        self.cache.put(filename, content)

        return content

    def show_stats(self):
        self.cache.show_stats()
