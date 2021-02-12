from datetime import datetime

class HL7Utils:
    def getHL7TimeStr(specifiedDateTime):
        return specifiedDateTime.strftime("%Y%m%d%H%M")

    def getDateTimeStr():
        t = datetime.now()
        return HL7Utils.getHL7TimeStr(t)

    def getHL7ADT(patient):
        #MSH|^~\&|HIS||Infinity||199903291650||ADT^A01|99022916500500050122|P|2.3
        #PID|||42||Krebs^Daniel||194204301420|M||W|13 Beer St.^#123^Beersteinville^VA^12345-6785^USA|978 907-7333|||spa|M|JEW|1001|012-34-5678|||||||||THA
        #PV1|||ITS^200^Bett1||||021-55-1366^Munster^Florence^S^II^Mr.^M.D.||||||||||0001^Carr^Mary^Jones^II^Mrs.^M.D.|||||||||||||||||||||||||||202102090909
        #OBX||NM|height||182.9|cm^^ISO+|||||R|||19990329165005
        #OBX||SN|weight||=^29.3|kg^^ISO+|||||R|||19990329165005

        resulting_message = "MSH|^~\&|HIS||Infinity||"+HL7Utils.getDateTimeStr()+"||ADT^A01|99022916500500050122|P|2.3\r"
        resulting_message += "PID|||"+patient.patientID+"||"+patient.lastName+"^"+patient.givenName+"||194204301420|M||W|13 Beer St.^#123^Beersteinville^VA^12345-6785^USA|978 907-7333|||spa|M|JEW|1001|012-34-5678|||||||||THA\r"
        resulting_message += "PV1|||"+patient.station+"^200^"+patient.bed+"||||021-55-1366^Munster^Florence^S^II^Mr.^M.D.||||||||||0001^Carr^Mary^Jones^II^Mrs.^M.D.|||||||||||||||||||||||||||202102090909\r"
        return resulting_message



    def getDischargeMessage(patientID):
        message = "MSH|^~\&|HIS||Infinity||199903291650||ADT^A03|99022916500500050122|P|2.3\r"
        message += "PID|||"+patientID+"||\r"
        return message


class PatientRecord:
    def __init__(self, givenName="",lastName="",patientID="",admissionDate="",station="",bed=""):
        self.givenName      =   givenName
        self.lastName       =   lastName
        self.patientID      =   patientID
        self.admissionDate  =   admissionDate
        self.station        =   station
        self.bed            =   bed
        self.trends         =   []

        #self.addTrend("spo2","11:00","99%")
        #self.addTrend("spo2","11:05","97%")
        #self.addTrend("spo2","11:10","95%")
        #self.addTrend("temp","11:00","35.5C")
        #self.addTrend("temp","11:10","34.5C")


    def addTrend(self, name, date, value):
        if not self.trendExists(name, date, value):
            trend_dict = {'name':name , 'date':date, 'val':value }
        
            self.trends.append (trend_dict)
        else:
            print("already in List")


    def trendExists(self, name, date, value):
        for trend in self.trends:
            if (trend['name']==name) and  (trend['date']==date) and  (trend['val']==value):
                return True
        return False


    def getTrendsBy(self, paramname):
        return sorted(self.trends, key=lambda k: k[paramname])

    def getTrendByName(self ):
        trends = self.getTrendsBy("name")
        resultingObj = {}
        trendList   = []
        for trendData in trends:
            paramName = trendData['name']
            if paramName in resultingObj:
                trendList=resultingObj[paramName]               
                
            else:
                trendList=[]
            trendList.append({"val":trendData['val']})
            resultingObj[paramName] = trendList
        return resultingObj

    def getTrendDateScale(self ):
        trends = self.getTrendsBy("date")
        resultingObj = {}
        trendList   = []
        for trendData in trends:
            paramName = trendData['date']
            if paramName in resultingObj:
                trendList=resultingObj[paramName]               
                
            else:
                trendList=[]
            trendList.append({"val":trendData['val']})
            resultingObj[paramName] = trendList
        return resultingObj

    def __str__(self):
        return ("Patient :"+self.patientID+" \n \t"+self.givenName+" "+self.lastName+" \n \t"+str(self.trends))


class BedRecord:
    def __init__(self, bedID, bedLabel="",patient=None,station=""):
        self.bedID = bedID
        self.bedLabel = bedLabel
        self.patient  = patient
        self.station  = station





    