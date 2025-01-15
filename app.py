import os
import tempfile
import uuid
import glob
import io
from datetime import datetime, timedelta
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, session
from flask_wtf import CSRFProtect
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from forms import PDFForm

# Initialize Flask app with proper configuration
app = Flask(__name__, static_folder=os.path.abspath('static'))
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))
csrf = CSRFProtect(app)

def format_date(date_obj):
    return date_obj.strftime('%m/%d/%Y') if date_obj else ''

TEMP_DIR = tempfile.gettempdir()

def cleanup_temp_files():
    """Remove PDF files older than 1 hour"""
    cutoff = datetime.now() - timedelta(hours=1)
    pattern = os.path.join(TEMP_DIR, '*.pdf')
    for f in glob.glob(pattern):
        if datetime.fromtimestamp(os.path.getctime(f)) < cutoff:
            try:
                os.remove(f)
            except OSError:
                pass


def create_overlay(data, page_number, is_ny_form=False):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)

    if page_number == 0:
        can.setFont("Helvetica", 7)
        can.drawString(444, 619, data['state'])
        can.setFont("Helvetica", 9)
        full_name = f"{data['first_name']} {data['middle_name']} {data['last_name']}"
        can.drawString(178, 122, full_name)
        current_date = datetime.today().strftime('%m/%d/%Y')
        can.drawString(103, 67, current_date)
    elif page_number == 1:
        if is_ny_form:
            full_name = f"{data['first_name']} {data['middle_name']} {data['last_name']}"
            can.drawString(67, 772, full_name)
            mother_name_full = f"{data['mother_name_first']} {data['mother_name_middle']} {data['mother_name_last']}"
            can.drawString(87, 753, mother_name_full)
            can.drawString(76, 734, data['dob'])
            can.drawString(350, 734, data['birth_place'])
            can.drawString(105, 713, data['prev_nationality'])
            can.drawString(370, 714, data['present_nationality'])
            can.drawString(350, 695, data['marital_status'])
            can.drawString(64, 674, data['religion'])
            can.drawString(80, 513, data['pass_issue_place'])
            can.drawString(81, 647, data['pass_issue_place'])
            can.drawString(426, 514, data['pass_num'])
            can.drawString(126, 500, data['pass_exp'])
            can.drawString(286, 513, data['pass_iss'])
            can.drawString(425, 648, data['profession'])
            can.drawString(256, 648, data['qualification'])

            # Combine address components
            full_address = f"{data['address_street']}, {data['address_city']}, {data['address_state']}, {data['address_country']}, {data['address_zip']}"
            can.drawString(160, 628, full_address)
            can.drawString(25, 610, data['phone_num'])

            # Business address
            full_bus_address = ""
            if data['bus_address_street']:
                full_bus_address = f"{data['bus_address_street']}, {data['bus_address_city']}, {data['bus_address_state']}"
            can.drawString(168, 592, full_bus_address)
            can.drawString(25, 574, data.get('bus_phone_num', ''))

            # Invitation details
            full_inviting_address = ""
            if data['inviting_name']:
                full_inviting_address = f"{data['inviting_name']}, {data['inviting_address_street']}, {data['inviting_address_city']}, {data['inviting_address_province']}, {data['inviting_address_postal_code']}, {data['inviting_address_country']}"
            can.setFont("Helvetica", 7)
            can.drawString(25, 240, full_inviting_address)
            can.setFont("Helvetica", 9)
            can.drawString(291, 470, data['arrival_date'])
            can.drawString(472, 472, data['departure_date'])
            can.drawString(353, 392, data['airline'])
            can.drawString(72, 391, data['arriving_city'])
            can.drawString(155, 470, data['stay_duration'])

            # Traveling companion
            traveling_companion_name = f"{data['traveling_companion_first_name']} {data['traveling_companion_middle_name']} {data['traveling_companion_last_name']}"
            can.drawString(378, 328, traveling_companion_name)
            can.drawString(25, 328, data['traveling_companion_relationship'])
            can.drawString(204, 328, data['traveling_companion_dob'])
            can.drawString(302, 328, data['traveling_companion_sex'])

            # Handle radio button selections with X marks
            can.setFont("Helvetica-Bold", 15)
            if data['sex'] == 'FEMALE':
                can.drawString(58, 694, 'X')
            elif data['sex'] == 'MALE':
                can.drawString(140, 694, 'X')

            # Visa type X marks
            visa_coordinates = {
                'WORK': (88, 552),
                'TRANSIT': (145, 552),
                'VISIT': (201, 552),
                'UMRAH': (258, 552),
                'RESIDENCE': (315, 552),
                'HAJJ': (371, 552),
                'DIPLOMACY': (428, 552),
            }

            if data['visa_type'] in visa_coordinates:
                x, y = visa_coordinates[data['visa_type']]
                can.drawString(x, y, 'X')
        else:
            can.setFont("Helvetica", 10)
            can.drawString(115, 635, data['first_name'])

            can.setFont("Helvetica", 8)
            can.drawString(270, 635, data['middle_name'])

            can.setFont("Helvetica", 10)
            can.drawString(369, 635, data['last_name'])
            can.drawString(122, 603, data['dob'])
            can.drawString(385, 603, data['birth_place'])
            can.drawString(156, 587, data['prev_nationality'])
            can.drawString(407, 588, data['present_nationality'])
            can.drawString(125, 571, data['pass_issue_place'])
            can.drawString(378, 571, data['pass_num'])
            can.drawString(135, 556, data['pass_exp'])
            can.drawString(378, 556, data['pass_iss'])
            can.drawString(113, 502, data['profession'])
            can.drawString(376, 502, data['qualification'])

            # Combine address components
            full_address = f"{data['address_street']}, {data['address_city']}, {data['address_state']}, {data['address_country']}, {data['address_zip']}"
            can.setFont("Helvetica", 8)
            can.drawString(221, 487, full_address)
            can.setFont("Helvetica", 10)
            can.drawString(55, 472, data['phone_num'])
            can.drawString(135, 457, data['email'])

            # Business address
            full_bus_address = ""
            if data['bus_address_street']:
                full_bus_address = f"{data['bus_address_street']}, {data['bus_address_city']}, {data['bus_address_state']}"
            can.drawString(55, 430, full_bus_address)
            can.drawString(320, 430, data.get('bus_phone_num', ''))

            # Invitation details
            full_inviting_address = ""
            if data['inviting_name']:
                full_inviting_address = f"{data['inviting_name']} {data['inviting_address_street']} {data['inviting_address_city']} {data['inviting_address_province']} {data['inviting_address_postal_code']} {data['inviting_address_country']}"
            can.setFont("Helvetica", 8)
            can.drawString(55, 302, full_inviting_address)
            can.setFont("Helvetica", 10)
            can.drawString(209, 261, data['arrival_date'])
            can.drawString(370, 261, data['airline'])
            can.drawString(486, 261, data['flight_num'])
            can.drawString(161, 245, data['departing_city'])
            can.drawString(451, 245, data['arriving_city'])
            can.drawString(216, 230, data['stay_duration'])

            # Traveling companion
            traveling_companion_name = f"{data['traveling_companion_first_name']} {data['traveling_companion_middle_name']} {data['traveling_companion_last_name']}"
            can.drawString(203, 198, traveling_companion_name)
            can.drawString(507, 198, data['traveling_companion_relationship'])

            # Name and date at bottom
            full_name = f"{data['first_name']} {data['middle_name']} {data['last_name']}"
            can.drawString(88, 66, full_name)
            current_date = datetime.today().strftime('%m/%d/%Y')
            can.drawString(485, 66, current_date)

            if data['religion'] == 'MUSLIM':
                can.drawString(107, 517, 'Muslim')
            else:
                can.drawString(107, 517, 'Non-Muslim')

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
                'OTHER': (478, 352),
                'COMPANION': (542, 352)
            }
            if data['visa_type'] in visa_coordinates:
                x, y = visa_coordinates[data['visa_type']]
                can.drawString(x, y, 'X')


    can.save()
    packet.seek(0)
    return packet

