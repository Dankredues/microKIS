import sys
sys.path.append("..")
import database
import sqlite3
import controller.patient_controller
import config

from models.bed_model import BedRecord
def insertBed(bed):
    connection =sqlite3.connect(config.DATABASE_PATH)
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


    
def getBeds():
    beds ={}
    connection = sqlite3.connect(config.DATABASE_PATH)
    cursor = connection.cursor()
    sql = "SELECT * FROM beds"
    cursor.execute(sql)

    # Ausgabe des Ergebnisses
    for dsatz in cursor:
        patient = controller.patient_controller.getPatientFromDBByID(dsatz[2])
        beds[dsatz[1]] = BedRecord(dsatz[0] , bedLabel=dsatz[1], patient=patient, station= dsatz[3] )

    # Verbindung beenden
    connection.close()
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
    
    return stations