from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from recommendations.engine import get_recommendations


def landing(request):
    return render(request, "dashboard/landing.html")


@login_required
def home(request):
    subjects = request.user.subjects.all()

    total_topics = sum(
        subject.topics.count()
        for subject in subjects
    )

    completed_topics = sum(
        subject.topics.filter(
            status="completed"
        ).count()
        for subject in subjects
    )

    focus_minutes = sum(
        session.minutes
        for session in request.user.focus_sessions.filter(
            completed=True
        )
    )

    progress = 0

    if total_topics:
        progress = round(
            completed_topics / total_topics * 100
        )

    recommendations = get_recommendations(
        request.user
    )

    next_item = (
        recommendations[0]
        if recommendations
        else None
    )

    return render(
        request,
        "dashboard/home.html",
        {
            "subjects": subjects,
            "total_topics": total_topics,
            "completed_topics": completed_topics,
            "focus_minutes": focus_minutes,
            "progress": progress,
            "next_item": next_item,
        }
    )
