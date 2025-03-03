import os
import tempfile
import uuid
import glob
from datetime import datetime, timedelta
from flask import Flask, render_template, send_file, flash, redirect, url_for
from flask import session
from flask import request
import io
from flask_wtf import CSRFProtect
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from forms import PDFForm

app = Flask(__name__, static_folder=os.path.abspath('static'))
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key-here")

DATE_FORMAT = "%m/%d/%Y"


def format_date(date_obj):
    return date_obj.strftime('%m/%d/%Y') if date_obj else ''


def parse_date_str(date_str):
    """
    Convert a string like 'MM/DD/YYYY' back into a datetime.date object.
    If date_str is empty or invalid, returns None.
    """
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, DATE_FORMAT).date()
    except ValueError:
        return None


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


csrf = CSRFProtect(app)


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
            can.setFont("Helvetica", 8)
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
            can.drawString(80, 515, data['pass_issue_place'])
            can.drawString(81, 647, data['pass_issue_place'])
            can.drawString(427, 515, data['pass_num'])
            can.drawString(126, 500, data['pass_exp'])
            can.drawString(286, 515, data['pass_iss'])
            can.drawString(425, 648, data['profession'])
            can.drawString(256, 648, data['qualification'])

            # Combine address components
            full_address = f"{data['address_street']}, {data['address_city']}, {data['address_state']}, {data['address_zip']}, {data['address_country']}"
            can.drawString(160, 628, full_address)
            can.drawString(25, 610, data['phone_num'])

            # Business address
            full_bus_address = ""
            if data['bus_address_street']:
                full_bus_address = f"{data['bus_address_street']}, {data['bus_address_city']}, {data['bus_address_state']}, {data['bus_address_zip']}, {data['bus_address_country']}"
            can.drawString(168, 592, data.get('bus_phone_num', ''))
            can.drawString(25, 574, full_bus_address)

            # Invitation details
            full_inviting_address = ""
            if data['inviting_name']:
                full_inviting_address = f"{data['inviting_name']} {data['inviting_address_street']} {data['inviting_address_city']} {data['inviting_address_province']} {data['inviting_address_postal_code']} {data['inviting_address_country']}"
            can.drawString(25, 240, full_inviting_address)
            can.drawString(291, 473, data['arrival_date'])
            can.drawString(472, 473, data['departure_date'])
            can.drawString(353, 395, data['airline'])
            can.drawString(72, 395, data['arriving_city'])
            can.drawString(155, 473, data['stay_duration'])

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
            can.setFont("Helvetica", 8)
            can.drawString(115, 635, data['first_name'])
            can.drawString(271, 635, data['middle_name'])
            can.drawString(368, 635, data['last_name'])
            mother_name_full = f"{data['mother_name_first']} {data['mother_name_middle']} {data['mother_name_last']}"
            can.drawString(134, 619, mother_name_full)
            can.drawString(122, 603, data['dob'])
            can.drawString(382, 603, data['birth_place'])
            can.drawString(156, 588, data['prev_nationality'])
            can.drawString(407, 588, data['present_nationality'])
            can.drawString(125, 572, data['pass_issue_place'])
            can.drawString(376, 572, data['pass_num'])
            can.drawString(136, 556, data['pass_exp'])
            can.drawString(377, 556, data['pass_iss'])
            can.drawString(112, 502, data['profession'])
            can.drawString(374, 502, data['qualification'])

            # Combine address components
            full_address = f"{data['address_street']}, {data['address_city']}, {data['address_state']}, {data['address_zip']}, {data['address_country']}"
            can.drawString(55, 475, full_address)
            can.drawString(221, 488, data['phone_num'])
            can.drawString(135, 457, data['email'])
            
            # Business address
            full_bus_address = ""
            if data['bus_address_street']:
                full_bus_address = f"{data['bus_address_street']} {data['bus_address_city']} {data['bus_address_state']} {data['bus_address_country']} {data['bus_address_zip']}"
            can.drawString(55, 430, full_bus_address)
            can.drawString(230, 444, data.get('bus_phone_num', ''))

            # Invitation details
            full_inviting_address = ""
            if data['inviting_name']:
                full_inviting_address = f"{data['inviting_name']} {data['inviting_address_street']} {data['inviting_address_city']} {data['inviting_address_province']} {data['inviting_address_postal_code']} {data['inviting_address_country']}"
            can.drawString(55, 302, full_inviting_address)
            can.drawString(209, 262, data['arrival_date'])
            can.drawString(370, 262, data['airline'])
            can.drawString(486, 262, data['flight_num'])
            can.drawString(161, 245, data['departing_city'])
            can.drawString(451, 245, data['arriving_city'])
            can.drawString(217, 229, data['stay_duration'])

            # Traveling companion
            traveling_companion_name = f"{data['traveling_companion_first_name']} {data['traveling_companion_middle_name']} {data['traveling_companion_last_name']}"
            can.drawString(203, 198, traveling_companion_name)
            can.drawString(507, 198, data['traveling_companion_relationship'])

            # Name and date at bottom
            full_name = f"{data['first_name']} {data['middle_name']} {data['last_name']}"
            can.drawString(88, 68, full_name)
            current_date = datetime.today().strftime('%m/%d/%Y')
            can.drawString(486, 68, current_date)

            if data['religion'] == 'MUSLIM':
                can.drawString(103, 517, 'Muslim')
            else:
                can.drawString(103, 517, 'Non-Muslim')

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
                'BUSINESS': (346, 376),
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

    return send_file(pdf_path,
                     mimetype='application/pdf',
                     as_attachment=True,
                     download_name=pdf_data['filename'])


