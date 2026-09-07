from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


BASE_DIR = Path(__file__).resolve().parent.parent
ARTIFACT_DIR = BASE_DIR / "ml_artifacts"


def generate_dataset(rows=10000):

    rng = np.random.default_rng(42)

    df = pd.DataFrame({
        "budget": rng.integers(5000, 250000, rows),
        "duration_days": rng.integers(1, 31, rows),
        "weather_risk": rng.integers(1, 11, rows),
        "crowd_level": rng.integers(1, 11, rows),
        "transport_reliability": rng.integers(1, 11, rows),
        "season": rng.choice(
            ["winter", "summer", "monsoon", "spring"],
            rows
        )
    })

    season_weight = df["season"].map({
        "winter": 4,
        "summer": 8,
        "monsoon": 22,
        "spring": 3,
    })

    score = (
        df["weather_risk"] * 6
        + df["crowd_level"] * 5
        - df["transport_reliability"] * 4
        + season_weight
        + rng.normal(0, 6, rows)
    )

    df["target"] = np.where(
        score < 32,
        "LOW",
        np.where(score < 65, "MEDIUM", "HIGH")
    )

    return df


def train_model(version):

    df = generate_dataset()

    X = df.drop(columns=["target"])
    y = df["target"]

    numeric_features = [
        "budget",
        "duration_days",
        "weather_risk",
        "crowd_level",
        "transport_reliability",
    ]

    categorical_features = ["season"]

    preprocessor = ColumnTransformer([
        (
            "numeric",
            "passthrough",
            numeric_features
        ),
        (
            "categorical",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            categorical_features
        ),
    ])

    pipeline = Pipeline([
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=250,
                random_state=42
            )
        ),
    ])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    pipeline.fit(X_train, y_train)

    predictions = pipeline.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    ARTIFACT_DIR.mkdir(exist_ok=True)

    artifact = (
        ARTIFACT_DIR /
        f"travelshield_{version}.pkl"
    )

    joblib.dump(pipeline, artifact)

    return str(
        artifact.relative_to(BASE_DIR)
    ), float(accuracy)
