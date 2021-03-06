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

    #Controls table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Controls(id integer,
                                moveLeft text,
                                moveRight text,
                                moveUp text,
                                moveDown text,
                                jump text,
                                shoot text,
                                combo text,
                                PRIMARY KEY(id))''')
    cursor.execute('SELECT * FROM Controls')
    if cursor.fetchone() == None:
        #Fill with default controls
        data = (0,'left','right','up','down','v','space','c')
        cursor.execute('INSERT INTO Controls VALUES (?,?,?,?,?,?,?,?)',data)

    connection.commit()
    connection.close()


#Enter new user (will be called for new game)
def enterProfile(userId,name,difficulty):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,name,START_LEVEL,START_LIVES,START_COINS,difficulty,userId)
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
    statistics = {"id":cursorResult[0],"name":cursorResult[1],"level":cursorResult[2],"lives":cursorResult[3],"coins":cursorResult[4],"difficulty":cursorResult[5]}
    connection.close()
    return statistics

#Function to change difficulty
def changeDifficulty(userId,difficulty):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (difficulty,userId)
    cursor.execute('UPDATE Profiles SET difficulty=? WHERE id=?',data)
    connection.commit()
    connection.close()

#Function to get current difficulty for a profile
def getDifficulty(userId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,)
    cursor.execute('SELECT difficulty FROM Profiles WHERE id=?',data)
    cursorResult = cursor.fetchone()
    connection.close()
    return cursorResult[0]

#Function to get players current level
def getLevel(userId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,)
    cursor.execute('SELECT level FROM Profiles WHERE id=?',data)
    cursorResult = cursor.fetchone()
    connection.close()
    return cursorResult[0]

#Function to set levels and coins
def setStats(userId,level,coins):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (level,coins,userId)
    cursor.execute('UPDATE Profiles SET level=?,coins=? WHERE id=?',data)
    connection.commit()
    connection.close()

#Function to get players current coins
def getCoins(userId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,)
    cursor.execute('SELECT coins FROM Profiles WHERE id=?',data)
    cursorResult = cursor.fetchone()
    connection.close()
    return cursorResult[0]

#Get controls
def getControls(userId):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    data = (userId,)
    cursor.execute('SELECT * FROM Controls WHERE id=?',data)
    cursorResult = cursor.fetchone()
    connection.close()
    returnData = [cursorResult[1],cursorResult[2],cursorResult[3],cursorResult[4],cursorResult[5],cursorResult[6],cursorResult[7]]
    return returnData

#Change controls
def changeControls(userId,controlsList):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    newControls = controlsList[:]

    newControls.append(userId)
    data = tuple(newControls)
    cursor.execute('UPDATE Controls SET moveLeft=?,moveRight=?,moveUp=?,moveDown=?,jump=?,shoot=?,combo=? WHERE id=?',data)
    connection.commit()
    connection.close()
