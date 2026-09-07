from django.contrib.auth.models import User
from django.db import models


class RiskModelVersion(models.Model):
    name = models.CharField(max_length=120)
    version = models.CharField(max_length=50, unique=True)
    artifact_path = models.CharField(max_length=255)
    accuracy = models.FloatField(default=0)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.active:
            RiskModelVersion.objects.exclude(
                pk=self.pk
            ).update(active=False)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} {self.version}"


class TravelAssessment(models.Model):

    RISK_LEVELS = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    origin = models.CharField(max_length=120)
    destination = models.CharField(max_length=120)

    duration_days = models.PositiveIntegerField()
    budget = models.PositiveIntegerField()

    weather_risk = models.PositiveIntegerField()
    crowd_level = models.PositiveIntegerField()
    transport_reliability = models.PositiveIntegerField()

    season = models.CharField(max_length=30)

    risk_score = models.FloatField(default=0)

    risk_level = models.CharField(
        max_length=20,
        choices=RISK_LEVELS,
        default="LOW"
    )

    confidence = models.FloatField(default=0)

    explanation = models.JSONField(default=dict)

    model_version = models.ForeignKey(
        RiskModelVersion,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]
