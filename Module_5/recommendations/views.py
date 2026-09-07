from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .engine import get_recommendations


@login_required
def home(request):
    items = get_recommendations(request.user)

    return render(
        request,
        "recommendations/home.html",
        {"recommendations": items}
    )
