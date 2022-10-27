# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5 import QtCore, QtGui, QtWidgets, QtQuick 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QAction, QMenu , QMenuBar, QApplication, QMessageBox, QFileDialog, QPlainTextEdit, QDialog, QDockWidget, QVBoxLayout, QTabWidget, QWidget, QDesktopWidget, QSizePolicy
from PyQt5.QtGui import QIcon, QStandardItem, QStandardItemModel
from PyQt5.QtQuick import QQuickItem, QQuickPaintedItem, QQuickView

from . import doabout
from . import bibli_asgard
from .bibli_asgard import *
from . import bibli_ihm_asgard
from .bibli_ihm_asgard import *                                                                        
from . import bibli_graph_asgard
from .bibli_graph_asgard import *
from . import doconfirme

from qgis.core import *
from qgis.gui import *
from qgis.PyQt.QtCore import QUrl

import qgis  
import os
import subprocess
import time
import sys

class Ui_Dialog_Asgard(object):
    def __init__(self):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True) #enable highdpi scaling
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True) #use highdpi icons
        self.iface = qgis.utils.iface
        self.firstOpen = True
        self.firstOpenConnect = True
    
    def setupUi(self, Dialog):
        self.Dialog = Dialog
        Dialog.setObjectName("Dialog")
        #--------
        mDic_LH = bibli_asgard.returnAndSaveDialogParam(self, "Load")
        self.mDic_LH = mDic_LH
        self.lScreenDialog, self.hScreenDialog = int(mDic_LH["dialogLargeur"]), int(mDic_LH["dialogHauteur"])
        self.dashBoard       = mDic_LH["dashBoard"]     #Onglet dashBord
        self.displayMessage  = False if mDic_LH["displayMessage"] == 'dialogTitle' else True #Qmessage box (dialogBox) ou barre de progression (dialogTitle)
        self.arboObjet       = False if mDic_LH["arboObjet"] != 'true' else True     #Arborescence des objets dans le treeview schéma
        self.fileHelp        = mDic_LH["fileHelp"]      #Type Fichier Help
        self.fileHelpPdf     = mDic_LH["fileHelpPdf"]   #Fichier Help  PDF
        self.fileHelpHtml    = mDic_LH["fileHelpHtml"]  #Fichier Help  HTML
        self.durationBarInfo = int(mDic_LH["durationBarInfo"])  #durée d'affichage des messages d'information
        #--------
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,self.lScreenDialog, self.hScreenDialog).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setWindowTitle("ASGARD Automatic and Simplified GrAnting for Rights in Databases")
        Dialog.setWindowModality(Qt.WindowModal)
        Dialog.setWindowFlags(Qt.WindowMaximizeButtonHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        iconSource = bibli_asgard.getThemeIcon("asgard2.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        #==========================         
        self.mSectionGauche = 0.25   # Pourcentage de la partie gauche des rôles et groupes
        #==========================
        #Affiche info si MAJ version
        self.barInfo = QgsMessageBar(self)
        self.barInfo.setSizePolicy( QSizePolicy.Minimum, QSizePolicy.Fixed )
        self.barInfo.setGeometry(220, 0, Dialog.width()-230, 25)
        #=====================================================
        #Path Icon
        myPathIcon = os.path.dirname(__file__)+"\\icons\\"
        self.myPathIcon = myPathIcon.replace("\\","/")

        #=====================================================  
        #=====================================================  
        #Menu Dialog
        iconReinitAllSchemas  = returnIcon(myPathIcon + "\\actions\\reinitialise_droits.png")
        iconDiagnosticAsgard  = returnIcon(myPathIcon + "\\actions\\diagnostic.png")
        iconMembreGconsult  = returnIcon(myPathIcon + "\\actions\\gconsult_roles.png")
        iconTableauBord  = returnIcon(myPathIcon + "\\actions\\tableaubord.png")
        iconNettoieRoles  = returnIcon(myPathIcon + "\\actions\\nettoyage_roles.png")
        iconReferencerAllSchemas  = returnIcon(myPathIcon + "\\actions\\referencerconservedroits.png")
        iconImportNomenclature  = returnIcon(myPathIcon + "\\actions\\nomenclature.png")
        iconInstallerAsgard  = returnIcon(myPathIcon + "\\actions\\installe_asgard.png")
        iconMajAsgard  = returnIcon(myPathIcon + "\\actions\\maj_asgard.png")
        iconDesinstallerAsgard  = returnIcon(myPathIcon + "\\actions\\desinstalle_asgard.png")
        iconInstallerPlume  = returnIcon(myPathIcon + "\\actions\\installe_plume.png")
        iconMajPlume  = returnIcon(myPathIcon + "\\actions\\maj_plume.png")
        iconDesinstallerPlume  = returnIcon(myPathIcon + "\\actions\\desinstalle_plume.png")
        iconReloadAM  = returnIcon(myPathIcon + "\\actions\\reload.png")
        
        self.mMenuBarDialog = QMenuBar(self)
        self.mMenuDialog = QMenu(self)
        self.mMenuBarDialog.addMenu(self.mMenuDialog)
        self.mMenuDialog.setTitle(QtWidgets.QApplication.translate("asgard_general_ui", "Settings"))
        #---
        self.mMenuParam = QMenu(self)
        self.mMenuBarDialog.addMenu(self.mMenuParam)
        self.mMenuParam.setTitle(QtWidgets.QApplication.translate("asgard_general_ui", "ParamSettings"))
        #---
        self.paramArbo = QAction("Object tree grouping ",Dialog)
        self.paramArbo.setCheckable(True) 
        self.paramArbo.setChecked(self.arboObjet)     #Arborescence des objets dans le treeview schéma
        self.paramArbo.setText(QtWidgets.QApplication.translate("asgard_main", "Object tree grouping "))
        self.mMenuParam.addAction(self.paramArbo)
        #-
        self.mMenuParam.addSeparator()
        #-
        self.paramDisplayMessage = QAction("Object tree grouping ",Dialog)
        self.paramDisplayMessage.setCheckable(True) 
        self.paramDisplayMessage.setChecked(self.displayMessage)      #Qmessage box (dialogBox) ou barre de progression (dialogTitle)
        self.paramDisplayMessage.setText(QtWidgets.QApplication.translate("asgard_main", "Dialog box for information messages"))
        self.mMenuParam.addAction(self.paramDisplayMessage)
        #---
        self.aboutMenuDialog = QAction("?",Dialog)
        self.mMenuBarDialog.addAction(self.aboutMenuDialog)
        #------------
        self.reinitAllSchemas = QAction(QIcon(iconReinitAllSchemas),"Reset all rights",Dialog)
        self.reinitAllSchemas.setText(QtWidgets.QApplication.translate("asgard_main", "Reset all rights"))
        self.mMenuDialog.addAction(self.reinitAllSchemas)
        #-
        self.diagnosticAsgard = QAction(QIcon(iconDiagnosticAsgard),"Find all anomalies",Dialog)
        self.diagnosticAsgard.setText(QtWidgets.QApplication.translate("asgard_main", "Find all anomalies"))
        self.mMenuDialog.addAction(self.diagnosticAsgard)
        #-
        self.nettoieRoles = QAction(QIcon(iconNettoieRoles),"Refresh the role names in the management table ",Dialog)
        self.nettoieRoles.setText(QtWidgets.QApplication.translate("asgard_main", "Refresh the role names in the management table "))
        self.mMenuDialog.addAction(self.nettoieRoles)
        #-
        self.mMenuDialog.addSeparator()
        #-
        self.tableauBord = QAction(QIcon(iconTableauBord),"Dashboard",Dialog)
        self.tableauBord.setText(QtWidgets.QApplication.translate("asgard_main", "Dashboard"))
        self.mMenuDialog.addAction(self.tableauBord)
        #-
        self.mMenuDialog.addSeparator()
        #-
        self.membreGconsult = QAction(QIcon(iconMembreGconsult),"Make all users members of g_consult",Dialog)
        self.membreGconsult.setText(QtWidgets.QApplication.translate("asgard_main", "Make all users members of g_consult"))
        self.mMenuDialog.addAction(self.membreGconsult)
        #-
        self.mMenuDialog.addSeparator()
        #-
        self.referencerAllSchemas = QAction(QIcon(iconReferencerAllSchemas),"Reference all the diagrams in the database",Dialog)
        self.referencerAllSchemas.setText(QtWidgets.QApplication.translate("asgard_main", "Reference all the diagrams in the database"))
        self.mMenuDialog.addAction(self.referencerAllSchemas)
        #-
        self.importNomenclature = QAction(QIcon(iconImportNomenclature),"Import or repair the national nomenclature",Dialog)
        self.importNomenclature.setText(QtWidgets.QApplication.translate("asgard_main", "Import or repair the national nomenclature"))
        self.mMenuDialog.addAction(self.importNomenclature)
        #-
        self.mMenuDialog.addSeparator()
        #-
        self.installerAsgard = QAction(QIcon(iconInstallerAsgard),"Install ASGARD on the base",Dialog)
        self.installerAsgard.setText(QtWidgets.QApplication.translate("asgard_main", "Install ASGARD on the base"))
        self.mMenuDialog.addAction(self.installerAsgard)
        #-
        self.majAsgard = QAction(QIcon(iconMajAsgard),"Update the ASGARD extension",Dialog)
        self.majAsgard.setText(QtWidgets.QApplication.translate("asgard_main", "Update the ASGARD extension"))
        self.mMenuDialog.addAction(self.majAsgard)
        #-
        self.desinstallerAsgard = QAction(QIcon(iconDesinstallerAsgard),"Uninstall the ASGARD extension",Dialog)
        self.desinstallerAsgard.setText(QtWidgets.QApplication.translate("asgard_main", "Uninstall the ASGARD extension"))
        self.mMenuDialog.addAction(self.desinstallerAsgard)
        #- For PLUME
        self.mMenuDialog.addSeparator()
        #-
        self.installerPlume = QAction(QIcon(iconInstallerPlume),"Install Plume on the base",Dialog)
        self.installerPlume.setText(QtWidgets.QApplication.translate("asgard_main", "Install Plume on the base"))
        self.mMenuDialog.addAction(self.installerPlume)
        #-
        self.majPlume = QAction(QIcon(iconMajPlume),"Update the Plume extension",Dialog)
        self.majPlume.setText(QtWidgets.QApplication.translate("asgard_main", "Update the Plume extension"))
        self.mMenuDialog.addAction(self.majPlume)
        #-
        self.desinstallerPlume = QAction(QIcon(iconDesinstallerPlume),"Uninstall the Plume extension",Dialog)
        self.desinstallerPlume.setText(QtWidgets.QApplication.translate("asgard_main", "Uninstall the Plume extension"))
        self.mMenuDialog.addAction(self.desinstallerPlume)
        #- Actions PLUME
        self.installerPlume.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONinstallerPlume', ''))
        self.majPlume.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONmajPlume', ''))
        self.desinstallerPlume.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONdesinstallerPlume', ''))
        #- For PLUME
        self.mMenuDialog.addSeparator()
        #- Actions
        self.reinitAllSchemas.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONreinitAllSchemasFunction', ''))
        self.diagnosticAsgard.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONdiagnosticAsgard', ''))
        self.membreGconsult.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONmembreGconsult', ''))
        self.nettoieRoles.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONnettoieRoles', ''))
        self.tableauBord.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONTableauBord', ''))
        self.referencerAllSchemas.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONreferencerAllSchemasFunction', ''))
        self.importNomenclature.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONimportNomenclature', ''))
        self.installerAsgard.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONinstallerAsgard', ''))
        self.majAsgard.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONmajAsgard', ''))
        self.desinstallerAsgard.triggered.connect(lambda : self.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'FONCTIONdesinstallerAsgard', ''))
        self.aboutMenuDialog.triggered.connect(self.clickAboutMenuDialog)
        self.paramArbo.triggered.connect(self.clickParamArbo)
        self.paramDisplayMessage.triggered.connect(self.clickParamDisplayMessage)
      
        self.mMenuDialog.addSeparator()
        #------------
        self.reloadAM = QAction(QIcon(iconReloadAM),"refresh",Dialog)
        libReloadAM = QtWidgets.QApplication.translate("asgard_main", "refresh")
        self.reloadAM.setText(libReloadAM)
        self.mMenuDialog.addAction(QIcon(iconReloadAM), libReloadAM, self.reloadBase, QKeySequence("F5"))
        #------------
        self.mMenuDialog.setEnabled(False)
        #=====================================================  
        #=====================================================
        #Image
        self.labelImage = QtWidgets.QLabel(Dialog)
        myPath = self.myPathIcon+"\\logo\\logo.png"
        myDefPath = myPath.replace("\\","/")
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        self.labelImage.setGeometry(QtCore.QRect(665, 20, 150, 80))
        self.labelImage.setObjectName("labelImage")
        #=====================================================
        #Image Cursor
        myPathCursorImage = self.myPathIcon +"\\icons\\cursor3.jpg"
        myPathCursorImage = myPathCursorImage.replace("\\","/")
        self.cursorImage = QCursor(QPixmap(myPathCursorImage))

        #ComboBox Adresse 
        self.labelAdresse = QtWidgets.QLabel(Dialog)
        self.labelAdresse.setGeometry(QtCore.QRect(20,34,170,20))
        self.labelAdresse.setObjectName("labelAdresse")
        self.labelAdresse.setAlignment(Qt.AlignRight)
        self.comboAdresse = QtWidgets.QComboBox(Dialog)
        self.comboAdresse.setGeometry(QtCore.QRect(200,30,440,23))
        self.comboAdresse.setObjectName("comboAdresse")

        #Zone affichage
        self.resultTextEdit = QtWidgets.QTextEdit(Dialog)
        self.resultTextEdit.setGeometry(QtCore.QRect(10, 45, 650,100))
        self.resultTextEdit.setObjectName("resultTextEdit") 
        self.resultTextEdit.setStyleSheet("QTextEdit {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: blue;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")
        
        self.resultTextEdit.setEnabled(False)
        self.resultTextEdit.setVisible(False)  #Cachée pour cette version, pas d'affichage des infos en permanence

        #==========================              
        #Zone Onglets
        self.tabWidget = QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setGeometry(QtCore.QRect(10, 70, self.lScreenDialog -20 ,self.hScreenDialog - 130))
        self.tabWidget.setStyleSheet("QTabWidget::pane {border: 2px solid #958B62; } \
                                      QTabBar::tab {border: 1px solid #958B62; border-bottom-color: none;\
                                                    border-top-left-radius: 6px;border-top-right-radius: 6px;\
                                                    width: 120px; padding: 2px;} \
                                      QTabBar::tab:selected {background: qlineargradient(x1: 0, y1: 0, x2: 0.5, y2: 0.5, stop: 0 #958B62, stop: 1 white);  font: bold;} \
                                     ")
        #--------------------------
        self.tab_widget_Explo = QWidget()
        self.tab_widget_Explo.setObjectName("tab_widget_Explo")
        labelTab_Explo = QtWidgets.QApplication.translate("asgard_general_ui", "  diagrams  ", None)
        self.tabWidget.addTab(self.tab_widget_Explo,labelTab_Explo)
        #--------------------------
        self.tab_widget_Droits = QWidget()
        self.tab_widget_Droits.setObjectName("tab_widget_Droits")
        labelTab_Droits = QtWidgets.QApplication.translate("asgard_general_ui", "   Roles   ", None)
        self.tabWidget.addTab(self.tab_widget_Droits,labelTab_Droits)
        #--------------------------
        self.tab_widget_Dash = QWidget()
        self.tab_widget_Dash.setObjectName("tab_widget_Dash")
        self.labelTab_Dash = QtWidgets.QApplication.translate("asgard_general_ui", "   statistics   ", None)
        self.tabWidget.addTab(self.tab_widget_Dash,self.labelTab_Dash)
        #--------------------------
        if self.dashBoard != 'true':
           self.tabWidget.removeTab(2)
        else : 
           self.tabWidget.insertTab(2, self.tab_widget_Dash, self.labelTab_Dash)
        self.tabWidget.setCurrentIndex(0)
        #--------------------------
        self.tab_widget_Diagnostic = QWidget()
        self.tab_widget_Diagnostic.setObjectName("tab_widget_Diagnostic")
        self.labelTab_Diagnostic = QtWidgets.QApplication.translate("asgard_general_ui", "   diagnostics   ", None)
        self.tabWidget.addTab(self.tab_widget_Diagnostic,self.labelTab_Diagnostic)
        #--------------------------
        self.tab_widget_TableauBord = QWidget()
        self.tab_widget_TableauBord.setObjectName("tab_widget_TableauBord")
        self.labelTab_TableauBord = QtWidgets.QApplication.translate("asgard_general_ui", "   dashboard   ", None)
        self.tabWidget.addTab(self.tab_widget_TableauBord,self.labelTab_TableauBord)
        #--------------------------

        #Menu contextuel QTabWidget for Diagnostic and Dashboard
        self.tabWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabWidget.customContextMenuRequested.connect(self.menuContextuelDiag) 
        #self.tabWidget.tabBarClicked.connect(self.clickOngletTabWidget)

        #==========================              
        #Zone affichage  displayInformations                
        self.displayInformations = QtWidgets.QGroupBox(self.tab_widget_Explo)
        self.displayInformations.setGeometry(QtCore.QRect(10, 10, self.tabWidget.width() -20 ,self.tabWidget.height() - 40))
        self.displayInformations.setObjectName("displayInformations") 
        self.displayInformations.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: #E1000F;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")      
                
        #==========================         
        self.groupBoxAffichageLeft = QtWidgets.QGroupBox(self.displayInformations)  
        self.groupBoxAffichageLeft.setGeometry(QtCore.QRect(0,0,(self.displayInformations.width() - 10)/2,self.displayInformations.height() - 0))
        self.groupBoxAffichageLeft.setObjectName("groupBoxAffichageLeft")
        self.groupBoxAffichageLeft.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")  

        #-- FILTRE schémas / obj
        self.labelFilter = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.labelFilter.setGeometry(QtCore.QRect(15, 10, 30, 20))
        self.labelFilter.setObjectName("labelFilter")
        self.labelFilter.setAlignment(Qt.AlignLeft)
        self.zoneFilter = QtWidgets.QLineEdit(self.groupBoxAffichageLeft)
        self.zoneFilter.setGeometry(QtCore.QRect(50, 6, 150, 20))
        self.zoneFilter.setObjectName("zoneFilter")
        self.zoneFilter.setPlaceholderText(QtWidgets.QApplication.translate("asgard_general_ui", "Enter text to filter ...", None))
        self.zoneFilter.textChanged.connect(self.onChanged)
        self.zoneFilter.setToolTip(QtWidgets.QApplication.translate("asgard_general_ui", "Enter text to filter ...", None))
        # 
        self.sep2 = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.sep2.setGeometry(QtCore.QRect(200, 8, 5, 18))
        self.sep2.setText("|")
        self.sep2.setStyleSheet("QLabel {   \
                                font: bold 18px;         \
                                }")  
        self.caseZoneFilter = QtWidgets.QCheckBox(self.groupBoxAffichageLeft)    
        self.caseZoneFilter.setGeometry(QtCore.QRect(210,6,23,23))
        self.caseZoneFilter.setObjectName("caseZoneFilter")
        self.caseZoneFilter.setChecked(False) 
        self.caseZoneFilter.toggled.connect(lambda : self.onChangeCaseFilter(self.zoneFilter.text())) 
        self.caseZoneFilter.setToolTip(QtWidgets.QApplication.translate("asgard_general_ui", "Sensibilite Case", None))
        self.labelCaseZoneFilter = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.labelCaseZoneFilter.setGeometry(QtCore.QRect(230, 10, 95, 20))
        self.labelCaseZoneFilter.setObjectName("labelCaseZoneFilter")
        self.labelCaseZoneFilter.setAlignment(Qt.AlignLeft)
        # 
        self.sep3 = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.sep3.setGeometry(QtCore.QRect(325, 8, 5, 18))
        self.sep3.setText("|")
        self.sep3.setStyleSheet("QLabel {   \
                                font: bold 18px;         \
                                }")  
        self.caseZoneFilterRepliquer = QtWidgets.QCheckBox(self.groupBoxAffichageLeft)    
        self.caseZoneFilterRepliquer.setGeometry(QtCore.QRect(335,6,23,23))
        self.caseZoneFilterRepliquer.setObjectName("caseZoneFilterRepliquer")
        self.caseZoneFilterRepliquer.setChecked(False) 
        self.caseZoneFilterRepliquer.toggled.connect(lambda : self.onChangeCaseFilter(self.zoneFilter.text())) 
        self.caseZoneFilterRepliquer.setToolTip(QtWidgets.QApplication.translate("asgard_general_ui", "Check to display only replicated objects", None))
        self.labelCaseZoneFilterRepliquer = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.labelCaseZoneFilterRepliquer.setGeometry(QtCore.QRect(355, 10, 60, 20))
        self.labelCaseZoneFilterRepliquer.setObjectName("labelCaseZoneFilterRepliquer")
        self.labelCaseZoneFilterRepliquer.setAlignment(Qt.AlignLeft)
        self.labelCaseZoneFilterRepliquer.setStyleSheet("QLabel {   \
                                font-weight: bold ;     \
                                color: #5770BE;      \
                                }")                   
        # 
        self.sep4 = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.sep4.setGeometry(QtCore.QRect(410, 8, 5, 18))
        self.sep4.setText("|")
        self.sep4.setStyleSheet("QLabel {   \
                                font: bold 18px;         \
                                }")  
        self.caseZoneFilterDerepliquer = QtWidgets.QCheckBox(self.groupBoxAffichageLeft)    
        self.caseZoneFilterDerepliquer.setGeometry(QtCore.QRect(420,6,23,23))
        self.caseZoneFilterDerepliquer.setObjectName("caseZoneFilterDerepliquer")
        self.caseZoneFilterDerepliquer.setChecked(False) 
        self.caseZoneFilterDerepliquer.toggled.connect(lambda : self.onChangeCaseFilter(self.zoneFilter.text())) 
        self.caseZoneFilterDerepliquer.setToolTip(QtWidgets.QApplication.translate("asgard_general_ui", "Check to display only non-replicated objects ", None))
        self.labelCaseZoneFilterDerepliquer = QtWidgets.QLabel(self.groupBoxAffichageLeft)
        self.labelCaseZoneFilterDerepliquer.setGeometry(QtCore.QRect(440, 10, 75, 20))
        self.labelCaseZoneFilterDerepliquer.setObjectName("labelCaseZoneFilterDerepliquer")
        self.labelCaseZoneFilterDerepliquer.setAlignment(Qt.AlignLeft)
        self.labelCaseZoneFilterDerepliquer.setStyleSheet("QLabel {   \
                                font-weight: bold ;     \
                                color: #958B62;      \
                                }") 
        #-- FILTRE schémas / obj

        self.groupBoxAffichageLeft.setVisible(False)
        #==========================              
        #==========================              
        createIHMAffichage(self)
        #==========================                                                 
        #==========================              
        #Zone affichage  displayInformationsDroits                
        self.displayInformationsDroits = QtWidgets.QGroupBox(self.tab_widget_Droits)
        self.displayInformationsDroits.setGeometry(QtCore.QRect(10, 10, self.tabWidget.width() -20 ,self.tabWidget.height() - 40))
        self.displayInformationsDroits.setObjectName("displayInformationsDroits") 
        self.displayInformationsDroits.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")      
        #==========================         
        self.groupBoxAffichageLeftDroits = QtWidgets.QGroupBox(self.displayInformationsDroits)  
        self.groupBoxAffichageLeftDroits.setGeometry(QtCore.QRect(0,0,(self.displayInformationsDroits.width() - 10) * self.mSectionGauche,self.displayInformationsDroits.height() - 0))
        self.groupBoxAffichageLeftDroits.setObjectName("groupBoxAffichageLeftDroits")
        self.groupBoxAffichageLeftDroits.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")  
        self.groupBoxAffichageLeftDroits.setVisible(False)
        #==========================              
        #==========================              
        createIHMAffichageDroits(self)
        #==========================                                                 
        #==========================              
        #Zone affichage  displayInformationsDash                
        self.displayInformationsDash = QtWidgets.QGroupBox(self.tab_widget_Dash)
        self.displayInformationsDash.setGeometry(QtCore.QRect(10, 10, self.tabWidget.width() -20 ,self.tabWidget.height() - 40))
        self.displayInformationsDash.setObjectName("displayInformationsDash") 
        self.displayInformationsDash.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")      
        #==========================         
        self.groupBoxAffichageLeftDash = QtWidgets.QGroupBox(self.displayInformationsDash)  
        self.groupBoxAffichageLeftDash.setGeometry(QtCore.QRect(0,0,(self.displayInformationsDash.width() - 10) * self.mSectionGauche,self.displayInformationsDash.height() - 0))
        self.groupBoxAffichageLeftDash.setObjectName("groupBoxAffichageLeftDash")
        self.groupBoxAffichageLeftDash.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")  
        self.groupBoxAffichageLeftDash.setVisible(False)
        #==========================              
        #==========================              
        createIHMAffichageDash(self)
        #==========================                                                 
        #==========================              
        #Zone affichage  displayInformationsDiagnostic               
        self.displayInformationsDiagnostic = QtWidgets.QGroupBox(self.tab_widget_Diagnostic)
        self.displayInformationsDiagnostic.setGeometry(QtCore.QRect(10, 10, self.tabWidget.width() -20 ,self.tabWidget.height() - 40))
        self.displayInformationsDiagnostic.setObjectName("displayInformationsDiagnostic") 
        self.displayInformationsDiagnostic.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")      
        #==========================              
        #==========================              
        createIHMAffichageDiagnostic(self)
        #==========================                                                 
        #==========================              
        #Zone affichage  displayInformationsDiagnostic               
        self.displayInformationsTableauBord = QtWidgets.QGroupBox(self.tab_widget_TableauBord)
        self.displayInformationsTableauBord.setGeometry(QtCore.QRect(10, 10, self.tabWidget.width() -20 ,self.tabWidget.height() - 40))
        self.displayInformationsTableauBord.setObjectName("displayInformationsTableauBord") 
        self.displayInformationsTableauBord.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")      
        #==========================              
        #==========================              
        createIHMAffichageTableauBord(self)
        #==========================                                                 
        #==========================              
        #Groupe liseré bas
        self.groupBoxDown = QtWidgets.QGroupBox(Dialog)
        self.groupBoxDown.setGeometry(QtCore.QRect(10,self.hScreenDialog - 50,self.lScreenDialog -20,40))
        self.groupBoxDown.setObjectName("groupBoxDown")
        self.groupBoxDown.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 1px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 12px;         \
                                padding: 6px;            \
                                }")  
  
        #=====================================================
        #Boutons  
        #------       
        self.okhButton = QtWidgets.QPushButton(self.groupBoxDown)
        self.okhButton.setGeometry(QtCore.QRect(((self.displayInformations.width() -200) / 3) + 100 + ((self.displayInformations.width() -200) / 3), 10, 100,23))
        self.okhButton.setObjectName("okhButton")
        #------                                    
        self.helpButton = QtWidgets.QPushButton(self.groupBoxDown)
        self.helpButton.setGeometry(QtCore.QRect((self.displayInformations.width() -200) / 3, 10, 100,23))
        self.helpButton.setObjectName("helpButton")
        #------  
        #Connections  
        self.helpButton.clicked.connect(Dialog.myHelpAM)
        self.okhButton.clicked.connect(Dialog.reject)        
        self.comboAdresse.currentIndexChanged.connect(lambda : self.initGeneral(self.Dialog))
                             
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        #========================== 
        #Alimentation de la ComboBox Adresse
        self.returnAdresse, i = {}, 0
        mListeBase = bibli_asgard.listBase(self)
        self.returnAdresse[0] = "Aucun"
        for i in range(len(mListeBase)) :
            self.returnAdresse[i + 1] = mListeBase[i]

        modelComboAdresse = QStandardItemModel()
        for key, value in self.returnAdresse.items() :
            modelComboAdresseCol1 = QStandardItem(str(value))
            modelComboAdresseCol2 = QStandardItem(str(key))
            modelComboAdresse.appendRow([modelComboAdresseCol1, modelComboAdresseCol2])
        self.comboAdresse.setModel(modelComboAdresse)
        
        mDic_Connect = bibli_asgard.returnAndSaveConnectionParam(self, "Load")
        self.comboAdresse.setCurrentText(mDic_Connect["urlConnect"])
        #========================== 
        self.retranslateUi(Dialog)
        returnToken = ""
        
    def clickAboutMenuDialog(self):
        d = doabout.Dialog()
        d.exec_()
        return

    def clickParamArbo(self):
        mDicAutre = {}
        mSettings = QgsSettings()
        mSettings.beginGroup("ASGARD_MANAGER")
        mSettings.beginGroup("Generale")
    
        mDicAutre["arboObjet"] = "false"
        for key, value in mDicAutre.items():
            if not mSettings.contains(key) :
               mSettings.setValue(key, value)
            else :
               mDicAutre[key] = 'true' if self.paramArbo.isChecked() else 'false'
        #--                 
        for key, value in mDicAutre.items():
            mSettings.setValue(key, value)
        mSettings.endGroup()
        mSettings.endGroup()
        #--
        self.arboObjet = self.paramArbo.isChecked()     #Arborescence des objets dans le treeview schéma
        self.reloadBase()
        return

    def clickParamDisplayMessage(self):
        mDicAutre = {}
        mSettings = QgsSettings()
        mSettings.beginGroup("ASGARD_MANAGER")
        mSettings.beginGroup("Generale")
        mDicAutre["displayMessage"] = "dialogBox"
        for key, value in mDicAutre.items():
            if not mSettings.contains(key) :
               mSettings.setValue(key, value)
            else :
               mDicAutre[key] = 'dialogBox' if self.paramDisplayMessage.isChecked() else 'dialogTitle'
        #--                 
        for key, value in mDicAutre.items():
            mSettings.setValue(key, value)
        mSettings.endGroup()
        mSettings.endGroup()
        #--
        self.displayMessage = self.paramDisplayMessage.isChecked()  #Qmessage box (dialogBox) ou barre de progression (dialogTitle)
        return
        
    def retranslateUi(self, Dialog):
        self.labelCaseZoneFilterRepliquer.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Replica  : ", None))
        self.labelCaseZoneFilterDerepliquer.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Not réplicated  : ", None))
        self.labelCaseZoneFilter.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Case sensitive  : ", None))
        self.labelFilter.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Filter : ", None))
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("asgard_general_ui", "ASGARD Manager - Automatic and Simplified GrAnting for Rights in Databases", None) + "  (" + str(bibli_asgard.returnVersion()) + ")")
        self.helpButton.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Help", None))
        self.okhButton.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Close", None))
        self.labelAdresse.setText(QtWidgets.QApplication.translate("asgard_general_ui", "List of PostgreSQL connections : ", None))
        self.labelChoiceGraph.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Choice of chart : ", None))
        self.executeButtonGraph.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Apply", None))
        self.executeButtonGraphColor.setText(QtWidgets.QApplication.translate("asgard_general_ui", "Block colors", None))
        #-
        self.labelTypeGraph.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Type", None))
        self.radioPie.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Circle", None))
        self.radioBar.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Bar", None))
        #-
        self.radioBarAuto.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Auto", None))
        self.radioBarFull.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "100 %", None))

        #-
        self.caseEtiGraph.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Labels", None))
        self.caseEtiLibelle.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Wording", None))
        self.caseEtiPourc.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Percentage", None))
        self.caseEtiValeur.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Value", None))
        #-
        self.caseLegGraph.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Legende", None))
        self.caseLegNord.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "North", None))
        self.caseLegOuest.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "West", None))
        self.caseLegEst.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "East", None))
        self.caseLegSud.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "South", None))
        #-
        self.caseTitreGraph.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Title", None))
        self.caseAnimationGraph.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Animation", None))
       
    #Menu contextuel QTabWidget for Diagnostic and Dashboard
    #------    
    def menuContextuelDiag(self, point):
        #Diagnostics
        self.diagMenu = QMenu(self.Dialog.tab_widget_Diagnostic)
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\graph_print.png")          
        zTitleMenu = QtWidgets.QApplication.translate("asgard_general_ui", "Diagnostic: Print preview", None)
        self.treeActionDiagPrint = QAction(QIcon(menuIcon), zTitleMenu, self.diagMenu)
        self.diagMenu.addAction(self.treeActionDiagPrint)
        #-
        zTitleMenu = QtWidgets.QApplication.translate("asgard_general_ui", "Diagnostic: Delele result", None)
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\diagnostic_efface.png")          
        self.treeActionDiagDelete = QAction(QIcon(menuIcon), zTitleMenu, self.diagMenu)
        self.diagMenu.addAction(self.treeActionDiagDelete)
        #-
        self.treeActionDiagPrint.triggered.connect( lambda : bibli_asgard.printViewDiagnostic(self, self))
        self.treeActionDiagDelete.triggered.connect( lambda : bibli_asgard.deletetViewDiagnostic(self, self))
        #-
        try :
           self.treeActionDiagPrint.setVisible(False if self.tabWidget.currentIndex() != 3 else True)
           self.treeActionDiagDelete.setVisible(False if self.tabWidget.currentIndex() != 3 else True)
        except :
           pass
        #-
        self.treeActionDiagPrint.setEnabled(False if self.Dialog.zone_affichage_diagnostic.toPlainText() == '' else True)
        self.treeActionDiagDelete.setEnabled(False if self.Dialog.zone_affichage_diagnostic.toPlainText() == '' else True)
        #-------
        #Dashboard
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\graph_print.png")          
        zTitleMenu = QtWidgets.QApplication.translate("asgard_general_ui", "Dashboard: Print preview", None)
        self.treeActionTableauBordPrint = QAction(QIcon(menuIcon), zTitleMenu, self.diagMenu)
        self.diagMenu.addAction(self.treeActionTableauBordPrint)
        #-
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\csv.png")          
        zTitleMenu = QtWidgets.QApplication.translate("asgard_general_ui", "Dashboard: Export CSV", None)
        self.treeActionTableauBordCsv = QAction(QIcon(menuIcon), zTitleMenu, self.diagMenu)
        self.diagMenu.addAction(self.treeActionTableauBordCsv)
        #-
        self.diagMenu.addSeparator()
        #-
        zTitleMenu = QtWidgets.QApplication.translate("asgard_general_ui", "Dashboard: Delele result", None)
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\diagnostic_efface.png")          
        self.treeActionTableauBordDelete = QAction(QIcon(menuIcon), zTitleMenu, self.diagMenu)
        self.diagMenu.addAction(self.treeActionTableauBordDelete)
        #-
        self.treeActionTableauBordPrint.triggered.connect( lambda : bibli_asgard.printViewTableauBord(self, self))
        self.treeActionTableauBordCsv.triggered.connect( lambda : bibli_asgard.csvTableauBord(self, self))
        self.treeActionTableauBordDelete.triggered.connect( lambda : bibli_asgard.deletetViewTableauBord(self, self))
        #-
        try :
           self.treeActionTableauBordPrint.setVisible(False if self.tabWidget.currentIndex() != 4 else True)
           self.treeActionTableauBordCsv.setVisible(False if self.tabWidget.currentIndex() != 4 else True)
           self.treeActionTableauBordDelete.setVisible(False if self.tabWidget.currentIndex() != 4 else True)
        except :
           pass
        #-
        self.treeActionTableauBordPrint.setEnabled(False if self.Dialog.zone_affichage_TableauBord.toPlainText() == '' else True)
        self.treeActionTableauBordCsv.setEnabled(False if self.Dialog.zone_affichage_TableauBord.toPlainText() == '' else True)
        self.treeActionTableauBordDelete.setEnabled(False if self.Dialog.zone_affichage_TableauBord.toPlainText() == '' else True)
        self.diagMenu.exec_(self.tabWidget.mapToGlobal(point))
        #-------
        return   
    #Menu contextuel QTabWidget for Diagnostic

    #------    
    def resizeEvent(self, event):
        if self.firstOpen :
           self.firstOpen = False
        else :
           bibli_asgard.resizeIhm(self, self.Dialog.width(), self.Dialog.height())
              
    #------       
    def initGeneral(self, Dialog) :
        self.groupBoxAffichageSchema.setVisible(False)
        self.groupBoxAffichageHelp.setVisible(False)
        self.groupBoxAffichageHelpDroits.setVisible(False)
        self.groupBoxAffichageRoleAttribut.setVisible(False)
        self.groupBoxAffichageRoleAppart.setVisible(False)
        self.executeButtonRole.setVisible(False)    
        self.mMenuDialog.setEnabled(False)

        #Etat Menu Gestion de la base
        self.installe_error       = False    # Si extension pas installée = True
        self.g_admin_error        = False    # Si membre de g_admin ou pas
        self.installe_error_plume = False    # Si extension pas installée = True

        debut = time.time()

        mIndex = self.comboAdresse.currentIndex()
        #--Save Url connection
        if self.firstOpenConnect :
           self.firstOpenConnect = False
        else :
           mDic_Connect = bibli_asgard.returnAndSaveConnectionParam(self, "Save")
        #-------------
        if mIndex != 0 :
           mNameBase = self.returnAdresse[mIndex]
           self.mBaseAsGard = BASEPOSTGRES(mNameBase)
           connectBaseAsgard= self.mBaseAsGard.connectBase()
           self.connectBaseAsgard = connectBaseAsgard
           
           if connectBaseAsgard[0] :
              # Gestion Retour et Installation pour le menu GESTION DE LA BASE
              self.asgardInstalle, self.asgardVersionDefaut, self.dbName  = bibli_asgard.returnInstalleEtVersionAsgard(self) 
              self.asgardVersionDefaut_error = True if self.asgardVersionDefaut == None else False
              zTitre =  QtWidgets.QApplication.translate("asgard_general_ui", "ASGARD MANAGER : Warning", None)
              #- For PLUME
              self.plumeInstalle, self.plumeVersionDefaut, self.dbNamePlume  = bibli_asgard.returnInstalleEtVersionPlume(self)
              if self.plumeInstalle == None  : self.installe_error_plume = True
              self.plumeVersionDefaut_error = True if self.plumeVersionDefaut == None else False
              #- For PLUME

              if self.asgardInstalle == None  :
                 if self.asgardVersionDefaut_error == False :
                    #Récup Nom de la base pour les messages dans confirm            
                    mConfigConnection = connectBaseAsgard[2].split()
                    #
                    zMess = QtWidgets.QApplication.translate("asgard_general_ui", "Initialization failed. The PostgreSQL ASGARD extension is not installed on the target database for this connection.", None)
                    mContExt = False
                    self.installe_error = True
                    #Membre de g_admin pour instancier le superUser
                    mKeySql = dicListSql(self,'IsSuperUser') 
                    r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
                    #Super utilisateur or not
                    self.isSuperUser = r[0][0]
                 else : 
                    mContExt = False
                    self.installe_error = True
              else : 
                 mContExt = True
                 self.installe_error = False

              self.g_admin_isValid = False
              self.g_admin_error = False
              if mContExt : 
                 #Membre de g_admin
                 mKeySql = dicListSql(self,'Membre_G_admin_ET_CreateRoleOuPas') 
                 r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
                 if r != None :
                    #-------------
                    self.g_admin_isValid = r[0][0]
                    #-- Permet de controler si le compte est g_admin ou parent de g_admin avec CREATEROLE
                    self.role_g_admin_createrole = r[0][1]
                    # Important de récupérer le user connecter pour les SQL des rôles
                    self.userConnecteEnCours = r[0][2] 
                    #Super utilisateur or not
                    self.isSuperUser = r[0][3] 
                 else :
                    mContExt = False
                    self.g_admin_error = True
                 #-------------

              if not mContExt :
                 self.g_admin_isValid = False
              elif not self.g_admin_isValid  :
                 mContExt = False
                 zMess = QtWidgets.QApplication.translate("asgard_general_ui", "Permission denied. To use the AsgardManager plugin, you must connect to the PostgreSQL server with a role that is a member of the g_admin group.)", None)

              #-------------
              if mContExt : 
                self.groupBoxAffichageLeft.setVisible(True)
                self.groupBoxAffichageRight.setVisible(True)
                self.groupBoxAffichageLeftDroits.setVisible(True)
                self.groupBoxAffichageRightDroits.setVisible(True)
                self.groupBoxAffichageRightDroitsSchemasZone.setVisible(True)
                self.groupBoxAffichageLeftDash.setVisible(True)
                self.groupBoxAffichageRightDash.setVisible(True)

                mConfigConnection = connectBaseAsgard[2].split()

                zMess = ""
                for t in  mConfigConnection : 
                    if "password" not in t:
                       zMess += t + "\n"
                self.resultTextEdit.setText(zMess) 
                #gestion des schémas
                mKeySql = dicListSql(self,'ListeSchema') 
                r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
                zTitre =  QtWidgets.QApplication.translate("asgard_general_ui", "ASGARD MANAGER : error handler ", None)
                if zMessError_Code == '' :
                   zMess = QtWidgets.QApplication.translate("asgard_general_ui", "Your database is not ASGARD compatible", None)
                else : 
                   zMessError_Erreur = cleanMessError(zMessError_Erreur)
                   zMess = str(zMessError_Code) + "\n" + str(zMessError_Erreur) + "\n" + str(zMessError_Diag)

                if r != None : 
                   #print("ListeSchema   %s" %(str(format(time.time()-debut,".3f"))))
                   mSchemas = [[row[0]] for row in r]
                   mListSchemas = [row[0] for row in r]
                   #gestion des schémas et tables et types
                   #mKeySql = dicListSql(self,'ListeSchemaTable')   
                   mKeySql = dicListSql(self,'ListeSchemaObjets') 
                   if r != None : 
                      r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql) 
                      #print("ListeSchemaObjets   %s" %(str(format(time.time()-debut,".3f"))))
                      mSchemasTables = [row for row in r]
                      #print("ListeSchemaObjets II   %s" %(str(format(time.time()-debut,".3f"))))
                      #gestion des schémas et blocs
                      mKeySql = dicListSql(self,'ListeSchemaBlocExiste')
                      r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
                      if r != None : 
                         #print("ListeSchemaBlocExiste   %s" %(str(format(time.time()-debut,".3f"))))
                         mSchemasBlocs = [row for row in r]
                         #print("ListeSchemaBlocExiste II  %s" %(str(format(time.time()-debut,".3f"))))
                         #gestion des editeurs et lecteurs
                         mKeySql = dicListSql(self,'ListeRolesEditeursLecteurs')
                         r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql) 
                         if r != None : 
                            #print("ListeRolesEditeursLecteurs   %s" %(str(format(time.time()-debut,".3f"))))
                            mRolesEditeursLecteurs = [row[0] for row in r]
                            #print("ListeRolesEditeursLecteurs II  %s" %(str(format(time.time()-debut,".3f"))))
                            #gestion des editeurs et lecteurs
                            mKeySql = dicListSql(self,'ListeRolesProducteurs')
                            r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql) 
                            if r != None : 
                               #print("ListeRolesProducteurs   %s" %(str(format(time.time()-debut,".3f"))))
                               mRolesProducteurs = sorted(list(set([row[0] for row in r])))
                               #print("ListeRolesProducteurs II  %s" %(str(format(time.time()-debut,".3f"))))
                               #gestion des roles de groupes
                               mKeySql = dicListSql(self,'listeDesRolesDeGroupeEtConnexions')
                               #print(mKeySql)
                               r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql) 
                               if r != None : 
                                  #print("listeDesRolesDeGroupeEtConnexions   %s" %(str(format(time.time()-debut,".3f"))))
                                  mlisteDesRolesDeGroupeEtConnexions = [row for row in r] 
                                  #print("listeDesRolesDeGroupeEtConnexions II  %s" %(str(format(time.time()-debut,".3f"))))
                                  #------
                                  #Alimentation  
                                  #Blocs fonctionnels 
                                  self.comboBloc.clear()
                                  #Gestion des blocs Qgis3.ini
                                  dicListBlocs = returnLoadBlocParam() 
                                  #Ajout des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings
                                  dicListBlocs = returnDicBlocUniquementNonReference(dicListBlocs, mSchemasBlocs)
                                  self.mSchemasBlocs = mSchemasBlocs
                                  self.dicListBlocs = dicListBlocs
                               
                                  modelcomboBloc = QStandardItemModel()
                                  for key, value in dicListBlocs.items() :
                                     modelcomboBlocCol1 = QStandardItem("(%s) %s" %(str(key),str(value)))
                                     modelcomboBlocCol2 = QStandardItem(str(key))
                                     modelcomboBloc.appendRow([modelcomboBlocCol1, modelcomboBlocCol2])
                                  self.comboBloc.setModel(modelcomboBloc)
                                  #print("Fin des requêtes et début TreeViews   %s" %(str(format(time.time()-debut,".3f"))))
                                  #-----
                                  self.ctrlReplication = False   #controle pour exploiter la réplication ou pas
                                  #-----
                                  #=======================
                                  #gestion des réplications
                                  #--
                                  self.labelCaseZoneFilterRepliquer.setVisible(self.ctrlReplication)
                                  self.caseZoneFilterRepliquer.setVisible(self.ctrlReplication)
                                  self.labelCaseZoneFilterDerepliquer.setVisible(self.ctrlReplication)
                                  self.caseZoneFilterDerepliquer.setVisible(self.ctrlReplication)
                                  self.sep3.setVisible(self.ctrlReplication)
                                  self.sep4.setVisible(self.ctrlReplication)
                                  #--
                                  if self.ctrlReplication :
                                     #Création Schéma, Séquence, Table si elle n'existe pas 
                                     mKeySql = dicListSql(self,'Fonction_CreateSchemaTableReplication')
                                     r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSqlCreate(Dialog, self.mBaseAsGard.mConnectEnCours, self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
                                     if r != False :
                                        pass
                                     else :
                                        #Géré en amont dans la fonction executeSqlNoReturn
                                        pass 
                                     #-- 
                                     mKeySql = dicListSql(self,'Fonction_Liste_Replication')
                                     r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql) 
                                     if r != None :
                                        # nombase, schema, nomobjet, typeobjet, etat 
                                        self.mListeMetadata = r
                                     else :
                                        self.mListeMetadata = []
                                  else :
                                     self.mListeMetadata = []
                                  #gestion des réplications
                                  #=======================
                                  #=======================
                                  #gestion Layer_Styles
                                  #--
                                  mKeySql = dicListSql(self,'Fonction_Layer_Styles')
                                  r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql) 
                                  if r != None :
                                     # - si layer_styles existe (valeur de ls_exists) ;
                                     # - si le rôle courant est membre de son propriétaire (valeur de ls_isowner). 
                                     self.mLayerStyles = r
                                  else :
                                     self.mLayerStyles = []
                                  #gestion Layer_Styles
                                  #=======================
                                  #------
                                  self.comboProd.clear()
                                  self.comboEdit.clear()
                                  self.comboLect.clear()
                                  #------
                                  #self.comboProd.addItem('Aucun')  #Nécessite un Prod
                                  self.comboEdit.addItem('Aucun')
                                  self.comboLect.addItem('Aucun')
                                  self.comboProd.addItems(mRolesProducteurs)    
                                  self.comboEdit.addItems(mRolesEditeursLecteurs)    
                                  self.comboLect.addItems(mRolesEditeursLecteurs) 
                                  QApplication.instance().setOverrideCursor(Qt.WaitCursor)
                                  self.createZoneInformations( Dialog, mNameBase, mConfigConnection, mSchemas, mSchemasTables, mSchemasBlocs, mRolesEditeursLecteurs, mRolesProducteurs, mlisteDesRolesDeGroupeEtConnexions )
                                  QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
                                  # Gestion Retour et Installation pourle menu GESTION DE LA BASE
                                  self.asgardInstalle, self.asgardVersionDefaut, self.dbName  = bibli_asgard.returnInstalleEtVersionAsgard(self) 
                                  #- For PLUME
                                  self.plumeInstalle, self.plumeVersionDefaut, self.dbNamePlume  = bibli_asgard.returnInstalleEtVersionPlume(self) 
                                  self.mMenuDialog.setEnabled(True)
                                  bibli_asgard.etatMenuGestionDeLaBase(self, self.installe_error)
                                  #bibli_asgard.etatMenuGestionDeLaBasePlume(self, self.installe_error_plume)
                                  #print("Origine FIN   %s" %(str(format(time.time()-debut,".3f"))))
                               else : 
                                  self.cleanAndMessError( zTitre, zMess ) 
                            else : 
                               self.cleanAndMessError( zTitre, zMess ) 
                         else : 
                            self.cleanAndMessError( zTitre, zMess ) 
                      else : 
                         self.cleanAndMessError( zTitre, zMess ) 
                   else : 
                      self.cleanAndMessError( zTitre, zMess ) 
                else : 
                   self.cleanAndMessError( zTitre, zMess ) 
              else :
                 #if self.plumeVersionDefaut_error == False : #Cas où pas de fichier d'installation de l'extension
                 #   bibli_asgard.etatMenuGestionDeLaBasePlume(self, self.installe_error_plume)
                    
                 if self.asgardVersionDefaut_error == False : #Cas où pas de fichier d'installation de l'extension
                    # Si mContExt False et si pb avec g_admin alors mess géré dans le gestionnaire d'erreur
                    if not self.g_admin_error :
                       self.cleanAndMessError( zTitre, zMess ) 
                       self.mMenuDialog.setEnabled(True)
                       bibli_asgard.etatMenuGestionDeLaBase(self, self.installe_error)
                    else :
                      self.mMenuDialog.setEnabled(False)
                      self.groupBoxAffichageRight.setVisible(False)
                      self.groupBoxAffichageLeft.setVisible(False)
                    #  Permission refusée par membre ou g_admin et installe OK
                    if not self.g_admin_error and self.installe_error == False :
                       self.mMenuDialog.setEnabled(False)
                       self.groupBoxAffichageRight.setVisible(False)
                       self.groupBoxAffichageLeft.setVisible(False)
                 else :
                    self.mMenuDialog.setEnabled(False)
                    self.groupBoxAffichageRight.setVisible(False)
                    self.groupBoxAffichageLeft.setVisible(False)
           else :
              self.mMenuDialog.setEnabled(False)
              self.groupBoxAffichageRight.setVisible(False)
              self.groupBoxAffichageLeft.setVisible(False)
        else :
           self.resultTextEdit.clear()
           self.groupBoxAffichageLeft.setVisible(False)
           self.groupBoxAffichageRight.setVisible(False)
           self.groupBoxAffichageLeftDroits.setVisible(False)
           self.groupBoxAffichageRightDroits.setVisible(False)
           self.groupBoxAffichageRightDroitsSchemasZone.setVisible(False)
           self.groupBoxAffichageLeftDash.setVisible(False)
           self.groupBoxAffichageRightDash.setVisible(False)
           #Graph
           if hasattr(self, 'mVisuWeb') :
              self.mVisuWeb.view.engine().clearComponentCache()
              self.mVisuWeb.view.setSource(QUrl(""))
            
        return
    #------       
    def cleanAndMessError(self, zTitre, zMess ) :
        self.groupBoxAffichageLeft.setVisible(False)
        self.groupBoxAffichageRight.setVisible(False)
        self.groupBoxAffichageLeftDroits.setVisible(False)
        self.groupBoxAffichageRightDroits.setVisible(False)
        self.groupBoxAffichageRightDroitsSchemasZone.setVisible(False)
        self.groupBoxAffichageLeftDash.setVisible(False)
        self.groupBoxAffichageRightDash.setVisible(False)
        bibli_asgard.displayMess(self, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
        #QMessageBox.information(self, zTitre, zMess)
        return

    #------       
    def executeSqlSchema(self, Dialog) :
        mode = self.mTreePostgresql.mode 
        if mode == "create" :
           mKeySql = dicListSql(self,'CreationSchemaLigne')
           zMessGood = QtWidgets.QApplication.translate("asgard_general_ui", "Good you have a create schema !!", None)
        elif mode == "update" :
           mKeySql = dicListSql(self,'ModificationSchemaLigne')
           zMessGood = QtWidgets.QApplication.translate("asgard_general_ui", "Good you have a update schema !!", None)
        
        mSchemaNewID, mSchemaOldID = self.mTreePostgresql.mSchemaID, "#ID_nom_schema#"
        mSchemaNew, mSchemaOld = self.zoneSchema.text(), "#nom_schema#"
        mIndexBloc = self.comboBloc.currentIndex()
        #BLoc Fonc obligatoire ou pas 
        mBlocNewTemp = (self.comboBloc.model().item(mIndexBloc,1).text() if self.comboBloc.model().item(mIndexBloc,1).text() != 'autre' else None)
        mBlocNew, mBlocOld = mBlocNewTemp  , "#bloc#" 
        mNiv1New, mNiv1Old = "", "#niv1#"
        mniv1_abrNew, mniv1_abrOld = "", "#niv1_abr#"
        mniv2New, mniv2Old = "", "#niv2#"
        mniv2_abrNew, mniv2_abrOld = "", "#niv2_abr#"
        mValueCreation = (True if self.caseActif.isChecked() else False)
        mcreationNew, mcreationOld = mValueCreation, "#creation#"
        #Modif 2021/03/10
        mproducteurNew, mproducteurOld = self.comboProd.currentText(), "#producteur#"
        mediteurNewTemp = (self.comboEdit.currentText() if self.comboEdit.currentText() != 'Aucun' else "")
        mediteurNew, mediteurOld = mediteurNewTemp, "#editeur#"
        mlecteurNewTemp = (self.comboLect.currentText() if self.comboLect.currentText() != 'Aucun' else "")
        mlecteurNew, mlecteurOld = mlecteurNewTemp, "#lecteur#"
        #mproducteurNew, mproducteurOld = self.comboProd.itemText(self.comboProd.currentIndex()), "#producteur#"
        #mediteurNewTemp = (self.comboEdit.itemText(self.comboEdit.currentIndex()) if self.comboEdit.itemText(self.comboEdit.currentIndex()) != 'Aucun' else "")
        #mediteurNew, mediteurOld = mediteurNewTemp, "#editeur#"
        #mlecteurNewTemp = (self.comboLect.itemText(self.comboLect.currentIndex()) if self.comboLect.itemText(self.comboLect.currentIndex()) != 'Aucun' else "")
        #mlecteurNew, mlecteurOld = mlecteurNewTemp, "#lecteur#"
        #Modif 2021/03/10
        mNomenclatureNew, mNomenclatureOld = (True if self.caseNomenclature.isChecked() else False), "#nomenclature#"
        mNiv1New, mNiv1Old = self.zoneNiv1.text(), "#niv1#"
        mNiv1AbrNew, mNiv1AbrOld = self.zoneNiv1_abr.text(), "#niv1_abr#"
        mNiv2New, mNiv2Old = self.zoneNiv2.text(), "#niv2#"
        mNiv2AbrNew, mNiv2AbrOld = self.zoneNiv2_abr.text(), "#niv2_abr#"
        #Contrôles
        mContinue = True
        if (mproducteurNew == mediteurNew) or (mproducteurNew == mlecteurNew) :
           zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the roles of producers, editors and readers cannot be equal", None) 
           mContinue = False
        #------       
        if (mediteurNew != "" or mlecteurNew != "") :
           if (mlecteurNew == mediteurNew) :
              zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the roles of producers, editors and readers cannot be equal", None) 
              mContinue = False
        #------       
        if (mSchemaNew == '' or mSchemaNew == None) :   
           zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "Schema cannot be empty", None) 
           mContinue = False
        #------       
        if mContinue :
         #------
         mBlocNewprefixe = mBlocNew if mBlocNew != None else ''
         if mode == "create" :
           #------ 
           mFindSchemaKillPrefixe = True if dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mSchemaNew)[0] != '' else False
           mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mSchemaNew)[0]
           mChaine =  dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mSchemaNew)[1] 
           mFindSchema = (mPrefixe + "_" + mChaine if mFindSchemaKillPrefixe else ((mBlocNew  + "_" + mChaine) if mBlocNew != None else mChaine))
           
           for libZoneActive in Dialog.mTreePostgresql.mListSchemaActifs :
               if mFindSchema == libZoneActive[0] or mPrefixe == libZoneActive[0] :
                  if libZoneActive[1] == 'd' :
                     zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in actif in the trash", None)
                  else : 
                     zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in actif", None) + " (" + str(libZoneActive[1]) + ")" 
                  mContinue = False
                  break
           if mContinue :
              #------    
              for libZoneActive in Dialog.mTreePostgresql.mListSchemaNonActifs :
                  if mFindSchema == libZoneActive[0] or mPrefixe == libZoneActive[0] :
                     if libZoneActive[1] == 'd' :
                        zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in non-active in the trash", None)
                     else : 
                        zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in non-active", None) + " (" + str(libZoneActive[1]) + ")" 
                     mContinue = False
                     break
              if mContinue :
                 #------    
                 for libZoneActive in Dialog.mTreePostgresql.mListSchemaExistants :
                     if mFindSchema == libZoneActive or mPrefixe == libZoneActive:
                        if libZoneActive[1] == 'd' :
                           zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in the trash", None)
                        else : 
                           zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists", None) + " (" + str(libZoneActive[1]) + ")"
                        mContinue = False
                        break
         elif mode == "update": 
           #------ 
           mFindSchemaKillPrefixe = True if dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mSchemaNew)[0] != '' else False
           mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mSchemaNew)[0]
           mChaine =  dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mSchemaNew)[1] 
           #------ 
           #pas de chgt schéma
           if self.mTreePostgresql.dicOldValueSchema["id_schema"] == mSchemaNew : 
              mFindSchema = (mBlocNew  + "_" + mChaine) if mBlocNew != None else mChaine
           else :
              #pas de chgt bloc
              if self.mTreePostgresql.dicOldValueSchema["id_bloc"] == mBlocNew : 
                 mFindSchema = (mPrefixe + "_" + mChaine if mFindSchemaKillPrefixe else ((mBlocNew  + "_" + mChaine) if mBlocNew != None else mChaine))
              else :
                 if mBlocNew == 'd' :
                    mFindSchema = mChaine
                 else :
                    mFindSchema = (mBlocNew  + "_" + mChaine) if mBlocNew != None else mChaine
           #------ 
           #si je reste sur le même Item
           if mFindSchema != mSchemaNewID :
              for libZoneActive in Dialog.mTreePostgresql.mListSchemaActifs :
                  if mFindSchema == libZoneActive[0] or mPrefixe == libZoneActive[0] :
                     if libZoneActive[1] == 'd' :
                        zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in actif in the trash", None)
                     else : 
                        zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in actif", None) + " (" + str(libZoneActive[1]) + ")"
                     mContinue = False
                     break
              if mContinue :
                 #------    
                 for libZoneActive in Dialog.mTreePostgresql.mListSchemaNonActifs :
                     if mFindSchema == libZoneActive[0] or mPrefixe == libZoneActive[0] :
                        if libZoneActive[1] == 'd' :
                           zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in non-active in the trash", None)
                        else : 
                           zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in non-active", None) + " (" + str(libZoneActive[1]) + ")"
                        mContinue = False
                        break
                 if mContinue :
                    #------    
                    for libZoneActive in Dialog.mTreePostgresql.mListSchemaExistants :
                        if mFindSchema == libZoneActive or mPrefixe == libZoneActive:
                           if libZoneActive[1] == 'd' :
                              zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists in the trash", None)
                           else : 
                              zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "the diagram already exists", None) + " (" + str(libZoneActive[1]) + ")"
                           mContinue = False
                           break
           
           #Affichage si aucune valeur modifiée
           tId    = ('id_schema', 'id_bloc', 'id_actif', 'id_producteur', 'id_editeur', 'id_lecteur', 'id_nomenclature', 'id_niv1', 'id_niv1_abr', 'id_niv2', 'id_Niv2_abr')
           #Modif 2021/03/10
           tValue = (mSchemaNew, mBlocNew, mcreationNew, self.comboProd.currentText(), self.comboEdit.currentText(), self.comboLect.currentText(), mNomenclatureNew, mNiv1New, mNiv1AbrNew, mNiv2New, mNiv2AbrNew) 
           #tValue = (mSchemaNew, mBlocNew, mcreationNew, self.comboProd.itemText(self.comboProd.currentIndex()), self.comboEdit.itemText(self.comboEdit.currentIndex()), self.comboLect.itemText(self.comboLect.currentIndex()), mNomenclatureNew, mNiv1New, mNiv1AbrNew, mNiv2New, mNiv2AbrNew) 
           #Modif 2021/03/10
           self.dicNewValueSchema = dict(zip(tId, tValue))
           dicOldValueSchema =  self.mTreePostgresql.dicOldValueSchema
           if not bibli_asgard.returnChange(dicOldValueSchema, self.dicNewValueSchema) :           
              zMess  = QtWidgets.QApplication.translate("asgard_general_ui", "No value changed", None)
              mContinue = False

        #------       
        if not mContinue :
           zTitre = QtWidgets.QApplication.translate("asgard_general_ui", "ASGARD MANAGER : Warning", None)
           bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Warning, self.Dialog.durationBarInfo)
           #QMessageBox.warning(self, zTitre, zMess)
        else :
           #------       
           dicReplace = {mSchemaOldID: mSchemaNewID, mSchemaOld: mSchemaNew, mBlocOld: mBlocNew, mNomenclatureOld: mNomenclatureNew, 
                         mNiv1Old: mNiv1New, mNiv1AbrOld: mNiv1AbrNew, mNiv2Old: mNiv2New, mNiv2AbrOld: mNiv2AbrNew,
                         mcreationOld: mcreationNew, mproducteurOld: mproducteurNew, mediteurOld: mediteurNew, mlecteurOld: mlecteurNew}
           #------       
           for key, value in dicReplace.items():
               if isinstance(value, bool) :
                  mValue = str(value)
               elif (value is None) :
                  mValue = "''"
               else :
                  value = value.replace("'", "''")
                  mValue = "'" + str(value) + "'"
                  
               mKeySql = mKeySql.replace(key, mValue)
           #print(mKeySql)
           #------ 
           r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSqlNoReturn(Dialog, self.mBaseAsGard.mConnectEnCours, self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)

           if r != False :
              zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("asgard_general_ui", "Information !!!", None)
              bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
              #QMessageBox.information(self, zTitre, zMess) 
           else :
              #Géré en amont dans la fonction executeSqlNoReturn
              pass 

           self.Dialog.groupBoxAffichageSchema.setVisible(False)
           self.Dialog.groupBoxAffichageRightDroitsSchemas.setVisible(False)
           
           return 

    #------       
    def returnIcon(self, iconAdress) :
        iconSource = iconAdress
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        return icon
                                    
    #------------
    def createZoneInformations(self, Dialog, mServeurName, mConfigConnection, mSchemas, mSchemasTables, mSchemasBlocs, mRolesEditeursLecteurs, mRolesProducteurs, mlisteDesRolesDeGroupeEtConnexions ) :
        #-- FILTRE schémas / obj
        self.mServeurNameFilter, self.mConfigConnectionFilter, self.mSchemasFilter, self.mSchemasTablesFilter, self.mSchemasBlocsFilter, self.mRolesEditeursLecteursFilter, self.mRolesProducteursFilter = mServeurName, mConfigConnection, mSchemas, mSchemasTables, mSchemasBlocs, mRolesEditeursLecteurs, mRolesProducteurs
        #-- FILTRE schémas / obj
        
        Dialog.resize(self.lScreenDialog, self.hScreenDialog)
        debut = time.time()
        if hasattr(self, 'mTreePostgresql') :
           self.mTreePostgresql.setVisible(False)
        self.mTreePostgresql = TREEVIEWASGARD(self.groupBoxAffichageLeft)
        self.mTreePostgresql.setObjectName("mTreePostgresql")
        self.mTreePostgresql.clear()
        
        self.mTreePostgresql.affiche(Dialog, self.myPathIcon, mServeurName, mConfigConnection, mSchemas, mSchemasTables, mSchemasBlocs, mRolesEditeursLecteurs, mRolesProducteurs, self.zoneFilter.text())
        self.mTreePostgresql.show()
        #print("mTreePostgresql   %s" %(str(format(time.time()-debut,".3f"))))
        
        if hasattr(self, 'mTreePostgresqlDroits') :
           self.mTreePostgresqlDroits.setVisible(False)
        self.mTreePostgresqlDroits = TREEVIEWASGARDDROITS(self.groupBoxAffichageLeftDroits)
        self.mTreePostgresqlDroits.setObjectName("mTreePostgresqlDroits")
        self.mTreePostgresqlDroits.clear()
        self.mTreePostgresqlDroits.afficheDroits(Dialog, self.myPathIcon, mServeurName, mConfigConnection, mlisteDesRolesDeGroupeEtConnexions) 
        self.mTreePostgresqlDroits.show()
        #print("mTreePostgresqlDroits   %s" %(str(format(time.time()-debut,".3f"))))
        
        if hasattr(self, 'mTreePostgresqlMembresOutGroupe') :
           self.mTreePostgresqlMembresOut.setVisible(False)
        self.mTreePostgresqlMembresOut = TREEVIEWASGARDMEMBRESOUT(self.groupBoxAffichageRoleAppartOut)
        self.mTreePostgresqlMembresOut.clear()
        #-
        if hasattr(self, 'mTreePostgresqlMembresOutBIS') :
           self.mTreePostgresqlMembresOutBIS.setVisible(False)
        self.mTreePostgresqlMembresOutBIS = TREEVIEWASGARDMEMBRESOUT(self.groupBoxAffichageRoleAppartOutBIS)
        self.mTreePostgresqlMembresOutBIS.clear()
           
        if hasattr(self, 'mTreePostgresqlMembresIn') :
           self.mTreePostgresqlMembresIn.setVisible(False)
        self.mTreePostgresqlMembresIn  = TREEVIEWASGARDMEMBRESIN(self.groupBoxAffichageRoleAppartIn)
        self.mTreePostgresqlMembresIn.clear()
        #-
        if hasattr(self, 'mTreePostgresqlMembresInBIS') :
           self.mTreePostgresqlMembresInBIS.setVisible(False)
        self.mTreePostgresqlMembresInBIS  = TREEVIEWASGARDMEMBRESIN(self.groupBoxAffichageRoleAppartInBIS)
        self.mTreePostgresqlMembresInBIS.clear()
        #print("mTreePostgresqlMembresOut   %s" %(str(format(time.time()-debut,".3f"))))

        mServeurName = QtWidgets.QApplication.translate("bibli_asgard", "Does not belong", None)
        mServeurName = QtWidgets.QApplication.translate("bibli_asgard", "Belongs", None)
        
        #Tree Schemas (edit, lect, prod)
        if hasattr(self, 'mTreePostgresqlSchemaLecteur') :
           self.mTreePostgresqlSchemaLecteur.setVisible(False)
        self.mTreePostgresqlSchemaLecteur  = TREEVIEWASGARDSCHEMALECTEUR(self.groupBoxAffichageRightDroitsSchemas)
        self.mTreePostgresqlSchemaLecteur.clear()
        #print("mTreePostgresqlSchemaLecteur   %s" %(str(format(time.time()-debut,".3f"))))

        if hasattr(self, 'mTreePostgresqlSchemaEditeur') :
           self.mTreePostgresqlSchemaEditeur.setVisible(False)
        self.mTreePostgresqlSchemaEditeur  = TREEVIEWASGARDSCHEMAEDITEUR(self.groupBoxAffichageRightDroitsSchemas)
        self.mTreePostgresqlSchemaEditeur.clear()
        #print("mTreePostgresqlSchemaEditeur   %s" %(str(format(time.time()-debut,".3f"))))

        if hasattr(self, 'mTreePostgresqlSchemaProducteur') :
           self.mTreePostgresqlSchemaProducteur.setVisible(False)
        self.mTreePostgresqlSchemaProducteur  = TREEVIEWASGARDSCHEMAPRODUCTEUR(self.groupBoxAffichageRightDroitsSchemas)
        self.mTreePostgresqlSchemaProducteur.clear()
        #print("mTreePostgresqlSchemaProducteur   %s" %(str(format(time.time()-debut,".3f"))))
        return

    # FILTER -----------------------------------
    def onChanged(self,mTextFilter):
        self.Dialog.groupBoxAffichageSchema.setVisible(False)
        self.Dialog.groupBoxAffichageHelp.setVisible(False)
        mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = self.returnItemTreePostgresql("LOAD", self.mTreePostgresql, "", "")
        if hasattr(self, 'mTreePostgresql') :
           self.mTreePostgresql.setVisible(False)
        self.mTreePostgresql = TREEVIEWASGARD(self.groupBoxAffichageLeft)
        self.mTreePostgresql.setObjectName("mTreePostgresql")
        self.mTreePostgresql.clear()
        self.mTreePostgresql.affiche(self.Dialog, self.myPathIcon, self.mServeurNameFilter, self.mConfigConnectionFilter, self.mSchemasFilter, self.mSchemasTablesFilter, self.mSchemasBlocsFilter, self.mRolesEditeursLecteursFilter, self.mRolesProducteursFilter, mTextFilter)
        self.mTreePostgresql.show()
        self.returnItemTreePostgresql("RESTORE", self.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
        return
        
    def onChangeCaseFilter(self, mTextFilter):
        self.Dialog.groupBoxAffichageSchema.setVisible(False)
        self.Dialog.groupBoxAffichageHelp.setVisible(False)
        mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = self.returnItemTreePostgresql("LOAD", self.mTreePostgresql, "", "")
        if hasattr(self, 'mTreePostgresql') :
           self.mTreePostgresql.setVisible(False)
        self.mTreePostgresql = TREEVIEWASGARD(self.groupBoxAffichageLeft)
        self.mTreePostgresql.setObjectName("mTreePostgresql")
        self.mTreePostgresql.clear()
        self.mTreePostgresql.affiche(self.Dialog, self.myPathIcon, self.mServeurNameFilter, self.mConfigConnectionFilter, self.mSchemasFilter, self.mSchemasTablesFilter, self.mSchemasBlocsFilter, self.mRolesEditeursLecteursFilter, self.mRolesProducteursFilter, mTextFilter)
        self.mTreePostgresql.show()
        self.returnItemTreePostgresql("RESTORE", self.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
        return
    # FILTER -----------------------------------

    #-----------------------------------
    def reloadBase(self):
        if hasattr(self, 'mBaseAsGard') :
           if hasattr(self, 'mTreePostgresql') :
              mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = self.returnItemTreePostgresql("LOAD", self.mTreePostgresql, "", "")
           if hasattr(self, 'mTreePostgresqlDroits') :
              mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = self.returnItemTreePostgresql("LOAD", self.mTreePostgresqlDroits, "", "")
           self.initGeneral(self.Dialog)
           if hasattr(self, 'mTreePostgresql') :
              self.returnItemTreePostgresql("RESTORE", self.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
           if hasattr(self, 'mTreePostgresqlDroits') :
              self.returnItemTreePostgresql("RESTORE", self.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)
        #--------------------------
        self.dashBoard     = bibli_asgard.returnAndSaveDialogParam(self, "Load")["dashBoard"]     #Onglet dashBord

        if self.dashBoard != 'true':
           self.tabWidget.removeTab(2)
        else : 
           self.tabWidget.insertTab(2, self.tab_widget_Dash, self.labelTab_Dash)
        self.tabWidget.setCurrentIndex(0)

        return

    #-----------------------------------
    def returnItemTreePostgresql(self, mActionTreeItem, mTree, mObjetSave, mObjetSelect) :

        if mActionTreeItem == "LOAD" :
           mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = [], []
           #----
           iterator = QTreeWidgetItemIterator(mTree)
           while iterator.value():
              itemValue = iterator.value()
              #----
              if mTree.objectName() == "mTreePostgresql" :
                 if itemValue.isExpanded() or itemValue.isSelected() :
                    mReturnItemTreePostgresql.append(itemValue.text(0))
                 if itemValue.isSelected() : 
                    if itemValue.parent() != None : 
                       if itemValue.parent().parent() == None : 
                          mReturnItemTreePostgresqlSelect.append(itemValue.text(0))
              #----
              elif mTree.objectName() == "mTreePostgresqlDroits" :
                 if itemValue.isExpanded() or itemValue.isSelected() :
                    mReturnItemTreePostgresql.append(itemValue.text(0))
                 if itemValue.isSelected() : 
                    mReturnItemTreePostgresqlSelect.append(itemValue.text(0))
              iterator += 1

           return mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect

        elif mActionTreeItem == "RESTORE" :
           iterator = QTreeWidgetItemIterator(mTree)
           while iterator.value():
              itemValue = iterator.value()
              itemText = iterator.value().text(0)
              for mBlocSchema in mObjetSave :
                  if itemText == mBlocSchema :
                     itemValue.setExpanded(True)
                  if itemText in mObjetSelect :
                     mTree.setCurrentItem(itemValue)
                     if hasattr(mTree, 'ihms') :
                        mTree.ihms(itemValue, 0)
                     if hasattr(mTree, 'ihmsDroits') :
                        mTree.ihmsDroits(itemValue, 0)
              iterator += 1
           return
          
    #-----------------------------------
    def myHelpAM(self):
        #-
        MonFichierPath = os.path.join(os.path.dirname(__file__) + "/doc/")
        MonFichierPath = MonFichierPath.replace("\\","/")
        mFileLocale = "am_doc.pdf"
        MonFichierDoc = os.path.join(MonFichierPath, mFileLocale)
        #-
        if self.fileHelp == "pdf" :
           valueDefautFileHelp = self.fileHelpPdf
        elif self.fileHelp == "html" :
           valueDefautFileHelp  = self.fileHelpHtml
        else :
           valueDefautFileHelp  = self.fileHelpHtml
        
        bibli_asgard.execPdf(valueDefautFileHelp)
        return

    #==================================================
    # Gestion des actions générales du menu de la boite de dialogue
    def dialogueConfirmationAction(self, mDialog, mBaseAsGard, mTypeAction, mKeySqlTransformee):
        d = doconfirme.Dialog(mDialog, mBaseAsGard, mTypeAction, mKeySqlTransformee)
        d.exec_() 
        
    #==================================================
    # Gestion du click sur les onglets pour traiter le tableau de bord
    def clickOngletTabWidget(self, posTab):
        print("toto")
        print(posTab)
                 