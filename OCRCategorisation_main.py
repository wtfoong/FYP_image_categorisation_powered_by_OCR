from wsgiref import validate

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMessageBox,QFileDialog
from PyQt6.QtCore import QObject, QThread, pyqtSignal

import image_categorisation_powered_by_OCR
from validation import validator
from OCRWindow import Ui_OCRWindow
from backend.folder_processes import folder_processes
from functools import partial


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(str)
    errormessage = pyqtSignal(str)
    
    def alertMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
    def categorise(self,ui):
        
        image_categorisation_powered_by_OCR.os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ui.txtGoogleCredential.text()
        image_folder = ui.txtImageFolder.text()
        categories_txtfile = ui.txtCategories.text()
        subProcessNumber = int(ui.txtSubprocessNumber.text())
        lines_to_read = int(ui.txtLinesToRead.text())
        accuracy_percentage = int(ui.txtAccPercentage.text())
        error=image_categorisation_powered_by_OCR.comparison.multiprocessing_image_categorisation(image_folder,subProcessNumber,categories_txtfile,lines_to_read,accuracy_percentage,self.progress)
        
        if error:
            raise error
        

    def run(self,ui):
        """Long-running task."""
        try:
            
            self.categorise(ui)
            self.finished.emit() 
        except Exception as e:
            self.errormessage.emit(str(e))
            self.finished.emit() 



