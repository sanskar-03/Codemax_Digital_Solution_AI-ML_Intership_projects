from django import forms
from .models import TravelAssessment

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = TravelAssessment
        fields = ["origin","destination","duration_days","budget","weather_risk","crowd_level","transport_reliability","season"]
        widgets = {
            "origin": forms.TextInput(attrs={"placeholder":"e.g. Delhi"}),
            "destination": forms.TextInput(attrs={"placeholder":"e.g. Manali"}),
            "duration_days": forms.NumberInput(attrs={"min":1,"max":90,"placeholder":"e.g. 5"}),
            "budget": forms.NumberInput(attrs={"min":1000,"placeholder":"e.g. 40000"}),
            "weather_risk": forms.NumberInput(attrs={"min":1,"max":10}),
            "crowd_level": forms.NumberInput(attrs={"min":1,"max":10}),
            "transport_reliability": forms.NumberInput(attrs={"min":1,"max":10}),
            "season": forms.Select(choices=[("winter","Winter"),("summer","Summer"),("monsoon","Monsoon"),("spring","Spring")]),
        }
        labels = {
            "duration_days":"Trip duration (days)", "budget":"Trip budget (₹)",
            "weather_risk":"Weather exposure", "crowd_level":"Expected crowding",
            "transport_reliability":"Transport reliability",
        }
        help_texts = {
            "weather_risk":"1 = very low exposure · 10 = severe exposure",
            "crowd_level":"1 = quiet · 10 = extremely crowded",
            "transport_reliability":"1 = unreliable · 10 = highly reliable",
        }
