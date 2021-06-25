from flask import Flask, render_template, request, redirect, url_for
from dog_data import *

app = Flask(__name__)

# shows index
@app.route('/')
def index():
    return render_template('index.html')

# shows list of dogs
@app.route('/dog_list')
def dog_list():
    # returns all data about all dogs
    dogs = show_dogs()
    return render_template('dogs.html', dogs=dogs)

# shows profile of specific dog identified by ID
@app.route('/dog_profile/<int:dog_id>')
def dog_profile(dog_id):
    # returns information about one dog. Dog ID number used to identify
    dog = read_dog_by_id(dog_id)
    return render_template('dog_profile.html', dog=dog)

# shows dog enrollment page
@app.route('/enroll')
def enroll():
    dog_4list = random_dog()
    return render_template('enroll.html', dog_4list=dog_4list)

# processes dog enrollment data
@app.route('/process', methods=['post'])
def process():
    # Prepares data by extracting it from the HTML form
    dog_data = {'name': request.form['dog_name'],
                'breed': request.form['dog_breed'],
                'age': request.form['dog_age'],
                'owner': request.form['dog_owner'],
                'treats': request.form['dog_treats'],
                'pic': request.form['dog_pic'],
                'medical': request.form['dog_medical'],
                'trainer': assign_trainer()} # randomly assigns a trainer to the dog
    # adds data to database
    enroll_dog(dog_data)
    return redirect(url_for('welcome', dog_name=request.form['dog_name'], dog_owner=request.form['dog_owner']))

# shows welcome page
@app.route('/welcome/<string:dog_name>/<string:dog_owner>')
def welcome(dog_name, dog_owner):
    # returns information about one dog. Dog name and owner used to identify
    dog = read_dog_by_name_owner(dog_name, dog_owner)
    return render_template('welcome.html', dog=dog)

# processes buttons on dog_profile page for editing dog profile data or deleting dog
@app.route('/modify/<int:dog_id>', methods=['POST'])
def modify(dog_id):
    # returns information about one dog. Dog ID number used to identify
    dog = read_dog_by_id(dog_id)

    # processes which action to take depending on which button is clicked. Redirects user to edit page or unenrolls dog
    if request.form['action'] == 'Edit':
        return render_template('edit.html', dog=dog)
    elif request.form['action'] == 'Unenroll':
        unenroll_dog(dog_id)
        return redirect(url_for('dog_list'))

# updates dog profile data
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

    # Update DB
    update_dogs(dog_data)
    # Redirect User
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

# renders the page for editing medical data
@app.route('/modify_medical/<int:dog_id>', methods=['POST'])
def modify_medical(dog_id):
    # returns information about one dog. Dog ID number used to identify
    dog = read_dog_by_id(dog_id)
    return render_template('edit_medical.html', dog=dog)

# processes edits to medical data
@app.route('/edit_medical/<int:dog_id>', methods=['post'])
def edit_medical_record(dog_id):
    # get medical data from the form
    dog_medical = request.form['edit_medical']

    # prepare medical data and dog ID data for DB update
    dog_data = {
        'medical': dog_medical,
        'id': dog_id
    }
    # updates DB
    edit_medical(dog_data)
    # redirects user to dog's profile
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

# renders the list of trainers
@app.route('/trainer_list')
def trainer_list():
    # returns all dogs ordered by trainer
    dogs = order_by_trainer()
    return render_template('list_trainers.html', dogs=dogs, trainers=employed_trainers)

# renders the trainer profiles
@app.route('/trainer_profile/<string:trainer>')
def trainer_profile(trainer):
    # returns all the dogs trained by the same trainer
    dogs = show_trainers_dogs(trainer)
    return render_template('trainer_profile.html', dogs=dogs, trainer=trainer)

# processes updates to tricks
@app.route('/update_tricks/<int:dog_id>', methods=['post'])
def update_tricks(dog_id):
    # gets trick data from the form
    tricks = request.form['dog_tricks']

    # packages trick data with dog ID data for DB update
    dog_data = {
        'tricks': tricks,
        'id': dog_id,
    }
    # updates DB
    update_trick(dog_data)
    return redirect(url_for('dog_profile', dog_id=dog_id))
    pass

if __name__ == '__main__':
    app.run(debug=False)