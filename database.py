## #######################################################################
## ## DATABASE Functions and Initial Setup.  DEPRECATED AS OF 15 02 2021 #
## ## author : DK, V 1.2                                                 #
## #######################################################################
import sqlite3
import config
import os
from models.patient_model import PatientRecord
from models.bed_model import BedRecord

import shared_data
from controller.bed_controller import *
from controller.patient_controller import *
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


