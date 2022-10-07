from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QMessageBox,QFileDialog
from PyQt6.QtCore import QObject, QThread, pyqtSignal

import image_categorisation_powered_by_OCR
from validation import validator
from OCRWindow import Ui_OCRWindow
from advanceSettings import Ui_AdvanceSettings
from backend.folder_processes import folder_processes
from functools import partial


class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(int,int)
    errormessage = pyqtSignal(str)
    
    def alertMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
    def categorise(self,ui,lines_to_read,acc_percentage):
        
        image_categorisation_powered_by_OCR.os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = ui.txtGoogleCredential.text()
        image_folder = ui.txtImageFolder.text()
        categories_txtfile = ui.txtCategories.text()
        subProcessNumber = int(ui.txtSubprocessNumber.text())
        lines_to_read = lines_to_read
        accuracy_percentage = acc_percentage
        print(lines_to_read)
        print(accuracy_percentage)
        error=image_categorisation_powered_by_OCR.comparison.multiprocessing_image_categorisation(image_folder,subProcessNumber,categories_txtfile,lines_to_read,accuracy_percentage,self.progress)
        
        if error:
            raise error
        

    def run(self,ui,lines_to_read,acc_percentage):
        """Long-running task."""
        try:
            
            self.categorise(ui,lines_to_read,acc_percentage)
            self.finished.emit() 
        except Exception as e:
            self.errormessage.emit(str(e))
            



