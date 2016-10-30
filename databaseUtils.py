#THIS FILE CONTAINS ALL FUNCTIONS THAT WILL BE USED FOR CREATING AND COMMUNICATING WITH DATABASE
import sqlite3

DATABASE = 'random.db'

#Create table for database
def setupDatabase():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Profiles (id integer,
                                name text,
                                level integer,
                                lives integer,
                                coins integer,
                                PRIMARY KEY(id))''')
    connection.commit()
    connection.close()
