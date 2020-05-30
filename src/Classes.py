from machine import Pin

class Button:
    def __init__(self, pin):
        self.button = Pin(pin, Pin.IN, Pin.PULL_UP)

    def state(self):
        return not self.button.value()

class lights:

    def __init__(self, led_pins=(21, 22, 19)):
        a, b, c = led_pins

        self.state = "Not activated"
        self.red = LED(a)
        self.yellow = LED(b)
        self.green = LED(c)

    def red_state(self):
        self.red.on()
        self.yellow.off()
        self.green.off()
        self.state = "red"

    def yellow_state(self):
        self.red.off()
        self.yellow.on()
        self.green.off()
        self.state = "yellow"

    def green_state(self):
        self.red.off()
        self.yellow.off()
        self.green.on()
        self.state = "green"

    def off(self):
        self.state = "Not activated"
        self.red.off()
        self.yellow.off()
        self.green.off()

    def update_state(self, state):
        if state=="red":
            self.red_state()
        elif state == "yellow":
            self.yellow_state()
        elif state == "green":
            self.green_state()