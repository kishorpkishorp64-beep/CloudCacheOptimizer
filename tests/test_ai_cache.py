
from pathlib import Path
from tempfile import TemporaryDirectory

from cache_engine.ai_cache import AICache
PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "ml_model" / "cache_reuse_model.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        " Run ml_model/train_model.py before testing the AI cache."
    )

with TemporaryDirectory() as temp:
    cache = AICache(Path(temp) / "ai_cache", max_size_mb=1)

    print("\n--- ADD OBJECTS ---")
    cache.put("A.txt", b"A" * (400 * 1024))
    cache.put("B.txt", b"B" * (400 * 1024))

    print("\n--- ACCESS OBJECT A ---")
    cache.get("A.txt")

    print("\n--- ADD OBJECT C ---")
    cache.put("C.txt", b"C" * (400 * 1024))

    print("\n--- FINAL STATISTICS ---")
    cache.show_stats()
