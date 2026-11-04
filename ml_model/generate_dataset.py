
import csv
import random
from pathlib import Path

random.seed(42)

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)

dataset_path = DATA_DIR / "cache_training_data.csv"

rows = []

# Generate access-history examples for 100 objects.
for object_id in range(1, 101):
    size_kb = random.randint(10, 500)
    access_count = random.randint(1, 100)
    seconds_since_last_access = random.randint(1, 3600)

    # Synthetic label: frequent and recently accessed objects
    # are more likely to be reused.
    likely_reuse = int(
        access_count >= 50
        and seconds_since_last_access <= 600
    )

    rows.append({
        "object_id": f"object_{object_id}",
        "size_kb": size_kb,
        "access_count": access_count,
        "seconds_since_last_access": seconds_since_last_access,
        "likely_reuse": likely_reuse,
    })

with dataset_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print("AI training dataset created successfully!")
print("File:", dataset_path)
print("Number of objects:", len(rows))
print("Features: size, access frequency, recency")
print("Target: likely reuse (0 or 1)")
