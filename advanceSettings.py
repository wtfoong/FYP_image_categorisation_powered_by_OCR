from wsgiref import validate
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMessageBox
from validation import validator


class Ui_AdvanceSettings(object):
    
    def validate(self,main_w,AdvanceSettings):
        flag = True
        if not (self.txtAccPercentage.text() and self.txtLinesToRead.text()):
            self.alertMessage("Please fill up all fields!")
            flag = False
        elif not validator.validateAccuracyPercentage(int(self.txtAccPercentage.text())):
            self.alertMessage("Please make sure accuracy percentage is in the range of 1 to 100!")
            flag = False
            
        if flag:            
            # main_w.lines_to_read=int(self.txtLinesToRead.text())
            # main_w.acc_percentage=int(self.txtAccPercentage.text())  
            main_w.show()
            AdvanceSettings.hide()
      
    def cancel(self):
        self.txtLinesToRead.setText("0")
        self.txtAccPercentage.setText("75")
        
        
    def alertMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
    
    
    def setupUi(self, AdvanceSettings, MainWindow):
        AdvanceSettings.setObjectName("AdvanceSettings")
        AdvanceSettings.setFixedSize(1002, 192)
        self.centralwidget = QtWidgets.QWidget(AdvanceSettings)
        self.centralwidget.setObjectName("centralwidget")
        self.txtLinesToRead = QtWidgets.QLineEdit(self.centralwidget)
        self.txtLinesToRead.setValidator(QIntValidator(0, 999))
        self.txtLinesToRead.setGeometry(QtCore.QRect(240, 19, 739, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtLinesToRead.setFont(font)
        self.txtLinesToRead.setObjectName("txtLinesToRead")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setEnabled(True)
        self.label_5.setGeometry(QtCore.QRect(11, 19, 223, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setEnabled(True)
        self.label_6.setGeometry(QtCore.QRect(11, 50, 223, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.txtAccPercentage = QtWidgets.QLineEdit(self.centralwidget)
        self.txtAccPercentage.setValidator(QIntValidator(0, 999))
        self.txtAccPercentage.setGeometry(QtCore.QRect(240, 50, 739, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtAccPercentage.setFont(font)
        self.txtAccPercentage.setObjectName("txtAccPercentage")
        self.btnConfirmAdvanceSetting = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.validate(MainWindow,AdvanceSettings))
        self.btnConfirmAdvanceSetting.setGeometry(QtCore.QRect(840, 100, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnConfirmAdvanceSetting.setFont(font)
        self.btnConfirmAdvanceSetting.setObjectName("btnConfirmAdvanceSetting")
        self.btnCancel = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.cancel())
        self.btnCancel.setGeometry(QtCore.QRect(240, 100, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCancel.setFont(font)
        self.btnCancel.setObjectName("btnCancel")
        AdvanceSettings.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(AdvanceSettings)
        self.statusbar.setObjectName("statusbar")
        AdvanceSettings.setStatusBar(self.statusbar)

        self.retranslateUi(AdvanceSettings)
        QtCore.QMetaObject.connectSlotsByName(AdvanceSettings)

    def retranslateUi(self, AdvanceSettings):
        _translate = QtCore.QCoreApplication.translate
        AdvanceSettings.setWindowTitle(_translate("AdvanceSettings", "Advance Settings"))
        self.txtLinesToRead.setPlaceholderText(_translate("AdvanceSettings", "Number of lines to read from OCR data and compare to category, put 0 to read all"))
        self.label_5.setText(_translate("AdvanceSettings", "Lines to read"))
        self.label_6.setText(_translate("AdvanceSettings", "Accuracy Percentage"))
        self.txtAccPercentage.setPlaceholderText(_translate("AdvanceSettings", "How accurate the OCR data need to be in compare to the category, decides accuracy of the result"))
        self.btnConfirmAdvanceSetting.setText(_translate("AdvanceSettings", "Confirm"))
        self.btnCancel.setText(_translate("AdvanceSettings", "Reset"))
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AdvanceSettings = QtWidgets.QMainWindow()
    ui = Ui_AdvanceSettings()
    ui.setupUi(AdvanceSettings)
    AdvanceSettings.show()
    sys.exit(app.exec())
