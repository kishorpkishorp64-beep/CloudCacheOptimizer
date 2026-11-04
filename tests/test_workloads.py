
from contextlib import redirect_stdout
from io import StringIO

from cache_engine.cache_manager import CacheManager
from cache_engine.fifo_cache import FIFOCache
from cache_engine.ai_cache import AICache


CACHE_SIZE_MB = 1


def run_workload(cache, objects, requests):
    # Suppress the detailed cache logs during testing.
    with redirect_stdout(StringIO()):
        for filename in requests:
            content = cache.get(filename)

            if content is None:
                cache.put(filename, objects[filename])

    # Read the counters directly because show_stats() only prints.
    total = cache.hits + cache.misses

    return {
        "hits": cache.hits,
        "misses": cache.misses,
        "evictions": cache.evictions,
        "hit_rate": round(cache.hits / total * 100, 2) if total else 0,
    }


def repeated_access_test():
    print("\n========== REPEATED ACCESS WORKLOAD ==========")

    objects = {
        name: name[0].encode() * (400 * 1024)
        for name in ["A.txt", "B.txt", "C.txt", "D.txt", "E.txt"]
    }

    # A and B are popular before and after a short burst of other files.
    requests = (
        ["A.txt", "B.txt"] * 20
        + ["C.txt", "D.txt", "E.txt"] * 2
        + ["A.txt", "B.txt"] * 20
    )

    caches = {
        "LRU": CacheManager("storage/workload_lru", CACHE_SIZE_MB),
        "FIFO": FIFOCache("storage/workload_fifo", CACHE_SIZE_MB),
        "AI": AICache("storage/workload_ai", CACHE_SIZE_MB),
    }

    results = {}

    for name, cache in caches.items():
        results[name] = run_workload(cache, objects, requests)

    print(f"\n{'Metric':<15}{'LRU':>10}{'FIFO':>10}{'AI':>10}")
    print("-" * 45)

    for metric in ["hits", "misses", "evictions", "hit_rate"]:
        print(
            f"{metric:<15}"
            f"{results['LRU'][metric]:>10}"
            f"{results['FIFO'][metric]:>10}"
            f"{results['AI'][metric]:>10}"
        )


def sequential_access_test():
    print("\n========== SEQUENTIAL ACCESS WORKLOAD ==========")

    objects = {
        f"File{i}.txt": bytes([i]) * (400 * 1024)
        for i in range(1, 6)
    }

    # Visit every file in order, repeating the sequence 10 times.
    requests = [f"File{i}.txt" for _ in range(10) for i in range(1, 6)]

    caches = {
        "LRU": CacheManager("storage/sequential_lru", CACHE_SIZE_MB),
        "FIFO": FIFOCache("storage/sequential_fifo", CACHE_SIZE_MB),
        "AI": AICache("storage/sequential_ai", CACHE_SIZE_MB),

    }

    results = {}

    for name, cache in caches.items():
        results[name] = run_workload(cache, objects, requests)

    print(f"\n{'Metric':<15}{'LRU':>10}{'FIFO':>10}{'AI':>10}")
    print("-" * 45)

    for metric in ["hits", "misses", "evictions", "hit_rate"]:
        print(
            f"{metric:<15}"
            f"{results['LRU'][metric]:>10}"
            f"{results['FIFO'][metric]:>10}"
            f"{results['AI'][metric]:>10}"
        )


def mixed_access_test():
    print("\n========== MIXED ACCESS WORKLOAD ==========")

    objects = {
        name: name[0].encode() * (400 * 1024)
        for name in ["A.txt", "B.txt", "C.txt", "D.txt", "E.txt"]
    }

    # A and B are popular, while C, D, and E appear occasionally.
    requests = (
        ["A.txt", "B.txt", "A.txt", "C.txt",
         "A.txt", "B.txt", "D.txt", "A.txt",
         "B.txt", "E.txt", "A.txt", "B.txt"] * 5
    )

    caches = {
        "LRU": CacheManager("storage/mixed_lru", CACHE_SIZE_MB),
        "FIFO": FIFOCache("storage/mixed_fifo", CACHE_SIZE_MB),
        "AI": AICache("storage/mixed_ai", CACHE_SIZE_MB),
    }

    results = {}

    for name, cache in caches.items():
        results[name] = run_workload(cache, objects, requests)

    print(f"\n{'Metric':<15}{'LRU':>10}{'FIFO':>10}{'AI':>10}")
    print("-" * 45)

    for metric in ["hits", "misses", "evictions", "hit_rate"]:
        print(
            f"{metric:<15}"
            f"{results['LRU'][metric]:>10}"
            f"{results['FIFO'][metric]:>10}"
            f"{results['AI'][metric]:>10}"
        )


def changing_popularity_test():
    print("\n========== CHANGING POPULARITY WORKLOAD ==========")

    objects = {
        name: name[0].encode() * (400 * 1024)
        for name in ["A.txt", "B.txt", "C.txt", "D.txt", "E.txt"]
    }

    # Phase 1: A and B are popular.
    phase_one = ["A.txt", "B.txt"] * 15

    # Phase 2: popularity shifts to D and E.
    phase_two = ["D.txt", "E.txt"] * 15

    # Phase 3: the new popular files continue being requested.
    phase_three = ["D.txt", "E.txt"] * 10

    requests = phase_one + phase_two + phase_three

    caches = {
        "LRU": CacheManager("storage/changing_lru", CACHE_SIZE_MB),
        "FIFO": FIFOCache("storage/changing_fifo", CACHE_SIZE_MB),
        "AI": AICache("storage/changing_ai", CACHE_SIZE_MB),
    }

    results = {}

    for name, cache in caches.items():
        results[name] = run_workload(cache, objects, requests)

    print(f"\n{'Metric':<15}{'LRU':>10}{'FIFO':>10}{'AI':>10}")
    print("-" * 45)

    for metric in ["hits", "misses", "evictions", "hit_rate"]:
        print(
            f"{metric:<15}"
            f"{results['LRU'][metric]:>10}"
            f"{results['FIFO'][metric]:>10}"
            f"{results['AI'][metric]:>10}"
        )

if __name__ == "__main__":
    changing_popularity_test()