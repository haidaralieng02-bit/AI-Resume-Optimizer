from io import BytesIO
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT

def create_pdf(text):
    out = BytesIO()
    doc = SimpleDocTemplate(out, pagesize=LETTER, rightMargin=45, leftMargin=45,
                            topMargin=45, bottomMargin=45)
    styles = getSampleStyleSheet()
    body = ParagraphStyle("ResumeBody", parent=styles["BodyText"], fontName="Helvetica",
                          fontSize=9.5, leading=12)
    heading = ParagraphStyle("ResumeHeading", parent=body, fontName="Helvetica-Bold",
                             fontSize=10.5, leading=14, spaceBefore=7, spaceAfter=3)
    story = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            story.append(Spacer(1, 4))
            continue
        safe = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        style = heading if line.isupper() and len(line) < 60 else body
        story.append(Paragraph(safe, style))
    doc.build(story)
    return out.getvalue()
