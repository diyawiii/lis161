import sqlite3, random

db_path = 'test.db'

trainers = ['Youngster Joey', 'Sabrina', 'Red', 'Steven']

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
    query = 'SELECT id FROM dogs WHERE name=? AND owner=?'
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
    query = 'INSERT INTO dogs (name, breed, age, owner, treats) VALUES (?,?,?,?,?)'
    values = (dog_data['name'],
              dog_data['breed'],
              dog_data['age'],
              dog_data['owner'],
              dog_data['treats'])
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

def assign_trainer():
    return trainers[random.randint(0, len(trainers))]

def add_trainer(name):
    trainers.append(name)

def order_by_trainer():
    conn, cur = connect_db(db_path)
    query = 'SELECT * FROM dogs ORDER BY trainer'
    result = cur.execute(query).fetchall()
    conn.close()
    return result

#