class Ui_MainWindow(object):
    
        
    def openOCRWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_OCRWindow()
        self.ui.setupUi(self.window,MainWindow)
        self.ui.txtGoogleCredential_2.setText(self.txtGoogleCredential.text())
        self.window.show()
        MainWindow.hide()
        
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
        elif not validator.validatePath(self.txtImageFolder.text(),"Image folder path is not valid or the folder does not exist!"):
            flag = False
        elif not validator.validatePath(self.txtCategories.text(),"Category text file path is not valid or the file does not exist!"):
            flag = False
        elif not validator.validateImageFolderPath(self.txtImageFolder.text()):
            self.alertMessage("Image folder is empty!")
            flag = False
        elif not validator.chkIfIstxtFile(self.txtCategories.text()):
            self.alertMessage("Category text file path does not lead to a text file!")
            flag = False
        elif not validator.validateCategories_txt(self.txtCategories.text()):
            self.alertMessage("Category text file is empty!")
            flag = False
        elif not validator.validateAccuracyPercentage(int(self.txtAccPercentage.text())):
            self.alertMessage("Please make sure accuracy percentage is in the range of 1 to 100!")
            flag = False
            
        if flag:  
            
            self.recordData()
             # Step 2: Create a QThread object
            self.thread = QThread()
            # Step 3: Create a worker object
            self.worker = Worker()
            # Step 4: Move worker to the thread
            self.worker.moveToThread(self.thread)
            # Step 5: Connect signals and slots
            
            self.thread.started.connect(partial(self.worker.run,self))
            self.worker.errormessage.connect(self.erroralert)
            self.worker.progress.connect(self.loading)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.btnCategorise.setEnabled(False)
            self.btnCategoryTxt.setEnabled(False)
            self.btnGoogleJson.setEnabled(False)
            self.btnImageFolder.setEnabled(False)
            
            self.thread.finished.connect(
                self.txtProcessing.hide
            )  
            self.thread.finished.connect(
                self.enableButtons
            )
            
            self.thread.finished.connect(
                self.alldone
            )
    def loading(self,message):
        self.txtProcessing.show()
        self.txtProcessing.setText(message)
        
    def erroralert(self,message):
        self.alertMessage(message)
    def alldone(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("All image categorised")
        msg.setWindowTitle("All done!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()   
          
    def enableButtons(self):
        self.btnCategorise.setEnabled(True)
        self.btnCategoryTxt.setEnabled(True)
        self.btnGoogleJson.setEnabled(True)
        self.btnImageFolder.setEnabled(True)
    def alertMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
            
    def recordData(self):
        datalist = [self.txtGoogleCredential.text(), self.txtImageFolder.text(), self.txtCategories.text(), self.txtSubprocessNumber.text(), self.txtLinesToRead.text(), self.txtAccPercentage.text()]
        folder_processes.writeToFile("data.txt",datalist)
        
    def readData(self):
        try:
            datalist = folder_processes.get_all_categories("data.txt")
            self.txtGoogleCredential.setText(datalist[0])
            self.txtImageFolder.setText(datalist[1])
            self.txtCategories.setText(datalist[2])
            self.txtSubprocessNumber.setText(datalist[3])
            self.txtLinesToRead.setText(datalist[4])
            self.txtAccPercentage.setText(datalist[5])
        except:
            pass
        
    def openFile(self,message,rule,path):
        file = QFileDialog.getOpenFileName(None,message, path, rule)
        return file
    def openFolder(self,message,path):
        file = QtWidgets.QFileDialog.getExistingDirectory(None, message,path)
        return file
       
    def getCategoriseTxt(self,message,rule):
        file = self.openFile(message,rule,self.txtCategories.text())
        self.txtCategories.setText(file[0])
    def getGoogleCredentialJson(self,message,rule):
        file = self.openFile(message,rule,self.txtGoogleCredential.text())
        self.txtGoogleCredential.setText(file[0])
    def getImageFolder(self,message):
        folder = self.openFolder(message,self.txtImageFolder.text())
        
        self.txtImageFolder.setText(folder)
        
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 353)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnOCRWindow = QtWidgets.QPushButton(self.centralwidget,clicked = lambda: self.openOCRWindow())
        self.btnOCRWindow.setGeometry(QtCore.QRect(20, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnOCRWindow.setFont(font)
        self.btnOCRWindow.setObjectName("btnOCRWindow")
        self.btnCategorise = QtWidgets.QPushButton(self.centralwidget, clicked = lambda:self.validate())
        self.btnCategorise.setGeometry(QtCore.QRect(870, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCategorise.setFont(font)
        self.btnCategorise.setObjectName("btnCategorise")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(14, 33, 1051, 188))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
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
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.txtGoogleCredential = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtGoogleCredential.setFont(font)
        self.txtGoogleCredential.setReadOnly(True)
        self.txtGoogleCredential.setObjectName("txtGoogleCredential")
        self.gridLayout.addWidget(self.txtGoogleCredential, 0, 1, 1, 1)
        self.btnGoogleJson = QtWidgets.QPushButton(self.widget, clicked= lambda: self.getGoogleCredentialJson("Select Google credential json file","Json file (*.json)"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGoogleJson.sizePolicy().hasHeightForWidth())
        self.btnGoogleJson.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnGoogleJson.setFont(font)
        self.btnGoogleJson.setObjectName("btnGoogleJson")
        self.gridLayout.addWidget(self.btnGoogleJson, 0, 2, 1, 1)
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
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.txtImageFolder = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtImageFolder.setFont(font)
        self.txtImageFolder.setReadOnly(True)
        self.txtImageFolder.setObjectName("txtImageFolder")
        self.gridLayout.addWidget(self.txtImageFolder, 1, 1, 1, 1)
        self.btnImageFolder = QtWidgets.QPushButton(self.widget, clicked= lambda: self.getImageFolder("Select image folder"))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnImageFolder.setFont(font)
        self.btnImageFolder.setObjectName("btnImageFolder")
        self.gridLayout.addWidget(self.btnImageFolder, 1, 2, 1, 1)
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
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.txtCategories = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtCategories.setFont(font)
        self.txtCategories.setReadOnly(True)
        self.txtCategories.setObjectName("txtCategories")
        self.gridLayout.addWidget(self.txtCategories, 2, 1, 1, 1)
        self.btnCategoryTxt = QtWidgets.QPushButton(self.widget, clicked = lambda: self.getCategoriseTxt("Open txt file","Text files (*.txt)"))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCategoryTxt.setFont(font)
        icon = QtGui.QIcon.fromTheme("folder")
        self.btnCategoryTxt.setIcon(icon)
        self.btnCategoryTxt.setObjectName("btnCategoryTxt")
        self.gridLayout.addWidget(self.btnCategoryTxt, 2, 2, 1, 1)
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
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.txtSubprocessNumber = QtWidgets.QLineEdit(self.widget)
        self.txtSubprocessNumber.setValidator(QIntValidator(0, 999))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtSubprocessNumber.setFont(font)
        self.txtSubprocessNumber.setObjectName("txtSubprocessNumber")
        self.gridLayout.addWidget(self.txtSubprocessNumber, 3, 1, 1, 1)
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
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.txtLinesToRead = QtWidgets.QLineEdit(self.widget)
        self.txtLinesToRead.setValidator(QIntValidator(0, 999))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtLinesToRead.setFont(font)
        self.txtLinesToRead.setObjectName("txtLinesToRead")
        self.gridLayout.addWidget(self.txtLinesToRead, 4, 1, 1, 1)
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
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.txtAccPercentage = QtWidgets.QLineEdit(self.widget)
        self.txtAccPercentage.setValidator(QIntValidator(0, 999))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtAccPercentage.setFont(font)
        self.txtAccPercentage.setObjectName("txtAccPercentage")
        self.gridLayout.addWidget(self.txtAccPercentage, 5, 1, 1, 1)
        self.txtProcessing = QtWidgets.QLineEdit(self.centralwidget)
        self.txtProcessing.setGeometry(QtCore.QRect(290, 250, 481, 25))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtProcessing.setFont(font)
        self.txtProcessing.setReadOnly(True)
        self.txtProcessing.setPlaceholderText("")
        self.txtProcessing.setObjectName("txtProcessing")
        self.txtProcessing.hide()
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
        self.btnGoogleJson.setText(_translate("MainWindow", "..."))
        self.label_3.setText(_translate("MainWindow", "Image folder path"))
        self.txtImageFolder.setPlaceholderText(_translate("MainWindow", "Path to images to be categorised"))
        self.btnImageFolder.setText(_translate("MainWindow", "..."))
        self.label_2.setText(_translate("MainWindow", "Categories text file path"))
        self.txtCategories.setPlaceholderText(_translate("MainWindow", "Path to text file that stores categories"))
        self.btnCategoryTxt.setText(_translate("MainWindow", "..."))
        self.label_4.setText(_translate("MainWindow", "Subprocess number"))
        self.txtSubprocessNumber.setPlaceholderText(_translate("MainWindow", "Number of sub-processes, determines the speed of categorisation"))
        self.label_5.setText(_translate("MainWindow", "Lines to read"))
        self.txtLinesToRead.setPlaceholderText(_translate("MainWindow", "Number of lines to read from OCR data and compare to category, put 0 to read all"))
        self.label_6.setText(_translate("MainWindow", "Accuracy Percentage"))
        self.txtAccPercentage.setPlaceholderText(_translate("MainWindow", "How accurate the OCR data need to be in compare to the category, decides accuracy of the result"))


    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
