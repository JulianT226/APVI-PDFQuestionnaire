from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from PyPDF2 import PdfWriter, PdfReader
import os

def create_template():
    # Create directory for templates if it doesn't exist
    template_dir = os.path.join('static', 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # Create first page with ReportLab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Add some basic layout elements for the first page
    can.setFont("Helvetica-Bold", 16)
    can.drawString(200, 750, "Saudi Visa Application Form")
    can.setFont("Helvetica", 12)
    can.drawString(100, 700, "Personal Information")
    can.drawString(100, 400, "Contact Information")
    can.drawString(100, 200, "Declaration")
    can.save()
    
    # Create second page
    packet2 = io.BytesIO()
    can2 = canvas.Canvas(packet2, pagesize=letter)
    can2.setFont("Helvetica-Bold", 14)
    can2.drawString(100, 750, "Additional Information")
    can2.drawString(100, 500, "Travel Details")
    can2.save()
    
    # Create PDF writer and add pages
    output = PdfWriter()
    
    # Add first page
    packet.seek(0)
    new_pdf = PdfReader(packet)
    output.add_page(new_pdf.pages[0])
    
    # Add second page
    packet2.seek(0)
    new_pdf2 = PdfReader(packet2)
    output.add_page(new_pdf2.pages[0])
    
    # Save the template
    template_path = os.path.join(template_dir, 'saudi_visa_form.pdf')
    with open(template_path, 'wb') as template_file:
        output.write(template_file)
    
    print("PDF template created successfully!")

if __name__ == '__main__':
    create_template()
