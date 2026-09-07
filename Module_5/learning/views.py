from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Subject, Topic
from .forms import SubjectForm, TopicForm


@login_required
def subjects(request):
    items = Subject.objects.filter(user=request.user)

    return render(
        request,
        "learning/subjects.html",
        {"subjects": items}
    )


@login_required
def create_subject(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            subject = form.save(commit=False)
            subject.user = request.user
            subject.save()

            return redirect("learning:subjects")
    else:
        form = SubjectForm()

    return render(
        request,
        "learning/subject_form.html",
        {"form": form}
    )


@login_required
def subject_detail(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    topics = subject.topics.all()

    return render(
        request,
        "learning/subject_detail.html",
        {
            "subject": subject,
            "topics": topics,
        }
    )


@login_required
def create_topic(request, subject_id):
    subject = get_object_or_404(
        Subject,
        id=subject_id,
        user=request.user
    )

    if request.method == "POST":
        form = TopicForm(request.POST)

        if form.is_valid():
            topic = form.save(commit=False)
            topic.subject = subject
            topic.save()

            return redirect(
                "learning:subject_detail",
                subject_id=subject.id
            )
    else:
        form = TopicForm()

    return render(
        request,
        "learning/topic_form.html",
        {
            "form": form,
            "subject": subject,
        }
    )


@login_required
def complete_topic(request, topic_id):
    topic = get_object_or_404(
        Topic,
        id=topic_id,
        subject__user=request.user
    )

    topic.status = "completed"
    topic.progress = 100
    topic.save()

    return redirect(
        "learning:subject_detail",
        subject_id=topic.subject.id
    )
