from datetime import datetime

from collections import defaultdict



class HL7Utils:
    def getHL7TimeStr(specifiedDateTime):
        return specifiedDateTime.strftime("%Y%m%d%H%M")

    def getDateTimeStr():
        t = datetime.now()
        return HL7Utils.getHL7TimeStr(t)

    def getHL7ADT(patient):
        #MSH|^~\&|HIS||Infinity||199903291650||ADT^A01|99022916500500050122|P|2.3
        #PID|||42||Krebs^Daniel||194204301420|M||W|13 Beer St.^#123^Beersteinville^VA^12345-6785^USA|978 907-7333|||spa|M|JEW|1001|012-34-5678|||||||||THA
        #PV1|||ITS^200^Bett1||||021-55-1366^Munster^Florence^S^II^Mr.^M.D.||||||||||0001^Carr^Mary^Jones^II^Mrs.^M.D.|||||||||||||||||||||||||||2021 02 09 09 09
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

