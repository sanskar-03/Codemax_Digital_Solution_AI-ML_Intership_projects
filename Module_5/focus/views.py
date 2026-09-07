from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import FocusSessionForm


@login_required
def start_session(request):
    if request.method == "POST":
        form = FocusSessionForm(
            request.POST,
            user=request.user
        )

        if form.is_valid():
            session = form.save(commit=False)
            session.user = request.user
            session.save()

            return redirect(
                "focus:timer",
                session_id=session.id
            )
    else:
        form = FocusSessionForm(user=request.user)

    return render(
        request,
        "focus/start.html",
        {"form": form}
    )


@login_required
def timer(request, session_id):
    session = request.user.focus_sessions.filter(
        id=session_id
    ).first()

    if not session:
        return redirect("focus:start")

    return render(
        request,
        "focus/timer.html",
        {"session": session}
    )


@login_required
def complete_session(request, session_id):
    session = request.user.focus_sessions.filter(
        id=session_id
    ).first()

    if session:
        session.completed = True
        session.save()

    return redirect("dashboard:home")
