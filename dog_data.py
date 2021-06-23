import sqlite3, random

db_path = 'test.db'

trainers = ['Youngster Joey', 'Sabrina', 'Red', 'Steven', 'Allister']

# Connect to a database
def connect_db(path):
    conn = sqlite3.connect(path)
    # Convert tuples to dictionaries
    conn.row_factory = sqlite3.Row
    return (conn, conn.cursor())

# Show dog name and id
def show_dogs():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs'
    results = cur.execute(query).fetchall()
    conn.close()
    return results

def read_dog_by_name_owner(dog_name, dog_owner):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs WHERE name=? AND owner=?'
    results = cur.execute(query, (dog_name, dog_owner,)).fetchone()
    conn.close()
    print(results)
    return results

# Read a pet given a pet id
def read_dog_by_id(dog_id):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs WHERE id=?'
    result = cur.execute(query, (dog_id,)).fetchone()
    conn.close()
    return result

# Insert Pet Data to DB
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

# Delete a pet record
def unenroll_dog(dog_id):
    conn, cur = connect_db(db_path)
    query = 'DELETE FROM dogs WHERE id=?'
    cur.execute(query, (dog_id,))
    conn.commit()
    conn.close()

# Update Pet Data from DB
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

def update_medical(dog_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE dogs SET medical = (SELECT medical FROM dogs WHERE id=?) ||","|| char(10) || ? WHERE id=?'
    values = (dog_data['id'],
              dog_data['medical'],
              dog_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

def edit_medical(dog_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE dogs SET medical = ? WHERE id=?'
    values = (dog_data['medical'],
              dog_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()

def assign_trainer():
    return trainers[random.randint(0, len(trainers)-1)]

def order_by_trainer():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs ORDER BY trainer'
    result = cur.execute(query).fetchall()
    conn.close()
    return result

def show_trainers():
    conn, cur = connect_db(db_path)
    query = 'SELECT DISTINCT trainer FROM dogs'
    result = cur.execute(query).fetchall()
    conn.close()
    return result

def show_trainers_dogs(name):
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs WHERE trainer=?'
    result = cur.execute(query, (name,)).fetchall()
    conn.close()
    return result

def update_trick(dog_data):
    conn, cur = connect_db(db_path)
    query = 'UPDATE dogs SET tricks= (SELECT tricks FROM dogs WHERE id=?) ||", " || ? WHERE id=?'
    values = (dog_data['id'], dog_data['tricks'], dog_data['id'])
    cur.execute(query, values)
    conn.commit()
    conn.close()
