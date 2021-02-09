

from flask import Flask, render_template, session, redirect, url_for, escape, request
from draegertools.patientclass import PatientRecord,HL7Utils
import hl7
from hl7.mllp import open_hl7_connection
import asyncio
import config

app = Flask(__name__)


patientB = None #PatientRecord(givenName ="Thomas", lastName="Hasse", patientID= "1", bed="Bett1", station="ITS")
patientA = None #PatientRecord(givenName ="Patrick", lastName="Giannogonas", patientID= "2", bed="Bett42", station="ITS")



beds={ "bed1":patientA,"bed2":patientB,"bed3":None, "bed4":None}

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
        patient = beds[bed]
        if patient!=None:
            await sendHL7Patient(patient)

async def discharge(patientID):
    global beds
    discharge = HL7Utils.getDischargeMessage(str(patientID))
    for bed in beds:
        patient = beds[bed]
        
        
        if (beds[bed]!= None ):
            print("bedisNotNONE")
            if (patient.patientID==patientID):
                beds[bed] = None
    await sendMesasge(discharge)


app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    return render_template("/base.html", beds=beds)
    
    
@app.route("/sendToGW")
def sendToGW_view():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(updateBeds())
    return render_template("/base.html" , infoType=1, message="update Sent!", beds=beds)
    
    
@app.route("/showTrends")
def trends_view():

    return render_template("/trends.html" , message="No New Trends!!")
    
    
@app.route("/admit", methods=['GET', 'POST'])

def admit_view():
    
    if request.method == 'POST':
        data = request.form
        newPatient = PatientRecord(givenName =data["givenName"], lastName=data["lastName"], patientID=data["patientID"], bed=data["bed"], station=data["station"])
        beds[data["bed"]] = newPatient

        return redirect(url_for('sendToGW_view'))

    return render_template("/admit.html" , message="Bitte Alle Infos ausfüllen")


@app.route("/discharge/<patientID>")
def discharge_view(patientID):
    

    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(discharge(patientID))
    return render_template("/base.html" , infoType=1, message="Patient Discharged", beds=beds)