from django import forms
from .models import TravelAssessment


class AssessmentForm(forms.ModelForm):

    class Meta:
        model = TravelAssessment

        fields = [
            "origin",
            "destination",
            "duration_days",
            "budget",
            "weather_risk",
            "crowd_level",
            "transport_reliability",
            "season",
        ]

        widgets = {
            "season": forms.Select(
                choices=[
                    ("winter", "Winter"),
                    ("summer", "Summer"),
                    ("monsoon", "Monsoon"),
                    ("spring", "Spring"),
                ]
            )
        }
