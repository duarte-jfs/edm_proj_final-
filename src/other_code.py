# from machine import Pin

# print("starting")
# button_right = Pin(18, Pin.IN)
# current_value = button_right.value()
# watcher = 0


# def loop():

#     global current_value
#     global button_right
#     global watcher

#     while True:
#         if button_right.value() == 0 and watcher == 0:
#             print("button clicked ")
#             watcher = 1
#         if watcher == 1 and button_right.value() == 1:
#             watcher = 0


# try:
#     loop()
# except KeyboardInterrupt:
#     print('Got Ctrl-C')