from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

def create_sample_pdf(path):
    c = canvas.Canvas(path, pagesize=letter)
    c.setFont("Helvetica-Bold", 20)
    c.drawString(100, 700, "Sample Document Title")  # Title (H1)

    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 660, "Section 1: Introduction")  # H2

    c.setFont("Helvetica", 12)
    c.drawString(100, 640, "This is a sample paragraph under Introduction.")

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, 600, "Subsection 1.1: Background")  # H3

    c.drawString(100, 580, "More detailed text here.")

    c.save()

# Ensure input directory exists
os.makedirs("input", exist_ok=True)
create_sample_pdf("input/sample.pdf")
print("Sample PDF created at input/sample.pdf")
