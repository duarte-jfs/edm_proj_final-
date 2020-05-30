# from machine import Pin, ADC
# from utime import ticks_ms, sleep


# print("starting everything")

# adc = ADC(Pin(32))
# adc.width(ADC.WIDTH_12BIT)
# adc.atten(ADC.ATTN_11DB)

# print("About to start measurement...")
# sleep(1)

# red = Pin(21, Pin.OUT)
# yellow = Pin(22, Pin.OUT)
# green = Pin(19, Pin.OUT)


# def get_voltage():
#     return adc.read()/4095*3.3


# def loop():
#     print("starting")
#     start = ticks_ms()
#     counter = 0
#     while True:
#         if 0 < get_voltage() <= 1.1:
#             green.value(True)
#             yellow.value(False)
#             red.value(False)
#         if 1.1 < get_voltage() <= 2.2:
#             green.value(True)
#             yellow.value(True)
#             red.value(False)
#         if 2.2 < get_voltage() <= 3.3:
#             green.value(True)
#             yellow.value(True)
#             red.value(True)

#         if ticks_ms()-start >= 500:
#             print("Measurement ", counter, " = ", get_voltage(), " V")
#             counter += 1
#             start = ticks_ms()


# try:
#     loop()
# except KeyboardInterrupt:
#     print("Time to go. Shutting down...")
#     green.value(False)
#     yellow.value(False)
#     red.value(False)
from umqttsimple import MQTTClient
import ubinascii
from machine import unique_id, Pin, reset, ADC
from time import sleep, time

mqtt_server = "192.168.1.68"
client_id = ubinascii.hexlify(unique_id())

topic_sub = b'test'
topic_pub = b'measurement'

last_message = 0
message_interval = 0.5
counter = 0


def sub_cb(topic, msg):
    print((topic, msg))
#   if topic == b'notification' and msg == b'received':
#     print('ESP received hello message')


def connect_and_subscribe():
    global client_id, mqtt_server, topic_sub

    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    print('Connected to %s MQTT broker, subscribed to %s topic' %
          (mqtt_server, topic_sub))
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


def loop():
    global counter
    global last_message
    global client
    while True:
        try:
            client.check_msg()
            if (time() - last_message) > message_interval:
                msg = b"Measurement %4d = %5f V" % (counter, get_voltage())
                client.publish(topic_pub, msg)
                last_message = time()
                counter += 1
        except OSError as e:
            restart_and_reconnect()


try:
    loop()
except KeyboardInterrupt:
    print("Time to go now. Shutting down...")
