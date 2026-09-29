from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
import os


def create_pdf(content):

    os.makedirs("generated", exist_ok=True)

    path = "generated/LegalEase_Document.pdf"

    doc = SimpleDocTemplate(
        path,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "Title",
        parent=styles["Title"],
        alignment=TA_CENTER,
        spaceAfter=20
    )

    normal_style = ParagraphStyle(
        "Normal",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=8
    )

    story = []

    lines = content.splitlines()

    first_line = True

    for line in lines:

        line = line.strip()

        if not line:
            story.append(Spacer(1, 8))
            continue

        safe_line = (
            line
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        if first_line:
            story.append(
                Paragraph(safe_line, title_style)
            )
            first_line = False
        else:
            story.append(
                Paragraph(safe_line, normal_style)
            )

    doc.build(story)

    return path