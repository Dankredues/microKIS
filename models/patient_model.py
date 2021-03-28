from collections import defaultdict
import config
import random
class PatientRecord:
    def __init__(self, givenName="",lastName="",patientID="",admissionDate="",station="",bed=""):
        self.givenName      =   givenName
        self.lastName       =   lastName
        self.patientID      =   patientID
        self.admissionDate  =   admissionDate
        self.station        =   station
        self.bed            =   bed
        self.trends         =   defaultdict(dict)
        if config.USE_DEMO_DATA:
            for i in range(59):
                 sys = random.randrange(100,120,1)
                 dia = random.randrange(80,90,1)
                 mean = int((sys+dia)/2)
                 self.addTrend("393216^NIBP_SYS^EHC","11:"+f"{i:02d}",sys)
                 self.addTrend("393217^NIBP_DIA^EHC","11:"+f"{i:02d}",dia)
                 self.addTrend("393218^NIBP_MEAN^EHC","11:"+f"{i:02d}",mean)
                 self.addTrend("327681^SPO2_PR^EHC","11:"+f"{i:02d}",random.randrange(60,90,1))
    def addTrend(self, name, date, value):   
        self.trends[date][name] = value



    def trendExists(self, name, date):
        if ( date in self.trends ) & ( name in self.trends[date] ):
            return True
        return False


    def __str__(self):
        return ("Patient :"+self.patientID+" \n \t"+self.givenName+" "+self.lastName+" \n \t"+str(self.trends))