class Ui_MainWindow(object):
    lines_to_read = 0
    acc_percentage = 75
        
    def openAdvanceSettings(self):

        if int(self.ui.txtLinesToRead.text()) !=0:
                self.lines_to_read = int(self.ui.txtLinesToRead.text())
        if int(self.ui.txtAccPercentage.text()) !=75:
            self.acc_percentage = int(self.ui.txtAccPercentage.text())
        self.window.show()
        MainWindow.hide()
        
    def openOCRWindow(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_OCRWindow()
        self.ui.setupUi(self.window,MainWindow)
        self.ui.txtGoogleCredential_2.setText(self.txtGoogleCredential.text())
        self.window.show()
        MainWindow.hide()
        
    def validate(self):
        flag = True
        if not (self.txtGoogleCredential.text() and self.txtImageFolder.text() and self.txtCategories.text() and self.txtSubprocessNumber.text()):
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
            self.alertMessage("No image in folder path provided!")
            flag = False
        elif not validator.chkIfIstxtFile(self.txtCategories.text()):
            self.alertMessage("Category text file path does not lead to a text file!")
            flag = False
        elif not validator.validateCategories_txt(self.txtCategories.text()):
            self.alertMessage("Category text file is empty!")
            flag = False
        elif int(self.txtSubprocessNumber.text())<1:
            self.alertMessage("Please make sure subprocess number is larger than 1!")
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

            
            self.thread.started.connect(partial(self.worker.run,self,int(self.ui.txtLinesToRead.text()),int(self.ui.txtAccPercentage.text())))
            self.worker.errormessage.connect(self.erroralert)
            self.worker.errormessage.connect(self.thread.quit)
            self.worker.errormessage.connect(self.worker.deleteLater)
            self.worker.progress.connect(self.loading)
            self.worker.finished.connect(self.thread.quit)
            self.worker.finished.connect(self.worker.deleteLater)
            self.worker.finished.connect(self.alldone)
            self.thread.finished.connect(self.thread.deleteLater)
            
            
            
            # Step 6: Start the thread
            self.thread.start()

            # Final resets
            self.btnCategorise.setEnabled(False)
            self.btnCategoryTxt.setEnabled(False)
            self.btnGoogleJson.setEnabled(False)
            self.btnImageFolder.setEnabled(False)
            self.txtSubprocessNumber.setEnabled(False)

            
            self.thread.finished.connect(
                self.progressBar.hide
            ) 
            self.thread.finished.connect(
                self.lblProgress.hide
            )  
            self.thread.finished.connect(
                self.enableUI
            )
            
            
    def loading(self,current,total):
        self.progressBar.show()
        self.progressBar.setRange(0,total)
        self.progressBar.setValue(current)
        self.lblProgress.show()
        self.lblProgress.setText("Image categorising, "+str(current)+"/"+str(total)+" batches is categorised.")
        
    def erroralert(self,message):
        self.alertMessage(message)
    def alldone(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setText("All image categorised")
        msg.setWindowTitle("All done!")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()   
          
    def enableUI(self):
        self.btnCategorise.setEnabled(True)
        self.btnCategoryTxt.setEnabled(True)
        self.btnGoogleJson.setEnabled(True)
        self.btnImageFolder.setEnabled(True)
        self.txtSubprocessNumber.setEnabled(True)

        
    def alertMessage(self,message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        retval = msg.exec()
            
    def recordData(self):
        datalist = [self.txtGoogleCredential.text(), self.txtImageFolder.text(), self.txtCategories.text(), self.txtSubprocessNumber.text()]
        folder_processes.writeToFile("data.txt",datalist)
        
    def readData(self):
        try:
            datalist = folder_processes.get_all_categories("data.txt")
            self.txtGoogleCredential.setText(datalist[0])
            self.txtImageFolder.setText(datalist[1])
            self.txtCategories.setText(datalist[2])
            self.txtSubprocessNumber.setText(datalist[3])
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
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 1051, 188))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
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
        self.btnGoogleJson = QtWidgets.QPushButton(self.layoutWidget, clicked= lambda: self.getGoogleCredentialJson("Select Google credential json file","Json file (*.json)"))
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
        self.txtGoogleCredential = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtGoogleCredential.setFont(font)
        self.txtGoogleCredential.setReadOnly(True)
        self.txtGoogleCredential.setObjectName("txtGoogleCredential")
        self.gridLayout.addWidget(self.txtGoogleCredential, 0, 1, 1, 1)
        self.txtImageFolder = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtImageFolder.setFont(font)
        self.txtImageFolder.setReadOnly(True)
        self.txtImageFolder.setObjectName("txtImageFolder")
        self.gridLayout.addWidget(self.txtImageFolder, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
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
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
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
        self.btnImageFolder = QtWidgets.QPushButton(self.layoutWidget, clicked= lambda: self.getImageFolder("Select image folder"))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnImageFolder.setFont(font)
        self.btnImageFolder.setObjectName("btnImageFolder")
        self.gridLayout.addWidget(self.btnImageFolder, 1, 2, 1, 1)
        self.txtCategories = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtCategories.setFont(font)
        self.txtCategories.setReadOnly(True)
        self.txtCategories.setObjectName("txtCategories")
        self.gridLayout.addWidget(self.txtCategories, 2, 1, 1, 1)
        self.btnCategoryTxt = QtWidgets.QPushButton(self.layoutWidget, clicked = lambda: self.getCategoriseTxt("Open txt file","Text files (*.txt)"))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCategoryTxt.setFont(font)
        icon = QtGui.QIcon.fromTheme("folder")
        self.btnCategoryTxt.setIcon(icon)
        self.btnCategoryTxt.setObjectName("btnCategoryTxt")
        self.gridLayout.addWidget(self.btnCategoryTxt, 2, 2, 1, 1)
        self.txtSubprocessNumber = QtWidgets.QLineEdit(self.layoutWidget)
        self.txtSubprocessNumber.setValidator(QIntValidator(0, 999))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtSubprocessNumber.setFont(font)
        self.txtSubprocessNumber.setObjectName("txtSubprocessNumber")
        self.gridLayout.addWidget(self.txtSubprocessNumber, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.layoutWidget)
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
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(250, 250, 601, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.hide()
        self.lblProgress = QtWidgets.QLabel(self.centralwidget)
        self.lblProgress.setEnabled(True)
        self.lblProgress.setGeometry(QtCore.QRect(245, 280, 601, 25))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblProgress.sizePolicy().hasHeightForWidth())
        self.lblProgress.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lblProgress.setFont(font)
        self.lblProgress.setText("")
        self.lblProgress.setWordWrap(True)
        self.lblProgress.setObjectName("lblProgress")
        self.btnAdvanceSettings = QtWidgets.QPushButton(self.centralwidget, clicked = lambda:self.openAdvanceSettings())
        self.btnAdvanceSettings.setGeometry(QtCore.QRect(870, 210, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnAdvanceSettings.setFont(font)
        icon = QtGui.QIcon.fromTheme("folder")
        self.btnAdvanceSettings.setIcon(icon)
        self.btnAdvanceSettings.setObjectName("btnCategoryTxt_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)


        self.txtGoogleCredential.setDisabled(True)
        self.txtImageFolder.setDisabled(True)
        self.txtCategories.setDisabled(True)
        self.retranslateUi(MainWindow)
        self.readData()
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_AdvanceSettings()
        self.ui.setupUi(self.window,MainWindow)
        self.ui.txtLinesToRead.setText(str(self.lines_to_read))
        self.ui.txtAccPercentage.setText(str(self.acc_percentage))
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
        self.txtSubprocessNumber.setPlaceholderText(_translate("MainWindow", "Number of images to be processed at once, determines the speed of categorisation"))
        self.btnAdvanceSettings.setText(_translate("MainWindow", "Advance Settings"))
        

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
