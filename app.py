from flask import Flask, render_template, request, redirect, url_for
from dog_data import *

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dogs')
def dogs():
    dogs = show_dogs()
    return render_template('dogs.html',dogs=dogs)

@app.route('/dog_profile/<int:dog_id>')
def dog_profile(dog_id):
    dog = read_dog_by_id(dog_id)
    return render_template('dog_profile.html',dog=dog)

@app.route('/enroll')
def enroll():
    return render_template('enroll.html')


@app.route('/process', methods=['post'])
def process():
    # Prepare data by extracting it from the HTML form
    dog_data = {'name': request.form['dog_name'],
                'breed': request.form['dog_breed'],
                'age': request.form['dog_age'],
                'owner': request.form['dog_owner'],
                'treats': request.form['dog_treats'],
                'pic': request.form['dog_pic'],
                'medical': request.form['dog_medical'],
                'trainer': assign_trainer()}
    enroll_dog(dog_data)
    return redirect(url_for('welcome', dog_name=request.form['dog_name'], dog_owner=request.form['dog_owner']))

@app.route('/welcome/<string:dog_name>/<string:dog_owner>')
def welcome(dog_name, dog_owner):
    dog = read_dog_by_name_owner(dog_name, dog_owner)
    return render_template('welcome.html', dogs=dog)

@app.route('/modify/<int:dog_id>', methods=['POST'])
def modify(dog_id):
    dog = read_dog_by_id(dog_id)
    if request.form['action'] == 'Edit':
        return render_template('edit.html', dog=dog)
    elif request.form['action'] == 'Delete':
        unenroll_dog(dog_id)
        return redirect(url_for('dogs'))


@app.route('/update/<int:dog_id>', methods=['post'])
def update(dog_id):
    # Get data from the form
    dog_name = request.form['dog_name']
    dog_age = request.form['dog_age']
    dog_owner = request.form['dog_owner']
    dog_breed = request.form['dog_breed']
    dog_treats = request.form['dog_treats']
    dog_pic = request.form['dog_pic']

    # Prepare data for DB Update
    dog_data = {
        'name': dog_name,
        'breed': dog_breed,
        'age': dog_age,
        'owner': dog_owner,
        'treats': dog_treats,
        'id': dog_id,
        'pic': dog_pic,
    }

    #Update DB
    update_dogs(dog_data)
    # Redirect User
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

@app.route('/modify_medical/<int:dog_id>', methods=['POST'])
def modify_medical(dog_id):
    dog = read_dog_by_id(dog_id)
    return render_template('edit_medical.html', dog=dog)

@app.route('/update_medical/<int:dog_id>', methods=['POST'])
def update_medical_record(dog_id):
    dog_medical = request.form['new_medical']
    dog_data = {
        'medical': dog_medical,
        'id': dog_id
    }
    update_medical(dog_data)
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

@app.route('/edit_medical/<int:dog_id>', methods=['post'])
def edit_medical_record(dog_id):
    dog_medical = request.form['edit_medical']
    dog_data = {
        'medical': dog_medical,
        'id': dog_id
    }
    edit_medical(dog_data)
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

@app.route('/trainers')
def trainers():
    dogs = order_by_trainer()
    trainers = show_trainers()
    return render_template('list_trainers.html', dogs=dogs, trainers=trainers)

@app.route('/trainer_profile/<string:trainer>')
def trainer_profile(trainer):
    dogs = show_trainers_dogs(trainer)
    return render_template('trainer_profile.html', dogs=dogs, trainer=trainer)

@app.route('/update_tricks/<int:dog_id>', methods=['post'])
def update_tricks(dog_id):
    tricks = request.form['dog_tricks']
    dog_data = {
        'tricks': tricks,
        'id': dog_id,
    }
    update_trick(dog_data)
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

if __name__ == '__main__':
    app.run(debug=True)