from flask import Flask, render_template, session, redirect, url_for, escape, request
from utilities.hl7_tools import HL7Utils
from hl7_sender import updateBeds
from models.patient_model import PatientRecord
from models.bed_model import BedRecord

import hl7
from hl7.mllp import open_hl7_connection
import asyncio,aiorun
import config
import database
import shared_data
from hl7_receiver import *
from hl7_sender import *
from threading import Thread
from myutils import *
from main import app
import json

import strings_de as strings

# import module 
import traceback 

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    return render_template("/base.html",config=config, strings=strings, stations=shared_data.stations, beds=shared_data.beds)
    
    
@app.route("/sendToGW")
def sendToGW_view():
    if config.USE_HL7_OUTBOUND:
        try:
            asyncio.set_event_loop(asyncio.SelectorEventLoop())
            asyncio.get_event_loop().run_until_complete(updateBeds())
            return render_template("/base.html" ,config=config, strings=strings, infoType=1, message=strings.GW_UPDATE_SENT,stations=shared_data.stations, beds=shared_data.beds)
        except:
            traceback.print_exc() 
            return render_template("/base.html" ,config=config, strings=strings, infoType=2, message=strings.ERR_NO_CON_TO_GW,stations=shared_data.stations, beds=shared_data.beds)
    else:
        return render_template("/base.html" ,config=config, strings=strings, stations=shared_data.stations, beds=shared_data.beds)
    

    
    
@app.route("/admit", methods=['GET', 'POST'])
def admit_view():
    
    if request.method == 'POST':
        data = request.form
        newPatient = PatientRecord(givenName =data["givenName"], lastName=data["lastName"], patientID=data["patientID"], bed=data["bed"], station=data["station"])
        database.instertPatient(newPatient)
        
        for bedname in shared_data.beds:
            print(shared_data.beds[bedname].bedLabel+"=="+data["bed"])
            bed = shared_data.beds[bedname]
            if (bed.bedLabel == data["bed"]) and (bed.station == data["station"]):
                bed.patient = newPatient
                database.updateBed(bed)
                updateBedList()
                return redirect(url_for('sendToGW_view'))
            
        return render_template("/admit.html",config=config, strings=strings, infoType=2, message=strings.ERR_BED_DOES_NOT_EXIST )
        
#        beds[data["bed"]] = newPatient 

        return redirect(url_for('sendToGW_view'))

    return render_template("/admit.html" )

@app.route("/admit/<bed>", methods=['GET', 'POST'])
def admit_view_filled(bed):
    return render_template("/admit.html" ,config=config, strings=strings, bed=bed , beds=shared_data.beds)

  


@app.route("/discharge/<patientID>")
def discharge_view(patientID):
    print(patientID)
   
    try:
        
        for bed in shared_data.beds:
            if shared_data.beds[bed].patient != None:
                if shared_data.beds[bed].patient.patientID==str(patientID):
                    
                    database.deletePatient(patientID)
                    
                    updateBedList()
                    if(config.USE_HL7_OUTBOUND):
                        try:
                            asyncio.set_event_loop(asyncio.SelectorEventLoop())
                            asyncio.get_event_loop().run_until_complete(discharge(patientID))
                            
                            return render_template("/base.html" ,config=config, strings=strings, infoType=1, message=strings.BEDS_REFRESH_SUCCESS, stations=shared_data.stations,beds=shared_data.beds)
                        except:
                            return render_template("/base.html" ,config=config, strings=strings, infoType=2, message=strings.ERR_GW_ASYNC ,stations=shared_data.stations, beds=shared_data.beds)
                    else:
                        return render_template("/base.html" ,config=config, strings=strings,  stations=shared_data.stations,beds=shared_data.beds)
        return render_template("/base.html" ,config=config, strings=strings, infoType=2, message=strings.ERR_BED_DOES_NOT_EXIST, beds=shared_data.beds, stations=shared_data.stations)    
        
        
        
            
    except:
        traceback.print_exc() 
        return render_template("/base.html" ,config=config, strings=strings, infoType=2, message=strings.ERR_NO_CON_TO_GW , beds=shared_data.beds,stations=shared_data.stations)
        
        
@app.route("/force_discharge/<patientID>")
def forcedischarge(patientID):
    print(patientID)
    try:
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(discharge(patientID))
        
        return render_template("/base.html" , config=config, strings=strings, infoType=2, message=stirngs.BED_FORCE_DELETE ,stations=shared_data.stations, beds=shared_data.beds)

    except:
        traceback.print_exc() 
        return render_template("/base.html" ,config=config, strings=strings, infoType=2, message=strings.ERR_NO_CON_TO_GW  ,stations=shared_data.stations, beds=shared_data.beds)

@app.route("/station/<station>")
def staion_view(station):
    print(station)
    
    viewbeds = shared_data.stations[station]


    return render_template("/station_overview.html" ,config=config, strings=strings,  beds=viewbeds , stations=shared_data.stations,station=station)




@app.route("/viewPatient/<patientID>")
def patient_view(patientID):    
    patient = getPatientByID(str(patientID))

    


    d = patient.trends
    dateHeader = sorted(d.keys())
    paramLabels = sorted(list({k2 for v in d.values() for k2 in v}))
    #print(paramLabels)
    paramData = {}
    colors = ['red','blue','green','black','pink','grey','yellow']
    for parm in paramLabels:
        paramValue = []
        for date in dateHeader:
            if parm in d[date]:
                value = {'x':(d[date].get(parm, '-')), 'y':date}
                paramValue.append(value)
        
        paramData[parm] = paramValue
    #print(paramData)


    return render_template("/trends.html" ,config=config, strings=strings,  patient=patient, trendColor=colors, paramLabels= paramLabels,  trends=d, trendscale=dateHeader, paramData=paramData)
