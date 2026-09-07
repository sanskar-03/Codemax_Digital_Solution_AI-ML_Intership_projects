from django.db import models
from django.contrib.auth.models import User
from learning.models import Topic


class QuizAttempt(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE
    )

    score = models.PositiveIntegerField(default=0)

    total_questions = models.PositiveIntegerField(default=10)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def percentage(self):
        if not self.total_questions:
            return 0

        return round(
            self.score / self.total_questions * 100
        )
