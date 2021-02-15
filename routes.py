from flask import Flask, render_template, session, redirect, url_for, escape, request
from draegertools.patientclass import PatientRecord,HL7Utils
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

@app.route('/static/<path:path>')
def send_js(path):
    return send_from_directory('static', path)


@app.route("/")
def index():
    return render_template("/base.html", stations=shared_data.stations, beds=shared_data.beds)
    
    
@app.route("/sendToGW")
def sendToGW_view():
    try:
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(updateBeds())
        return render_template("/base.html" , infoType=1, message="Aktualisierung an Monitoring gesendet!",stations=shared_data.stations, beds=shared_data.beds)
    except:
        return render_template("/base.html" , infoType=2, message="Keine Verbindung zum Gateway! Es wurden keine Daten ans Monitoring gesendet!",stations=shared_data.stations, beds=shared_data.beds)
    
    
@app.route("/showTrends")
def trends_view():

    return render_template("/trends.html" , message="No New Trends!!")
    
    
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
            
        return render_template("/admit.html", infoType=2, message="Bett existiert nicht!" )
        
#        beds[data["bed"]] = newPatient 

        return redirect(url_for('sendToGW_view'))

    return render_template("/admit.html" )

@app.route("/admit/<bed>", methods=['GET', 'POST'])
def admit_view_filled(bed):
    global beds
    print (beds)
    return render_template("/admit.html" , bed=shared_data.bed , beds=shared_data.beds)

  


@app.route("/discharge/<patientID>")
def discharge_view(patientID):
    print(patientID)
   
    try:
        
        for bed in shared_data.beds:
            
            if beds[bed].patient.patientID==str(patientID):
                
                database.deletePatient(patientID)
                
                updateBedList()
                try:
                    asyncio.set_event_loop(asyncio.SelectorEventLoop())
                    asyncio.get_event_loop().run_until_complete(discharge(patientID))
                    
                    return render_template("/base.html" , infoType=1, message="Betten aktualisiert!", stations=shared_data.stations,beds=shared_data.beds)
                except:
                    return render_template("/base.html" , infoType=2, message="Gateway ASYNC Error",stations=shared_data.stations, beds=shared_data.beds)
        return render_template("/base.html" , infoType=2, message="Bett nicht Gefunden!", beds=shared_data.beds, stations=shared_data.stations)    
        
        
        
            
    except:
        return render_template("/base.html" , infoType=2, message="Keine Verbindung zum Gateway! Es wurden keine Daten ans Monitoring gesendet!", beds=shared_data.beds,stations=shared_data.stations)
        
        
@app.route("/force_discharge/<patientID>")
def forcedischarge(patientID):
    print(patientID)
    try:
        asyncio.set_event_loop(asyncio.SelectorEventLoop())
        asyncio.get_event_loop().run_until_complete(discharge(patientID))
        
        return render_template("/base.html" , infoType=2, message="FORCED Remove Bed!",stations=shared_data.stations, beds=shared_data.beds)

    except:
        return render_template("/base.html" , infoType=2, message="Keine Verbindung zum Gateway! Es wurden keine Daten ans Monitoring gesendet!",stations=shared_data.stations, beds=shared_data.beds)

@app.route("/station/<station>")
def staion_view(station):
    print(station)
    
    viewbeds = shared_data.stations[station]


    return render_template("/station_overview.html" , infoType=1, message="Achtung! IN ENTWICKLUNG!", beds=viewbeds , stations=shared_data.stations,station=station)




@app.route("/viewPatient/<patientID>")
def patient_view(patientID):    
    patient = getPatientByID(str(patientID))

    


    d = patient.trends
    dateHeader = sorted(d.keys())
    paramLabels = sorted(list({k2 for v in d.values() for k2 in v}))
    'print(paramLabels)
    paramData = {}
    colors = ['red','blue','green','black','pink','grey','yellow']
    for parm in paramLabels:
        paramValue = []
        for date in dateHeader:
            if parm in d[date]:
                value = {'x':(d[date].get(parm, '-')), 'y':date}
                paramValue.append(value)
        
        paramData[parm] = paramValue
    'print(paramData)


    return render_template("/trends.html" , infoType=1, message="Achtung! IN ENTWICKLUNG!", patient=patient, trendColor=colors, paramLabels= paramLabels,  trends=d, trendscale=dateHeader, paramData=paramData)
