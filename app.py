

from flask import Flask, render_template, session, redirect, url_for, escape, request
from draegertools.patientclass import PatientRecord,HL7Utils
import hl7
from hl7.mllp import open_hl7_connection
import asyncio
app = Flask(__name__)


patientB = PatientRecord(givenName ="Thomas", lastName="Hasse", patientID= "1", bed="Bett1", station="ITS")
patientA = PatientRecord(givenName ="Patrick", lastName="Giannogonas", patientID= "2", bed="Bett42", station="ITS")



beds={ "bed1":patientA,"bed2":patientB,"bed3":None}

async def sendMesasge(message):
    hl7_reader, hl7_writer = await asyncio.wait_for(
        open_hl7_connection("192.168.1.121", 9100),
        timeout=10,
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


async def main():
    global patientA,patientB
    print(patientA.givenName)
    print(patientB.givenName)
    await sendHL7Patient(patientA)
    await sendHL7Patient(patientB)



app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    return render_template("/base.html", beds=beds)
    
    
@app.route("/sendToGW")
def sendToGW_view():
    asyncio.set_event_loop(asyncio.SelectorEventLoop())
    asyncio.get_event_loop().run_until_complete(main())
    return render_template("/base.html" , infoType=1, message="update Sent!")
    