# boilerplate.
import asyncio
import aiorun
import shared_data

from models.patient_model import PatientRecord
#from models.bed_model import BedRecord

from myutils import *

from datetime import datetime
import hl7
from hl7.mllp import start_hl7_server




def parseHL7Message(message):
    
    patientID  = -1
    patient = None
    for segment in message:
        if str(segment[0])=="PID":   
            #print ("foundPatientRecord")
            patientID  =  segment[3]
            patient = getPatientByID(str(patientID))
        if str(segment[0])=="OBX":   
            #print ("foundOBX ")
            if str(segment[2])=="NM":          
                datestr = str(segment[-1])

                print(datestr)
                date_time_obj = datetime.strptime(datestr, '%Y%m%d%H%M%S')
                formattedDate = date_time_obj.strftime("%d.%m.%Y %H:%M")
                if(patient!=None):
                    patient.addTrend(str(segment[3]),  formattedDate ,str(segment[5]))


    #print("Updating Patient "+ str(patientID) +"\n \t "+nibp_sys +"\n \t "+nibp_dia +"\n \t "+nibp_mean+"\n \t "+temp)




async def process_hl7_messages(hl7_reader, hl7_writer):
    """This will be called every time a socket connects
    with us.
    """
    peername = hl7_writer.get_extra_info("peername")
    print(f"Connection established {peername}")
    try:
        # We're going to keep listening until the writer
        # is closed. Only writers have closed status.
        while not hl7_writer.is_closing():
            hl7_message = await hl7_reader.readmessage()
            #print(f'Received message\n {hl7_message}'.replace('\r', '\n'))
            # Now let's send the ACK and wait for the
            # writer to drain

            hl7_writer.writemessage(hl7_message.create_ack())

            await hl7_writer.drain()

            parseHL7Message(hl7_message)
    except asyncio.IncompleteReadError:
        # Oops, something went wrong, if the writer is not
        # closed or closing, close it.
        if not hl7_writer.is_closing():
            hl7_writer.close()
            await hl7_writer.wait_closed()
    print(f"Connection closed {peername}")


async def recieiver_loop():
    print("Looping")
    try:
        # Start the server in a with clause to make sure we
        # close it
        async with await start_hl7_server(
            process_hl7_messages, port=2575
        ) as hl7_server:
            # And now we server forever. Or until we are
            # cancelled...
            await hl7_server.serve_forever()
    except asyncio.CancelledError:
        # Cancelled errors are expected
        pass
    except Exception:
        raise
        #pass #print("Error occurred in main")


def start_hl7_receiver():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(recieiver_loop())
    loop.close()
    #aiorun.run(recieiver_loop(), stop_on_unhandled_errors=True)