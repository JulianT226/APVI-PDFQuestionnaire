from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField, DateField
from wtforms.validators import DataRequired, Email, Length, Optional

class PDFForm(FlaskForm):
    
    # State Selection
    state = SelectField(
        'Which consulate office are you applying through?',
        choices=[
            ('Washington, DC', 'Washington, DC'), ('Houston, TX', 'Houston, TX'), ('Los Angeles, CA', 'Los Angeles, CA'), ('New York, NY', 'New York, NY')
        ],
        validators=[DataRequired()]
    )
    # Personal Information
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    middle_name = StringField('Middle Name', validators=[Optional(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    mother_name_first = StringField('Mother\'s Name', validators=[Optional(), Length(max=50)])
    mother_name_middle = StringField('Mother\'s Middle Name', validators=[Optional(), Length(max=50)])
    mother_name_last = StringField('Mother\'s Last Name', validators=[Optional(), Length(max=50)])
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
    pass_exp = DateField('Date of Expiration', validators=[DataRequired()])
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
    address_country = StringField('Country', validators=[DataRequired(), Length(max=100)])
    address_zip = StringField('Zip Code', validators=[Optional(), Length(max=10)])
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
            ('EMPLOYMENT', 'Work'), ('RESIDENCE', 'Residential'),
            ('STUDENT', 'Student'), ('UMRAH', 'Umrah'),
            ('HAJJ', 'Hajj'), ('DIPLOMAT', 'Diplomat'),
            ('SPECIAL', 'Special'), ('PERSONNEL', 'Personnel'),
            ('REENTRY', 'Re-entry'), ('TOURISM', 'Tourist'),
            ('COMMERCE', 'Commerce'), ('BUSINESSMEN', 'Business'),
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
    inviting_address_postal_code = StringField('Postal Code', validators=[Optional(), Length(max=20)])
    inviting_address_country = StringField('Country', validators=[Optional(), Length(max=100)])

    # Travel Information
    arrival_date = DateField('Arrival Date', validators=[DataRequired()])
    departure_date = DateField('Departure Date', validators=[Optional()])
    airline = StringField('Airline', validators=[Optional(), Length(max=100)])
    flight_num = StringField('Flight Number', validators=[Optional(), Length(max=20)])
    departing_city = StringField('Departing City', validators=[DataRequired(), Length(max=100)])
    arriving_city = StringField('Arriving City', validators=[DataRequired(), Length(max=100)])
    stay_duration = StringField('Stay Duration', validators=[Optional(), Length(max=50)])

    # Traveling Companion
    is_child = RadioField(
        'Is this application for a child?',
        choices=[('Yes', 'Yes'), ('No', 'No')],
        validators=[DataRequired()]
    )
    traveling_companion_first_name = StringField('Name of Traveling Companion', validators=[Optional(), Length(max=200)])
    traveling_companion_middle_name = StringField('Middle Name of Traveling Companion', validators=[Optional(), Length(max=100)])
    traveling_companion_last_name = StringField('Last Name of Traveling Companion', validators=[Optional(), Length(max=100)])
    traveling_companion_dob = DateField('Date of Birth of Traveling Companion', validators=[Optional()])
    traveling_companion_sex = RadioField(
        'Traveling Companion Sex',
        choices=[('Male', 'Male'), ('Female', 'Female')],
        validators=[Optional()]
    )
    traveling_companion_relationship = StringField(
        "Applicant's Relationship with Traveling Companion",
        validators=[Optional(), Length(max=100)]
    )