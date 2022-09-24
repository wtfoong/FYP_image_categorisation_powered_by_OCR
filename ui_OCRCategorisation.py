# Form implementation generated from reading ui file 'c:\Users\rainy\OneDrive - Asia Pacific University\FYP\fypSystem\OCRCategorisation.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1081, 353)
        MainWindow.setAutoFillBackground(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.btnOCRWindow = QtWidgets.QPushButton(self.centralwidget)
        self.btnOCRWindow.setGeometry(QtCore.QRect(20, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnOCRWindow.setFont(font)
        self.btnOCRWindow.setObjectName("btnOCRWindow")
        self.btnCategorise = QtWidgets.QPushButton(self.centralwidget)
        self.btnCategorise.setGeometry(QtCore.QRect(870, 250, 141, 61))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCategorise.setFont(font)
        self.btnCategorise.setObjectName("btnCategorise")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(14, 33, 1051, 188))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
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
        self.txtGoogleCredential = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtGoogleCredential.setFont(font)
        self.txtGoogleCredential.setReadOnly(True)
        self.txtGoogleCredential.setObjectName("txtGoogleCredential")
        self.gridLayout.addWidget(self.txtGoogleCredential, 0, 1, 1, 1)
        self.btnGoogleJson = QtWidgets.QPushButton(self.layoutWidget)
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
        self.txtImageFolder = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtImageFolder.setFont(font)
        self.txtImageFolder.setReadOnly(True)
        self.txtImageFolder.setObjectName("txtImageFolder")
        self.gridLayout.addWidget(self.txtImageFolder, 1, 1, 1, 1)
        self.btnImageFolder = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnImageFolder.setFont(font)
        self.btnImageFolder.setObjectName("btnImageFolder")
        self.gridLayout.addWidget(self.btnImageFolder, 1, 2, 1, 1)
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
        self.txtCategories = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtCategories.setFont(font)
        self.txtCategories.setReadOnly(True)
        self.txtCategories.setObjectName("txtCategories")
        self.gridLayout.addWidget(self.txtCategories, 2, 1, 1, 1)
        self.btnCategoryTxt = QtWidgets.QPushButton(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnCategoryTxt.setFont(font)
        icon = QtGui.QIcon.fromTheme("folder")
        self.btnCategoryTxt.setIcon(icon)
        self.btnCategoryTxt.setObjectName("btnCategoryTxt")
        self.gridLayout.addWidget(self.btnCategoryTxt, 2, 2, 1, 1)
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
        self.txtSubprocessNumber = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtSubprocessNumber.setFont(font)
        self.txtSubprocessNumber.setObjectName("txtSubprocessNumber")
        self.gridLayout.addWidget(self.txtSubprocessNumber, 3, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.layoutWidget)
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
        self.txtLinesToRead = QtWidgets.QLineEdit(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.txtLinesToRead.setFont(font)
        self.txtLinesToRead.setObjectName("txtLinesToRead")
        self.gridLayout.addWidget(self.txtLinesToRead, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.layoutWidget)
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
        self.txtAccPercentage = QtWidgets.QLineEdit(self.layoutWidget)
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
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
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
        self.txtLinesToRead.setPlaceholderText(_translate("MainWindow", "Number of lines to read from OCR data and compare to category, leave blank to read all"))
        self.label_6.setText(_translate("MainWindow", "Accuracy Percentage"))
        self.txtAccPercentage.setPlaceholderText(_translate("MainWindow", "How accurate the OCR data need to be in compare to the category, decides accuracy of the result"))
