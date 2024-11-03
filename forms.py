from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Email, Length

class PDFForm(FlaskForm):
    full_name = StringField('Full Name', 
        validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email',
        validators=[DataRequired(), Email()])
    phone = StringField('Phone Number',
        validators=[DataRequired(), Length(min=10, max=15)])
    address = TextAreaField('Address',
        validators=[DataRequired(), Length(max=200)])
    comments = TextAreaField('Additional Comments',
        validators=[Length(max=500)])
