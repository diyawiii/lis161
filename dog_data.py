import sqlite3, random
import random

db_path = 'test.db'

# list of employed trainers
employed_trainers = ['Youngster Joey', 'Sabrina', 'Red', 'Steven', 'Allister']

# Connect to a database
def connect_db(path):
    conn = sqlite3.connect(path)
    # Convert tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# returns all information about all dogs
def show_dogs():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs'
    results = cur.execute(query).fetchall()
    conn.close()
    return results

# Return information about a dog given their name and owner
def read_dog_by_name_owner(dog_name, dog_owner):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs WHERE name=? AND owner=?'
    results = cur.execute(query, (dog_name, dog_owner,)).fetchone()
    conn.close()
    return results

# Return information about a dog given their id
def read_dog_by_id(dog_id):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs WHERE id=?'
    result = cur.execute(query, (dog_id,)).fetchone()
    conn.close()
    return result

# selects 4 random dogs and returns their name and pic url
def random_dog():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs'
    result = cur.execute(query).fetchall()
    enroll_showcase = []
    while len(enroll_showcase) < 4:
        chosen_dog = random.choice(result)
        if random.randint(0, 1) == 1 and not (chosen_dog['name'], chosen_dog['pic'], chosen_dog['id']) in enroll_showcase:
            enroll_showcase.append((chosen_dog['name'], chosen_dog['pic'], chosen_dog['id']))
            continue
    conn.close()
    return enroll_showcase


# Insert dog data to DB
def enroll_dog(dog_data):
    conn, cur = connect_db(db_path)
    query = 'INSERT INTO dogs (name, breed, age, owner, treats, pic, trainer, medical) VALUES (?,?,?,?,?,?,?,?)'
    values = (dog_data['name'],
              dog_data['breed'],
              dog_data['age'],
              dog_data['owner'],
              dog_data['treats'],
              dog_data['pic'],
              dog_data['trainer'],
              dog_data['medical'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

# Delete a dog's data from the DB
def unenroll_dog(dog_id):
    conn, cur = connect_db(db_path)
    query = 'DELETE FROM dogs WHERE id=?'
    cur.execute(query, (dog_id,))
    conn.commit()
    conn.close()

# Update dog's profile data in DB
def update_dogs(dog_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE dogs SET name=?, breed=?, age=?, owner=?, treats=?, pic=? WHERE id=?'
    values = (dog_data['name'],
              dog_data['breed'],
              dog_data['age'],
              dog_data['owner'],
              dog_data['treats'],
              dog_data['pic'],
              dog_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

# Edit dog's existing medical data in DB given the dog's ID
def edit_medical(dog_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE dogs SET medical = ? WHERE id=?'
    values = (dog_data['medical'],
              dog_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

# randomly assigns a trainer to a dog from the list of employed trainers
def assign_trainer():
    return employed_trainers[random.randint(0, len(employed_trainers)-1)]

# orders DB by trainer
def order_by_trainer():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs ORDER BY trainer'
    result = cur.execute(query).fetchall()
    conn.close()
    return result

# shows all dogs trained by a specific trainer identified by the trainer's name
def show_trainers_dogs(trainer_name):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs WHERE trainer=?'
    result = cur.execute(query, (trainer_name,)).fetchall()
    conn.close()
    return result

# Add new trick data to dog's existing data in DB given the dog's ID
def update_trick(dog_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE dogs SET tricks=? WHERE id=?'
    values = (dog_data['tricks'], dog_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()