@app.route('/download-pdf')
def download_pdf():
    if 'pdf_download' not in session:
        return redirect(url_for('index'))

    pdf_data = session['pdf_download']
    pdf_path = os.path.join(TEMP_DIR, f"{pdf_data['id']}.pdf")

    if not os.path.exists(pdf_path):
        flash('PDF file not found', 'error')
        return redirect(url_for('index'))

    return send_file(
        pdf_path,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=pdf_data['filename']
    )

@app.route('/success')
def success():
    if 'pdf_download' not in session:
        return redirect(url_for('index'))

    download_url = url_for('download_pdf')
    return render_template('success.html', download_url=download_url)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PDFForm()

    if form.state.data == 'New York, NY':
        form.visa_type.choices = [
            ('WORK', 'Work'),
            ('TRANSIT', 'Transit'),
            ('VISIT', 'Visit'),
            ('UMRAH', 'Umrah'),
            ('RESIDENCE', 'Residence'),
            ('HAJJ', 'Hajj'),
            ('DIPLOMACY', 'Diplomacy'),
        ]

    if form.validate_on_submit():
        # Store form data in session for review
        session['form_data'] = {
            'state': form.state.data,
            'first_name': form.first_name.data,
            'middle_name': form.middle_name.data,
            'last_name': form.last_name.data,
            'dob': form.dob.data.strftime('%Y-%m-%d'),
            'birth_place': form.birth_place.data,
            'has_prev_nationality': form.has_prev_nationality.data,
            'prev_nationality': form.prev_nationality.data,
            'present_nationality': form.present_nationality.data,
            'mother_name_first': form.mother_name_first.data,
            'mother_name_middle': form.mother_name_middle.data,
            'mother_name_last': form.mother_name_last.data,
            'pass_issue_place': form.pass_issue_place.data,
            'pass_num': form.pass_num.data,
            'pass_exp': form.pass_exp.data.strftime('%Y-%m-%d'),
            'pass_iss': form.pass_iss.data.strftime('%Y-%m-%d'),
            'sex': form.sex.data,
            'marital_status': form.marital_status.data,
            'religion': form.religion.data,
            'profession': form.profession.data,
            'qualification': form.qualification.data,
            'address_street': form.address_street.data,
            'address_city': form.address_city.data,
            'address_state': form.address_state.data,
            'address_country': form.address_country.data,
            'address_zip': form.address_zip.data,
            'phone_num': form.phone_num.data,
            'email': form.email.data,
            'bus_address_street': form.bus_address_street.data,
            'bus_address_city': form.bus_address_city.data,
            'bus_address_state': form.bus_address_state.data,
            'bus_phone_num': form.bus_phone_num.data,
            'visa_type': form.visa_type.data,
            'inviting_name': form.inviting_name.data,
            'inviting_address_street': form.inviting_address_street.data,
            'inviting_address_city': form.inviting_address_city.data,
            'inviting_address_province': form.inviting_address_province.data,
            'inviting_address_postal_code': form.inviting_address_postal_code.data,
            'inviting_address_country': form.inviting_address_country.data,
            'arrival_date': form.arrival_date.data.strftime('%Y-%m-%d'),
            'departure_date': form.departure_date.data.strftime('%Y-%m-%d'),
            'airline': form.airline.data,
            'flight_num': form.flight_num.data,
            'departing_city': form.departing_city.data,
            'arriving_city': form.arriving_city.data,
            'stay_duration': form.stay_duration.data,
            'traveling_companion_first_name': form.traveling_companion_first_name.data,
            'traveling_companion_middle_name': form.traveling_companion_middle_name.data,
            'traveling_companion_last_name': form.traveling_companion_last_name.data,
            'traveling_companion_dob': form.traveling_companion_dob.data.strftime('%Y-%m-%d'),
            'traveling_companion_sex': form.traveling_companion_sex.data or '',
            'traveling_companion_relationship': form.traveling_companion_relationship.data
        }
        return redirect(url_for('review_form'))

    return render_template('form.html', form=form)

