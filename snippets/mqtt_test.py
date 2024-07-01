import paho.mqtt.client as mqtt

def on_message(client, userdata, message):
    print('received message')

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"connected with {reason_code}")
    client.subscribe("$SYS/#")

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_connect = on_connect
mqttc.on_message = on_message

mqttc.username_pw_set('mohr', '#dfggwergg')
mqttc.connect("cran-gw.e-technik.tu-ilmenau.de", 18330, 60)
mqttc.loop_forever()