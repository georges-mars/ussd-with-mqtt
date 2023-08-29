#my code
from flask import Flask, request

import paho.mqtt.client as mqtt
import requests
import json
app = Flask(__name__)

import os

response = ""
unique = ['1','mars', 'elvis', 'Kori', 'brian','205', 'keith']
    
 



def search_id(identity, unique):
    return identity in unique

        

    
#///creating the methods of communiction
@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)#/////getting the session id
    service_code = request.values.get("serviceCode", None)#//////////getting the service code
    #phone_number = request.values.get("phoneNumber", None)#getting the phone number that requested
    text =request.values.get("text", "default")#getting the request
    session_state = text.split('*')  
    
    current_level = len(session_state)
    
        # Create an MQTT client with id
    

    # Create an MQTT client with the specified client ID
    client = mqtt.Client()

    def make_request():
    # Get the JSON data from the request body
        data = request.get_json()

        # Perform an HTTP request
        url = data.get('url')
        response = requests.get(url)
        client.subscribe (f"{session_state[2]}/temp", 0)
        
        
    def make_request1():
    # Get the JSON data from the request body
        data = request.get_json()

        # Perform an HTTP request
        url = data.get('url')
        response = requests.get(url)
        client.subscribe (f"{session_state[2]}/humidity", 0)
        
    def make_request2():
        # Get the JSON data from the request body
        data = request.get_json()

        # Perform an HTTP request
        url = data.get('url')
        response = requests.get(url)
        client.subscribe (f"{session_state[2]}/light", 0)
        
        
    def make_request3():
    # Get the JSON data from the request body
        data = request.get_json()

        # Perform an HTTP request
        url = data.get('url')
        response = requests.get(url)
        client.subscribe (f"{session_state[2]}/pH", 0)
        
        
    def make_request4():
        # Get the JSON data from the request body
        data = request.get_json()

        # Perform an HTTP request
        url = data.get('url')
        response = requests.get(url)
        client.subscribe (f"{session_state[2]}/fertility", 0)
        
    def make_request5():
        # Get the JSON data from the request body
        data = request.get_json()

        # Perform an HTTP request
        url = data.get('url')
        response = requests.get(url)
        client.subscribe (f"{session_state[2]}/moisture", 0)
        
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            
        else :
            print(f"Connection failed with code {rc}")
            
    def temp_message(client, userdata, message):
        if message.topic == f"{session_state[2]}/temp":
            answer = json.loads(message.payload.decode())
            return (f"END Your temperature is {answer}")
        
    def humidity_message(client, userdata, message):
        if message.topic == f"{session_state[2]}/humidity":
            answer = json.loads(message.payload.decode())
            return(f"END Your humidity level is {answer}")
        
    def light_message(client, userdata, message):
        if message.topic == f"{session_state[2]}/light":
            answer = json.loads(message.payload.decode())
            return(f"END Your light level is {answer}")

    def pH_message(client, userdata, message):
        if message.topic == f"{session_state[2]}/pH":
            answer = json.loads(message.payload.decode())
            return(f"END Your pH level is {answer}")    
        
    def fertility_message(client, userdata, message):
        if message.topic == f"{session_state[2]}/fertility":
            answer = json.loads(message.payload.decode())
            return(f"END Your fertility level is {answer}")
 
    def moisture_message(client, userdata, message):
        if message.topic == f"{session_state[2]}/moisture":
            answer = json.loads(message.payload.decode())
            return(f"END Your moisture level is {answer}")
        
    def on_publish(client, userdata, mid):
        return("Message published")
    


    #connecting the client to the server....the last parameter is the keep alive parameter
    
    client.on_connect = on_connect
    client.on_message = [temp_message, humidity_message, light_message, pH_message, fertility_message, moisture_message]
    client.on_publish = on_publish
    
    
    if current_level == 1:
        response  = "CON Hello and welcome to E-shamba. Have you bought the device from our trusted dealerships shops\n"
        response += "1. Yes\n"
        response += "2. No"
        
    elif current_level == 2 and session_state[1] == '1':
        response = "CON Hello and thank you  for trusting e-shamba into you farm. Prepare to increase your yields by 90%\n"
        response += "Kindly input your unique ID. It is located on the LEFT HAND SIDE of your device"
        new_client_id= session_state[2]
        client.client_id = new_client_id
        client.connect("test.mosquitto.org", 1883, 30) 
        client.loop_start()
        
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
        make_request()
        
        #   temperature= '45.2'
        #response=f"Your temperature is {temperature}. This is suitable for crops such as grapes, sukumawiki, sweatpotatoes, peanut"
        
        
        
    elif current_level== 4 and session_state [3]== '2':
        make_request1()
        
        #humidity ='68.5'
        #response = "END Your Humidity is " + humidity + " This humidity is too low for your plants. E-Shamba suggest you set up a green house around the plant or switch to crops such as fruitnuts, watermellon which can thrive perfectly in our farm under this humidity."
        
    elif current_level== 4 and session_state[3] == '3':
        make_request2()
       #lght='20%'
       #response= "END Your light intensity is " +lght
        
    elif current_level== 4 and session_state[3] == '4':
        
        make_request3()
        
        #phval='7'
        #response ="END Your pH is " +phval +" .This means your soil is acidic and capable of growing crops such as tea, coffee, blueberries"
        
    elif current_level== 4 and session_state [3]== '5':
      
        make_request4()
        
        #fertlvl='50%'
        #response ="END your soil fertility level is " +fertlvl + " kindly add nitrogeneous fertilisers to make it better and also phospatic fertilisers."
        
    elif current_level== 4 and session_state[3] == '6':
        
        make_request5()
        
        #soilmoi='20%'
        #response ="END Your soil moisture content is "+soilmoi +" kindly add water"
    

    return response

    

#Receive response from africas talking
@app.route('/call', methods=['POST'])
def call_back_client():
    return '<Response> <Dial phoneNumbers="" maxDuration="5"/></Response>'


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))




