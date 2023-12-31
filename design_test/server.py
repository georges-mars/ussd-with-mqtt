#my code
from flask import Flask, request
import threading 
import paho.mqtt.client as mqtt
import requests
import json
from mqtt_client import start_mqtt_subscriber

app = Flask(__name__)

import os

response = ""
unique = ['1','mars', 'elvis', 'Kori', 'brian','205', 'keith']
    
mqtt_data = {}

def search_id(identity, unique):
    return identity in unique
         
#///creating the methods of communictionb
@app.route('/post_data', methods=['POST', 'GET'])
def post_data():
    data = request.get_json()
    mqtt_data["temperature"]=data.get("temperature")
    mqtt_data["humidity"]=data.get("humidity")
    mqtt_data["light"]=data.get("light")
    mqtt_data["pH"]=data.get("pH")
    mqtt_data["fertility"]=data.get("fertility")
    mqtt_data["moisture"]=data.get("moisture")
    print(mqtt_data)
    return "Data posted"
    
    
@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    print ("connected to mqtt server")
    global response
    global mqtt_data
    session_id = request.values.get("sessionId", None)#/////getting the session id
    service_code = request.values.get("serviceCode", None)#//////////getting the service code
    #phone_number = request.values.get("phoneNumber", None)#getting the phone number that requested
    text =request.values.get("text", "default")#getting the request
    session_state = text.split('*')  
    
    current_level = len(session_state)
    
    
    
    
    if current_level == 1:
        response  = "CON Hello and welcome to E-shamba. Have you bought the device from our trusted dealerships shops\n"
        response += "1. Yes\n"
        response += "2. No"
        
    elif current_level == 2 and session_state[1] == '1':
        response = "CON Hello and thank you  for trusting e-shamba into you farm. Prepare to increase your yields by 90%\n"
        response += "Kindly input your unique ID. It is located on the LEFT HAND SIDE of your device"
        
        
    elif current_level ==2 and session_state[1]== '2':
        response = "END Kindly go to the nearest dealershops and buy the device"
            
    elif current_level == 3:
        if search_id(session_state[2],unique):
            
            
            response = "CON Hello and Welcome " +session_state[2]+" what do you want to access?\n"
            response += "1.Current temp\n"
            response += "2.Current humidity\n"
            response += "3.Current light intensity\n"
            response += "4.Current pH Level\n"
            response += "5.Current fertility level\n"
            response += "6.Current soil moisture content"
            
        else:
            response = "END Kindly stop lying and go buy the device."
        
    elif current_level== 4 and session_state[3] == '1':
        if "temperature" in mqtt_data:
            temperature = mqtt_data["temperature"]
            response = f"END Your temperature is {temperature}"
        else:
            response = "END Temperature data not available"
        
        #   temperature= '45.2'
        #response=f"Your temperature is {temperature}. This is suitable for crops such as grapes, sukumawiki, sweatpotatoes, peanut"
        
        
        
    elif current_level== 4 and session_state [3]== '2':
        if "humidity" in mqtt_data:
            humidity = mqtt_data["humidity"]
            response = "END Your humidity is "+humidity
        else:
            response = "END humidity data not available"
        
        #humidity ='68.5'
        #response = "END Your Humidity is " + humidity + " This humidity is too low for your plants. E-Shamba suggest you set up a green house around the plant or switch to crops such as fruitnuts, watermellon which can thrive perfectly in our farm under this humidity."
        
    elif current_level== 4 and session_state[3] == '3':
        if "light" in mqtt_data:
            light = mqtt_data["light"]
            response = f"END Your light is {light}"
        else:
            response = "END light data not available"
       #lght='20%'
       #response= "END Your light intensity is " +lght
        
    elif current_level== 4 and session_state[3] == '4':
        
        if "pH" in mqtt_data:
            pH = mqtt_data["pH"]
            response = f"END Your pH is {pH}"
        else:
            response = "END pH data not available"
        
        #phval='7'
        #response ="END Your pH is " +phval +" .This means your soil is acidic and capable of growing crops such as tea, coffee, blueberries"
        
    elif current_level== 4 and session_state [3]== '5':
      
        if "fertility" in mqtt_data:
            fertility = mqtt_data["fertility"]
            response = f"END Your fertility is {fertility}"
        else:
            response = "END fertility data not available"
        
        #fertlvl='50%'
        #response ="END your soil fertility level is " +fertlvl + " kindly add nitrogeneous fertilisers to make it better and also phospatic fertilisers."
        
    elif current_level== 4 and session_state[3] == '6':
        
        if "moisture" in mqtt_data:
            moisture = mqtt_data["moisture"]
            response = f"END Your moisture is {moisture}"
        else:
            response = "END moisture data not available"
        
        #soilmoi='20%'
        #response ="END Your soil moisture content is "+soilmoi +" kindly add water"
    

    return response
   
#Receive response from africas talking
@app.route('/call', methods=['POST'])
def call_back_client():
    return '<Response> <Dial phoneNumbers="" maxDuration="5"/></Response>'


if __name__ == '__main__':
    mqtt_thread = threading.Thread(target=start_mqtt_subscriber)
    mqtt_thread.daemon = True  # Daemonize the thread so it exits when the main thread exits
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))
 




