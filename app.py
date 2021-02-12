

from flask import Flask, render_template, session, redirect, url_for, escape, request
from draegertools.patientclass import PatientRecord,HL7Utils
import hl7
from hl7.mllp import open_hl7_connection
import asyncio
import config
import database
from shared_data import *



app = Flask(__name__)


patientB = PatientRecord(givenName ="Thomas", lastName="Hasse", patientID= "1", bed="Bett1", station="ITS")
patientA = None #PatientRecord(givenName ="Patrick", lastName="Giannogonas", patientID= "2", bed="Bett42", station="ITS")



database.initDB()


def updateBedList():
    
    global beds, stations

    beds = database.getBeds()
    stations = database.getStationsFromBeds(beds)

            


updateBedList()



async def sendMesasge(message):
    hl7_reader, hl7_writer = await asyncio.wait_for(
        open_hl7_connection(config.HL7_SERVER_IP, config.HL7_SERVER_PORT),
        timeout=config.HL7_TIMEOUT,
    )

    hl7_message = hl7.parse(message)

    # Write the HL7 message, and then wait for the writer
    # to drain to actually send the message
    hl7_writer.writemessage(hl7_message)
    await hl7_writer.drain()
    print(f'Sent message\n {hl7_message}'.replace('\r', '\n'))

    # Now wait for the ACK message from the receiever
    hl7_ack = await asyncio.wait_for(
      hl7_reader.readmessage(),
      timeout=10
    )
    print(f'Received ACK\n {hl7_ack}'.replace('\r', '\n'))

async def sendHL7Patient(patient):
    hl7msg = HL7Utils.getHL7ADT(patient)
    await sendMesasge(hl7msg)


async def updateBeds():
    global beds
    for bed in beds:
        patient = beds[bed].patient
        if patient!=None:
            await sendHL7Patient(patient)

async def discharge(patientID):
    global beds
    discharge = HL7Utils.getDischargeMessage(str(patientID))
    database.clearPatient(patientID)
    
    await sendMesasge(discharge)
    updateBedList()


app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    return render_template("/base.html", stations=stations, beds=beds)
    
    
@app.route("/sendToGW")
def sendToGW_view():
    try:
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(updateBeds())
        return render_template("/base.html" , infoType=1, message="Aktualisierung an Monitoring gesendet!",stations=stations, beds=beds)
    except:
        return render_template("/base.html" , infoType=2, message="Keine Verbindung zum Gateway! Es wurden keine Daten ans Monitoring gesendet!",stations=stations, beds=beds)
    
    
@app.route("/showTrends")
def trends_view():

    return render_template("/trends.html" , message="No New Trends!!")
    
    
@app.route("/admit", methods=['GET', 'POST'])
def admit_view():
    
    if request.method == 'POST':
        data = request.form
        newPatient = PatientRecord(givenName =data["givenName"], lastName=data["lastName"], patientID=data["patientID"], bed=data["bed"], station=data["station"])
        database.instertPatient(newPatient)
        
        for bedname in beds:
            print(beds[bedname].bedLabel+"=="+data["bed"])
            bed = beds[bedname]
            if (bed.bedLabel == data["bed"]) and (bed.station == data["station"]):
                bed.patient = newPatient
                database.updateBed(bed)
                updateBedList()
                return redirect(url_for('sendToGW_view'))
            
        return render_template("/admit.html", infoType=2, message="Bett existiert nicht!" )
        
#        beds[data["bed"]] = newPatient 

        return redirect(url_for('sendToGW_view'))

    return render_template("/admit.html" )

@app.route("/admit/<bed>", methods=['GET', 'POST'])
def admit_view_filled(bed):
    global beds
    print (beds)
    return render_template("/admit.html" , bed=bed , beds=beds)

  


@app.route("/discharge/<patientID>")
def discharge_view(patientID):
    print(patientID)
   
    try:
        
        for bed in beds:
            
            if beds[bed].patient.patientID==str(patientID):
                
                database.deletePatient(patientID)
                
                updateBedList()
                try:
                    asyncio.set_event_loop(asyncio.SelectorEventLoop())
                    asyncio.get_event_loop().run_until_complete(discharge(patientID))
                    
                    return render_template("/base.html" , infoType=1, message="Betten aktualisiert!", stations=stations,beds=beds)
                except:
                    return render_template("/base.html" , infoType=2, message="Gateway ASYNC Error",stations=stations, beds=beds)
        return render_template("/base.html" , infoType=2, message="Bett nicht Gefunden!", beds=beds, stations=stations)    
        
        
        
            
    except:
        return render_template("/base.html" , infoType=2, message="Keine Verbindung zum Gateway! Es wurden keine Daten ans Monitoring gesendet!", beds=beds,stations=stations)
        
        
@app.route("/force_discharge/<patientID>")
def forcedischarge(patientID):
    print(patientID)
    try:
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(discharge(patientID))
        
        return render_template("/base.html" , infoType=2, message="FORCED Remove Bed!",stations=stations, beds=beds)

    except:
        return render_template("/base.html" , infoType=2, message="Keine Verbindung zum Gateway! Es wurden keine Daten ans Monitoring gesendet!",stations=stations, beds=beds)

@app.route("/station/<station>")
def staion_view(station):
    print(station)
    global beds,stations
    viewbeds = stations[station]


    return render_template("/station_overview.html" , infoType=1, message="Achtung! IN ENTWICKLUNG!", beds=viewbeds , stations=stations,station=station)
