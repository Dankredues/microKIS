import sqlite3
import config
import os
from draegertools.patientclass import PatientRecord, BedRecord
from shared_data import *

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

    sql = "CREATE TABLE beds(" \
      "bedID INTEGER PRIMARY KEY, " \
      "bedLabel TEXT, " \
      "patientID TEXT, " \
      "station TEXT)"
    cursor.execute(sql)


    sql = "CREATE TABLE trend_data(" \
      "trendID INTEGER PRIMARY KEY AUTOINCREMENT, " \
      "patientID TEXT, " \
      "timestring TEXT, " \
      "unit TEXT, " \
      "value TEXT)"
    cursor.execute(sql)

    sql = "INSERT INTO patients VALUES('Julia', " \
      "'Mertens', 0, '1337_42', 'ITS', 'bed2')"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    insertBed(BedRecord(101,bedLabel="Bett1",patient=None,station="ITS"))
    insertBed(BedRecord(102,bedLabel="Bett2",patient=None,station="ITS"))
    insertBed(BedRecord(103,bedLabel="Bett3",patient=None,station="ITS"))
    insertBed(BedRecord(104,bedLabel="Bett4",patient=None,station="ITS"))
    insertBed(BedRecord(201,bedLabel="ZNA1",patient=None,station="ZNA"))
    insertBed(BedRecord(202,bedLabel="ZNA2",patient=None,station="ZNA"))





def insertBed(bed):
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    if bed.patient ==None:
        patientID="-1"
    else:
        patientID = bed.patient.patientID
    sql = "INSERT INTO beds VALUES('"+str(bed.bedID)+"', '"+bed.bedLabel+"', '"+patientID+"', '"+bed.station+"')"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return True

def updateBed(bed):
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    if bed.patient ==None:
        patientID="-1"
    else:
        patientID = bed.patient.patientID
    sql = "UPDATE beds SET bedLabel='"+bed.bedLabel+"', patientID='"+patientID+"', station='"+bed.station+"' WHERE bedID='"+ str(bed.bedID) +"'"
    cursor.execute(sql)
    connection.commit()
    connection.close()
    return True



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
    global beds
    for bed in beds:
        if(id==beds[bed].patient.patientID):
            beds[bed].patient = None
            return True
    return False


def getBeds():
    beds ={}
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT * FROM beds"
    cursor.execute(sql)

    # Ausgabe des Ergebnisses
    for dsatz in cursor:
        patient = getPatientFromDBByID(dsatz[2])
        print(str(patient))
        beds[dsatz[1]] = BedRecord(dsatz[0] , bedLabel=dsatz[1], patient=patient, station= dsatz[3] )

    # Verbindung beenden
    connection.close()
    print(str(beds))
    return beds

def getStationsFromBeds(beds):
    stations = {}
    for bed in beds:
        bed = beds[bed]
        patient = bed.patient
        station = bed.station

        if not (station in stations.keys()):
            stations[station]={}
        stationbeds = stations[station]
        stationbeds[bed] = bed
    print (stations)
    return stations


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
        print("DBG:!  "+dsatz[5]+ dsatz[3])
        beds[dsatz[5]] = PatientRecord(givenName=dsatz[0],lastName=dsatz[1],patientID=dsatz[3],station=dsatz[4],bed=dsatz[5])

    # Verbindung beenden
    connection.close()
    print(str(beds))
    return beds


