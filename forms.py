from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, RadioField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional

class PDFForm(FlaskForm):
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    birth_place = StringField('Country of Birth', validators=[DataRequired(), Length(max=100)])
    
    # Nationality Information
    prev_nationality = StringField('Previous Nationality', validators=[Optional(), Length(max=50)])
    present_nationality = StringField('Present Nationality', validators=[DataRequired(), Length(max=50)])
    
    # Passport Information
    pass_issue_place = StringField('Passport Issue Place', validators=[DataRequired(), Length(max=100)])
    pass_num = StringField('Passport Number', validators=[DataRequired(), Length(max=20)])
    pass_exp = DateField('Expiry Date', validators=[DataRequired()])
    pass_iss = DateField('Issue Date', validators=[DataRequired()])
    
    # Personal Details
    sex = RadioField('Sex', choices=[('MALE', 'Male'), ('FEMALE', 'Female')], validators=[DataRequired()])
    marital_status = RadioField('Marital Status', 
                              choices=[('MARRIED', 'Married'), ('SINGLE', 'Single')],
                              validators=[DataRequired()])
    religion = RadioField('Religion', 
                          choices=[('MUSLIM', 'Muslim'), ('NON-MUSLIM', 'Non-Muslim')],
                          validators=[DataRequired()])
    profession = StringField('Profession', validators=[DataRequired(), Length(max=100)])
    qualification = StringField('Qualification', validators=[DataRequired(), Length(max=100)])
    
    # Contact Information
    address_street = StringField('Street', validators=[DataRequired(), Length(max=200)])
    address_city = StringField('City', validators=[DataRequired(), Length(max=100)])
    address_state = StringField('State/Province', validators=[DataRequired(), Length(max=100)])
    phone_num = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    
    # Business Information
    bus_address_street = StringField('Street', validators=[Optional(), Length(max=200)])
    bus_address_city = StringField('City', validators=[Optional(), Length(max=100)])
    bus_address_state = StringField('State/Province', validators=[Optional(), Length(max=100)])
    bus_phone_num = StringField('Employer Phone Number', validators=[Optional(), Length(min=10, max=15)])
    
    # Visa Information
    visa_type = SelectField('Visa Type', choices=[
        ('EMPLOYMENT', 'Employment'),
        ('RESIDENCE', 'Residence'),
        ('STUDENT', 'Student'),
        ('UMRAH', 'Umrah'),
        ('HAJJ', 'Hajj'),
        ('DIPLOMAT', 'Diplomat'),
        ('SPECIAL', 'Special'),
        ('PERSONNEL', 'Personnel'),
        ('REENTRY', 'Re-entry'),
        ('TOURISM', 'Tourism'),
        ('COMMERCE', 'Commerce'),
        ('BUSINESSMEN', 'Businessmen'),
        ('GOVERNMENT', 'Government'),
        ('WORK VISIT', 'Work Visit'),
        ('FAMILY VISIT', 'Family Visit'),
        ('OTHERS', 'Others'),
        ('COMPANION', 'Companion')
    ], validators=[DataRequired()])
    
    # Invitation Details
    inviting_name = StringField('Inviting Person/Organization Name', validators=[DataRequired(), Length(max=200)])
    inviting_address = TextAreaField('Inviting Person/Organization Address', validators=[DataRequired(), Length(max=500)])
    
    # Travel Information
    arrival_date = DateField('Arrival Date', validators=[Optional()])
    airline = StringField('Airline', validators=[Optional(), Length(max=100)])
    flight_num = StringField('Flight Number', validators=[Optional(), Length(max=20)])
    departing_city = StringField('Departing City', validators=[Optional(), Length(max=100)])
    arriving_city = StringField('Arriving City', validators=[Optional(), Length(max=100)])
    stay_duration = StringField('Duration of Stay', validators=[Optional(), Length(max=50)])
