# TravelShield V3

TravelShield is a travel risk and disruption assessment
platform built with Django and a versioned machine-learning
workflow.

## Core capabilities

- Authentication
- Travel assessment workflow
- Synthetic dataset generation
- Machine-learning training
- Saved `.pkl` model artifacts
- Accuracy metrics
- Model version registry
- Administrator-controlled active model
- Prediction confidence
- Explainable assessment factors
- REST API
- Weather integration service
- PDF assessment reports
- Celery background task configuration
- Redis support
- PostgreSQL support
- Docker deployment files

## Start locally

```powershell
run_local.bat
```

## Create administrator

```powershell
.venv\Scripts\python.exe manage.py createsuperuser
```

## Train the first model

```powershell
.venv\Scripts\python.exe manage.py train_risk_model --version 1.0.0 --activate
```

## Run

Open:

`http://127.0.0.1:8000/`

## API

Authenticated endpoint:

`GET /api/assessments/`

## Production note

The generated training data is synthetic and suitable for
demonstrating the software and machine-learning pipeline.
Real operational deployment requires validated real-world
datasets and domain-specific evaluation.
