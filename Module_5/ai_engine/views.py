from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from learning.models import Topic
from .services import generate_study_response


@login_required
def assistant(request):
    topics = Topic.objects.filter(
        subject__user=request.user
    )

    response_data = None

    if request.method == "POST":
        topic_id = request.POST.get("topic")
        prompt = request.POST.get("prompt")

        topic = None

        if topic_id:
            topic = topics.filter(id=topic_id).first()

        response_data = generate_study_response(
            topic,
            prompt
        )

    return render(
        request,
        "ai_engine/assistant.html",
        {
            "topics": topics,
            "response_data": response_data,
        }
    )
