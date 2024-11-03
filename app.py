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
            template_path = os.path.join(app.static_folder, 'templates', 'form_template.pdf')
            pdf_reader = PdfReader(template_path)
            pdf_writer = PdfWriter()
            
            # Get the first page
            page = pdf_reader.pages[0]
            pdf_writer.add_page(page)
            
            # Create form fields dictionary
            form_fields = {
                'full_name': form.full_name.data,
                'email': form.email.data,
                'phone': form.phone.data,
                'address': form.address.data,
                'comments': form.comments.data
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
                download_name='filled_form.pdf'
            )
            
        except Exception as e:
            flash(f'Error generating PDF: {str(e)}', 'danger')
            return redirect(url_for('index'))
            
    return render_template('form.html', form=form)
