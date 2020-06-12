from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import paho.mqtt.client as mqtt
import sys
import numpy as np


class MQTT_Client(QtCore.QObject):
    # Define the signals. Qt terminology.

    messageSignal = QtCore.pyqtSignal(str)

    connected = QtCore.pyqtSignal()
    disconnected = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QObject.__init__(self)

        # define your default client settings
        self.host = "localhost"
        self.port = 1883
        self.keepAlive = 60
        self.cleanSession = True
        self.subscribe_topic = "measurement"

        self.state = "disconnected"  # created to keep track of the state of the client

        # Create the paho client and set your callbacks
        self.client = mqtt.Client(clean_session=self.cleanSession)
        self.client.on_connect = self.on_connect1
        self.client.on_message = self.on_message1
        self.client.on_disconnect = self.on_disconnect1

    def on_message1(self, mqttc, obj, msg):
        mstr = msg.payload.decode("ascii")
        self.messageSignal.emit(mstr)  # Emit the signal.Qt terminology

    def on_connect1(self, *args):
        self.connected.emit() # Emit the signal.Qt terminology

    def on_disconnect1(self, *args):
        self.disconnected.emit() # Emit the signal.Qt terminology

    @QtCore.pyqtSlot()
    def connectToHost(self):
        #The function to connect the client to the broker.

        self.client.connect(self.host,
                            port=self.port,
                            keepalive=self.keepAlive)
        self.state = "connected"
        self.client.subscribe(self.subscribe_topic)
        self.client.loop_start()

    @QtCore.pyqtSlot()
    def disconnectFromHost(self):
        #Call this function if you want to disconnect the broker
        self.state = "disconnected"
        self.client.disconnect()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        #Here starts the main constructor. It mainly constitutes all the 
        #"architecture" of the app: Instances the objects, places them in the respective layouts and other things.
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.mqtt_label = QtWidgets.QLabel(self.centralwidget)
        self.mqtt_label.setObjectName("mqtt_label")
        self.verticalLayout_2.addWidget(
            self.mqtt_label, 0, QtCore.Qt.AlignHCenter)

        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.host_label = QtWidgets.QLabel(self.centralwidget)
        self.host_label.setObjectName("host_label")
        self.horizontalLayout_3.addWidget(self.host_label)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.line_host = QtWidgets.QLineEdit(self.centralwidget)
        self.line_host.setObjectName("line_host")
        self.horizontalLayout_3.addWidget(self.line_host)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.port_label = QtWidgets.QLabel(self.centralwidget)
        self.port_label.setObjectName("port_label")
        self.horizontalLayout_4.addWidget(self.port_label)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.line_port = QtWidgets.QLineEdit(self.centralwidget)
        self.line_port.setObjectName("line_port")
        self.horizontalLayout_4.addWidget(self.line_port)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.topic_label = QtWidgets.QLabel(self.centralwidget)
        self.topic_label.setObjectName("topic_label")
        self.horizontalLayout_5.addWidget(self.topic_label)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.line_topic = QtWidgets.QLineEdit(self.centralwidget)
        self.line_topic.setObjectName("line_topic")
        self.horizontalLayout_5.addWidget(self.line_topic)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.button_conn = QtWidgets.QPushButton(self.centralwidget)
        self.button_conn.setObjectName("button_conn")
        self.verticalLayout_2.addWidget(self.button_conn)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.n_points = QtWidgets.QLabel(self.centralwidget)
        self.n_points.setObjectName("n_points")
        self.verticalLayout_3.addWidget(self.n_points)
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider.setTickInterval(4)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.verticalLayout_3.addWidget(self.horizontalSlider)
        self.verticalLayout_2.addLayout(self.verticalLayout_3)

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot_long = pg.PlotWidget(self.centralwidget)
        self.plot_long.setObjectName("plot_long")
        self.verticalLayout.addWidget(self.plot_long)

        self.plot = pg.PlotWidget(self.centralwidget)
        self.plot.setObjectName("plot")
        self.verticalLayout.addWidget(self.plot)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 25)
        self.horizontalLayout.setStretch(1, 75)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #-------------------The functional part of the app starts here-------------------------#
        #initialize the live data plot
        self.N = 3000 #pre set the amount of points the live data plot
        self.xdata = [0] #initialize some dummy data
        self.ydata = [0]

        self.curve1 = pg.PlotDataItem(self.xdata, self.ydata) #instance the curve object
        self.plot.addItem(self.curve1)
        self.plot.setLabels(title="Data from potentiometer",
                            bottom="Time in miliseconds from start of measurement", left="Voltage (V)")

        #initialize the long range data plot
        self.xdata_long = [0]
        self.ydata_long = [0]
        self.curve2 = pg.PlotDataItem(self.xdata_long, self.ydata_long)
        self.plot_long.addItem(self.curve2)
        self.plot_long.setLabels(title="Data from potentiometer from the beggining",
                                 bottom="Time in miliseconds from start of measurement",
                                 left="Voltage (V)")

        #Instance the custom client
        self.client = MQTT_Client()

        #Connect the signals to its respective slots
        self.client.messageSignal.connect(self.onMessage)
        self.button_conn.clicked.connect(self.connect)
        self.horizontalSlider.valueChanged.connect(self.set_n)
        self.line_host.editingFinished.connect(self.host_edit)
        self.line_port.editingFinished.connect(self.port_edit)
        self.line_topic.editingFinished.connect(self.topic_edit)

        # adding a timer to get the long ranged data
        self.qtimer = QtCore.QTimer()
        self.qtimer.setInterval(1000)
        self.qtimer.timeout.connect(self.get_long_data) #Connect the timeout event to a slot

        # Second timer to get the frequency
        self.qtimer1 = QtCore.QTimer()
        self.qtimer1.setInterval(10000)
        self.qtimer1.timeout.connect(self.get_freq)


    def get_freq(self):
        #Prints the avg sampling frequency on the listwidget
        x = np.asarray(self.xdata)
        xdiff = x[1:]-x[:len(x)-1]
        dt = np.mean(xdiff)/1000
        self.listWidget.addItem(
            "--> Avg sampling frequency from \n the last {} points:\n{} Hz".format(len(x), str(1/dt)[:7]))

    def host_edit(self):
        #reassigns the new hostname based on the line edit
        text = self.line_host.text()
        if text == "": #catches the null editing of a line
            pass
        else:
            self.client.host = text
            self.listWidget.addItem("--> Hostname changed to:{}".format(text))

    def port_edit(self):
        #reassings a new port based on the line edit
        text = self.line_port.text()
        if text == "":
            pass
        else:
            try:
                self.client.port = int(text)
                self.listWidget.addItem("--> Port changed to:{}".format(text))
            except ValueError:
                self.listWidget.addItem("--> Insert an integer, not a string.")

    def topic_edit(self):
        #Reassigns a new topic to subscribe.

        text = self.line_topic.text()
        if text == "":
            pass
        else:
            self.client.subscribe_topic = text
            self.listWidget.addItem(
                "--> Topic to subscribe changed to:{}".format(text))

    def connect(self):
        #handles the connection after clicking the button
        if self.client.state == "connected":
            self.listWidget.addItem("-->Already connected to a host")
        else:
            try:
                self.client.connectToHost()
                self.listWidget.addItem("--> GUI connected: \n hostname: \"{}\"   \n Port: {} \n Clean session {} \n Subscribed to \"{}\"".format(
                    self.client.host, self.client.port, self.client.cleanSession, self.client.subscribe_topic))

                # start the timers
                self.qtimer.start()
                self.qtimer1.start()
            except:
                self.listWidget.addItem("--> Something went wrong. Try again")

    def get_long_data(self):
        if len(self.xdata) > 1:
            try:
                self.xdata_long.append(self.xdata[-1])
                self.ydata_long.append(np.mean(self.ydata[-10:]))
                self.curve2.setData(self.xdata_long[1:], self.ydata_long[1:])
            except IndexError:
                pass

    def set_n(self, value):
        #handles the change on the slider for the number of points.
        n_points = [50*i for i in range(100)]
        self.N = n_points[value]

    def onMessage(self, msg):
        #Handles the reception of a new message from the broker

        data, time = msg.split("|")
        data = [float(i)/4095*3.3 for i in data.split()]
        time = [float(i) for i in time.split()]

        self.ydata += data
        self.xdata += time

        N = self.N
        if len(self.xdata) >= N:
            self.xdata = self.xdata[-N:]
            self.ydata = self.ydata[-N:]

        try:
            self.curve1.setData(self.xdata[1:], self.ydata[1:])
        except IndexError:
            pass

    def retranslateUi(self, MainWindow):
        #Just another function to handle the backbones of the app. Just renames stuff
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data interface"))
        self.mqtt_label.setText(_translate(
            "MainWindow", "MQTT client options"))
        self.host_label.setText(_translate("MainWindow", "Hostname"))
        self.port_label.setText(_translate("MainWindow", "Port"))
        self.topic_label.setText(_translate(
            "MainWindow", "Topic to subscribe"))
        self.button_conn.setText(_translate("MainWindow", "Connect to Host"))
        self.n_points.setText(_translate(
            "MainWindow", "Number of points in plot:"))
        self.plot_long.setStatusTip(_translate(
            "MainWindow", "Displays the data for long periods of time"))


if __name__ == "__main__": #Launch the GUI
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
