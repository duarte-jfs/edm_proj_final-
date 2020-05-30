#main
from umqttsimple import MQTTClient
import ubinascii
from machine import unique_id, Pin, reset, ADC
from time import sleep, time

mqtt_server = "192.168.1.68"
client_id = ubinascii.hexlify(unique_id())


topic_pub = b'measurement'


def sub_cb(topic, msg):
    print((topic, msg))


def connect_and_subscribe():
    global client_id, mqtt_server

    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    print('Connected to %s MQTT broker' %
          (mqtt_server))
    return client


def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()


try:
    client = connect_and_subscribe()
except OSError as e:
    restart_and_reconnect()

# Now that the client is connected lets get some info to send
adc = ADC(Pin(32))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)


def get_voltage():
    return adc.read()/4095*3.3


def loop(message_interval=0.5, precision=4, packet_size=20):
    global client

    last_message = 0
    counter = 0
    msg = b""
    while True:
        try:

            if len(msg) < packet_size*(precision+2):
                msg += str(get_voltage())[0:precision+2]+" "
            if (time() - last_message) > message_interval:
                client.publish(topic_pub, msg)
                last_message = time()
                counter += 1
                msg=b""
        except OSError as e:
            restart_and_reconnect()


try:
    loop(message_interval=0.5, precision=4, packet_size=100)
except KeyboardInterrupt:
    print("Time to go now. Shutting down...")
