from django.db import models
from django.contrib.auth.models import User


class Subject(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="subjects"
    )

    name = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    goal = models.CharField(
        max_length=255,
        blank=True
    )

    deadline = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Topic(models.Model):
    DIFFICULTY = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    STATUS = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="topics"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY,
        default="beginner"
    )

    estimated_minutes = models.PositiveIntegerField(default=30)

    priority = models.PositiveIntegerField(default=5)

    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default="not_started"
    )

    progress = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
