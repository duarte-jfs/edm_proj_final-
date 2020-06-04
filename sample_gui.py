# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sample_gui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


import pyqtgraph as pg
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import paho.mqtt.client as mqtt
import sys


class MQTT_Client(QObject):
    # Define your signals
    messageSignal = pyqtSignal(str)

    connected = pyqtSignal()
    disconnected = pyqtSignal()

    def __init__(self):
        QObject.__init__(self)

        self.host = "localhost"
        self.port = 1883
        self.keepAlive = 60
        self.cleanSession = True
        self.subscribe_topic = "measurement"

        self.client = mqtt.Client(clean_session=self.cleanSession)
        self.client.on_connect = self.on_connect1
        self.client.on_message = self.on_message1
        self.client.on_disconnect = self.on_disconnect1

    def on_message1(self, mqttc, obj, msg):
        mstr = msg.payload.decode("ascii")
        # print("on_message", mstr, obj, mqttc)
        self.messageSignal.emit(mstr)

    def on_connect1(self, *args):
        # print("on_connect", args)
        self.connected.emit()

    def on_disconnect1(self, *args):
        # print("on_disconnect", args)
        self.disconnected.emit()

    @pyqtSlot()
    def connectToHost(self):
        self.client.connect(self.host,
                            port=self.port,
                            keepalive=self.keepAlive)

        self.client.subscribe(self.subscribe_topic)
        self.client.loop_start()

    @pyqtSlot()
    def disconnectFromHost(self):
        self.client.disconnect()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 0, 0, 1, 1)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.plot = pg.PlotWidget(self.centralwidget)
        self.plot.setObjectName("widget")
        self.horizontalLayout.addWidget(self.plot)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

        self.client = MQTT_Client()
        self.client.messageSignal.connect(self.onMessage)
        self.pushButton.clicked.connect(self.client.connectToHost)

        ##starts here
        self.xdata = [0]
        self.ydata = [0]
        self.curve1 = pg.PlotDataItem(self.xdata, self.ydata)
        self.plot.addItem(self.curve1)

    def onMessage(self,msg):
        data=[float(value) for value in msg.split()]
        self.ydata+=data
        self.xdata+=[self.xdata[-1]+i for i in range(1,len(data)+1)]

        N=2000
        if len(self.xdata)>=N:
            self.xdata=self.xdata[-N:]
            self.ydata = self.ydata[-N:]

        self.curve1.setData(self.xdata,self.ydata)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
