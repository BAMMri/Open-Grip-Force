# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pyDigitimer.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_PyDigitimerWidget(object):
    def setupUi(self, PyDigitimerWidget):
        PyDigitimerWidget.setObjectName(_fromUtf8("PyDigitimerWidget"))
        PyDigitimerWidget.resize(445, 257)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(PyDigitimerWidget.sizePolicy().hasHeightForWidth())
        PyDigitimerWidget.setSizePolicy(sizePolicy)
        PyDigitimerWidget.setStyleSheet(_fromUtf8("QSpinBox:disabled {\n"
"    background-color: #F0F0F0;\n"
"    color: #999999;\n"
"}\n"
"\n"
"QPushButton:disabled {\n"
"    color: #999999;\n"
"}"))
        self.comportCombo = QtGui.QComboBox(PyDigitimerWidget)
        self.comportCombo.setGeometry(QtCore.QRect(20, 10, 211, 28))
        self.comportCombo.setObjectName(_fromUtf8("comportCombo"))
        self.connectButton = QtGui.QPushButton(PyDigitimerWidget)
        self.connectButton.setGeometry(QtCore.QRect(240, 10, 91, 29))
        self.connectButton.setObjectName(_fromUtf8("connectButton"))
        self.settingsBox = QtGui.QGroupBox(PyDigitimerWidget)
        self.settingsBox.setEnabled(False)
        self.settingsBox.setGeometry(QtCore.QRect(30, 60, 371, 161))
        self.settingsBox.setObjectName(_fromUtf8("settingsBox"))
        self.freqSpin = QtGui.QSpinBox(self.settingsBox)
        self.freqSpin.setGeometry(QtCore.QRect(100, 30, 86, 33))
        self.freqSpin.setMinimum(1)
        self.freqSpin.setMaximum(200)
        self.freqSpin.setObjectName(_fromUtf8("freqSpin"))
        self.onSpin = QtGui.QSpinBox(self.settingsBox)
        self.onSpin.setGeometry(QtCore.QRect(100, 70, 86, 33))
        self.onSpin.setMinimum(100)
        self.onSpin.setMaximum(10000)
        self.onSpin.setSingleStep(100)
        self.onSpin.setObjectName(_fromUtf8("onSpin"))
        self.offSpin = QtGui.QSpinBox(self.settingsBox)
        self.offSpin.setGeometry(QtCore.QRect(100, 110, 86, 33))
        self.offSpin.setMinimum(100)
        self.offSpin.setMaximum(10000)
        self.offSpin.setSingleStep(100)
        self.offSpin.setObjectName(_fromUtf8("offSpin"))
        self.label = QtGui.QLabel(self.settingsBox)
        self.label.setGeometry(QtCore.QRect(20, 40, 81, 19))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.settingsBox)
        self.label_2.setGeometry(QtCore.QRect(190, 40, 81, 19))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.settingsBox)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 81, 19))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.label_4 = QtGui.QLabel(self.settingsBox)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 81, 19))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.label_5 = QtGui.QLabel(self.settingsBox)
        self.label_5.setGeometry(QtCore.QRect(190, 80, 81, 19))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_6 = QtGui.QLabel(self.settingsBox)
        self.label_6.setGeometry(QtCore.QRect(190, 120, 81, 19))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.setButton = QtGui.QPushButton(self.settingsBox)
        self.setButton.setGeometry(QtCore.QRect(260, 110, 89, 35))
        self.setButton.setObjectName(_fromUtf8("setButton"))

        self.retranslateUi(PyDigitimerWidget)
        QtCore.QMetaObject.connectSlotsByName(PyDigitimerWidget)

    def retranslateUi(self, PyDigitimerWidget):
        PyDigitimerWidget.setWindowTitle(_translate("PyDigitimerWidget", "Digitimer pulse generator", None))
        self.connectButton.setText(_translate("PyDigitimerWidget", "Connect", None))
        self.settingsBox.setTitle(_translate("PyDigitimerWidget", "Settings", None))
        self.label.setText(_translate("PyDigitimerWidget", "Frequency:", None))
        self.label_2.setText(_translate("PyDigitimerWidget", "Hz", None))
        self.label_3.setText(_translate("PyDigitimerWidget", "OnTime:", None))
        self.label_4.setText(_translate("PyDigitimerWidget", "OffTime:", None))
        self.label_5.setText(_translate("PyDigitimerWidget", "ms", None))
        self.label_6.setText(_translate("PyDigitimerWidget", "ms", None))
        self.setButton.setText(_translate("PyDigitimerWidget", "Set", None))

