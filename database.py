import sqlite3
import config
import os
from draegertools.patientclass import PatientRecord

database = None

def initDB():
    if os.path.exists(config.DATABASE_PATH):
        print("Found Existing DB. skipping")

    else:
        setupDB()

def setupDB():
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    sql = "CREATE TABLE patients(" \
      "givenName TEXT, " \
      "lastName name TEXT, " \
      "id INTEGER PRIMARY KEY, " \
      "patientID TEXT, " \
      "station TEXT, "\
      "bed TEXT)"
    cursor.execute(sql)

    sql = "INSERT INTO patients VALUES('Julia', " \
      "'Mertens', 0, '1337_42', 'ITS', 'bed2')"
    cursor.execute(sql)
    connection.commit()
    connection.close()

def instertPatient(patient):
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    sql = "select max(id) from patients"
    cursor.execute(sql)

    
         
    
    sql = "INSERT INTO patients VALUES('"+patient.givenName+"', " \
    "'"+patient.lastName+"', "+str(patient.patientID)+", '"+patient.patientID+"', '"+patient.station+"', '"+patient.bed+"')"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return True

def deletePatient(patientID):
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
       
    sql = "DELETE FROM patients WHERE patientID='"+patientID+"'"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return True

def getPatients():
    beds ={}
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()

    # SQL-Abfrage
    sql = "SELECT * FROM patients"

    # Kontrollausgabe der SQL-Abfrage
    # print(sql)

    # Absenden der SQL-Abfrage
    # Empfang des Ergebnisses
    cursor.execute(sql)

    # Ausgabe des Ergebnisses
    for dsatz in cursor:
        beds[dsatz[5]] = PatientRecord(givenName=dsatz[0],lastName=dsatz[1],patientID=dsatz[3],station=dsatz[4],bed=dsatz[5])

    # Verbindung beenden
    connection.close()
    return beds


