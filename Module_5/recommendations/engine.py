from datetime import date
from learning.models import Topic


def calculate_priority(topic):
    score = 0

    # User-defined priority: 10 - 50 points
    score += min(topic.priority, 10) * 5

    # Incomplete work deserves attention
    if topic.status != "completed":
        score += 25

    # Lower progress means more remaining work
    score += max(0, 20 - topic.progress // 5)

    # Difficulty
    difficulty_scores = {
        "beginner": 5,
        "intermediate": 10,
        "advanced": 15,
    }

    score += difficulty_scores.get(
        topic.difficulty,
        5
    )

    # Subject deadline urgency
    deadline = topic.subject.deadline

    if deadline:
        days = (deadline - date.today()).days

        if days <= 0:
            score += 30
        elif days <= 3:
            score += 25
        elif days <= 7:
            score += 15

    return min(score, 100)


def get_recommendations(user):
    topics = Topic.objects.filter(
        subject__user=user
    ).exclude(
        status="completed"
    )

    results = []

    for topic in topics:
        results.append({
            "topic": topic,
            "score": calculate_priority(topic),
        })

    return sorted(
        results,
        key=lambda item: item["score"],
        reverse=True
    )
