from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from quizzes.models import QuizAttempt


@login_required
def home(request):
    sessions = request.user.focus_sessions.all()

    completed_sessions = sessions.filter(
        completed=True
    )

    total_minutes = sum(
        item.minutes
        for item in completed_sessions
    )

    attempts = QuizAttempt.objects.filter(
        user=request.user
    )

    average_score = 0

    if attempts.exists():
        average_score = round(
            sum(item.percentage for item in attempts)
            / attempts.count()
        )

    topics = []

    for subject in request.user.subjects.all():
        for topic in subject.topics.all():
            topics.append({
                "name": topic.title,
                "progress": topic.progress,
            })

    return render(
        request,
        "reports/home.html",
        {
            "total_minutes": total_minutes,
            "sessions": completed_sessions.count(),
            "quiz_attempts": attempts.count(),
            "average_score": average_score,
            "topics": topics,
        }
    )
