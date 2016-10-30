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
                                difficulty integer,
                                PRIMARY KEY(id))''')
    cursor.execute('SELECT * FROM Profiles')
    if cursor.fetchone() == None:
        #now fill with four profiles
        startProfiles = [ (0,'EMPTY',START_LEVEL,START_LIVES,START_COINS,0),
                          (1,'EMPTY',START_LEVEL,START_LIVES,START_COINS,0),
                          (2,'EMPTY',START_LEVEL,START_LIVES,START_COINS,0),
                          (3,'EMPTY',START_LEVEL,START_LIVES,START_COINS,0),]
        cursor.executemany('INSERT INTO Profiles VALUES (?,?,?,?,?,?)',startProfiles)

    connection.commit()
    connection.close()


#Enter new user (will be called for new game)
def enterProfile(userId,name):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,name,START_LEVEL,START_LIVES,START_COINS,0,userId)
    cursor.execute('UPDATE Profiles SET id=?,name=?,level=?,lives=?,coins=?,difficulty=? WHERE id=?',data)
    connection.commit()
    connection.close()

#Function to get all names from database
def getProfiles():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute('SELECT name from Profiles')
    names = []
    for n in cursor:
        names.append(n[0])
    connection.close()
    return names

#Function to get profile data
def getData(userId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,)
    cursor.execute('SELECT * FROM Profiles WHERE id=?',data)
    cursorResult = cursor.fetchone()
    statistics = {"name":cursorResult[1],"level":cursorResult[2],"lives":cursorResult[3],"coins":cursorResult[4],"difficulty":cursorResult[5]}
    connection.close()
    return statistics
