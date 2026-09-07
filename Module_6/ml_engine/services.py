from pathlib import Path
from datetime import datetime, timezone
import json

import joblib
import numpy as np
import pandas as pd

from django.conf import settings

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
)

from workspace.models import RiskModelVersion


BASE_DIR = Path(settings.BASE_DIR)

DATA_DIR = BASE_DIR / "data"
MODEL_DIR = BASE_DIR / "ml_models"

DATA_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


FEATURE_COLUMNS = [
    "weather_risk",
    "crime_risk",
    "health_risk",
    "political_risk",
    "transport_disruption",
    "destination_popularity",
    "trip_duration",
    "season_risk",
]


def generate_dataset(
    rows=3000,
    random_state=42,
):
    """
    Generate a structured synthetic travel risk dataset.

    Target:
        0 = LOW
        1 = MEDIUM
        2 = HIGH
    """

    rng = np.random.default_rng(random_state)

    weather_risk = rng.integers(
        0,
        101,
        rows,
    )

    crime_risk = rng.integers(
        0,
        101,
        rows,
    )

    health_risk = rng.integers(
        0,
        101,
        rows,
    )

    political_risk = rng.integers(
        0,
        101,
        rows,
    )

    transport_disruption = rng.integers(
        0,
        101,
        rows,
    )

    destination_popularity = rng.integers(
        0,
        101,
        rows,
    )

    trip_duration = rng.integers(
        1,
        31,
        rows,
    )

    season_risk = rng.integers(
        0,
        101,
        rows,
    )

    noise = rng.normal(
        0,
        6,
        rows,
    )

    risk_score = (
        weather_risk * 0.16
        + crime_risk * 0.24
        + health_risk * 0.14
        + political_risk * 0.20
        + transport_disruption * 0.15
        + season_risk * 0.11
        - destination_popularity * 0.04
        + trip_duration * 0.35
        + noise
    )

    risk_score = np.clip(
        risk_score,
        0,
        100,
    )

    risk_level = np.where(
        risk_score < 35,
        0,
        np.where(
            risk_score < 65,
            1,
            2,
        ),
    )

    df = pd.DataFrame(
        {
            "weather_risk": weather_risk,
            "crime_risk": crime_risk,
            "health_risk": health_risk,
            "political_risk": political_risk,
            "transport_disruption": transport_disruption,
            "destination_popularity": destination_popularity,
            "trip_duration": trip_duration,
            "season_risk": season_risk,
            "risk_score": risk_score,
            "risk_level": risk_level,
        }
    )

    dataset_path = (
        DATA_DIR /
        "travel_risk_dataset.csv"
    )

    df.to_csv(
        dataset_path,
        index=False,
    )

    return df, dataset_path


def train_and_save_model(
    version="1.0.0",
    activate=False,
):
    """
    Complete TravelShield V3 ML pipeline.
    """

    # --------------------------------------------------
    # 1. Generate dataset
    # --------------------------------------------------

    df, dataset_path = generate_dataset()

    # --------------------------------------------------
    # 2. Features and target
    # --------------------------------------------------

    X = df[
        FEATURE_COLUMNS
    ]

    y = df[
        "risk_level"
    ]

    # --------------------------------------------------
    # 3. Train/Test split
    # --------------------------------------------------

    (
        X_train,
        X_test,
        y_train,
        y_test,
    ) = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    # --------------------------------------------------
    # 4. Train model
    # --------------------------------------------------

    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1,
    )

    model.fit(
        X_train,
        y_train,
    )

    # --------------------------------------------------
    # 5. Predictions
    # --------------------------------------------------

    predictions = model.predict(
        X_test
    )

    # --------------------------------------------------
    # 6. Metrics
    # --------------------------------------------------

    accuracy = accuracy_score(
        y_test,
        predictions,
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0,
    )

    classification_results = (
        classification_report(
            y_test,
            predictions,
            output_dict=True,
            zero_division=0,
        )
    )

    # --------------------------------------------------
    # 7. Create safe version name
    # --------------------------------------------------

    safe_version = (
        version
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )

    # --------------------------------------------------
    # 8. Save .pkl model
    # --------------------------------------------------

    model_filename = (
        f"travel_risk_model_{safe_version}.pkl"
    )

    model_path = (
        MODEL_DIR /
        model_filename
    )

    trained_at = (
        datetime.now(
            timezone.utc
        ).isoformat()
    )

    model_package = {
        "model": model,
        "feature_columns": FEATURE_COLUMNS,
        "version": version,
        "trained_at": trained_at,
        "metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
        },
    }

    joblib.dump(
        model_package,
        model_path,
    )

    # --------------------------------------------------
    # 9. Save metadata JSON
    # --------------------------------------------------

    metadata = {
        "project": "TravelShield",
        "model_type": "RandomForestClassifier",
        "version": version,
        "trained_at": trained_at,
        "dataset_path": str(
            dataset_path
        ),
        "dataset_rows": int(
            len(df)
        ),
        "feature_columns": FEATURE_COLUMNS,
        "metrics": {
            "accuracy": float(
                accuracy
            ),
            "precision": float(
                precision
            ),
            "recall": float(
                recall
            ),
            "f1_score": float(
                f1
            ),
        },
        "classification_report": (
            classification_results
        ),
    }

    metadata_path = (
        MODEL_DIR /
        f"travel_risk_model_{safe_version}.json"
    )

    with open(
        metadata_path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            metadata,
            file,
            indent=4,
        )

    # --------------------------------------------------
    # 10. Register model in Django database
    # --------------------------------------------------

    if activate:

        RiskModelVersion.objects.update(
            active=False
        )

    risk_model, created = (
        RiskModelVersion.objects.update_or_create(
            version=version,
            defaults={
                "name": (
                    "TravelShield Risk "
                    "Prediction Model"
                ),
                "artifact_path": str(
                    model_path
                ),
                "accuracy": float(
                    accuracy
                ),
                "active": activate,
            },
        )
    )

    # Extra safety:
    # ensure this model becomes active
    # if --activate was provided.

    if activate and not risk_model.active:

        risk_model.active = True

        risk_model.save()

    # --------------------------------------------------
    # 11. Return training results
    # --------------------------------------------------

    return {
        "version": version,
        "rows": int(
            len(df)
        ),
        "accuracy": round(
            float(accuracy),
            4,
        ),
        "precision": round(
            float(precision),
            4,
        ),
        "recall": round(
            float(recall),
            4,
        ),
        "f1_score": round(
            float(f1),
            4,
        ),
        "dataset_path": str(
            dataset_path
        ),
        "model_path": str(
            model_path
        ),
        "metadata_path": str(
            metadata_path
        ),
        "database_record_created": (
            created
        ),
    }