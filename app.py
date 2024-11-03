import os
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_wtf import CSRFProtect
from PyPDF2 import PdfReader, PdfWriter
from forms import PDFForm
import io

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "your-secret-key-here")
csrf = CSRFProtect(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PDFForm()
    if form.validate_on_submit():
        try:
            # Read the PDF template
            template_path = os.path.join(app.static_folder, 'templates', 'saudi_visa_form.pdf')
            pdf_reader = PdfReader(template_path)
            pdf_writer = PdfWriter()
            
            # Get the first page
            page = pdf_reader.pages[0]
            pdf_writer.add_page(page)
            
            # Create form fields dictionary
            form_fields = {
                'first_name': form.first_name.data,
                'middle_name': form.middle_name.data,
                'last_name': form.last_name.data,
                'mother_name': form.mother_name.data,
                'dob': form.dob.data.strftime('%Y-%m-%d'),
                'birth_place': form.birth_place.data,
                'prev_nationality': form.prev_nationality.data,
                'present_nationality': form.present_nationality.data,
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
                'phone_num': form.phone_num.data,
                'email': form.email.data,
                'bus_address_street': form.bus_address_street.data,
                'bus_address_city': form.bus_address_city.data,
                'bus_address_state': form.bus_address_state.data,
                'bus_phone_num': form.bus_phone_num.data,
                'visa_type': form.visa_type.data,
                'inviting_name': form.inviting_name.data,
                'inviting_address': form.inviting_address.data,
                'arrival_date': form.arrival_date.data.strftime('%Y-%m-%d'),
                'airline': form.airline.data,
                'flight_num': form.flight_num.data,
                'departing_city': form.departing_city.data,
                'arriving_city': form.arriving_city.data,
                'stay_duration': form.stay_duration.data
            }
            
            # Update form fields
            pdf_writer.update_page_form_field_values(
                pdf_writer.pages[0],
                form_fields
            )
            
            # Save to memory buffer
            output_buffer = io.BytesIO()
            pdf_writer.write(output_buffer)
            output_buffer.seek(0)
            
            return send_file(
                output_buffer,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=f'saudi_visa_application_{form.last_name.data}.pdf'
            )
            
        except Exception as e:
            flash(f'Error generating PDF: {str(e)}', 'danger')
            return redirect(url_for('index'))
            
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
