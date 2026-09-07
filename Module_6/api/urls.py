from django.urls import path

from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from workspace.models import TravelAssessment


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def assessments(request):

    queryset = TravelAssessment.objects.filter(
        user=request.user
    )

    data = []

    for item in queryset:
        data.append({
            "id": item.id,
            "origin": item.origin,
            "destination": item.destination,
            "risk_level": item.risk_level,
            "risk_score": item.risk_score,
            "confidence": item.confidence,
            "model_version": (
                item.model_version.version
                if item.model_version
                else None
            ),
        })

    return Response(data)


urlpatterns = [
    path(
        "assessments/",
        assessments,
        name="api_assessments"
    ),
]
