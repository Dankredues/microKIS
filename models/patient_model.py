from collections import defaultdict

class PatientRecord:
    def __init__(self, givenName="",lastName="",patientID="",admissionDate="",station="",bed=""):
        self.givenName      =   givenName
        self.lastName       =   lastName
        self.patientID      =   patientID
        self.admissionDate  =   admissionDate
        self.station        =   station
        self.bed            =   bed
        self.trends         =   defaultdict(dict)
        
       
    def addTrend(self, name, date, value):        
        self.trends[date][name] = value



    def trendExists(self, name, date):
        if ( date in self.trends ) & ( name in self.trends[date] ):
            return True
        return False


    def __str__(self):
        return ("Patient :"+self.patientID+" \n \t"+self.givenName+" "+self.lastName+" \n \t"+str(self.trends))



