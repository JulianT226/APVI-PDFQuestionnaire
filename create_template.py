from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfform
import os

def create_form_template():
    # Create the PDF template
    c = canvas.Canvas("static/templates/form_template.pdf", pagesize=letter)
    
    # Set font and size for labels
    c.setFont("Helvetica-Bold", 12)
    
    # Add form fields with proper positioning
    form = c.acroForm
    
    # Full Name field
    c.drawString(50, 700, "Full Name:")
    form.textfield(name='full_name', 
                  tooltip='Enter your full name',
                  x=50, y=670, 
                  width=500, height=30,
                  maxlen=100)
    
    # Email field
    c.drawString(50, 620, "Email:")
    form.textfield(name='email',
                  tooltip='Enter your email',
                  x=50, y=590,
                  width=500, height=30,
                  maxlen=100)
    
    # Phone field
    c.drawString(50, 540, "Phone Number:")
    form.textfield(name='phone',
                  tooltip='Enter your phone number',
                  x=50, y=510,
                  width=500, height=30,
                  maxlen=15)
    
    # Address field
    c.drawString(50, 460, "Address:")
    form.textfield(name='address',
                  tooltip='Enter your address',
                  x=50, y=380,
                  width=500, height=70)
    
    # Comments field
    c.drawString(50, 330, "Additional Comments:")
    form.textfield(name='comments',
                  tooltip='Enter any additional comments',
                  x=50, y=200,
                  width=500, height=120)
    
    # Save the PDF
    c.save()

if __name__ == '__main__':
    # Ensure the directory exists
    os.makedirs('static/templates', exist_ok=True)
    create_form_template()
    print("PDF template created successfully!")
