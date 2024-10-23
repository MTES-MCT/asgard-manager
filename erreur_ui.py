# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT-Mer/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020 

import os.path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from . import bibli_asgard
from .bibli_asgard import *

class Ui_Dialog(object):
    def setupUi(self, Dialog, mTypeErreur, zMessError_Erreur):
        self.zMessError_Erreur = zMessError_Erreur
        self.mTypeErreur = mTypeErreur
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,520,350).size()).expandedTo(Dialog.minimumSizeHint()))
        iconSource = bibli_asgard.getThemeIcon("asgard2.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        #----------
        self.labelImage = QtWidgets.QLabel(Dialog)
        if self.mTypeErreur == "ASGARDGEREE" :
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\erreur_normale_asgard.png"
        elif self.mTypeErreur == "ASGARDNONGEREE" :
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\erreur_asgard_non_geree.png"
        elif self.mTypeErreur == "ASGARDMANAGER" :
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\erreur_asgard_manager.png"
        else :
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\erreur_normale_asgard.png"
        myDefPath = myPath.replace("\\","/");
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        self.labelImage.setGeometry(QtCore.QRect(20, 0, 100, 100))
        self.labelImage.setObjectName("labelImage")
        #----------
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(100, 30, 430, 30))
        self.label_2.setAlignment(Qt.AlignLeft)        
        font = QtGui.QFont()
        font.setPointSize(12) 
        font.setWeight(50) 
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        #----------
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        palette = QtGui.QPalette()
        #----------
        brush = QtGui.QBrush(QtGui.QColor(0,0,0,0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive,QtGui.QPalette.Base,brush)
        brush = QtGui.QBrush(QtGui.QColor(255,255,255))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled,QtGui.QPalette.Base,brush)
        #----------
        self.textEdit.setPalette(palette)
        self.textEdit.setAutoFillBackground(True)
        self.textEdit.width = 410
        self.textEdit.height = 150
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.textEdit.setGeometry(QtCore.QRect(10, 90, 500, 150))
        #----------
        self.labelRedmine = QtWidgets.QTextBrowser(Dialog)
        self.labelRedmine.setGeometry(QtCore.QRect(15, int( Dialog.height() ) - 30, 500, 25))
        self.labelRedmine.setAlignment(Qt.AlignLeft)        
        self.labelRedmine.setObjectName("labelRedmine")
        self.labelRedmine.setStyleSheet("QTextBrowser {   \
                                border-width: 0px;       \
                                background-color: transparent;      \
                                }") 
        self.labelRedmineTitre = QtWidgets.QLabel(Dialog)
        self.labelRedmineTitre.setGeometry(QtCore.QRect(20, int( Dialog.height() ) - 50, 440, 30))
        self.labelRedmineTitre.setAlignment(Qt.AlignLeft)        
        self.labelRedmineTitre.setObjectName("labelRedmineTitre")
        self.labelRedmineTitre.setStyleSheet("QLabel { color: #958B62; font : bold; }") 
        #----------
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QtCore.QRect(250, 260, 100, 25))
        self.pushButton.clicked.connect(Dialog.reject)
        #----------
        self.retranslateUi(Dialog)

    def retranslateUi(self, Dialog):
        mMessErreurAsgardManager =  QtWidgets.QApplication.translate("erreur_ui", "AsgardManager has encountered an error.", None)
        mMessErreurAsgardGere    =  QtWidgets.QApplication.translate("erreur_ui", "Operation prohibited.", None)
        mMessErreurAsgardNonGere =  QtWidgets.QApplication.translate("erreur_ui", "ASGARD has encountered an error.", None)
        mMessErreur = mMessErreurAsgardGere
        #mMessRedAsgardManager =  "https://qgis.projets.developpement-durable.gouv.fr/projects/asgardmanager"
        #mMessRedAsgardGere    =  "https://qgis.projets.developpement-durable.gouv.fr/projects/asgard"
        #mMessRedAsgardNonGere =  "https://qgis.projets.developpement-durable.gouv.fr/projects/asgard"
        mMessRedAsgardManager =  "https://portail-support.din.developpement-durable.gouv.fr/projects/assistance-produits-geomatiques"        
        mMessRedAsgardGere    =  "https://portail-support.din.developpement-durable.gouv.fr/projects/assistance-produits-geomatiques"        
        mMessRedAsgardNonGere =  "https://portail-support.din.developpement-durable.gouv.fr/projects/assistance-produits-geomatiques"        
        if self.mTypeErreur == "ASGARDGEREE" :
           mMessErreur = mMessErreurAsgardGere
           mMessRed    = mMessRedAsgardGere
           mMessRedTitre = "Redmine ASGARD"
        elif self.mTypeErreur == "ASGARDNONGEREE" :
           mMessErreur = mMessErreurAsgardNonGere
           mMessRed    = mMessRedAsgardNonGere
           mMessRedTitre = "Redmine ASGARD"
        elif self.mTypeErreur == "ASGARDMANAGER" :
           mMessErreur = mMessErreurAsgardManager
           mMessRed    = mMessRedAsgardManager
           mMessRedTitre = "Redmine AsgardManager"
        else :
           mMessErreur = mMessErreurAsgardManager =  QtWidgets.QApplication.translate("erreur_ui", "Unreported errors", None)
           mMessRed    = mMessRedAsgardGere
           mMessRed    = mMessRedAsgardGere
           mMessRedTitre = "Redmine ASGARD"
        #----------
        MonHtml = ""
        MonHtml += "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        MonHtml += "p, li { white-space: pre-wrap; }\n"
        MonHtml += "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:8pt; font-weight:400; font-style:normal;\">\n"
        MonHtml += "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\'; font-size:8pt;\"><span style=\" font-weight:600;\">"
        MonHtml1 = ''
        MonHtml1 += "<br>"
        MonHtml += MonHtml1
        MonHtml += "</span>" 
        MonHtml2 = "<br>"
        MonHtml2 += self.zMessError_Erreur
        MonHtml += MonHtml2
        MonHtml += "</i></p></body></html>"
        Dialog.setWindowTitle("ASGARD Manager - (" + str(bibli_asgard.returnVersion()) + ")")
        self.textEdit.setHtml(QtWidgets.QApplication.translate("erreur_ui", MonHtml, None))
        self.label_2.setText(QtWidgets.QApplication.translate("erreur_ui", mMessErreur, None))
        if self.mTypeErreur != "ASGARDGEREE" :
           self.labelRedmineTitre.setText('Redmine')
           mLibelle = QtWidgets.QApplication.translate("erreur_ui", "To help improve the tool, report this anomaly to us on the ", None) 
           mLink = '<a href=\"' + mMessRed + '\">' + mLibelle + " " + mMessRedTitre + '</a>'
           self.labelRedmine.setText(mLink)
           self.labelRedmine.setOpenExternalLinks(True)       
        self.pushButton.setText(QtWidgets.QApplication.translate("erreur_ui", "OK", None))
                                                    
