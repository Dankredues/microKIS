import shared_data
import database
from models.patient_model import PatientRecord
#from models.bed_model import BedRecord



def updateBedList():
    shared_data.beds = database.getBeds()
    shared_data.stations = database.getStationsFromBeds(shared_data.beds)


    print("breakpoint")





def getPatientByID(patientID):
    beds = shared_data.beds
    for bed in beds:
        if not beds[bed].patient==None:
            if str(beds[bed].patient.patientID) == str(patientID):
                return beds[bed].patient
    return None          