import shared_data
from myutils import *
from utilities.hl7_tools import HL7Utils
import asyncio
from hl7.mllp import open_hl7_connection
import config
import hl7

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

async def discharge(patientID):
    discharge = HL7Utils.getDischargeMessage(str(patientID))
    database.clearPatient(patientID)
    
    await sendMesasge(discharge)
    updateBedList()




async def updateBeds():
    
    for bed in shared_data.beds:
        patient = shared_data.beds[bed].patient
        if patient!=None:
            await sendHL7Patient(patient)