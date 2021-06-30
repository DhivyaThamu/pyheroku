import os
from typing import Text
from voiceREC import enrollment
from flask import Flask, render_template, request,flash, redirect, render_template, request, session, url_for
import sounddevice as sd
import simpleaudio as sa
from scipy.io.wavfile import write
from playsound import playsound
from pydub import AudioSegment
import requests
from flask import Flask,request,jsonify
import pymongo
from flask.templating import render_template
import requests
from flask import Flask,request,jsonify


from flask_cors import CORS
app = Flask(__name__)


@app.route('/')
def home():
    return render_template("indextest.html")

myclient = pymongo.MongoClient("mongodb+srv://ksvuser01:ksvatlas123@cluster0.pmda5.mongodb.net/")

db=myclient.ksvbanking

mycol = db.tbl_voicebiometricDetails


@app.route("/login", methods=["POST"])
def receive_data():
    


    

    uniqueID = request.form["username"]
    
    session['my_id']=uniqueID

    #query = { Unique ID: uniqueID , Enrollment_status  :  "YES"  }
    
    docs = mycol.find( { "UniqueID": uniqueID , "Enrollment_status"  :  "YES"   } ).count()

    
    
    #return f"{docs} "
    
    
    if docs == 1: 
                                        
        #verification()
        #return "Enrolled"
        return render_template("indextestverify.html", post="Veify")
    elif docs==0:
        
        
        
        #enrollment()
        return render_template("indextest1.html", post="Enroll_"+uniqueID)

    #return f"<h1>Name: {name}, Password: {password}</h1>"


@app.route("/enroll", methods=["POST"])
def enroll():
    

   
    uniqueID = session.get('my_id', None)

    fs = 44100  # Sample rate
    seconds = 20 # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    sd.wait()  # Wait until recording is finished

    write("output.wav", fs, myrecording)  # Save as WAV file 

    sound = AudioSegment.from_wav("output.wav")
    sound = sound.set_channels(1)
    sound.export("output.wav", format="wav")
    

    id ="file"
    
    msg ="D:\bot\3+Rasa+ChatBot+Files\3 Rasa ChatBot Files\output.wav"

    enroll_url = 'http://34.231.177.128:8080/ksvvoiceservice/rest/service/enrollment/output/AI_BOTNEW'


    test_data =  {
        "file": open(r'D:/bot/3+Rasa+ChatBot+Files/3 Rasa ChatBot Files/output.wav', "rb")}

    result = requests.post(url = enroll_url, files= test_data)

    
    

    #return f"{result.text}"
    res=result.text
    # db.mycol.update({ "UniqueID" : uniqueID },{ "$set": { "Enrollment_status" : "YES" } } )
    mycol.insert({"CustomerNumber":"-","CustomerName":"-", "UniqueID": uniqueID , "Enrollment_status"  :  "YES" ,"Enrollment_result" :res})
    #db.mycol.update_one( { "UniqueID": uniqueID }, { "$set": { "Enrollment_status": "YES" }} )
    return render_template("indextest1.html", post=res)


@app.route("/Verify", methods=["POST"])
def Verify():
    

    uniqueID = session.get('my_id', None)

    fs = 44100  # Sample rate
    seconds = 20 # Duration of recording

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)

    sd.wait()  # Wait until recording is finished

    write("output.wav", fs, myrecording)  # Save as WAV file 

    sound = AudioSegment.from_wav("output.wav")
    sound = sound.set_channels(1)
    sound.export("output.wav", format="wav")
    

    id ="file"
    
    msg ="D:\bot\3+Rasa+ChatBot+Files\3 Rasa ChatBot Files\output.wav"

    enroll_url = 'http://34.231.177.128:8080/ksvvoiceservice/rest/service/verification/output/AI_BOTNEW'


    test_data =  {
    "file": open(r'D:/bot/3+Rasa+ChatBot+Files/3 Rasa ChatBot Files/output.wav', "rb")}

    result = requests.post(url = enroll_url, files= test_data)

    
    

    #return f"{result.text}"
    res=result.text
    # db.mycol.update({ "UniqueID" : uniqueID },{ "$set": { "Enrollment_status" : "YES" } } )
    #mycol.insert({"CustomerNumber":"-","CustomerName":"-", "UniqueID": uniqueID , "Enrollment_status"  :  "YES" ,"Enrollment_result" :res})
    #db.mycol.update_one( { "UniqueID": uniqueID }, { "$set": { "Enrollment_status": "YES" }} )
    return render_template("indextestverify.html", post=res)





if __name__ == "__main__":
     app.secret_key = os.urandom(24)
     app.run(debug=True)