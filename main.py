from flask import Flask, render_template, session, redirect, url_for, escape, request
from utilities.hl7_tools import HL7Utils
from models.patient_model import PatientRecord
from models.bed_model import BedRecord
import hl7

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


if config.USE_HL7_INBOUND:
    print("Starting HL7 Listener Deamon ....")
    _thread = Thread(target=asyncio.run, args=(recieiver_loop(),))
    _thread.start()
    print("\t [OK]")
