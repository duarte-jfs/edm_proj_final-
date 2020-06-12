# main
from umqttsimple import MQTTClient
import ubinascii
from machine import unique_id, Pin, reset, ADC, Timer
from utime import ticks_ms, sleep, ticks_us, ticks_add,ticks_diff
import ujson

mqtt_server = "192.168.1.68"
client_id = ubinascii.hexlify(unique_id())

topic_pub = b'measurement'

def connect():
    global client_id, mqtt_server

    client = MQTTClient(client_id, mqtt_server)
    client.connect()    
    print('Connected to %s MQTT broker ' % (mqtt_server))

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

#---------------data part---------------#
message_interval = 50 #in miliseconds
sample_freq=8000 #Hz
ticks_max=ticks_add(0,-1)
print("Time intil clock resets: ", ticks_max/1e6/60, " minutes")
#---------------------------------------#

start_beggining=ticks_us() #saves the start of the measurement
data=[]

def publish(*args):
    global data
    global start_beggining

    data.append(ticks_diff(ticks_us(),start_beggining))
    client.publish(topic_pub,ujson.dumps(data))

    data=[ticks_us()] #initiates a new data packet
    start_beggining=ticks_us() #saves the new measurement beggining

    
tim = Timer(-1)
tim.init(period=message_interval, mode=Timer.PERIODIC, callback=publish)

def loop():
    global client
    global message_interval
    global data
    global sample_freq

    dt=int(1/sample_freq*1e6)
    deadline=ticks_add(ticks_us(),dt) #calculate the deadline

    while True:
        try:       
            if ticks_diff(deadline,ticks_us())<=0:
                data.append(adc.read())
                deadline=ticks_add(ticks_us(),dt)

        except OSError as e:
            restart_and_reconnect()
try:
    loop()
except KeyboardInterrupt:
    print("Time to go now. Shutting down...")
finally:
    tim.deinit()