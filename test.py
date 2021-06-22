from flask import Flask, render_template, url_for, session, jsonify, request, redirect
from dog_data import *


app = Flask(__name__)
app.config['SECRETKEY'] = 'Hushitsasecret!'
conn = sqlite3.connect('test.db', check_same_thread=False)

conn.execute('DROP TABLE IF EXISTS DogList')
conn.execute('CREATE TABLE DogList (Dogname TEXT, Breed TEXT, Age TEXT, Owner TEXT, Treats TEXT)') #Trainer, maybe ID number and Vaccination, m
'''
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/animals/<pet_type>')
def animals(pet_type):
    return render_template('animals.html',pet_type=pet_type, pets=pets[pet_type])

@app.route('/animals/<pet_type>/<int:pet_id>')
def pet(pet_type, pet_id):
    pet = pets[pet_type][pet_id]
    return render_template('pet_profile.html',pet=pet)
'''
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/doglist')
def doglist():
    return render_template('test.html', doglist=dogs)

@app.route('/enrollment', methods = ['GET', 'POST'])
def enrollment():
    #if request.method == 'GET':
    return '''<form method="POST" action="/welcome">
                Your dog's name <br>
                <input type="text" name="name"><br>
                Your name <br> 
                <input type="text" name="owner"><br>
                Your dog's breed <br>
                <input type="text" name="breed"><br>
                Your dog's age <br>
                <input type="text" name="age"><br>
                Your dog's favorite treats <br>
                <input type="text" name="treats"><br>
                <input type="submit" value="Enroll your Dog!"><br>
            </form>'''

@app.route('/process', methods=['POST'])
def process():
    name = str(request.form['name'])
    breed = str(request.form['breed'])
    age = int(request.form['age'])
    owner = str(request.form['owner'])
    treats = str(request.form['treats'])
    jsonify({'name': name, 'breed': breed, 'age': age, 'owner': owner, 'treats': treats})



@app.route('/welcome', methods=['POST', 'GET'])
def welcome():
       name = str(request.form['name'])
       breed = str(request.form['breed'])
       age = int(request.form['age'])
       owner = str(request.form['owner'])
       treats = str(request.form['treats'])

       #with sqlite3.connect('test.db') as conn:
       cur = conn.cursor()
       cur.execute('INSERT INTO DogList (Dog name, Breed, Age, Owner, Treats) VALUES (?, ?, ?, ?, ?)', (name, breed, age, owner, treats))
       conn.commit()

       cur.close()
       return 'Welcome to Doggo Training school {} and {}!'.format(name, owner)
       #data = request.get_json()
       #name = data['name']
       #breed = data['breed']
       #age = data['age']
       #owner = data['owner']
       #treats = data['treats']
       #return render_template('test.html', name = name, breed = breed, age = age, owner = owner, treats = treats)

@app.route('/sqltest')
def sqltest():
    cur = conn.cursor()
    cur.execute('INSERT INTO DogList (Dogname, Breed, Age, Owner, Treats) VALUES (?, ?, ?, ?, ?)', ('Dog', 'Dog', 2, 'Himself', 'bananas'))
    conn.commit()
    cur.execute('SELECT Dogname, Breed, Age, Owner, Treats FROM DogList')
    for row in cur:
        print(row)
    conn.commit()
    cur.close()

if __name__ == '__main__':
    app.run(debug=True)