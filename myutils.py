import shared_data
import database
from draegertools.patientclass import PatientRecord



def updateBedList():
    shared_data.beds = database.getBeds()
    shared_data.stations = database.getStationsFromBeds(shared_data.beds)


    print("breakpoint")





def getPatientByID(patientID):
    beds = shared_data.beds
    for bed in beds:
        if str(beds[bed].patient.patientID) == str(patientID):
            return beds[bed].patient
    return None          