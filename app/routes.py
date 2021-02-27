from flask import Flask, render_template, redirect, url_for, request, flash, session, jsonify
from functools import wraps

from app import app
from app.forms import *
from app.models.application import *
from app.models.animal import Animal
from app.models.vaccination import Vaccination


def login_required(f):
    @wraps(f)
    def dec_func(*args, **kwargs):
        if not session.get('username'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return dec_func

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('username'):
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        username = form.user_name.data
        password = form.password.data

        user = User.get_user(username)
        if user and (user.password == password):
            session['username'] = user.user_name
            session['role'] = User.get_role(username)
            return redirect('/dashboard')
        else:
            flash('Invalid Credentials. Please try again.', "danger")
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session['username'] = False
    session.pop('username', None)

    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    animals = Animal.get_animals()
    animalcap = Animal.get_animalcapacity()

    return render_template('dashboard.html', animals_data=animals, title='Animal Dashboard',
                           dashboard=True, animalcap=animalcap)

@app.route('/details/<int:petid>', methods=['GET', 'POST'])
@login_required
def details(petid):
    animal_form = AnimalForm()
    vaccine_form = VaccinationForm()
    vaccine_form.petid.data = petid
    if animal_form.validate_on_submit():
        Animal.update_animal(animal_form, petid)
        flash('Animal details updated successfully', "success")
    elif vaccine_form.validate_on_submit():
        if Vaccination.update_vaccination(petid, vaccine_form, session.get('username')):
            flash('New vaccination entry added successfully', "success")
        else:
            flash('Invalid vaccination entry', "danger")
        
    animal = Animal.get_animal(petid)
    animal_form = populate_form(animal)
    vaccines = Vaccination.get_vaccines(petid)
    vaccine_form.vaccine_type.choices = Vaccination.get_eligible_vaccines(petid)

    return render_template('animaldetail.html', animal_form=animal_form, vaccine_form=vaccine_form, vaccines=vaccines, details=True)

@app.route('/addanimal', methods=['GET', 'POST'])
@login_required
def addanimal():
    form = AnimalForm()
    form.add_animal = True
    if  form.species.data == 'None':
        form.breed.choices = [(i['breed'],i['breed']) for i in Animal.get_breedspecies('Cat')]
    else:
        form.breed.choices = [(i['breed'],i['breed']) for i in Animal.get_breedspecies(form.species.data)]
    if form.validate_on_submit():
        animal = Animal(None, form.name.data, form.species.data, form.sex.data, form.alteration_status.data,
                        form.age.data, form.description.data,form.surrender_date.data, form.surrender_reason.data,
                        form.is_animal_control_surrender.data, breed=form.breed.data, microchipid=form.microchipid.data)
        petid = Animal.add_animal(animal, session.get('username'))
        flash('Pet record with id {} created successfully'.format(petid),"success")
        return redirect(url_for('details', petid=petid))

    return render_template('addanimal.html', form=form, addanimal=True)

def populate_form(animal):
    form = AnimalForm()
    form.species.choices = Animal.get_species()
    form.name.data = animal.name
    form.sex.data = animal.sex
    form.age.data = animal.age
    form.description.data = animal.description
    form.surrender_reason.data = animal.surrender_reason
    form.surrender_date.data = animal.surrender_date
    form.is_animal_control_surrender.data = animal.is_animal_control_surrender
    form.alteration_status.data = animal.alteration_status
    form.species.data = animal.species
    form.breed.choices = [(i['breed'],i['breed']) for i in Animal.get_breedspecies(form.species.data)]
    form.breed.data = animal.breed
    form.microchipid.data = animal.microchipid

    return form

def populate_appform(applicant):
    form = AdoptionAppForm()
    form.email.data = applicant.email
    form.first_name.data = applicant.first_name
    form.last_name.data = applicant.last_name
    form.street.data = applicant.street
    form.city.data = applicant.city
    form.state.data = applicant.state
    form.zip_code.data = applicant.zip
    form.phone_number.data = applicant.phone_number

    return form
