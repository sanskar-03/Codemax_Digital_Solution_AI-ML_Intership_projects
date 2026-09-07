from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from learning.models import Topic
from .models import QuizAttempt


@login_required
def quiz_home(request):
    topics = Topic.objects.filter(
        subject__user=request.user
    )

    return render(
        request,
        "quizzes/home.html",
        {"topics": topics}
    )


@login_required
def take_quiz(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id,
        subject__user=request.user
    )

    questions = [
        {
            "question": f"What is an important concept in {topic.title}?",
            "options": [
                "Core concept",
                "Unrelated topic",
                "Random answer",
                "None",
            ],
            "answer": "Core concept",
        },
        {
            "question": f"Why is {topic.title} important?",
            "options": [
                "For understanding the subject",
                "It is never useful",
                "Only for entertainment",
                "None",
            ],
            "answer": "For understanding the subject",
        },
        {
            "question": f"What should you do after learning {topic.title}?",
            "options": [
                "Practice it",
                "Forget it",
                "Avoid revision",
                "Stop learning",
            ],
            "answer": "Practice it",
        },
    ]

    if request.method == "POST":
        score = 0

        for index, item in enumerate(questions):
            if request.POST.get(f"q{index}") == item["answer"]:
                score += 1

        attempt = QuizAttempt.objects.create(
            user=request.user,
            topic=topic,
            score=score,
            total_questions=len(questions),
        )

        return redirect(
            "quizzes:result",
            attempt_id=attempt.id
        )

    return render(
        request,
        "quizzes/take_quiz.html",
        {
            "topic": topic,
            "questions": questions,
        }
    )


@login_required
def result(request, attempt_id):
    attempt = get_object_or_404(
        QuizAttempt,
        id=attempt_id,
        user=request.user
    )

    return render(
        request,
        "quizzes/result.html",
        {"attempt": attempt}
    )
