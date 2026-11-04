
from pathlib import Path
from tempfile import TemporaryDirectory

from cache_engine.cache_manager import CacheManager
from cache_engine.fifo_cache import FIFOCache
from cache_engine.ai_cache import AICache


def run_workload(cache, requests, objects):
    for filename in requests:
        content = cache.get(filename)

        if content is None:
            # Simulate retrieving the object from original storage.
            content = objects[filename]
            cache.put(filename, content)

    total = cache.hits + cache.misses

    return {
        "hits": cache.hits,
        "misses": cache.misses,
        "evictions": cache.evictions,
        "hit_rate": cache.hits / total * 100 if total else 0,
    }


def main():
    # Five objects, each 400 KB.
    # A 1 MB cache can hold only two of these objects.
    objects = {
        name: name[0].encode() * (400 * 1024)
        for name in ["A.txt", "B.txt", "C.txt", "D.txt", "E.txt"]
    }

    # A is frequently requested.
    # B is also reused, while C, D and E create cache pressure.
    pattern = [
        "A.txt", "B.txt", "A.txt", "C.txt",
        "A.txt", "B.txt", "A.txt", "D.txt",
        "A.txt", "B.txt", "A.txt", "E.txt",
        "A.txt", "B.txt", "C.txt", "A.txt",
        "B.txt", "A.txt", "D.txt", "A.txt",
    ]

    # Repeat the workload to observe cache behavior over time.
    requests = pattern * 5

    with TemporaryDirectory() as temp:
        base = Path(temp)

        caches = {
            "LRU": CacheManager(base / "lru", max_size_mb=1),
            "FIFO": FIFOCache(base / "fifo", max_size_mb=1),
            "AI": AICache(base / "ai", max_size_mb=1),
        }

        results = {}

        for name, cache in caches.items():
            print(f"\nRunning {name} cache...")
            results[name] = run_workload(cache, requests, objects)

    print("\n========== CACHE COMPARISON ==========")
    print(f"Total requests: {len(requests)}")
    print(f"{'Metric':<18}{'LRU':>12}{'FIFO':>12}{'AI':>12}")
    print("-" * 54)

    for metric in ("hits", "misses", "evictions"):
        print(
            f"{metric.title():<18}"
            f"{results['LRU'][metric]:>12}"
            f"{results['FIFO'][metric]:>12}"
            f"{results['AI'][metric]:>12}"
        )

    print(
        f"{'Hit rate (%)':<18}"
        f"{results['LRU']['hit_rate']:>11.2f}%"
        f"{results['FIFO']['hit_rate']:>11.2f}%"
        f"{results['AI']['hit_rate']:>11.2f}%"
    )


if __name__ == "__main__":
    main()
