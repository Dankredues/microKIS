import sys
sys.path.append("..")

import database
from models.patient_model import PatientRecord
import sqlite3
import config
import shared_data

def getPatientFromDBByID(id):
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT * FROM patients WHERE patientID='"+str(id)+"'"
    cursor.execute(sql)
    patient = None
    for dsatz in cursor:
        patient = PatientRecord(givenName=dsatz[0],lastName=dsatz[1],patientID=dsatz[3],station=dsatz[4],bed=dsatz[5])
    connection.close()
    return patient

def clearPatient(id):
    
    for bed in shared_data.beds:
        if (shared_data.beds[bed].patient != None):
            if(id==shared_data.beds[bed].patient.patientID):
                beds[bed].patient = None
                return True
    return False



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


