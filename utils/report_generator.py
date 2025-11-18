from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from io import BytesIO

def generate_pdf(match_percent, skills):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()

    story = []
    story.append(Paragraph("<b>Resume Analysis Report</b>", styles['Title']))
    story.append(Spacer(1, 20))

    story.append(Paragraph(f"<b>Match Score:</b> {match_percent:.2f}%", styles['Normal']))
    story.append(Spacer(1, 12))

    skill_text = ", ".join(skills)
    story.append(Paragraph(f"<b>Matched Skills:</b> {skill_text}", styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
