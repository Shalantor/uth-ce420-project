#THIS FILE CONTAINS ALL FUNCTIONS THAT WILL BE USED FOR CREATING AND COMMUNICATING WITH DATABASE
import sqlite3

DATABASE = 'random.db'
START_LEVEL = 1
START_LIVES = 3
START_COINS = 0

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
    cursor.execute('SELECT * FROM Profiles')
    if cursor == None:
        #now fill with four profiles
        startProfiles = [ (0,'EMPTY',START_LEVEL,START_LIVES,START_COINS),
                          (1,'EMPTY',START_LEVEL,START_LIVES,START_COINS),
                          (2,'EMPTY',START_LEVEL,START_LIVES,START_COINS),
                          (3,'EMPTY',START_LEVEL,START_LIVES,START_COINS),]
        cursor.executemany('INSERT INTO Profiles VALUES (?,?,?,?,?)',startProfiles)

    connection.commit()
    connection.close()


#Enter new user (will be called for new game)
def enterProfile(userId,name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,name,START_LEVEL,START_LIVES,START_COINS,userId)
    cursor.execute('UPDATE Profiles SET id=?,name=?,level=?,lives=?,coins=? WHERE id=?',data)
    connection.commit()
    connection.close()
