from django.contrib import admin
from .models import RiskModelVersion, TravelAssessment


@admin.register(RiskModelVersion)
class RiskModelVersionAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "version",
        "accuracy",
        "active",
        "created_at"
    )


@admin.register(TravelAssessment)
class TravelAssessmentAdmin(admin.ModelAdmin):
    list_display = (
        "origin",
        "destination",
        "risk_level",
        "risk_score",
        "confidence",
        "created_at"
    )