@app.route('/review', methods=['GET'])
def review():
    if 'form_data' not in session:
        flash("Please complete your application first.", "warning")
        return redirect(url_for('index'))
    return render_template('review.html')


@app.route('/success')
def success():
    if 'pdf_download' not in session:
        return redirect(url_for('index'))

    download_url = url_for('download_pdf')
    template_name = session['pdf_download'].get('template_name',
                                                'saudi_visa_form.pdf')
    blank_pdf_url = url_for('static', filename=f'templates/{template_name}')
    return render_template('success.html',
                           download_url=download_url,
                           blank_pdf_url=blank_pdf_url)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = PDFForm()

    # If returning from review, prepopulate the form from session data
    if request.method == 'GET' and 'form_data' in session:
        form_data = session['form_data']

        # Convert date strings back to datetime.date objects
        form_data['dob'] = parse_date_str(form_data.get('dob'))
        form_data['pass_exp'] = parse_date_str(form_data.get('pass_exp'))
        form_data['pass_iss'] = parse_date_str(form_data.get('pass_iss'))
        form_data['arrival_date'] = parse_date_str(
            form_data.get('arrival_date'))
        form_data['departure_date'] = parse_date_str(
            form_data.get('departure_date'))
        form_data['traveling_companion_dob'] = parse_date_str(
            form_data.get('traveling_companion_dob'))
        form.process(data=form_data)

    # Adjust visa type choices if state is New York, NY
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

    if request.method == 'POST':
        # If the POST came from the review page, the hidden "confirmed" field is present.
        if 'confirmed' in request.form:
            form_data = session.get('form_data')
            if not form_data:
                flash("Session expired. Please start over.", "error")
                return redirect(url_for('index'))
        else:
            # Otherwise, validate the complete form normally
            if form.validate_on_submit():
                form_data = {
                    'state': form.state.data,
                    'visa_type': form.visa_type.data,
                    'first_name': form.first_name.data,
                    'middle_name': form.middle_name.data,
                    'last_name': form.last_name.data,
                    'dob': format_date(form.dob.data),
                    'birth_place': form.birth_place.data,
                    'has_prev_nationality': form.has_prev_nationality.data,
                    'prev_nationality': form.prev_nationality.data or form.present_nationality.data,
                    'present_nationality': form.present_nationality.data,
                    'mother_name_first': form.mother_name_first.data,
                    'mother_name_middle': form.mother_name_middle.data,
                    'mother_name_last': form.mother_name_last.data,
                    'pass_issue_place': form.pass_issue_place.data,
                    'pass_num': form.pass_num.data,
                    'pass_exp': format_date(form.pass_exp.data),
                    'pass_iss': format_date(form.pass_iss.data),
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
                    'bus_address_country': form.bus_address_country.data,
                    'bus_address_zip': form.bus_address_zip.data,
                    'bus_phone_num': form.bus_phone_num.data,
                    'inviting_name': form.inviting_name.data,
                    'inviting_address_street': form.inviting_address_street.data,
                    'inviting_address_city': form.inviting_address_city.data,
                    'inviting_address_province': form.inviting_address_province.data,
                    'inviting_address_postal_code': form.inviting_address_postal_code.data,
                    'inviting_address_country': form.inviting_address_country.data,
                    'arrival_date': format_date(form.arrival_date.data),
                    'departure_date': format_date(form.departure_date.data),
                    'airline': form.airline.data,
                    'flight_num': form.flight_num.data,
                    'departing_city': form.departing_city.data,
                    'arriving_city': form.arriving_city.data,
                    'stay_duration': form.stay_duration.data,
                    'is_child': form.is_child.data,
                    'traveling_companion_first_name': form.traveling_companion_first_name.data,
                    'traveling_companion_middle_name': form.traveling_companion_middle_name.data,
                    'traveling_companion_last_name': form.traveling_companion_last_name.data,
                    'traveling_companion_dob': format_date(form.traveling_companion_dob.data),
                    'traveling_companion_sex': form.traveling_companion_sex.data or '',
                    'traveling_companion_relationship': form.traveling_companion_relationship.data
                }
                session['form_data'] = form_data
                return redirect(url_for('review'))
            else:
                # If validation fails, render the form with errors.
                return render_template('form.html', form=form)

        # User has confirmed on the review page, so proceed to generate the PDF.
        is_ny_form = (form_data['state'] == "New York, NY")
        template_name = 'saudi_visa_form_ny.pdf' if is_ny_form else 'saudi_visa_form.pdf'
        
        # Ensure static_folder is a valid string
        static_folder = app.static_folder if app.static_folder else os.getcwd()
        template_path = os.path.join(static_folder, 'templates', template_name)

        app.logger.info(
            f"Using template {template_name} for state {form_data['state']}")
        existing_pdf = PdfReader(template_path)
        output = PdfWriter()

        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            overlay = PdfReader(create_overlay(form_data, i, is_ny_form))
            page.merge_page(overlay.pages[0])
            output.add_page(page)

        cleanup_temp_files()
        pdf_id = str(uuid.uuid4())
        filename = f'saudi_visa_application_{form_data["last_name"]}.pdf'
        pdf_path = os.path.join(TEMP_DIR, f"{pdf_id}.pdf")

        with open(pdf_path, 'wb') as f:
            output.write(f)

        session['pdf_download'] = {
            'id': pdf_id,
            'filename': filename,
            'template_name': template_name
        }

        return redirect(url_for('success'))

    return render_template('form.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
