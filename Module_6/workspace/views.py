from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)

from .forms import AssessmentForm
from .models import (
    RiskModelVersion,
    TravelAssessment
)

from ml_engine.predictor import predict
from reports.services import build_assessment_pdf


@login_required
def home(request):

    assessments = (
        TravelAssessment.objects
        .filter(user=request.user)
    )

    active_model = (
        RiskModelVersion.objects
        .filter(active=True)
        .first()
    )

    return render(
        request,
        "workspace/home.html",
        {
            "total": assessments.count(),
            "high": assessments.filter(
                risk_level="HIGH"
            ).count(),
            "active_model": active_model,
            "recent": assessments[:6],
        }
    )


@login_required
def workspace(request):

    form = AssessmentForm(
        request.POST or None
    )

    if request.method == "POST" and form.is_valid():

        assessment = form.save(
            commit=False
        )

        assessment.user = request.user

        result = predict(assessment)

        assessment.model_version = result["model"]
        assessment.risk_level = result["level"]
        assessment.risk_score = result["score"]
        assessment.confidence = result["confidence"]
        assessment.explanation = result["explanation"]

        assessment.save()

        return redirect(
            "assessment_detail",
            pk=assessment.pk
        )

    return render(
        request,
        "workspace/form.html",
        {"form": form}
    )


@login_required
def assessment_detail(request, pk):

    assessment = get_object_or_404(
        TravelAssessment,
        pk=pk,
        user=request.user
    )

    return render(
        request,
        "workspace/detail.html",
        {"assessment": assessment}
    )


@login_required
def assessment_pdf(request, pk):

    assessment = get_object_or_404(
        TravelAssessment,
        pk=pk,
        user=request.user
    )

    buffer = build_assessment_pdf(
        assessment
    )

    return FileResponse(
        buffer,
        as_attachment=True,
        filename=(
            f"travelshield_assessment_"
            f"{assessment.pk}.pdf"
        )
    )


def landing(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, "public/landing.html")


@login_required
def assessment_history(request):
    assessments = TravelAssessment.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "workspace/history.html", {"assessments": assessments})
