from django import forms
from .models import FocusSession
from learning.models import Topic


class FocusSessionForm(forms.ModelForm):
    class Meta:
        model = FocusSession
        fields = ["topic", "minutes"]

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields["topic"].queryset = Topic.objects.filter(
                subject__user=user
            )
