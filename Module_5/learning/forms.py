from django import forms
from .models import Subject, Topic


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ["name", "description", "goal", "deadline"]


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            "title",
            "description",
            "difficulty",
            "estimated_minutes",
            "priority",
        ]
