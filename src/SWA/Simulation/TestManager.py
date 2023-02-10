import ACS
import COMMS
import EPS
import Payload
import Subsystem
import TCS
import sqlite3
import 



def data_entry():
    print("data entry")
    number = 1234
    name = "Bitches"
    c.execute("INSERT INTO Questions (Number, Name) VALUES(?, ?)", (number, name))
    
    conn.commit()



def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS TestTable (Number REAL, Name TEXT)')

def openConnection():
    global conn
    conn = sqlite3.connect('..\db.sqlite3')
    global c
    c = conn.cursor()

def closeConnection():
    c.close()
    conn.close()

print('!!!!!!!  Creating table !!!!!!!!!!!!!!!!')
openConnection()
#create_table()
data_entry()
closeConnection()




