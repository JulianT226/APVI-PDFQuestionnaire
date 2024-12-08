from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from PyPDF2 import PdfWriter
import os

def create_template():
    # Create directory for templates if it doesn't exist
    template_dir = os.path.join('static', 'templates')
    os.makedirs(template_dir, exist_ok=True)
    
    # Create PDF with form fields
    output = PdfWriter()
    
    # Create a new PDF with Reportlab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Add form fields
    form = output.add_blank_page(letter)
    
    # Personal Information fields
    form.update_page_form_field_values(
        form, {
            'first_name': '',
            'middle_name': '',
            'last_name': '',
            'mother_name': '',
            'dob': '',
            'birth_place': '',
            'prev_nationality': '',
            'present_nationality': '',
            'pass_issue_place': '',
            'pass_num': '',
            'pass_exp': '',
            'pass_iss': '',
            'sex': '',
            'marital_status': '',
            'religion': '',
            'profession': '',
            'qualification': '',
            'address_street': '',
            'address_city': '',
            'address_state': '',
            'phone_num': '',
            'email': '',
            'bus_address_street': '',
            'bus_address_city': '',
            'bus_address_state': '',
            'bus_phone_num': '',
            'visa_type': '',
            'inviting_name': '',
            'inviting_address_street': '',
            'inviting_address_city': '',
            'inviting_address_province': '',
            'arrival_date': '',
            'airline': '',
            'flight_num': '',
            'departing_city': '',
            'arriving_city': '',
            'stay_duration': '',
            'traveling_companion_first_name': '',
            'traveling_companion_middle_name': '',
            'traveling_companion_last_name': '',
            'traveling_companion_relationship': ''
        }
    )
    
    # Save the template
    template_path = os.path.join(template_dir, 'saudi_visa_form.pdf')
    with open(template_path, 'wb') as template_file:
        output.write(template_file)
    
    print("PDF template created successfully!")

if __name__ == '__main__':
    create_template()
