from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox,QFileDialog
from validation import validator

import image_categorisation_powered_by_OCR as imgc


class Ui_OCRWindow(object):
    def backToCategorise(self,main_w,OCRWindow):
        main_w.show()
        OCRWindow.hide()
        
    def ocrImage(self):
       imgc.os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = self.txtGoogleCredential_2.text()
       try:
            if imgc.comparison.detect_text(self.txtImage.text()):
                    OCRResult = "\n".join([str(x) for x in imgc.comparison.detect_text(self.txtImage.text())])
            else:
                OCRResult = "No Text in image!"
            self.txtAOCRResult.setText(OCRResult)
       except Exception as e:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText(str(e))
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            retval = msg.exec()
       
    def validate(self):
        flag = True
        if not (self.txtGoogleCredential_2.text() and self.txtImage.text()):
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Please fill up all fields!")
            msg.setWindowTitle("Error")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            retval = msg.exec()
            flag = False
        elif not validator.validatePath(self.txtImage.text(),"Image file path is not valid or the image does not exist!"):
            flag = False
       
        if flag:
            self.ocrImage()
        
    def openFile(self,message,rule,path):
        file = QFileDialog.getOpenFileName(None,message, path, rule)
        return file
    
    def getGoogleCredentialJson(self,message,rule):
        file = self.openFile(message,rule,self.txtGoogleCredential_2.text())
        self.txtGoogleCredential_2.setText(file[0])
    
    def getImageFile(self,message,rule):
        file = self.openFile(message,rule,self.txtImage.text())
        self.txtImage.setText(file[0])
        
    def setupUi(self, OCRWindow, MainWindow):
        OCRWindow.setObjectName("OCRWindow")
        OCRWindow.setFixedSize(1078, 350)
        OCRWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QtWidgets.QWidget(OCRWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnBack = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.backToCategorise(MainWindow,OCRWindow))
        self.btnBack.setGeometry(QtCore.QRect(880, 140, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnBack.setFont(font)
        self.btnBack.setObjectName("btnBack")
        self.btnOCR = QtWidgets.QPushButton(self.centralwidget, clicked = lambda: self.validate())
        self.btnOCR.setGeometry(QtCore.QRect(880, 230, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnOCR.setFont(font)
        self.btnOCR.setObjectName("btnOCR")
        self.txtAOCRResult = QtWidgets.QTextEdit(self.centralwidget)
        self.txtAOCRResult.setGeometry(QtCore.QRect(10, 140, 831, 181))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtAOCRResult.setFont(font)
        self.txtAOCRResult.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.txtAOCRResult.setObjectName("txtAOCRResult")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(11, 31, 1051, 62))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 0, 0, 1, 1)
        self.txtGoogleCredential_2 = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtGoogleCredential_2.setFont(font)
        self.txtGoogleCredential_2.setReadOnly(True)
        self.txtGoogleCredential_2.setObjectName("txtGoogleCredential_2")
        self.txtGoogleCredential_2.setEnabled(False)
        self.gridLayout.addWidget(self.txtGoogleCredential_2, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.txtImage = QtWidgets.QLineEdit(self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtImage.setFont(font)
        self.txtImage.setReadOnly(True)
        self.txtImage.setObjectName("txtImage")
        self.txtImage.setEnabled(False)
        self.gridLayout.addWidget(self.txtImage, 1, 1, 1, 1)
        self.btnImageFile = QtWidgets.QPushButton(self.widget, clicked= lambda: self.getImageFile("Select image","Image file (*.png *.jpg *.gif *.jpeg)"))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnImageFile.sizePolicy().hasHeightForWidth())
        self.btnImageFile.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnImageFile.setFont(font)
        self.btnImageFile.setObjectName("btnImageFile")
        self.gridLayout.addWidget(self.btnImageFile, 1, 2, 1, 1)
        self.btnGoogleJson = QtWidgets.QPushButton(self.widget, clicked= lambda: self.getGoogleCredentialJson("Select Google credential json file","Json file (*.json)") )
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
        OCRWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(OCRWindow)
        QtCore.QMetaObject.connectSlotsByName(OCRWindow)

    def retranslateUi(self, OCRWindow):
        _translate = QtCore.QCoreApplication.translate
        OCRWindow.setWindowTitle(_translate("OCRWindow", "OCR Window"))
        self.btnBack.setText(_translate("OCRWindow", "Back"))
        self.btnOCR.setText(_translate("OCRWindow", "OCR"))
        self.label_7.setText(_translate("OCRWindow", "Google Credential json file path"))
        self.txtGoogleCredential_2.setPlaceholderText(_translate("OCRWindow", "File path to google credential json file"))
        self.label_8.setText(_translate("OCRWindow", "Image path"))
        self.txtImage.setPlaceholderText(_translate("OCRWindow", "Path to images to be OCR, currently only supports .png, .jpg, .gif, and .jpeg "))
        self.btnImageFile.setText(_translate("OCRWindow", "..."))
        self.btnGoogleJson.setText(_translate("OCRWindow", "..."))


    
        
    


# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     OCRWindow = QtWidgets.QMainWindow()
#     ui = Ui_OCRWindow()
#     ui.setupUi(OCRWindow)
#     OCRWindow.show()
#     sys.exit(app.exec())
