import paho.mqtt.client as mqtt
MQTT_SERVER = "broker.hivemq.com"
MQTT_TOPIC = "IvanHu"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC)
    
def on_message(client, userdata, msg):
    # Create a copy of userdata for use within this callback
    global client_userdata
    print("Initial: " + str(client_userdata))

    # handle the header
    if client_userdata["isHeaderReceived"] == 0:
        print("Header received, ", end = '')
        client_userdata["headerString"] = str(msg.payload).strip("b'")
        client_userdata["isHeaderReceived"] = 1
        print("isHeaderReceived set to " + str(client_userdata["isHeaderReceived"]))
    # handle payloads    
    else:
        # if first segment
        if client_userdata["currentSegment"] == 1:            
            f = open('inputjpg_encrypted_encoded', "wb")
            f.write(msg.payload)
            f.close()
            client_userdata["currentSegment"] += 1
        # if last segment    
        elif client_userdata["currentSegment"] == int(client_userdata["headerString"].split(",")[0]):
            f = open('inputjpg_encrypted_encoded', "ab+")
            f.write(msg.payload)
            f.close()
            client_userdata["isHeaderReceived"] = 0
            client_userdata["currentSegment"] = 1
            client_userdata["headerString"] = ""
        else:
            f = open('inputjpg_encrypted_encoded', "ab+")
            f.write(msg.payload)
            f.close()
            client_userdata["currentSegment"] += 1
        print("Segment " + str(client_userdata["currentSegment"]) + " received.")
        
    print("Final: " + str(client_userdata))
    print("")
    
client_userdata = {
    "isHeaderReceived":     0,
    "currentSegment":       1,
    "headerString":      ""
}
            
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(MQTT_SERVER, 1883, 60)

client.loop_forever()
