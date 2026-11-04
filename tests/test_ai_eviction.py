
from pathlib import Path
from tempfile import TemporaryDirectory

from cache_engine.ai_cache import AICache


def main():
    with TemporaryDirectory() as temp_dir:
        cache_dir = Path(temp_dir)

        # Use a small cache so eviction is easy to test.
        cache = AICache(cache_dir, max_size_mb=1)

        # Fill the cache with a 600 KB object.
        cache.put("object_A.bin", b"A" * (600 * 1024))

        # Add another 600 KB object; one object must be evicted.
        cache.put("object_B.bin", b"B" * (600 * 1024))

        print("\n===== EVICTION TEST RESULTS =====")
        print("Cached objects:", list(cache.entries.keys()))
        print("Evictions:", cache.evictions)
        print("Cache size:", cache.current_size(), "bytes")

        assert cache.evictions == 1, "Expected exactly one eviction"
        assert len(cache.entries) == 1, "Expected one remaining object"
        assert cache.current_size() <= cache.max_size_bytes

        print("\nSUCCESS: Cache eviction test passed!")


if __name__ == "__main__":
    main()
