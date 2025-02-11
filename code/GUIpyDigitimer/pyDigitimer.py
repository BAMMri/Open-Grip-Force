import sys
import glob
import serial
import re

import PyQt4
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from pyDigitimer_ui import Ui_PyDigitimerWidget
import time

BAUD = 9600
#SERIAL_PORT = '/dev/ttyUSB0'
#SERIAL_PORT = '/dev/ttyS98'
SERIAL_TIMER_INTERVAL = 20
MAXPLOTLENGTH = 100

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
        #ports = glob.glob('/dev/pts/2')
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

class PyDigitimer(Ui_PyDigitimerWidget, QWidget):
    
    def __init__(self, parent = None):
        QWidget.__init__(self, parent)
        self.setupUi(self)
        ports = serial_ports()
        self.comportCombo.addItems(ports)
        self.connectButton.clicked.connect(self.serialConnect)
        self.setButton.clicked.connect(self.writeSettings)
        self.freqSpin.valueChanged.connect(self.invalidateSet)
        self.onSpin.valueChanged.connect(self.invalidateSet)
        self.offSpin.valueChanged.connect(self.invalidateSet)
        self.serial = None
        self.freq = 0
        self.onTime = 0
        self.offTime = 0
        
    def readStatus(self):
        time.sleep(0.5)
        self.serial.flushInput()
        self.serial.write("?\n")
        time.sleep(0.1)
        while self.serial.inWaiting():
            statusLine = self.serial.readline()
            print statusLine
        m = re.match(r'Status: (\d+),(\d+),(\d+)', statusLine)
        if m is None:
            QMessageBox.warning(self, "Error", "Error parsing status", QMessageBox.Ok)
            return
        
        self.freq = int(m.group(1))
        self.onTime = int(m.group(2))
        self.offTime = int(m.group(3))
        
        self.freqSpin.setValue(self.freq)
        self.onSpin.setValue(self.onTime)
        self.offSpin.setValue(self.offTime)
        
    def invalidateSet(self):
        if self.setButton.isEnabled():
            if (self.freq == self.freqSpin.value()
                and self.onTime == self.onSpin.value()
                and self.offTime == self.offSpin.value()):
                
                self.setButton.setStyleSheet("")
            else:
                self.setButton.setStyleSheet("background-color: #CC9999")
            
    def serialConnect(self):
        if self.serial is not None:
            # we are already connected
            ans = QMessageBox.warning(self, "Disconnect", "Are you sure you want to disconnect?", QMessageBox.Yes | QMessageBox.No)
            if ans == QMessageBox.Yes:
                self.serialDisconnect()
            return
        try:
            self.serial = serial.Serial(str(self.comportCombo.currentText()), BAUD, timeout=0.5)
        except (OSError, serial.SerialException):
            self.serial = None
            return
        
        self.readStatus()
        self.connectButton.setText("Disconnect")
        self.comportCombo.setEnabled(False)
        self.settingsBox.setEnabled(True)
        

    def serialDisconnect(self):
        self.connectButton.setText("Connect")
        self.comportCombo.setEnabled(True)
        self.serial = None
        self.settingsBox.setEnabled(False)
        
    def writeSettings(self):
        self.serial.flushInput()
        self.freq = self.freqSpin.value()
        self.onTime = self.onSpin.value()
        self.offTime = self.offSpin.value()
        outStr = "%d,%d,%d" % (self.freq, self.onTime, self.offTime)
        print "Writing: ", outStr
        self.serial.write(outStr + "\n")
        print self.serial.readline()
        self.setButton.setStyleSheet("")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PyDigitimer()
    window.show()
    window.setFixedSize(window.size())
    sys.exit(app.exec_())
