from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, DateField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional

class PDFForm(FlaskForm):
    
    # State Selection
    state = SelectField(
        'What state do you currently live in?',
        choices=[
            ('AL', 'Alabama'), ('AK', 'Alaska'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
            ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
            ('FL', 'Florida'), ('GA', 'Georgia'), ('HI', 'Hawaii'), ('ID', 'Idaho'),
            ('IL', 'Illinois'), ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'),
            ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'), ('MD', 'Maryland'),
            ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
            ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'),
            ('NH', 'New Hampshire'), ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'),
            ('NC', 'North Carolina'), ('ND', 'North Dakota'), ('OH', 'Ohio'), ('OK', 'Oklahoma'),
            ('OR', 'Oregon'), ('PA', 'Pennsylvania'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'),
            ('SD', 'South Dakota'), ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'),
            ('VT', 'Vermont'), ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'),
            ('WI', 'Wisconsin'), ('WY', 'Wyoming')
        ],
        validators=[DataRequired()]
    )
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    birth_place = StringField('Country of Birth', validators=[DataRequired(), Length(max=100)])

    # Nationality Information
    has_prev_nationality = RadioField(
        'Do you have a previous nationality?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired()]
    )
    prev_nationality = StringField('Previous Nationality', validators=[Optional(), Length(max=50)])
    present_nationality = StringField('Current Nationality', validators=[DataRequired(), Length(max=50)])

    # Passport Information
    pass_issue_place = StringField('Passport Issue Place', validators=[DataRequired(), Length(max=100)])
    pass_num = StringField('Passport Number', validators=[DataRequired(), Length(max=20)])
    pass_exp = DateField('Expiry Date', validators=[DataRequired()])
    pass_iss = DateField('Issue Date', validators=[DataRequired()])

    # Personal Details
    sex = RadioField(
        'Sex',
        choices=[('MALE', 'Male'), ('FEMALE', 'Female')],
        validators=[DataRequired()]
    )
    marital_status = RadioField(
        'Marital Status',
        choices=[('MARRIED', 'Married'), ('SINGLE', 'Single')],
        validators=[DataRequired()]
    )
    religion = RadioField(
        'Religion',
        choices=[('MUSLIM', 'Muslim'), ('NON-MUSLIM', 'Non-Muslim')],
        validators=[DataRequired()]
    )
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
    bus_phone_num = StringField('Phone Number', validators=[Optional(), Length(min=10, max=15)])

    # Visa Information
    visa_type = SelectField(
        'Visa Type',
        choices=[
            ('EMPLOYMENT', 'Employment'), ('RESIDENCE', 'Residence'),
            ('STUDENT', 'Student'), ('UMRAH', 'Umrah'),
            ('HAJJ', 'Hajj'), ('DIPLOMAT', 'Diplomat'),
            ('SPECIAL', 'Special'), ('PERSONNEL', 'Personnel'),
            ('REENTRY', 'Re-entry'), ('TOURISM', 'Tourism'),
            ('COMMERCE', 'Commerce'), ('BUSINESSMEN', 'Businessmen'),
            ('GOVERNMENT', 'Government'), ('WORK VISIT', 'Work Visit'),
            ('FAMILY VISIT', 'Family Visit'), ('OTHER', 'Other'),
            ('COMPANION', 'Companion')
        ],
        validators=[DataRequired()]
    )

    # Invitation Details
    inviting_name = StringField('Name', validators=[DataRequired(), Length(max=200)])
    inviting_address_street = StringField('Street', validators=[Optional(), Length(max=200)])
    inviting_address_city = StringField('City', validators=[Optional(), Length(max=100)])
    inviting_address_province = StringField('Province', validators=[Optional(), Length(max=100)])

    # Travel Information
    arrival_date = DateField('Arrival Date', validators=[DataRequired()])
    airline = StringField('Airline', validators=[Optional(), Length(max=100)])
    flight_num = StringField('Flight Number', validators=[Optional(), Length(max=20)])
    departing_city = StringField('Departing City', validators=[DataRequired(), Length(max=100)])
    arriving_city = StringField('Arriving City', validators=[DataRequired(), Length(max=100)])
    stay_duration = StringField('e.g. "2 weeks"', validators=[Optional(), Length(max=50)])

    # Traveling Companion
    is_child = RadioField(
        'Is this application for a child?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired()]
    )
    traveling_companion_first_name = StringField('Name of Traveling Companion', validators=[Optional(), Length(max=200)])
    traveling_companion_middle_name = StringField('Middle Name of Traveling Companion', validators=[Optional(), Length(max=100)])
    traveling_companion_last_name = StringField('Last Name of Traveling Companion', validators=[Optional(), Length(max=100)])
    traveling_companion_relationship = StringField(
        "Applicant's Relationship with Traveling Companion",
        validators=[Optional(), Length(max=100)]
    )
    
    # Purpose of Travel
    purpose_of_travel = TextAreaField(
        'Purpose of Travel',
        validators=[DataRequired(), Length(max=500)],
        description='Please provide detailed information about the purpose of your visit'
    )
    
    # Emergency Contact
    emergency_contact_name = StringField(
        'Emergency Contact Name',
        validators=[DataRequired(), Length(max=100)]
    )
    emergency_contact_relationship = StringField(
        'Relationship',
        validators=[DataRequired(), Length(max=50)]
    )
    emergency_contact_phone = StringField(
        'Emergency Contact Phone',
        validators=[DataRequired(), Length(min=10, max=15)]
    )
    
    # Previous Visa Information
    had_previous_visa = RadioField(
        'Have you previously been issued a Saudi visa?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired()]
    )
    previous_visa_number = StringField(
        'Previous Visa Number',
        validators=[Optional(), Length(max=20)]
    )
    previous_visa_date = DateField(
        'Previous Visa Issue Date',
        validators=[Optional()]
    )