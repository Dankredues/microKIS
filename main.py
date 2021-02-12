from flask import Flask, render_template, session, redirect, url_for, escape, request
from draegertools.patientclass import PatientRecord,HL7Utils
import hl7
from hl7.mllp import open_hl7_connection
import asyncio,aiorun
import config
import database
from shared_data import *
from hl7_receiver import *
from hl7_sender import *
from threading import Thread
from myutils import *



app = Flask(__name__)

import routes

database.initDB()


updateBedList()


print("Starting HL7 Listener Deamon ....")
_thread = Thread(target=asyncio.run, args=(recieiver_loop(),))
_thread.start()
print("\t [OK]")



#testPat =   getPatientByID("421337")

#print(str(testPat))









async def updateBeds():
    global beds
    for bed in beds:
        patient = beds[bed].patient
        if patient!=None:
            await sendHL7Patient(patient)





