from webapp.app import app
from webapp.draegerIACS import iacsConfig
import webapp.iacsProfile as iacsPE
from webapp.iacsProfile.propertyTools import pConfiguration, pLimit, pGeneralLimit,pECG,pSPO2,pPressure,pTemperature
import zipfile
import os
import subprocess
import sqlite3
from flask import Flask, render_template, session, redirect, url_for, escape, request









UPLOAD_FOLDER = 'D:/dev/dankredues.com/webapp/uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
PROFILE_FOLDER = 'D:/dev/dankredues.com/webapp/profiles/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROFILE_FOLDER'] = PROFILE_FOLDER
app.secret_key = 'any random string'
counter = 2




def setupdb():
    # Verbindung zur Datenbank erzeugen
    connection = sqlite3.connect("profiles.db")

    # Datensatz-Cursor erzeugen
    cursor = connection.cursor()

    # Datenbanktabelle erzeugen
    sql = "CREATE TABLE configs(" \
        "name TEXT, " \
        "path TEXT, " \
        "id INTEGER PRIMARY KEY, " \
        "city TEXT, " \
        "hospital TEXT, " \
        "station TEXT, " \
        "downloadUrl TEXT, " \
        "swVersion TEXT)"
    cursor.execute(sql)

    # Datensatz erzeugen
    sql = "INSERT INTO configs VALUES('OPZ AWR Bonn', " \
        "'D:/dev/dankredues.com/webapp/iacsProfile/OPZ_AWR', 0, 'Bonn', 'UKB', 'AWR', '', 'VG7.1')"
    cursor.execute(sql)
    connection.commit()

    # Verbindung beenden
    connection.close()


def updateProfileDB():
    # Verbindung, Cursor
    global myList,counter
    myList={}
    connection = sqlite3.connect("profiles.db")
    cursor = connection.cursor()

    # SQL-Abfrage
    sql = "SELECT * FROM configs"

    # Kontrollausgabe der SQL-Abfrage
    # print(sql)

    # Absenden der SQL-Abfrage
    # Empfang des Ergebnisses
    cursor.execute(sql)

    # Ausgabe des Ergebnisses
    counter = 0
    for dsatz in cursor:
        # "INSERT INTO configs VALUES('OPZ AWR Bonn', " \
        #"'\"D:/dev/dankredues.com/webapp/iacsProfile/OPZ_AWR\"', 0, 'Bonn', 'UKB', 'AWR', '', 'VG7.1')"
        counter = counter +1
        myList[str(dsatz[2])] =iacsConfig(dsatz[0],dsatz[1],dsatz[7],dsatz[3],dsatz[4],dsatz[5])
    # Verbindung beenden
    print(myList)
    connection.close()



def saveToDB( iacsProfile):
     # Datensatz erzeugen
    global counter
    connection = sqlite3.connect("profiles.db")
    cursor = connection.cursor()

    print("\n \n counter "+str(counter) )
    sql = "INSERT INTO configs VALUES('"+iacsProfile.name+"', " \
        "'"+iacsProfile.path+"', "+str(counter)+", '"+iacsProfile.city+"', '"+iacsProfile.hospital+"', '"+iacsProfile.station+"', '', 'VG7.1')"
    cursor.execute(sql)
    connection.commit()

    # Verbindung beenden
    connection.close()

updateProfileDB()
   

if not os.path.exists("profiles.db"):
        print("Erzeuge neue Datenbank")
        setupdb()







@app.route('/draeger/listConfigs')
def listConfigs():



   return render_template("/draeger/listprofile.html", availConfs = myList)


def execute(cmd):
            popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True)
            for stdout_line in iter(popen.stdout.readline, ""):
                yield stdout_line 
            popen.stdout.close()
            return_code = popen.wait()
            if return_code:
                raise subprocess.CalledProcessError(return_code, cmd)

@app.route('/draeger/uploadConfig', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        print('request.files', request.files)
        print('request.files', request.form)
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return redirect(request.url)
        if file:
            filename =file.filename
            file.save(app.config['UPLOAD_FOLDER']+filename)

            print (app.config['UPLOAD_FOLDER']+request.form['name'])
            os.mkdir(app.config['PROFILE_FOLDER']+request.form['name'])
            confname = request.form['name']

            # Entzippen

            with zipfile.ZipFile(app.config['UPLOAD_FOLDER']+filename, 'r') as zip_ref:                
                zip_ref.extractall(app.config['PROFILE_FOLDER']+request.form['name'])
            file.save(app.config['PROFILE_FOLDER']+request.form['name']+'/'+filename)
            filePath = app.config['PROFILE_FOLDER']+request.form['name']+'/draeger/'
            command =  "D:\dev\dankredues.com\webapp\iacsProfile\S14_UserProfileMigrator.exe -d -c \""+filePath+"\""

            
            saveToDB(iacsConfig(confname,filePath))
            updateProfileDB()

            for path in execute(command):
                print(path, end="")

            return redirect(url_for('listConfigs'))
    return 'nothing uploaded'

@app.route('/draeger/showConf/<confnum>', methods=['GET'])
def showConf(confnum):
   global myList
   path = myList[confnum].path
   name = myList[confnum].name
   profileConfs = iacsPE.profile_tools.getIncludedConfigs(path)
   
     
   return render_template("/draeger/viewprofile.html", configs=profileConfs, profileDetails = myList[confnum])

@app.route('/draeger/parseConfig')
def parseConfig():
    
   profileConfs = iacsPE.profile_tools.getIncludedConfigs("D:/dev/dankredues.com/webapp/iacsProfile/OPZ_AWR")
   returnText = ""

   for key in profileConfs:
     spo2 = profileConfs[key].spo2Limits
     for limit in spo2:
      print(str(limit))
     
   return render_template("/draeger/viewprofile.html", configs=profileConfs)