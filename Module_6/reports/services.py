from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def build_assessment_pdf(assessment):

    buffer = BytesIO()

    pdf = canvas.Canvas(
        buffer,
        pagesize=A4
    )

    pdf.setTitle("TravelShield Assessment")

    pdf.drawString(
        72,
        780,
        "TravelShield Assessment Report"
    )

    pdf.drawString(
        72,
        740,
        f"Route: {assessment.origin} -> "
        f"{assessment.destination}"
    )

    pdf.drawString(
        72,
        710,
        f"Risk Level: {assessment.risk_level}"
    )

    pdf.drawString(
        72,
        680,
        f"Risk Score: {assessment.risk_score}"
    )

    pdf.drawString(
        72,
        650,
        f"Confidence: {assessment.confidence}%"
    )

    if assessment.model_version:
        pdf.drawString(
            72,
            620,
            "Model Version: "
            + assessment.model_version.version
        )

    pdf.save()

    buffer.seek(0)

    return buffer
