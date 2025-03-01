import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    client.subscribe("measurement")


def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload) +"\n")
    # print(type(msg.payload))
    a=str(msg.payload).split(", ")
    a[0]=a[0][3:]
    a[-1]=a[-1][:-2]
    print(a)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)


try:    
    client.loop_forever()
    pass
except KeyboardInterrupt:
    print("Time to go now. Shutting down...")
