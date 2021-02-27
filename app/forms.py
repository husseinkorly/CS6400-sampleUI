from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectField, SelectMultipleField, PasswordField, TextAreaField, DecimalField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError, NumberRange, Email, InputRequired
from wtforms.fields.html5 import DateField
from wtforms_components import DateRange
from flask_wtf import FlaskForm
from flask import session
from datetime import date

from app.models.animal import Animal
from app.models.vaccination import Vaccination


class LoginForm(FlaskForm):
    user_name = StringField("User Name", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    search = SubmitField('Search')


class AnimalForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=1, max=50)])
    sex = SelectField('Sex', choices=[('male', 'Male'), ('female', 'Female'), ('unknown', 'Unknown')])
    age = IntegerField('Age in Months', validators=[DataRequired(), NumberRange(min=1)])
    description = TextAreaField('Description', validators=[DataRequired(), Length(min=1, max=250)])
    surrender_reason = TextAreaField('Surrender Reason', validators=[DataRequired(), Length(min=1, max=250)])
    surrender_date = DateField('Surrender Date', format='%Y-%m-%d', validators=[DataRequired(), DateRange(max=date.today())])
    is_animal_control_surrender = BooleanField('Surrendered by Animal Control')
    alteration_status = BooleanField('Neutered/Spayed')
    species = SelectField('Species', choices=Animal.get_species())
    breed = SelectMultipleField('Breed', choices=Animal.get_breeds(), validators=[DataRequired()])
    microchipid = StringField('MicrochipId')
    submit = SubmitField('Submit')
    add_animal = False

    def validate_species(self, species):
        if self.add_animal and (Animal.get_animalcapacity()[species.data])-1 < 0:
            raise ValidationError('No space available to add a {}'.format(species.data))

    def validate_breed(self, breed):
        breeds = breed.data
        if len(breeds) > 1 and ('Unknown' in breeds or 'Mixed' in breeds):
            raise ValidationError('Invalid selection')


class VaccinationForm(FlaskForm):
    petid        = HiddenField()
    vaccine_type = SelectField('Type', choices=Vaccination.get_vaccine_types())
    vaccinationdate = DateField('Vaccination Date', format='%Y-%m-%d', validators=[DataRequired(), DateRange(max=date.today())])
    expirydate = DateField('Expiry Date', format='%Y-%m-%d', validators=[DataRequired()])
    vaccinationnumber = StringField('Vaccination Number')
    submit = SubmitField('Submit')

    def validate_vaccinationdate(self, vaccinationdate):
        if vaccinationdate.data > self.expirydate.data:
            raise ValidationError('Vaccination date cannot be greater than expiry date')
        animal = Animal.get_animal(self.petid.data)
        if vaccinationdate.data < animal.surrender_date and animal.accepted_by != session.get('username'):
            raise ValidationError('Historical vaccination can only be entered by user who made the surrender')


class AdoptionAppForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=1, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=1, max=50)])
    co_first_name = StringField('Co-applicant First Name')
    co_last_name = StringField('Co-applicant Last Name')
    street = StringField('Street', validators=[DataRequired(), Length(min=1, max=50)])
    city = StringField('City', validators=[DataRequired(), Length(min=1, max=50)])
    state = StringField('State', validators=[DataRequired(), Length(min=1, max=50)])
    zip_code = StringField('Zip Code', validators=[DataRequired(), Length(min=1, max=10)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(min=1, max=20)])
    date = DateField('Application Date',validators = [DataRequired(), DateRange(max=date.today())])
    submit = SubmitField('Submit')
