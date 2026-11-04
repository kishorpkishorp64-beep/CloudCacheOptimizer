
from pathlib import Path

import joblib
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_DIR / "ml_model" / "cache_reuse_model.joblib"

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Trained model not found. Run train_model.py first."
    )

saved = joblib.load(MODEL_PATH)
model = saved["model"]
features = saved["features"]


def predict_reuse(size_kb, access_count, seconds_since_last_access):
    sample = pd.DataFrame([{
        "size_kb": size_kb,
        "access_count": access_count,
        "seconds_since_last_access": seconds_since_last_access,
    }])

    probability = model.predict_proba(sample[features])[0]
    classes = list(model.classes_)
    reuse_index = classes.index(1)

    reuse_probability = float(probability[reuse_index])
    prediction = int(reuse_probability >= 0.5)

    return prediction, reuse_probability


if __name__ == "__main__":
    examples = [
        (100, 80, 30),
        (450, 3, 3000),
        (200, 60, 120),
    ]

    print("===== AI CACHE REUSE PREDICTIONS =====")

    for size, accesses, age in examples:
        prediction, probability = predict_reuse(size, accesses, age)

        print(f"\nObject size: {size} KB")
        print(f"Access count: {accesses}")
        print(f"Seconds since last access: {age}")
        print(f"Predicted reuse: {'Likely' if prediction else 'Unlikely'}")
        print(f"Reuse probability: {probability:.2%}")
