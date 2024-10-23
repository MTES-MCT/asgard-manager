# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT-Mer/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020 

import os.path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from . import bibli_asgard
from .bibli_asgard import *

class Ui_Dialog(object):
    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,700,550).size()).expandedTo(Dialog.minimumSizeHint()))
        iconSource = bibli_asgard.getThemeIcon("asgard2.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)

        self.groupDialog = QtWidgets.QGroupBox(Dialog)
        self.groupDialog.setGeometry(QtCore.QRect(5, 5, int( Dialog.width() )-10,  int( Dialog.height() )-10))
        self.groupDialog.setObjectName("groupDialog")
        self.groupDialog.setStyleSheet("QGroupBox {border: 3px solid #958B62;}")
        
        self.label_2 = QtWidgets.QLabel(self.groupDialog)
        self.label_2.setGeometry(QtCore.QRect((int( self.groupDialog.width()/2 ) - 100), 5, 200, 30))
        self.label_2.setAlignment(Qt.AlignCenter)        
        font = QtGui.QFont()
        font.setPointSize(15) 
        font.setWeight(50) 
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        self.labelImage = QtWidgets.QLabel(self.groupDialog)
        myPath = os.path.dirname(__file__)+"\\icons\\logo\\logo.png"
        myDefPath = myPath.replace("\\","/");
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        self.labelImage.setGeometry(QtCore.QRect(10, 50, 266, 60))
        self.labelImage.setObjectName("labelImage")

        self.labelImage2 = QtWidgets.QLabel(self.groupDialog)
        myPath = os.path.dirname(__file__)+"\\icons\\logo\\logoabout.png";
        myDefPath = myPath.replace("\\","/");
        carIcon2 = QtGui.QImage(myDefPath)
        self.labelImage2.setPixmap(QtGui.QPixmap.fromImage(carIcon2))
        self.labelImage2.setGeometry(QtCore.QRect(int( self.groupDialog.width()/2 ) - 55, 40, int( self.groupDialog.width()/2 ) + 50, int( self.groupDialog.height() ) - 80))
        self.labelImage2.setObjectName("labelImage2")
        #self.labelImage2.setStyleSheet("QLabel {border: 3px solid #958B62;}")

        self.textEdit = QtWidgets.QTextEdit(self.groupDialog)
        palette = QtGui.QPalette()

        brush = QtGui.QBrush(QtGui.QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)

        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)
        self.textEdit.setPalette(palette)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.width = 300
        self.textEdit.height = 100
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.textEdit.setGeometry(QtCore.QRect(10, 120, 280, 360))

        self.pushButton = QtWidgets.QPushButton(self.groupDialog)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QtCore.QRect(410, int( self.groupDialog.height() ) - 35, 100, 25))
        self.pushButton.clicked.connect(Dialog.reject)

        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        MonHtml = ""
        MonHtml += "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        MonHtml += "p, li { white-space: pre-wrap; }\n"
        MonHtml += "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
        MonHtml += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-weight:600;\">"
        mVERSION = " = version 1.6"
        MonHtml1 = QtWidgets.QApplication.translate("about", "ASGARD Manager", None) + "  (" + str(bibli_asgard.returnVersion()) + ")"
        MonHtml += MonHtml1
        MonHtml += "</span>" 
        MonHtml2 = "<br><br>"
        MonHtml2 += QtWidgets.QApplication.translate("about", "A tool dedicated to ADL and / or ADL delegates, Asgard Manager was developed to allow IG departments of the ministry, which do not have strong skills under the PostGreSQL environment, to exploit the features of the Asgard extension.", None)
        MonHtml2 += "<br><br>"
        MonHtml2 += QtWidgets.QApplication.translate("about", "Asgard Manager encapsulates the instructions or functionality of the Asgard extension and PostGreSQL SQL language", None)
        MonHtml += MonHtml2
        MonHtml += "<br><br>"
        MonHtml3 = QtWidgets.QApplication.translate("about", "Representation of functional blocks, diagrams, objects, roles of groups and connections with dedicated iconography and graphic statistical analyzes.", None) 
        MonHtml += MonHtml3
        MonHtml += "</b><br>"
        MonHtml += "</p></td></tr></table>"
        MonHtml += "<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p>\n"
        MonHtml += "<p style=\"margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">"
        MonHtml += "<font color='#0000FF'><b><u>" + QtWidgets.QApplication.translate("about", "Designer/Developer Didier LECLERC", None) + "</u></b></font><br><br>"
        MonHtml += "<font color='#0000FF'><b><u>" + QtWidgets.QApplication.translate("about", "functional analysis Leslie LEMAIRE", None) + "</u></b></font><br><br>"
        MonHtml += "<b>"
        MonHtml4 = QtWidgets.QApplication.translate("about", "MTE / MCTRCT / Mer", None) 
        MonHtml += MonHtml4
        MonHtml += "</b><br><b>"
        MonHtml5 = QtWidgets.QApplication.translate("about", "digital service", None) 
        MonHtml += MonHtml5
        MonHtml += "</b><br>"
        MonHtml6 = QtWidgets.QApplication.translate("about", "digital service SG/SNUM/UNI/DRC", None) 
        MonHtml += MonHtml6
        MonHtml += "<br><br><i>"
        MonHtml7 = QtWidgets.QApplication.translate("about", "Development in 2020/2021", None) 
        MonHtml += MonHtml7
        MonHtml += "</i></p></body></html>"

        Dialog.setWindowTitle(QtWidgets.QApplication.translate("about", "ASGARD Manager - Automatic and Simplified GrAnting for Rights in Databases", None) + "  (" + str(bibli_asgard.returnVersion()) + ")")
        self.label_2.setText(QtWidgets.QApplication.translate("about", "ASGARD Manager", None))
        self.textEdit.setHtml(QtWidgets.QApplication.translate("about", MonHtml, None))
        self.pushButton.setText(QtWidgets.QApplication.translate("about", "OK", None))
