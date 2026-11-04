
from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

PROJECT_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = PROJECT_DIR / "data" / "cache_training_data.csv"
MODEL_PATH = PROJECT_DIR / "ml_model" / "cache_reuse_model.joblib"

if not DATASET_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATASET_PATH}\n"
        "Run generate_dataset.py first."
    )

df = pd.read_csv(DATASET_PATH)

features = [
    "size_kb",
    "access_count",
    "seconds_since_last_access",
]
target = "likely_reuse"

X = df[features]
y = df[target]

if y.nunique() < 2 or y.value_counts().min() < 2:
    raise ValueError(
        "The dataset needs at least two examples of each class. "
        "Run generate_dataset.py again."
    )

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

model = RandomForestClassifier(
    n_estimators=100,
    max_depth=5,
    random_state=42,
    class_weight="balanced",
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

joblib.dump(
    {"model": model, "features": features},
    MODEL_PATH,
)
print("\n===== AI MODEL TRAINING RESULTS =====")
print("Training examples:", len(X_train))
print("Testing examples:", len(X_test))
print(f"Test accuracy: {accuracy:.2%}")
print("\nClassification report:")
print(classification_report(y_test, predictions, zero_division=0))
print("\nModel saved to:", MODEL_PATH)
print("\nSTEP 8 COMPLETED SUCCESSFULLY!")
