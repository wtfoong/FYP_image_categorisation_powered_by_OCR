from wsgiref import validate

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMessageBox

import image_categorisation_powered_by_OCR
from validation import validator
from OCRWindow import Ui_OCRWindow
from backend.folder_processes import folder_processes


class Ui_MainWindow(object):
    def categorise(self):
        
        image_categorisation_powered_by_OCR.os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.txtGoogleCredential.text()
        image_folder = self.txtImageFolder.text()
        categories_txtfile = self.txtCategories.text()
        subProcessNumber = int(self.txtSubprocessNumber.text())
        lines_to_read = int(self.txtLinesToRead.text())
        accuracy_percentage = int(self.txtAccPercentage.text())

        image_categorisation_powered_by_OCR.comparison.multiprocessing_image_categorisation(image_folder,subProcessNumber,categories_txtfile,lines_to_read,accuracy_percentage)
        
    def openOCRWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_OCRWindow()
        self.ui.setupUi(self.window,MainWindow)
        self.ui.txtGoogleCredential_2.setText(self.txtGoogleCredential.text())
        self.window.show()
        
    def validate(self):
        flag = True
        if not (self.txtGoogleCredential.text() and self.txtImageFolder.text() and self.txtCategories.text() and self.txtSubprocessNumber.text() and self.txtLinesToRead.text() and self.txtAccPercentage.text()):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please fill up all fields!")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            flag = False
        
        elif not validator.validatePath(self.txtGoogleCredential.text(),"Google credential json file path is not valid or the file does not exist!"):
            flag = False
        
        
        if flag:  
            
            self.recordData()
            self.categorise()
           
            
    def recordData(self):
        datalist = [self.txtGoogleCredential.text(), self.txtImageFolder.text(), self.txtCategories.text(), self.txtSubprocessNumber.text(), self.txtLinesToRead.text(), self.txtAccPercentage.text()]
        folder_processes.writeToFile("data.txt",datalist)
        
    def readData(self):
        datalist = folder_processes.get_all_categories("data.txt")
        self.txtGoogleCredential.setText(datalist[0])
        self.txtImageFolder.setText(datalist[1])
        self.txtCategories.setText(datalist[2])
        self.txtSubprocessNumber.setText(datalist[3])
        self.txtLinesToRead.setText(datalist[4])
        self.txtAccPercentage.setText(datalist[5])
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 353)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnOCRWindow = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.openOCRWindow())
        self.btnOCRWindow.setGeometry(QtCore.QRect(20, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnOCRWindow.setFont(font)
        self.btnOCRWindow.setObjectName("btnOCRWindow")
        self.btnCategorise = QtWidgets.QPushButton(self.centralwidget,clicked = lambda:self.validate())
        self.btnCategorise.setGeometry(QtCore.QRect(870, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCategorise.setFont(font)
        self.btnCategorise.setObjectName("btnCategorise")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 21, 1061, 182))
        self.widget.setObjectName("widget")
        self.formLayout = QtWidgets.QFormLayout(self.widget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label)
        self.txtGoogleCredential = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtGoogleCredential.setFont(font)
        self.txtGoogleCredential.setObjectName("txtGoogleCredential")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtGoogleCredential)
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_3)
        self.txtImageFolder = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtImageFolder.setFont(font)
        self.txtImageFolder.setObjectName("txtImageFolder")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtImageFolder)
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_2)
        self.txtCategories = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtCategories.setFont(font)
        self.txtCategories.setObjectName("txtCategories")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtCategories)
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_4)
        self.txtSubprocessNumber = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtSubprocessNumber.setFont(font)
        self.txtSubprocessNumber.setValidator(QIntValidator(0, 999))
        self.txtSubprocessNumber.setObjectName("txtSubprocessNumber")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtSubprocessNumber)
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.txtLinesToRead = QtWidgets.QLineEdit(self.widget)
        self.txtLinesToRead.setValidator(QIntValidator(0, 999))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtLinesToRead.setFont(font)
        self.txtLinesToRead.setObjectName("txtLinesToRead")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtLinesToRead)
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.txtAccPercentage = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtAccPercentage.setFont(font)
        self.txtAccPercentage.setObjectName("txtAccPercentage")
        self.txtAccPercentage.setValidator(QIntValidator(0, 999))
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.txtAccPercentage)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
    
        self.retranslateUi(MainWindow)
        self.readData()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Categorisor"))
        self.btnOCRWindow.setText(_translate("MainWindow", "OCR single image"))
        self.btnCategorise.setText(_translate("MainWindow", "Categorise"))
        self.label.setText(_translate("MainWindow", "Google Credential json file path"))
        self.txtGoogleCredential.setPlaceholderText(_translate("MainWindow", "File path to google credential json file"))
        self.label_3.setText(_translate("MainWindow", "Image folder path"))
        self.txtImageFolder.setPlaceholderText(_translate("MainWindow", "Path to images to be categorised"))
        self.label_2.setText(_translate("MainWindow", "Categories text file path"))
        self.txtCategories.setPlaceholderText(_translate("MainWindow", "Path to text file that stores categories"))
        self.label_4.setText(_translate("MainWindow", "Subprocess number"))
        self.txtSubprocessNumber.setPlaceholderText(_translate("MainWindow", "Number of sub-processes, determines the speed of categorisation"))
        self.label_5.setText(_translate("MainWindow", "Lines to read"))
        self.txtLinesToRead.setPlaceholderText(_translate("MainWindow", "Number of lines to read from OCR data and compare to category, leave blank to read all"))
        self.label_6.setText(_translate("MainWindow", "Accuracy Percentage"))
        self.txtAccPercentage.setPlaceholderText(_translate("MainWindow", "How accurate the OCR data need to be in compare to the category, decides how accurate the result of the system."))


    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
