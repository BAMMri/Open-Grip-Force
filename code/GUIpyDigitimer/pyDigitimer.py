import sys
import glob
import serial
import re
import time


from PyQt5.QtWidgets import *  # CHANGE: Explicitly import QtWidgets
from PyQt5.QtWidgets import QApplication
from pyDigitimer_ui import Ui_PyDigitimerWidget


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

class PyDigitimer(QWidget, Ui_PyDigitimerWidget): # CHANGE
    
    def __init__(self, parent = None):
        """
        Args:
            parent: The parent widget to which this object will be added
        """
        super().__init__(parent)  # # CHANGE
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
        """
        Reads status from the device via serial communication and updates the frequency, on time, and off time values accordingly.
        """
        time.sleep(0.5)
        self.serial.reset_input_buffer() # CHANGE
        self.serial.write(b"?\n") # CHANGE
        time.sleep(0.1)
        while self.serial.in_waiting:
            statusLine = self.serial.readline().decode().strip()
            print (statusLine)
        m = re.match(r'Status: (\d+),(\d+),(\d+)', statusLine) #maybe (r'Status: (\d+),(\d+),(\d+)', statusLine)?
        if m is None:
            QMessageBox.warning(self, "Error", "Error parsing status", QMessageBox.StandardButton.Ok) #change
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
        """
        Connects to a serial port.

        Parameters:
        None

        Returns:
        None
        """
        if self.serial is not None:
            # we are already connected
            ans = QMessageBox.warning(self, "Disconnect", "Are you sure you want to disconnect?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)  # CHANGE
            if ans == QMessageBox.StandardButton.Yes: #Change
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
        """

        Writes the current settings to the serial port.

        The following settings are used:
        - Frequency: The current frequency value from freqSpin
        - On Time: The current on time value from onSpin
        - Off Time: The current off time value from offSpin

        An output string is created by formatting the settings values separated by commas.
        The output string is then written to the serial port followed by a newline character.

        After writing, the method prints the output string and reads a response from the serial port, decoding and stripping the output.
        Finally, the setButton style sheet is set to an empty string.

        """
        self.serial.reset_input_buffer()  # CHANGE
        self.freq = self.freqSpin.value()
        self.onTime = self.onSpin.value()
        self.offTime = self.offSpin.value()
        outStr = f"{self.freq},{self.onTime},{self.offTime}"  # CHANGE: Use f-string formatting
        print("Writing:", outStr)  # CHANGE: Fix print statement
        self.serial.write((outStr + "\n").encode())  # CHANGE: Encode string before writing
        print(self.serial.readline().decode().strip())  # CHANGE: Decode readline() output
        self.setButton.setStyleSheet("")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    window = PyDigitimer()
    window.show()
    window.setFixedSize(window.size())
    sys.exit(app.exec())
