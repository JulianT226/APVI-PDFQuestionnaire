import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_wtf import CSRFProtect
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from forms import PDFForm
import io
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key-here")
csrf = CSRFProtect(app)

def create_overlay(data, page_number):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    if page_number == 0:
        can.setFont("Helvetica", 7)
        can.drawString(444, 619, "")  # consular field left empty
        can.setFont("Helvetica", 10)
        full_name = f"{data['first_name']} {data['middle_name']} {data['last_name']}"
        can.drawString(178, 122, full_name)
        current_date = datetime.today().strftime('%m/%d/%Y')
        can.drawString(103, 67, current_date)
    elif page_number == 1:
        can.drawString(115, 635, data['first_name'])
        
        can.setFont("Helvetica", 8)
        can.drawString(270, 635, data['middle_name'])
        
        can.setFont("Helvetica", 10)
        can.drawString(369, 635, data['last_name'])
        can.drawString(134, 618, data['mother_name'])
        can.drawString(122, 603, data['dob'])
        can.drawString(385, 603, data['birth_place'])
        can.drawString(156, 587, data['prev_nationality'])
        can.drawString(407, 588, data['present_nationality'])
        can.drawString(125, 571, data['pass_issue_place'])
        can.drawString(378, 571, data['pass_num'])
        can.drawString(135, 556, data['pass_exp'])
        can.drawString(378, 556, data['pass_iss'])
        can.drawString(107, 517, data['religion'])
        can.drawString(113, 502, data['profession'])
        can.drawString(376, 502, data['qualification'])
        
        # Combine address components
        full_address = f"{data['address_street']}, {data['address_city']}, {data['address_state']}"
        can.drawString(221, 487, full_address)
        can.drawString(55, 472, data['phone_num'])
        can.drawString(135, 457, data['email'])
        
        # Business address
        full_bus_address = ""
        if data['bus_address_street']:
            full_bus_address = f"{data['bus_address_street']}, {data['bus_address_city']}, {data['bus_address_state']}"
        can.drawString(55, 430, full_bus_address)
        can.drawString(320, 430, data.get('bus_phone_num', ''))
        
        # Invitation details
        inviting_name_address = f"{data['inviting_name']}, {data['inviting_address']}"
        can.drawString(55, 302, inviting_name_address)
        can.drawString(209, 261, data['arrival_date'])
        can.drawString(370, 261, data['airline'])
        can.drawString(486, 261, data['flight_num'])
        can.drawString(161, 245, data['departing_city'])
        can.drawString(451, 245, data['arriving_city'])
        can.drawString(216, 230, data['stay_duration'])
        
        # Name and date at bottom
        full_name = f"{data['first_name']} {data['middle_name']} {data['last_name']}"
        can.drawString(88, 66, full_name)
        current_date = datetime.today().strftime('%m/%d/%Y')
        can.drawString(485, 66, current_date)
        
        # Handle radio button selections with X marks
        can.setFont("Helvetica-Bold", 12)
        if data['sex'] == 'FEMALE':
            can.drawString(110, 531, 'X')
        elif data['sex'] == 'MALE':
            can.drawString(157, 531, 'X')
            
        if data['marital_status'] == 'MARRIED':
            can.drawString(365, 530, 'X')
        elif data['marital_status'] == 'SINGLE':
            can.drawString(412, 531, 'X')
            
        # Visa type X marks
        visa_coordinates = {
            'EMPLOYMENT': (105, 398),
            'RESIDENCE': (159, 398),
            'STUDENT': (217, 398),
            'UMRAH': (281, 398),
            'HAJJ': (346, 399),
            'DIPLOMAT': (413, 399),
            'SPECIAL': (478, 398),
            'PERSONNEL': (541, 398),
            'REENTRY': (157, 370),
            'TOURISM': (218, 375),
            'COMMERCE': (281, 375),
            'BUSINESSMEN': (346, 376),
            'GOVERNMENT': (413, 376),
            'WORK VISIT': (477, 375),
            'FAMILY VISIT': (541, 375),
            'OTHERS': (478, 352),
            'COMPANION': (542, 352)
        }
        if data['visa_type'] in visa_coordinates:
            x, y = visa_coordinates[data['visa_type']]
            can.drawString(x, y, 'X')

    can.save()
    packet.seek(0)
    return packet

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PDFForm()
    if form.validate_on_submit():
        try:
            # Read the PDF template
            template_path = os.path.join(app.static_folder, 'templates', 'saudi_visa_form.pdf')
            existing_pdf = PdfReader(template_path)
            
            # Debug logging for page count
            app.logger.info(f"Template PDF contains {len(existing_pdf.pages)} pages")
            
            output = PdfWriter()
            
            # Prepare form data
            form_data = {
                'first_name': form.first_name.data,
                'middle_name': form.middle_name.data,
                'last_name': form.last_name.data,
                'mother_name': form.mother_name.data,
                'dob': form.dob.data.strftime('%m/%d/%Y'),
                'birth_place': form.birth_place.data,
                'prev_nationality': form.prev_nationality.data,
                'present_nationality': form.present_nationality.data,
                'pass_issue_place': form.pass_issue_place.data,
                'pass_num': form.pass_num.data,
                'pass_exp': form.pass_exp.data.strftime('%m/%d/%Y'),
                'pass_iss': form.pass_iss.data.strftime('%m/%d/%Y'),
                'sex': form.sex.data,
                'marital_status': form.marital_status.data,
                'religion': form.religion.data,
                'profession': form.profession.data,
                'qualification': form.qualification.data,
                'address_street': form.address_street.data,
                'address_city': form.address_city.data,
                'address_state': form.address_state.data,
                'phone_num': form.phone_num.data,
                'email': form.email.data,
                'bus_address_street': form.bus_address_street.data,
                'bus_address_city': form.bus_address_city.data,
                'bus_address_state': form.bus_address_state.data,
                'bus_phone_num': form.bus_phone_num.data,
                'visa_type': form.visa_type.data,
                'inviting_name': form.inviting_name.data,
                'inviting_address': form.inviting_address.data,
                'arrival_date': form.arrival_date.data.strftime('%m/%d/%Y'),
                'airline': form.airline.data,
                'flight_num': form.flight_num.data,
                'departing_city': form.departing_city.data,
                'arriving_city': form.arriving_city.data,
                'stay_duration': form.stay_duration.data
            }
            
            # Process each page
            for i in range(len(existing_pdf.pages)):
                page = existing_pdf.pages[i]
                app.logger.info(f"Processing page {i+1}")
                
                # Create and merge overlay for all pages
                overlay = PdfReader(create_overlay(form_data, i))
                page.merge_page(overlay.pages[0])
                app.logger.info(f"Added overlay to page {i+1}")
                
                output.add_page(page)
                app.logger.info(f"Added page {i+1} to output PDF")
            
            # Save to memory buffer
            output_buffer = io.BytesIO()
            output.write(output_buffer)
            output_buffer.seek(0)
            
            app.logger.info(f"Generated PDF with {len(existing_pdf.pages)} pages")
            
            return send_file(
                output_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'saudi_visa_application_{form.last_name.data}.pdf'
            )
            
        except Exception as e:
            app.logger.error(f"Error generating PDF: {str(e)}")
            flash(f'Error generating PDF: {str(e)}', 'danger')
            return redirect(url_for('index'))
            
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