@app.route('/review', methods=['GET'])
def review_form():
    if 'form_data' not in session:
        flash('Please fill out the form first.', 'error')
        return redirect(url_for('index'))

    # Create a form instance and populate it with session data
    form = PDFForm()
    form_data = session['form_data']

    # Convert date strings back to date objects
    form.dob.data = datetime.strptime(form_data['dob'], '%Y-%m-%d').date()
    form.pass_exp.data = datetime.strptime(form_data['pass_exp'], '%Y-%m-%d').date()
    form.pass_iss.data = datetime.strptime(form_data['pass_iss'], '%Y-%m-%d').date()
    form.arrival_date.data = datetime.strptime(form_data['arrival_date'], '%Y-%m-%d').date()
    form.departure_date.data = datetime.strptime(form_data['departure_date'], '%Y-%m-%d').date()
    form.traveling_companion_dob.data = datetime.strptime(form_data['traveling_companion_dob'], '%Y-%m-%d').date()


    # Populate other fields
    for field, value in form_data.items():
        if hasattr(form, field) and field not in ['dob', 'pass_exp', 'pass_iss', 'arrival_date', 'departure_date', 'traveling_companion_dob']:
            getattr(form, field).data = value

    return render_template('review.html', form=form)

@app.route('/submit', methods=['POST'])
def submit_form():
    if 'form_data' not in session:
        flash('Please fill out the form first.', 'error')
        return redirect(url_for('index'))

    try:
        # Your existing PDF generation code here
        form_data = session['form_data']

        # Select template based on state
        state = form_data['state']
        template_name = 'saudi_visa_form_ny.pdf' if state == "New York, NY" else 'saudi_visa_form.pdf'
        template_path = os.path.join(app.static_folder, 'templates', template_name)

        app.logger.info(f"Using template {template_name} for state {state}")
        existing_pdf = PdfReader(template_path)

        is_ny_form = (template_name == 'saudi_visa_form_ny.pdf')

        output = PdfWriter()

        # Prepare form data  (Converting back to the format used in create_overlay)
        formatted_form_data = {
            'state': form_data['state'],
            'first_name': form_data['first_name'],
            'middle_name': form_data['middle_name'],
            'last_name': form_data['last_name'],
            'dob': datetime.strptime(form_data['dob'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            'birth_place': form_data['birth_place'],
            'has_prev_nationality': form_data['has_prev_nationality'],
            'prev_nationality': form_data['prev_nationality'],
            'present_nationality': form_data['present_nationality'],
            'mother_name_first': form_data['mother_name_first'],
            'mother_name_middle': form_data['mother_name_middle'],
            'mother_name_last': form_data['mother_name_last'],
            'pass_issue_place': form_data['pass_issue_place'],
            'pass_num': form_data['pass_num'],
            'pass_exp': datetime.strptime(form_data['pass_exp'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            'pass_iss': datetime.strptime(form_data['pass_iss'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            'sex': form_data['sex'],
            'marital_status': form_data['marital_status'],
            'religion': form_data['religion'],
            'profession': form_data['profession'],
            'qualification': form_data['qualification'],
            'address_street': form_data['address_street'],
            'address_city': form_data['address_city'],
            'address_state': form_data['address_state'],
            'address_country': form_data['address_country'],
            'address_zip': form_data['address_zip'],
            'phone_num': form_data['phone_num'],
            'email': form_data['email'],
            'bus_address_street': form_data['bus_address_street'],
            'bus_address_city': form_data['bus_address_city'],
            'bus_address_state': form_data['bus_address_state'],
            'bus_phone_num': form_data['bus_phone_num'],
            'visa_type': form_data['visa_type'],
            'inviting_name': form_data['inviting_name'],
            'inviting_address_street': form_data['inviting_address_street'],
            'inviting_address_city': form_data['inviting_address_city'],
            'inviting_address_province': form_data['inviting_address_province'],
            'inviting_address_postal_code': form_data['inviting_address_postal_code'],
            'inviting_address_country': form_data['inviting_address_country'],
            'arrival_date': datetime.strptime(form_data['arrival_date'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            'departure_date': datetime.strptime(form_data['departure_date'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            'airline': form_data['airline'],
            'flight_num': form_data['flight_num'],
            'departing_city': form_data['departing_city'],
            'arriving_city': form_data['arriving_city'],
            'stay_duration': form_data['stay_duration'],
            'traveling_companion_first_name': form_data['traveling_companion_first_name'],
            'traveling_companion_middle_name': form_data['traveling_companion_middle_name'],
            'traveling_companion_last_name': form_data['traveling_companion_last_name'],
            'traveling_companion_dob': datetime.strptime(form_data['traveling_companion_dob'], '%Y-%m-%d').strftime('%m/%d/%Y'),
            'traveling_companion_sex': form_data['traveling_companion_sex'],
            'traveling_companion_relationship': form_data['traveling_companion_relationship']
        }

        # Process each page
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]

            # Create and merge overlay for all pages
            overlay = PdfReader(create_overlay(formatted_form_data, i, is_ny_form))
            page.merge_page(overlay.pages[0])
            output.add_page(page)

        # Clean up old temporary files
        cleanup_temp_files()

        # Generate unique ID and filename
        pdf_id = str(uuid.uuid4())
        filename = f'saudi_visa_application_{form_data["last_name"]}.pdf'
        pdf_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")

        # Save PDF to temp file
        with open(pdf_path, 'wb') as f:
            output.write(f)

        # Store only the ID and filename in session
        session['pdf_download'] = {
            'id': pdf_id,
            'filename': filename
        }

        # Redirect to success page
        return redirect(url_for('success'))

    except Exception as e:
        app.logger.error(f"Error generating PDF: {str(e)}")
        flash(f'Error generating PDF: {str(e)}', 'danger')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)