from flask import Flask, request, jsonify
import threading
import paho.mqtt.client as mqtt


app = Flask(__name__)

mqtt_data = {}
unique = ['1', 'mars', 'elvis', 'Kori', 'brian', '205', 'keith']

# MQTT configuration
mqtt_broker_address = "test.mosquitto.org"
mqtt_broker_port = 1883
mqtt_client_id = "eshamba-client"


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe("temp")
        client.subscribe("humidity")
        client.subscribe("light")
        client.subscribe("pH")
        client.subscribe("fertility")
        client.subscribe("moisture")
    else:
        print(f"Connection failed with code {rc}")


def on_message(client, userdata, message):
    topic = message.topic
    payload = message.payload.decode()
    mqtt_data[topic] = payload
    print(f"Received message on topic: {topic}, payload: {payload}")


mqtt_client = mqtt.Client(client_id=mqtt_client_id)
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message

# Connect to MQTT broker
mqtt_client.connect(mqtt_broker_address, mqtt_broker_port, 30)




@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    text = request.values.get("text", "default")
    session_state = text.split('*')
    current_level = len(session_state)

    if current_level == 1:
        response = "CON Hello and welcome to E-shamba. Have you bought the device from our trusted dealerships shops?\n"
        response += "1. Yes\n"
        response += "2. No"

    elif current_level == 2 and session_state[1] == '1':
        response = "CON Hello and thank you for trusting E-shamba with your farm. Prepare to increase your yields by 90%\n"
        response += "Kindly input your unique ID. It is located on the LEFT HAND SIDE of your device."

    elif current_level == 2 and session_state[1] == '2':
        response = "END Kindly go to the nearest dealership and buy the device."

    elif current_level == 3:
        if search_id(session_state[2], unique):
            response = "CON Hello and Welcome " + session_state[2] + ", what do you want to access?\n"
            response += "1. Current temp\n"
            response += "2. Current humidity\n"
            response += "3. Current light intensity\n"
            response += "4. Current pH Level\n"
            response += "5. Current fertility level\n"
            response += "6. Current soil moisture content"
        else:
            response = "END Kindly stop lying and go buy the device."

    elif current_level == 4:
        parameter_choice = session_state[3]
        parameter_name = get_parameter_name(parameter_choice)

        if parameter_name:
            if parameter_name in mqtt_data:
                parameter_value = mqtt_data[parameter_name]
                response = f"END Your {parameter_name} is {parameter_value}"
            else:
                response = f"END {parameter_name} data not available"
        else:
            response = "END Invalid parameter choice."

    return response


def search_id(identity, unique_list):
    return identity in unique_list


def get_parameter_name(choice):
    parameter_names = {
        '1': 'temp',
        '2': 'humidity',
        '3': 'light',
        '4': 'pH',
        '5': 'fertility',
        '6': 'moisture'
    }
    return parameter_names.get(choice)


if __name__ == '__main__':
    # Start the MQTT subscriber loop in a separate thread
    mqtt_thread = threading.Thread(target=mqtt_client.loop_forever)
    mqtt_thread.daemon = True
    mqtt_thread.start()
    app.run(host="0.0.0.0", port=10000)
