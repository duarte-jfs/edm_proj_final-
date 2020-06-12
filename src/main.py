# main
from umqttsimple import MQTTClient
import ubinascii
from machine import unique_id, Pin, reset, ADC, Timer
from utime import ticks_ms, sleep, ticks_us

mqtt_server = "192.168.1.68"
client_id = ubinascii.hexlify(unique_id())

topic_pub = b'measurement'

def connect():
    global client_id, mqtt_server

    client = MQTTClient(client_id, mqtt_server)
    client.connect()
    print('Connected to %s MQTT broker' % (mqtt_server))
    return client

def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    sleep(10)
    reset()


try:
    client = connect()
except OSError as e:
    restart_and_reconnect()

# Now that the client is connected lets get some info to send
adc = ADC(Pin(32))
adc.width(ADC.WIDTH_12BIT)
adc.atten(ADC.ATTN_11DB)

# I'll just make some use of the lights
green = Pin(19, Pin.OUT)
yellow = Pin(22, Pin.OUT)
red = Pin(21, Pin.OUT)

#---------------data part---------------#
precision = 4
message_interval = 20
packet_size = 100
long_message_interval=5000
#---------------------------------------#

def get_voltage():
    return adc.read()

def loop():
    global client
    global message_interval
    global precision
    global packet_size
    global long_message_interval

    last_message = 0
    counter = 0

    data = b""
    times=b""
    
    while True:
        try:

            value = get_voltage()
            if 620 < value <= 1985:
                green.value(True)
                yellow.value(False)
                red.value(False)
            elif 1985 < value <= 3350:
                green.value(True)
                yellow.value(True)
                red.value(False)
            elif 3350 < value:
                green.value(True)
                yellow.value(True)
                red.value(True)
            else:
                green.value(False)
                yellow.value(False)
                red.value(False)

            if len(data) < packet_size*4:
                data += str(value)+" "    
                times+= str(ticks_ms())+" "

            if (ticks_ms() - last_message) > message_interval:
                msg=data+"|"+times
                client.publish(topic_pub, msg)
                last_message = ticks_ms()
                data = b""
                times = b""

            

        except OSError as e:
            restart_and_reconnect()


try:
    loop()
except KeyboardInterrupt:
    print("Time to go now. Shutting down...")
finally:
    green.value(False)
    yellow.value(False)
    red.value(False)