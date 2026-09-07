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

            "origin": forms.TextInput(
                attrs={
                    "placeholder": "Delhi",
                }
            ),

            "destination": forms.TextInput(
                attrs={
                    "placeholder": "Manali",
                }
            ),

            "duration_days": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 90,
                    "placeholder": "5",
                }
            ),

            "budget": forms.NumberInput(
                attrs={
                    "min": 1000,
                    "step": 500,
                    "placeholder": "40000",
                }
            ),

            "weather_risk": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "placeholder": "1 to 10",
                }
            ),

            "crowd_level": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "placeholder": "1 to 10",
                }
            ),

            "transport_reliability": forms.NumberInput(
                attrs={
                    "min": 1,
                    "max": 10,
                    "placeholder": "1 to 10",
                }
            ),

            "season": forms.Select(
                choices=[
                    ("winter", "Winter"),
                    ("spring", "Spring"),
                    ("summer", "Summer"),
                    ("monsoon", "Monsoon"),
                ]
            ),
        }

        labels = {
            "origin": "Starting city",
            "destination": "Destination",
            "duration_days": "Trip duration (days)",
            "budget": "Trip budget (₹)",
            "weather_risk": "Weather exposure",
            "crowd_level": "Expected crowding",
            "transport_reliability": "Transport reliability",
            "season": "Travel season",
        }

        help_texts = {
            "weather_risk":
                "1 = very low weather exposure · 10 = severe weather exposure",

            "crowd_level":
                "1 = quiet · 10 = extremely crowded",

            "transport_reliability":
                "1 = unreliable · 10 = highly reliable",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "field-control"
