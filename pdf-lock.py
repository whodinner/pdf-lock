import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

def create_watermark(watermark_text):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 40)
    can.setFillGray(0.5, 0.5)
    can.saveState()
    can.translate(300, 400)
    can.rotate(45)
    can.drawCentredString(0, 0, watermark_text)
    can.restoreState()
    can.save()
    packet.seek(0)
    return PdfReader(packet)

def add_watermark(input_pdf, output_pdf, watermark_text, password=None):
    watermark = create_watermark(watermark_text)
    watermark_page = watermark.pages[0]

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    if password:
        writer.encrypt(password)

    with open(output_pdf, "wb") as f:
        writer.write(f)

    print(f"Processed: {input_pdf} -> {output_pdf}")

if __name__ == "__main__":
    watermark_text = "WATERMARK AND OR BRAND GOES HERE"
    password = "SECRETPASSWORD"
    output_dir = "output" # this is the output folder where the PDF's will be assuming you are running this by going into the folder. Works with 1 or multiple PDF's.

    os.makedirs(output_dir, exist_ok=True)

    pdf_files = [f for f in os.listdir(".") if f.lower().endswith(".pdf")]

    if not pdf_files:
        print("No PDF files found in this folder.")
    else:
        for file in pdf_files:
            infile = file
            outfile = os.path.join(output_dir, f"watermarked_{file}")
            add_watermark(infile, outfile, watermark_text, password)
