#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 16:59:09 2024

@author: sabine
"""

import sys
import glob
import serial
import re
import time
from datetime import datetime
import os.path
import threading


import pyqtgraph as pg
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pyForceSense_ui import Ui_PyForceSenseWidget  # Assuming this was generated with pyuic5

BAUD = 9600
SERIAL_TIMER_INTERVAL = 20
MAXPLOTLENGTH = 100
breaktime=3.0 #3 seconds break time of force recording to read serial communication

forceStringPattern = re.compile(r'Force: ([-.0-9]+)')

def serial_ports():
    """ Lists serial port names """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class PyForceSense(Ui_PyForceSenseWidget, QWidget):
    
    def __init__(self, parent=None): #connects buttons to functions
        super(PyForceSense, self).__init__(parent)
        self.setupUi(self)
        self.maxForce = 0.0
        self.curForce = 0.0
        self.serialTimer = None
        self.resetMaxBtn.clicked.connect(self.resetMax)
        self.forcePlotObj = self.forcePlot.plot()
        self.plotData = []
        ports = serial_ports()
        self.trigPositions = []
        self.comportCombo.addItems(ports)
        self.connectButton.clicked.connect(self.serialConnect)
        self.autoNameButton.clicked.connect(self.autoName)
        self.logging = False
        self.logButton.clicked.connect(self.toggleLog)
        self.logFile = None
        self.clearButton.clicked.connect(lambda: self.serialOutputText.setPlainText(""))
        self.resetTareButton.clicked.connect(self.resetTare)
        self.serial = None
        self.autoName()
        self.yellowPen = pg.mkPen('y')
        self.ForceDeviceInfo_Button.clicked.connect(self.showForceDeviceInfo) #when button clicked calles function showForceDeviceInfo
        self.UpdateForceDeviceNr_Button.clicked.connect(self.updateForceDevice)
        self.UpdateScaleFaktor_Button.clicked.connect(self.updateForceDevic_ScaleFKT)

        

    def resetTare(self):
        if not self.checkSerialAvailable(): return
        ans = QMessageBox.warning(self, "Reset", "Resetting tare. Are you sure?", QMessageBox.Yes | QMessageBox.No)
        if ans == QMessageBox.Yes:
            self.serial.write(b"RESET\n")
        
    def toggleLog(self):
        if self.logging:
            self.logging = False
            self.logButton.setText("Start logging")
            self.logButton.setStyleSheet("")
            if self.logFile:
                self.serialOutputText.appendPlainText("Saving log")
                self.logFile.close()
                self.logFile = None
        else:
            if os.path.isfile(str(self.logName.text())):
                ret = QMessageBox.warning(self, "Warning", "LogFile exists! Overwrite?", QMessageBox.Yes | QMessageBox.No)
                if ret == QMessageBox.No:
                    return
            self.serialOutputText.appendPlainText("Opening log file: " + str(self.logName.text()))
            try:
                self.logFile = open(str(self.logName.text()), 'w')
                self.logFile.write("time,force,other\n")
            except:
                self.logFile = None
                self.serialOutputText.appendPlainText("Error opening log file")
                return
            self.logging = True
            self.logButton.setText("Stop logging")
            self.logButton.setStyleSheet("background-color: #FF5555;")
        
    def autoName(self):
        oldTxt = str(self.logName.text())
        pos = oldTxt.find('_')
        if pos < 0:
            baseStr = "LogFile"
        else:
            baseStr = oldTxt[:pos]
        self.logName.setText(baseStr + time.strftime("_%Y-%m-%d_%H.%M.%S.txt"))
        
    def serialConnect(self):
        if self.serial is not None:
            ans = QMessageBox.warning(self, "Disconnect", "Are you sure you want to disconnect?", QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.serialDisconnect()
            return
        try:
            self.serial = serial.Serial(str(self.comportCombo.currentText()), BAUD, timeout=0.5)
        except (OSError, serial.SerialException):
            self.serialOutputText.appendPlainText("Cannot open serial")
            self.serial = None
            return
        
        self.connectButton.setText("Disconnect")
        self.comportCombo.setEnabled(False)
        
        self.serialTimer = QTimer()
        self.serialTimer.timeout.connect(self.checkSerial)
        self.serialTimer.start(SERIAL_TIMER_INTERVAL)

    def serialDisconnect(self):
        self.connectButton.setText("Connect")
        self.comportCombo.setEnabled(True)
        if self.serialTimer: self.serialTimer.stop()
        self.serial = None
        
    def checkSerialAvailable(self):
        if not self.serial or not self.serial.readable():
            self.serialDisconnect()
            return False
        return True

    def checkSerial(self):
        if not self.checkSerialAvailable(): return
        if self.serial.in_waiting:
            serStr = self.serial.readline().strip()
            self.processSerial(serStr.decode())

    def makeLine(self, value):
        line = pg.InfiniteLine(movable=False, angle=90, pen=self.yellowPen, pos=value)
        self.forcePlot.addItem(line)
        return line

    def processSerial(self, serialString):
        m = forceStringPattern.match(serialString)
        if m is not None:
            self.curForce = float(m.group(1)) * 9.80665
            if self.curForce > self.maxForce: self.maxForce = self.curForce
            if self.logFile:
                timestamp = time.time()
                self.logFile.write("%f,%f,\"\"\n" % (timestamp, self.curForce))
            self.updateUi()
        else:
            self.serialOutputText.appendPlainText(serialString)
            if self.logFile:
                timestamp = time.time()
                self.logFile.write("%f,,\"%s\"\n" % (timestamp, serialString))
            if serialString.upper() == "TRIG":
                self.trigPositions.append(self.makeLine(len(self.plotData)))
            
    def closeEvent(self, event):
        if self.logFile:
            print("Saving log")
            self.logFile.close()
        event.accept()
            
    def resetMax(self):
        self.maxForce = 0.0
        self.updateUi()
            
    def updateUi(self):
        self.curForceLabel.setText('{:.2f}'.format(self.curForce))
        self.maxForceLabel.setText('{:.2f}'.format(self.maxForce))
        self.plotData.append(self.curForce)
        while len(self.plotData) > MAXPLOTLENGTH: 
            self.plotData.pop(0)
            while len(self.trigPositions) > 0 and self.trigPositions[0].value() <= 0:
                self.forcePlot.removeItem(self.trigPositions[0])
                self.trigPositions.pop(0)
            for posIndex in range(len(self.trigPositions)):
                self.trigPositions[posIndex].setValue(self.trigPositions[posIndex].value() - 1)
                
        self.forcePlotObj.setData(self.plotData)
        
    def showForceDeviceInfo(self):
        #write to serial GET_SENSOR and GET_SCALE and reeads respective answers and plots them to the “serialOutputText”
        if not self.checkSerialAvailable():
            self.serialOutputText.appendPlainText(f"Connection Error")
            return
        #self.serial.reset_input_buffer()
        self.serial.write(b"GET_SENSOR\n")
        sensorinfo = self.serial.readline().strip().decode('utf-8')  # Decode the byte string from comand line into a python string
        self.processSerial(sensorinfo)
        #time.sleep(0.05)  # Allow Arduino to process
        #self.serialOutputText.appendPlainText(f"{sensorinfo}")
        #self.serial.reset_input_buffer()
        self.serial.write(b"GET_SCALE\n")
        sensor_scaleFKT_info=self.serial.readline().strip().decode('utf-8')
        self.processSerial(sensor_scaleFKT_info)
        #self.serialOutputText.appendPlainText(f"{sensor_scaleFKT_info}")
        
    def updateForceDevice(self):
        #get future_current_sensor from ForceDeviceNrInput_QSpinBox, get current sensor from serial and print in “serialOutputText”, write to serial SET_SENSOR <current_sensor>, get from serial new current sensor and print in “serialOutputText” 
        if not self.checkSerialAvailable():
            self.serialOutputText.appendPlainText(f"Connection Error")
            return
        device_number = float(self.ForceDeviceNrInput_QSpinBox.value())
        self.serial.write(f"SET_SENSOR {device_number}\n".encode()) #updates the current sensor to the new device as inated by the qspin box, ARDUINO will output a serial text 
        sensorinfo_new=self.serial.readline().strip().decode('utf-8')
        self.serialOutputText.appendPlainText(f"{sensorinfo_new}") #outputs text in text window to check if device number update went as planned 
        
    def updateForceDevic_ScaleFKT(self):
        # get device number from ForceDeviceNrInput_QSpinBox, get scaleFKT from ScaleFaktorInput_QLineEdit, write to serial SET_SCALE, get current Sensor and Scale fkt from serial and print in “serialOutputText”
        if not self.checkSerialAvailable():
            self.serialOutputText.appendPlainText(f"Connection Error")
            return
        sensor_number_qspin = float(self.ForceDeviceNrInput_QSpinBox.value())
        try:
            scaleFKT=float(self.ScaleFaktorInput_QLineEdit.text())
        except ValueError:
            print("Error: Input is not a valid float")
            return
        self.serial.write(b"GET_SENSOR\n")
        current_sensorinfo = self.serial.readline().strip().decode('utf-8') 
        match = re.search(r"\d+(\.\d+)?", current_sensorinfo)  # Matches integers or floats, so extracts float from arduino info text 
        sensor_number = float(match.group())  # Convert the matched string to a float
        if sensor_number == sensor_number_qspin:
            self.serial.write(f"SET_SCALE {sensor_number} {scaleFKT}\n".encode())
            arduin_answer=self.serial.readline().strip().decode('utf-8') 
            self.serialOutputText.appendPlainText(f"{arduin_answer} ")
        else:
            ans = QMessageBox.warning(self, "Current Sensor not equal Spin Box Input", "Do you wanto to change scale factor for current sensor?", QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.serial.write(f"SET_SCALE {sensor_number} {scaleFKT}\n".encode())
                arduin_answer=self.serial.readline().strip().decode('utf-8') 
                self.serialOutputText.appendPlainText(f"{arduin_answer} ")
            if ans == QMessageBox.No:
                self.serial.write(f"SET_SCALE {sensor_number_qspin} {scaleFKT}\n".encode())
                arduin_answer=self.serial.readline().strip().decode('utf-8') 
                self.serialOutputText.appendPlainText(f"{arduin_answer} ")
                self.serial.write(b"GET_SENSOR\n")
                sensorinfo = self.serial.readline().strip().decode('utf-8')  # Decode the byte string from comand line into a python string
                self.serialOutputText.appendPlainText(f"{sensorinfo}") #outputs the current active sensor which is differnt from the change whichs scale factor got updated 
            return

        
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyForceSense()
    window.show()
    sys.exit(app.exec_())
