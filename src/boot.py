# boot.py - runs on boot-up
import network

ssid = "internet meo"
password = "432AF34F47"

# Lets connect to the network

def do_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect(ssid, password)
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())


do_connect()


