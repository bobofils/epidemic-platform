from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_pdf(
    filename,
    indicators
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    title = Paragraph(
        "Rapport Epidémique",
        styles['Title']
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )

    for key, value in indicators.items():

        p = Paragraph(
            f"{key}: {value}",
            styles['BodyText']
        )

        content.append(p)

    doc.build(content)