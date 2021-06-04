# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QAction, QMenu , QApplication, QMessageBox, QFileDialog, QTextEdit, QMainWindow, 
                            QTableView, QDockWidget, QVBoxLayout, QTabWidget, QWidget, QAbstractItemView)
 
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *

from . import bibli_asgard
from .bibli_asgard import *
import os
import sys
from qgis.PyQt.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
import textwrap


#==================================================
# Gestion de l'IHM pour les schémas
#==================================================
    
def createIHMAffichageDiagnostic(self) :
    self.zone_affichage_diagnostic = QtWidgets.QTextEdit(self.displayInformationsDiagnostic)
    self.zone_affichage_diagnostic.setGeometry(QtCore.QRect(10, 10, self.displayInformationsDiagnostic.width() -20 ,self.displayInformationsDiagnostic.height() - 20))
    self.zone_affichage_diagnostic.setObjectName("zone_affichage_diagnostic") 
    self.zone_affichage_diagnostic.setAcceptRichText(True)

    
    return
#==================================================
# Gestion de l'IHM pour les schémas
#==================================================
    
def createIHMAffichageDash(self) :
    if hasattr(self, 'connectBaseAsgard') :
       mConfigConnection = self.connectBaseAsgard[2].split()
       #self.dbName    = [ elem for elem in mConfigConnection if "dbname=" in elem ][0].split('=')[1]  #Nom de la base de données
    else :
       self.dbName = "Ma base de données"
       
    self.labelChoiceGraph = QtWidgets.QLabel(self.groupBoxAffichageLeftDash)
    self.labelChoiceGraph.setGeometry(QtCore.QRect(15,6,self.groupBoxAffichageLeftDash.width() - 20,20))
    self.labelChoiceGraph.setObjectName("labelChoiceGraph")
    self.labelChoiceGraph.setAlignment(Qt.AlignLeft)
    self.comboChoiceGraph = QtWidgets.QComboBox(self.groupBoxAffichageLeftDash)
    self.comboChoiceGraph.setGeometry(QtCore.QRect(10,21,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.comboChoiceGraph.setObjectName("comboChoiceGraph")
    #--------
    self.dicChoiceGraph = {
                          "Aucun"                                 : ["","",""] ,
                          "Volumes des bases de données"          : ["graph1","graph1_v_d_bdd","Pourcentage du volume des bases de données"] ,
                          "Volumes de la base 'Asgard' par blocs" : ["graph3","graph1_v_bdd_par_b","Pourcentage par bloc du volume de la base de données Asgard"] ,
                          "Ventilation des schémas par blocs"     : ["graph2","graph2_s_par_b", "Ventilation des schémas <b>ACTIFS</b> par blocs : <b>" + self.dbName + "</b>"] 
                          } 
    self.listChoiceGraph = [ key for key, value in self.dicChoiceGraph.items() ]                
    self.comboChoiceGraph.addItems(self.listChoiceGraph)
    self.comboChoiceGraph.setCurrentIndex(0)
    self.comboChoiceGraph.currentIndexChanged.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 

    #-- Cadre Paramètres
    self.groupBoxParametre = QtWidgets.QGroupBox(self.groupBoxAffichageLeftDash)
    self.groupBoxParametre.setGeometry(QtCore.QRect(10,50,self.groupBoxAffichageLeftDash.width() - 20, 235))
    self.groupBoxParametre.setObjectName("groupBoxParametre")
    self.groupBoxParametre.setStyleSheet("QGroupBox {   \
                                border-width: 2px;       \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                }")
 
    #Radio pie/bar
    self.groupBoxRadioPieBar = QtWidgets.QGroupBox(self.groupBoxAffichageLeftDash)
    self.groupBoxRadioPieBar.setGeometry(QtCore.QRect(10,50,self.groupBoxAffichageLeftDash.width() - 20, 45))
    self.groupBoxRadioPieBar.setObjectName("groupBoxRadioPieBar")
    self.groupBoxRadioPieBar.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")        
    self.labelTypeGraph = QtWidgets.QLabel(self.groupBoxRadioPieBar)
    self.labelTypeGraph.setGeometry(QtCore.QRect(5,5,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.labelTypeGraph.setObjectName("labelTypeGraph")
    self.labelTypeGraph.setAlignment(Qt.AlignLeft)
    #--
    self.radioPie = QtWidgets.QRadioButton(self.groupBoxRadioPieBar)
    self.radioPie.setGeometry(QtCore.QRect(35,10,50,23))
    self.radioPie.setObjectName("radioPie")
    self.radioBar = QtWidgets.QRadioButton(self.groupBoxRadioPieBar)
    self.radioBar.setGeometry(QtCore.QRect(35,25,50,20))
    self.radioBar.setObjectName("radioBar")
    self.radioPie.setChecked(True)
    self.radioPie.toggled.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 
    self.radioBar.toggled.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 
    #--
    self.spinBoxHole = QtWidgets.QDoubleSpinBox(self.groupBoxRadioPieBar)
    self.spinBoxHole.setGeometry(QtCore.QRect(90,12,50,20))
    self.spinBoxHole.setMaximum(1.00)
    self.spinBoxHole.setMinimum(0.00)
    self.spinBoxHole.setValue(0.15)
    self.spinBoxHole.setSingleStep(0.05)
    self.spinBoxHole.setDecimals(2)
    self.spinBoxHole.setObjectName("spinBoxHole")
    #--
    self.spinBoxMiddle = QtWidgets.QDoubleSpinBox(self.groupBoxRadioPieBar)
    self.spinBoxMiddle.setGeometry(QtCore.QRect(150,12,50,20))
    self.spinBoxMiddle.setMaximum(1.00)
    self.spinBoxMiddle.setMinimum(0.00)
    self.spinBoxMiddle.setValue(0.50)
    self.spinBoxMiddle.setSingleStep(0.05)
    self.spinBoxMiddle.setDecimals(2)
    self.spinBoxMiddle.setObjectName("spinBoxMiddle")
    self.spinBoxMiddle.setEnabled(False)
    #--
    self.spinBoxMax = QtWidgets.QDoubleSpinBox(self.groupBoxRadioPieBar)
    self.spinBoxMax.setGeometry(QtCore.QRect(210,12,50,20))
    self.spinBoxMax.setMaximum(1.00)
    self.spinBoxMax.setMinimum(0.00)
    self.spinBoxMax.setValue(0.70)
    self.spinBoxMax.setSingleStep(0.05)
    self.spinBoxMax.setDecimals(2)
    self.spinBoxMax.setObjectName("spinBoxMax")
    #--
    self.groupBoxBar = QtWidgets.QGroupBox(self.groupBoxRadioPieBar)
    self.groupBoxBar.setGeometry(QtCore.QRect(10,30,self.groupBoxRadioPieBar.width() - 20, 25))
    self.groupBoxBar.setObjectName("groupBoxBar")
    self.groupBoxBar.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }") 
    self.groupBoxBar.setVisible(False)
    #--
    self.radioBarAuto = QtWidgets.QRadioButton(self.groupBoxBar)
    self.radioBarAuto.setGeometry(QtCore.QRect(90,-5,50,20))
    self.radioBarAuto.setObjectName("radioBarAuto")
    self.radioBarFull = QtWidgets.QRadioButton(self.groupBoxBar)
    self.radioBarFull.setGeometry(QtCore.QRect(150,-5,50,23))
    self.radioBarFull.setObjectName("radioBarFull")
    self.radioBarAuto.setChecked(True)
    #--

    self.groupBoxCheckEtiquette = QtWidgets.QGroupBox(self.groupBoxAffichageLeftDash)
    self.groupBoxCheckEtiquette.setGeometry(QtCore.QRect(10,95,self.groupBoxAffichageLeftDash.width() - 20, 65))
    self.groupBoxCheckEtiquette.setObjectName("groupBoxCheckEtiquette")
    self.groupBoxCheckEtiquette.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")        
    self.caseEtiGraph = QtWidgets.QCheckBox(self.groupBoxCheckEtiquette)    
    self.caseEtiGraph.setGeometry(QtCore.QRect(5,0,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseEtiGraph.setObjectName("caseEtiGraph")
    self.caseEtiGraph.setChecked(True) 
    self.caseEtiGraph.toggled.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 
    #--
    self.caseEtiLibelle = QtWidgets.QCheckBox(self.groupBoxCheckEtiquette)    
    self.caseEtiLibelle.setGeometry(QtCore.QRect(35,15,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseEtiLibelle.setObjectName("caseEtiLibelle")
    self.caseEtiLibelle.setChecked(True) 
    #--
    self.caseEtiPourc = QtWidgets.QCheckBox(self.groupBoxCheckEtiquette)    
    self.caseEtiPourc.setGeometry(QtCore.QRect(35,30,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseEtiPourc.setObjectName("caseEtiPourc")
    self.caseEtiPourc.setChecked(False) 
    #--
    self.caseEtiValeur = QtWidgets.QCheckBox(self.groupBoxCheckEtiquette)    
    self.caseEtiValeur.setGeometry(QtCore.QRect(35,45,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseEtiValeur.setObjectName("caseEtiValeur")
    self.caseEtiValeur.setChecked(False) 
    #--
    #Chekcked Legende
    self.groupBoxCheckLegende = QtWidgets.QGroupBox(self.groupBoxAffichageLeftDash)
    self.groupBoxCheckLegende.setGeometry(QtCore.QRect(10,160,self.groupBoxAffichageLeftDash.width() - 20, 80))
    self.groupBoxCheckLegende.setObjectName("groupBoxCheckLegende")
    self.groupBoxCheckLegende.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")        
    self.caseLegGraph = QtWidgets.QCheckBox(self.groupBoxCheckLegende)    
    self.caseLegGraph.setGeometry(QtCore.QRect(5,0,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseLegGraph.setObjectName("LabelLegGraph")
    self.caseLegGraph.setChecked(True) 
    self.caseLegGraph.toggled.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 
    #--
    self.caseLegNord = QtWidgets.QRadioButton(self.groupBoxCheckLegende)    
    self.caseLegNord.setGeometry(QtCore.QRect(35,15,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseLegNord.setObjectName("caseLegNord")
    self.caseLegNord.setChecked(True) 
    #--
    self.caseLegOuest = QtWidgets.QRadioButton(self.groupBoxCheckLegende)    
    self.caseLegOuest.setGeometry(QtCore.QRect(35,30,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseLegOuest.setObjectName("caseLegOuest")
    self.caseLegOuest.setChecked(False) 
    #--
    self.caseLegEst = QtWidgets.QRadioButton(self.groupBoxCheckLegende)    
    self.caseLegEst.setGeometry(QtCore.QRect(35,45,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseLegEst.setObjectName("caseLegEst")
    self.caseLegEst.setChecked(False) 
    #--
    self.caseLegSud = QtWidgets.QRadioButton(self.groupBoxCheckLegende)    
    self.caseLegSud.setGeometry(QtCore.QRect(35,60,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseLegSud.setObjectName("caseLegSud")
    self.caseLegSud.setChecked(False) 
    #--
    #--
    #Titre et animation
    self.groupBoxCheckTitreAnim = QtWidgets.QGroupBox(self.groupBoxAffichageLeftDash)
    self.groupBoxCheckTitreAnim.setGeometry(QtCore.QRect(10,240,self.groupBoxAffichageLeftDash.width() - 20, 55))
    self.groupBoxCheckTitreAnim.setObjectName("groupBoxCheckTitreAnim")
    self.groupBoxCheckTitreAnim.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }")        
    self.caseTitreGraph = QtWidgets.QCheckBox(self.groupBoxCheckTitreAnim)    
    self.caseTitreGraph.setGeometry(QtCore.QRect(5,0,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseTitreGraph.setObjectName("LabelTitreGraph")
    self.caseTitreGraph.setChecked(True) 
    self.caseTitreGraph.toggled.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 
    #--
    self.zoneTitre = QtWidgets.QLineEdit(self.groupBoxCheckTitreAnim)    
    self.zoneTitre.setGeometry(QtCore.QRect(50,2,self.groupBoxAffichageLeftDash.width() - 75,20))
    self.zoneTitre.setObjectName("zoneTitre")
    #--
    self.caseAnimationGraph = QtWidgets.QCheckBox(self.groupBoxCheckTitreAnim)    
    self.caseAnimationGraph.setGeometry(QtCore.QRect(5,20,self.groupBoxAffichageLeftDash.width() - 20,23))
    self.caseAnimationGraph.setObjectName("caseAnimationGraph")
    self.caseAnimationGraph.setChecked(True) 
    #--

    #--------                   
    #Tree Schemas (Schémas par blocs)
    self.mTreeGraphSchemasBlocs  = bibli_asgard.TREEVIEWASGARDGRAPHSCHEMASBLOCS(self.groupBoxAffichageLeftDash)
    self.mTreeGraphSchemasBlocs.setVisible(False)
    #--------                   
    self.executeButtonGraphColor = QtWidgets.QPushButton(self.groupBoxAffichageLeftDash)
    self.executeButtonGraphColor.setGeometry(QtCore.QRect(self.groupBoxAffichageLeftDash.width()/2 - 50, self.groupBoxAffichageLeftDash.height() - 55, 100,23))
    self.executeButtonGraphColor.setObjectName("executeButtonGraphColor") 
    #--------                   
    self.executeButtonGraph = QtWidgets.QPushButton(self.groupBoxAffichageLeftDash)
    self.executeButtonGraph.setGeometry(QtCore.QRect(self.groupBoxAffichageLeftDash.width()/2 - 50, self.groupBoxAffichageLeftDash.height() - 30, 100,23))
    self.executeButtonGraph.setObjectName("executeButtonSchema") 

    self.executeButtonGraphColor.setGeometry(QtCore.QRect((self.groupBoxAffichageLeftDash.width() - 200) / 3, self.groupBoxAffichageLeftDash.height() - 30, 100,23))
    self.executeButtonGraph.setGeometry(QtCore.QRect(((self.groupBoxAffichageLeftDash.width() - 200) / 3 * 2) + 100, self.groupBoxAffichageLeftDash.height() - 30, 100,23))

    #Connections 
    self.executeButtonGraphColor.clicked.connect(lambda : bibli_graph_asgard.executeGraphColorBloc(self))
    self.executeButtonGraph.clicked.connect(lambda : bibli_graph_asgard.executeGraphQml(self))
    self.comboChoiceGraph.currentIndexChanged.connect(lambda : ShowHideTreeGraphSchemaBlocs(self)) 

    #--------  
    #--------  
    mX = self.groupBoxAffichageLeftDash.width() + 10
    mY = 0
    mL = self.displayInformationsDash.width() - self.groupBoxAffichageLeftDash.width() - 10
    mH = self.displayInformationsDash.height() - 0
    self.groupBoxAffichageRightDash = QtWidgets.QGroupBox(self.displayInformationsDash)
    self.groupBoxAffichageRightDash.setGeometry(QtCore.QRect(mX, mY, mL, mH))
    self.groupBoxAffichageRightDash.setObjectName("groupBoxAffichageRightDash")
    self.groupBoxAffichageRightDash.setStyleSheet("QGroupBox {   \
                                border-style: dashed;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }") 
    self.groupBoxAffichageRightDash.setVisible(True)

def ShowHideTreeGraphSchemaBlocs(self) :
    mChoixGraph     = self.comboChoiceGraph.currentText()
    mTypeGraph      = self.dicChoiceGraph[mChoixGraph][0]

    if hasattr(self, 'connectBaseAsgard') :
       mConfigConnection = self.connectBaseAsgard[2].split()
       #self.dbName    = [ elem for elem in mConfigConnection if "dbname=" in elem ][0].split('=')[1]  #Nom de la base de données
    else :
       self.dbName = "Ma base de données"
    #print("ShowHideTreeGraphSchemaBlocs" + str(self.dbName))

    if mTypeGraph == "graph1" or mTypeGraph == "graph3" :
       mTitre = self.dicChoiceGraph[mChoixGraph][2]   
    elif mTypeGraph == "graph2" :
       mTitre = "Ventilation des schémas <b>ACTIFS</b> par blocs : <b>" + self.dbName + "</b>"    
    elif mChoixGraph == 'Aucun' :
          mTitre = ""    
   
    #Ctrl Paramètres
    #-
    if mTypeGraph == "graph2" :
       self.radioPie.setChecked(True)
       self.radioBar.setEnabled(False)
    else :
       self.radioBar.setEnabled(True)
    #-
    if self.radioPie.isChecked() :
       self.groupBoxBar.setVisible(False) 
       self.spinBoxHole.setVisible(True) 
       self.spinBoxMiddle.setVisible(True) 
       self.spinBoxMax.setVisible(True) 
    elif self.radioBar.isChecked() :
       self.groupBoxBar.setVisible(True) 
       self.spinBoxHole.setVisible(False) 
       self.spinBoxMiddle.setVisible(False) 
       self.spinBoxMax.setVisible(False) 
    #-
    if self.caseEtiGraph.isChecked() :
       self.caseEtiLibelle.setEnabled(True)
       self.caseEtiPourc.setEnabled(True)
       self.caseEtiValeur.setEnabled(True)
    else :
       self.caseEtiLibelle.setEnabled(False)
       self.caseEtiPourc.setEnabled(False)
       self.caseEtiValeur.setEnabled(False)
    #-
    if self.caseLegGraph.isChecked() :
       self.caseLegNord.setEnabled(True)
       self.caseLegOuest.setEnabled(True)
       self.caseLegEst.setEnabled(True)
       self.caseLegSud.setEnabled(True)
    else :
       self.caseLegNord.setEnabled(False)
       self.caseLegOuest.setEnabled(False)
       self.caseLegEst.setEnabled(False)
       self.caseLegSud.setEnabled(False)
    #-
    if self.caseTitreGraph.isChecked() :
       self.zoneTitre.setEnabled(True)
    else :
       self.zoneTitre.setEnabled(False)

    self.zoneTitre.setText(mTitre)
    #-
      
    #Tree Bloc
    if mTypeGraph == "graph1" or mTypeGraph == "graph3" :
       if hasattr(self, 'mTreeGraphSchemasBlocs') :
          self.mTreeGraphSchemasBlocs.setVisible(False)
       self.spinBoxMiddle.setEnabled(False)
    elif mTypeGraph == "graph2" :
       if hasattr(self, 'mTreeGraphSchemasBlocs') :
          mCountItem = 0
          iterator = QTreeWidgetItemIterator(self.mTreeGraphSchemasBlocs)

          while iterator.value():
             mCountItem += 1
             iterator += 1

          if mCountItem == 0 : 
             self.mTreeGraphSchemasBlocs.clear()
             self.mTreeGraphSchemasBlocs.afficheGraphSchemasBlocs(self.Dialog, self.myPathIcon, self.mSchemasBlocs)
             self.mTreeGraphSchemasBlocs.show()    
          self.mTreeGraphSchemasBlocs.setVisible(True)
       self.spinBoxMiddle.setEnabled(True)
          
    if hasattr(self, 'mVisuWeb') :
       if mChoixGraph == 'Aucun' :
          self.mVisuWeb.effaceContenu()
    return
#==================================================
# Gestion de l'IHM pour les droits
#==================================================
def createIHMAffichageDroits(self) :
    self.groupBoxAffichageRightDroits = QtWidgets.QGroupBox(self.displayInformationsDroits)
    self.groupBoxAffichageRightDroits.setGeometry(QtCore.QRect(self.groupBoxAffichageLeftDroits.width() + 10, 0, 400, self.displayInformationsDroits.height() - 0))
    self.groupBoxAffichageRightDroits.setObjectName("groupBoxAffichageRightDroits")
    self.groupBoxAffichageRightDroits.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }") 
    self.groupBoxAffichageRightDroits.setVisible(True)

    #==================================================
    #==================================================
    self.groupBoxAffichageRightDroitsSchemasZone = QtWidgets.QGroupBox(self.displayInformationsDroits)
    mX = self.groupBoxAffichageRightDroits.x() + self.groupBoxAffichageRightDroits.width() + 10
    mY = 0
    mL = self.displayInformationsDroits.width() - self.groupBoxAffichageLeftDroits.width() - self.groupBoxAffichageRightDroits.width() - 25
    mH = self.displayInformationsDroits.height() - 0
    self.groupBoxAffichageRightDroitsSchemasZone.setGeometry(QtCore.QRect(mX, mY, mL, mH))
    self.groupBoxAffichageRightDroitsSchemasZone.setObjectName("groupBoxAffichageRightDroitsSchemasZone")
    self.groupBoxAffichageRightDroitsSchemasZone.setStyleSheet("QGroupBox {   \
                                border-style: dashed;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }") 
    self.groupBoxAffichageRightDroitsSchemasZone.setVisible(True)
    #---------
    self.groupBoxAffichageRightDroitsSchemas = QtWidgets.QGroupBox(self.groupBoxAffichageRightDroitsSchemasZone)
    self.groupBoxAffichageRightDroitsSchemas.setGeometry(QtCore.QRect(2, 2, self.groupBoxAffichageRightDroitsSchemasZone.width() - 4, self.groupBoxAffichageRightDroitsSchemasZone.height() - 4))
    self.groupBoxAffichageRightDroitsSchemas.setObjectName("groupBoxAffichageRightDroitsSchemas")
    self.groupBoxAffichageRightDroitsSchemas.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 0px;       \
                                border-radius: 10px;     \
                                border-color: red;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }") 
    self.groupBoxAffichageRightDroitsSchemas.setVisible(False)

    #==================================================
    #Affichage Help
    self.groupBoxAffichageHelpDroits = QtWidgets.QGroupBox(self.groupBoxAffichageRightDroits)
    self.groupBoxAffichageHelpDroits.setGeometry(QtCore.QRect(10, 10, self.Dialog.groupBoxAffichageRightDroits.width() - 20, self.Dialog.groupBoxAffichageRightDroits.height() - 20))
    self.groupBoxAffichageHelpDroits.setObjectName("groupBoxAffichageHelpDroits")
    self.groupBoxAffichageHelpDroits.setStyleSheet("QGroupBox {   \
                                border-width: 0px;       \
                                border-color: green;      \
                                }") 
    #Generation de l'aide
    genereAideDynamiqueDroits(self,"CREATE", [100,101,102,103,104, 105, 106, 107, 1060, 1070, 108])
    self.groupBoxAffichageHelpDroits.setVisible(False)
                                    
    #==================================================
    #Option Roles et Groupes Attributs
    self.groupBoxAffichageRoleAttribut= QtWidgets.QGroupBox(self.groupBoxAffichageRightDroits)
    self.groupBoxAffichageRoleAttribut.setGeometry(QtCore.QRect(5,5,self.Dialog.groupBoxAffichageRightDroits.width() - 10 , 185))
    self.groupBoxAffichageRoleAttribut.setObjectName("groupBoxAffichageRoleAttribut")
    self.groupBoxAffichageRoleAttribut.setStyleSheet("QGroupBox {   \
                                border-width: 0px;       \
                                border-color: #958B62;      \
                                }") 
    #--------  
    self.groupBoxAffichageRoleAttributGenerale = QtWidgets.QGroupBox(self.groupBoxAffichageRoleAttribut)
    self.groupBoxAffichageRoleAttributGenerale.setGeometry(QtCore.QRect(5,5,380, 120))
    self.groupBoxAffichageRoleAttributGenerale.setObjectName("groupBoxAffichageRoleAttributGenerale")  
    self.groupBoxAffichageRoleAttributGenerale.setStyleSheet("QGroupBox {   \
                                border-width: 2px;       \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                }")
    #--------  
    self.label_rolname = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributGenerale)     
    self.label_rolname.setGeometry(QtCore.QRect(0,19,118,18))
    self.label_rolname.setObjectName("label_rolname")
    self.label_rolname.setAlignment(Qt.AlignRight)
    #--------                            
    self.zone_rolnameID = QtWidgets.QLineEdit(self.groupBoxAffichageRoleAttributGenerale)
    self.zone_rolnameID.setGeometry(QtCore.QRect(130,15,220,23))
    self.zone_rolnameID.setObjectName("zone_rolnameID") 
    self.zone_rolnameID.setVisible(False) #Gestion Id
    #
    self.zone_rolname = QtWidgets.QLineEdit(self.groupBoxAffichageRoleAttributGenerale)
    self.zone_rolname.setGeometry(QtCore.QRect(130,15,220,23))
    self.zone_rolname.setObjectName("zone_rolname") 
    #--------  
    self.label_description = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributGenerale)     
    self.label_description.setGeometry(QtCore.QRect(0,49,118,18))
    self.label_description.setObjectName("label_description")
    self.label_description.setAlignment(Qt.AlignRight)
    #--------                            
    self.zone_description = QtWidgets.QTextEdit(self.groupBoxAffichageRoleAttributGenerale)
    self.zone_description.setGeometry(QtCore.QRect(130,45,220,36))
    self.zone_description.setObjectName("zone_description") 
    #--------  
    self.label_mdp = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributGenerale)     
    self.label_mdp.setGeometry(QtCore.QRect(0,92,118,18))
    self.label_mdp.setObjectName("label_mdp")
    self.label_mdp.setAlignment(Qt.AlignRight)
    #--------                            
    self.zone_mdp = QtWidgets.QLineEdit(self.groupBoxAffichageRoleAttributGenerale)
    self.zone_mdp.setGeometry(QtCore.QRect(130,88,220,23))
    self.zone_mdp.setObjectName("zone_mdp") 
    self.zone_mdp.setEnabled(False)
    #--------  
    self.groupBoxAffichageRoleAttributDroits = QtWidgets.QGroupBox(self.groupBoxAffichageRoleAttribut)
    self.groupBoxAffichageRoleAttributDroits.setGeometry(QtCore.QRect(5, 130, 380, 50))
    self.groupBoxAffichageRoleAttributDroits.setObjectName("groupBoxAffichageRoleAttributDroits")  
    self.groupBoxAffichageRoleAttributDroits.setStyleSheet("QGroupBox {   \
                                border-width: 2px;       \
                                border-color: #958B62;     \
                                font: bold 11px;         \
                                }") 
    #--------  
    self.label_simplecomplet = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_simplecomplet.setGeometry(QtCore.QRect(80,9,160,18))
    self.label_simplecomplet.setObjectName("label_simplecomplet")
    self.label_simplecomplet.setAlignment(Qt.AlignRight)
    #--------                            
    self.label_simplecomplet.setStyleSheet("QLabel {   \
                                font :italic; font-weight: bold ;     \
                                color: #958B62;      \
                                }") 
    #--------                            
    self.case_simplecomplet = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_simplecomplet.setGeometry(QtCore.QRect(250,5,30,23))
    self.case_simplecomplet.setObjectName("case_simplecomplet")
    self.case_simplecomplet.setChecked(False) 
    #Connections 
    self.case_simplecomplet.clicked.connect(lambda : showHideCtrlSimpleComplet(self, self.case_simplecomplet.isChecked()))
    #--------  
    self.label_rolcreaterole = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_rolcreaterole.setGeometry(QtCore.QRect(0,29,120,18))
    self.label_rolcreaterole.setObjectName("label_rolcreaterole")
    self.label_rolcreaterole.setAlignment(Qt.AlignRight)
    #--------                            
    self.case_rolcreaterole = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_rolcreaterole.setGeometry(QtCore.QRect(130,24,23,23))
    self.case_rolcreaterole.setObjectName("case_rolcreaterole")
    self.case_rolcreaterole.setChecked(False)                                  
    #--------  
    mMessToolTipTexte = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Grant the 'CREATE' right on the database and make the schema editor member role Z_ASGARD", None)
    self.label_rolgestionschema = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_rolgestionschema.setGeometry(QtCore.QRect(160,29,160,18))
    self.label_rolgestionschema.setObjectName("label_rolgestionschema")
    self.label_rolgestionschema.setAlignment(Qt.AlignRight)
    self.label_rolgestionschema.setToolTip("{}".format('\n'.join(returnListeTexte(self, mMessToolTipTexte, 50))))           
    #--------                            
    self.case_rolgestionschema = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_rolgestionschema.setGeometry(QtCore.QRect(330,24,23,23))
    self.case_rolgestionschema.setObjectName("case_rolgestionschema")          
    self.case_rolgestionschema.setChecked(False)
    self.case_rolgestionschema.setToolTip("{}".format('\n'.join(returnListeTexte(self, mMessToolTipTexte, 50))))           
    #-------- 
    self.label_rolsuper = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_rolsuper.setGeometry(QtCore.QRect(0,54,120,18))
    self.label_rolsuper.setObjectName("label_rolsuper")
    self.label_rolsuper.setAlignment(Qt.AlignRight)
    #--------                            
    self.case_rolsuper = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_rolsuper.setGeometry(QtCore.QRect(130,50,23,23))
    self.case_rolsuper.setObjectName("case_rolsuper")
    self.case_rolsuper.setChecked(False)                                  
    self.case_rolsuper.setEnabled(False)                                  
    #--------  
    self.label_rolinherit = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_rolinherit.setGeometry(QtCore.QRect(160,54,160,18))
    self.label_rolinherit.setObjectName("label_rolinherit")
    self.label_rolinherit.setAlignment(Qt.AlignRight)
    #--------                            
    self.case_rolinherit = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_rolinherit.setGeometry(QtCore.QRect(330,50,23,23))
    self.case_rolinherit.setObjectName("case_rolinherit")
    self.case_rolinherit.setChecked(False)
    self.case_rolinherit.setEnabled(False)
                                      
    #--------  
    self.label_rolreplication = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_rolreplication.setGeometry(QtCore.QRect(0,79,120,18))
    self.label_rolreplication.setObjectName("label_rolreplication")
    self.label_rolreplication.setAlignment(Qt.AlignRight)
    #--------                            
    self.case_rolreplication = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_rolreplication.setGeometry(QtCore.QRect(130,75,23,23))
    self.case_rolreplication.setObjectName("case_rolreplication")
    self.case_rolreplication.setChecked(False)                                  
    self.case_rolreplication.setEnabled(False)                                  
    #--------  
    self.label_rolcreatedb = QtWidgets.QLabel(self.groupBoxAffichageRoleAttributDroits)     
    self.label_rolcreatedb.setGeometry(QtCore.QRect(160,79,160,18))
    self.label_rolcreatedb.setObjectName("label_rolcreatedb")
    self.label_rolcreatedb.setAlignment(Qt.AlignRight)
    #--------                            
    self.case_rolcreatedb = QtWidgets.QCheckBox(self.groupBoxAffichageRoleAttributDroits)    
    self.case_rolcreatedb.setGeometry(QtCore.QRect(330,75,23,23))
    self.case_rolcreatedb.setObjectName("case_rolcreatedb")
    self.case_rolcreatedb.setChecked(False)         #--------                                  
                                                                
    #==================================================
    #Option Roles et Groupes Appartenance
    self.groupBoxAffichageRoleAppart= QtWidgets.QGroupBox(self.groupBoxAffichageRightDroits)
    self.groupBoxAffichageRoleAppart.setGeometry(QtCore.QRect(10, self.groupBoxAffichageRoleAttribut.y() + self.groupBoxAffichageRoleAttribut.height()  ,self.Dialog.groupBoxAffichageRoleAttributGenerale.width(), self.Dialog.groupBoxAffichageRightDroits.height() - self.groupBoxAffichageRoleAttribut.height() - 50))
    self.groupBoxAffichageRoleAppart.setObjectName("groupBoxAffichageRoleAppart")
    self.groupBoxAffichageRoleAppart.setStyleSheet("QGroupBox {   \
                                border-width: 2px;       \
                                border-color: #958B62;      \
                                }") 
    #--------                                  
    self.groupBoxAffichageRoleAppartOut= QtWidgets.QGroupBox(self.groupBoxAffichageRoleAppart)
    self.groupBoxAffichageRoleAppartOut.setGeometry(QtCore.QRect(2, 2,(self.groupBoxAffichageRoleAppart.width() /2) - 10 , self.groupBoxAffichageRoleAppart.height() - 4))
    self.groupBoxAffichageRoleAppartOut.setObjectName("groupBoxAffichageRoleAppartOut")
    self.groupBoxAffichageRoleAppartOut.setStyleSheet("QGroupBox {   \
                                border-width: 0px;       \
                                border-color: #958B62;      \
                                }") 
    #------ 
    #Boutons  
    #------ 
    self.executeDroits = QtWidgets.QPushButton(self.groupBoxAffichageRoleAppart)
    self.executeDroits.setGeometry(QtCore.QRect(self.groupBoxAffichageRoleAppartOut.width() , (self.groupBoxAffichageRoleAppart.height()/2) - (self.executeDroits.height()/2) , 20, 60))
    self.executeDroits.setObjectName("executeDroits") 
    self.executeDroits.setVisible(False)
    #-------- 
    self.labelOutIn = QtWidgets.QLabel(self.groupBoxAffichageRoleAppart)     
    self.labelOutIn.setGeometry(QtCore.QRect(self.groupBoxAffichageRoleAppartOut.width() , (self.groupBoxAffichageRoleAppart.height()/2) - (self.executeDroits.height()/2) , 20, 60))
    self.labelOutIn.setObjectName("labelOutIn")
    self.labelOutIn.setVisible(False)
    #Connections 
    self.executeDroits.clicked.connect(lambda : bibli_asgard.deplaceItemOutIn(self))
                                
    #--------                                  
    self.groupBoxAffichageRoleAppartIn= QtWidgets.QGroupBox(self.groupBoxAffichageRoleAppart)
    self.groupBoxAffichageRoleAppartIn.setGeometry(QtCore.QRect((self.groupBoxAffichageRoleAppart.width() /2) + 10 , 2,(self.groupBoxAffichageRoleAppart.width() /2) - 12, self.groupBoxAffichageRoleAppart.height() - 4 ))
    self.groupBoxAffichageRoleAppartIn.setObjectName("groupBoxAffichageRoleAppartIn")
    self.groupBoxAffichageRoleAppartIn.setStyleSheet("QGroupBox {   \
                                border-width: 0px;       \
                                border-color: #958B62;      \
                                }")                                         

    #==================================================
    self.groupBoxAffichageRoleAppart.setVisible(False)
    self.groupBoxAffichageRoleAttribut.setVisible(False)
    
    #------ 
    #Boutons  
    #------ 
    self.executeButtonRole = QtWidgets.QPushButton(self.groupBoxAffichageRightDroits)
    self.executeButtonRole.setGeometry(QtCore.QRect((self.groupBoxAffichageRoleAppart.width() /2) - (self.executeButtonRole.width() /2) + self.groupBoxAffichageRoleAppart.x(), self.groupBoxAffichageRightDroits.height() - 33, 100,23))
    self.executeButtonRole.setObjectName("executeButtonRole") 
    self.executeButtonRole.setVisible(False)    
    #Connections 
    self.executeButtonRole.clicked.connect(lambda : executeSqlRole(self, self)) 

    #Translation                                                                                                                           
    self.executeButtonRole.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Apply", None))
    self.label_simplecomplet.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Simplified / Complete : ", None))
    self.label_rolname.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Name : ", None))
    self.label_description.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Comments : ", None))
    self.label_mdp.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Password : ", None))
    self.label_rolcreaterole.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "creation of roles : ", None))
    self.label_rolcreatedb.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "database creation : ", None))
    self.label_rolsuper.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "super user : ", None))
    self.label_rolinherit.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Inherits rights : ", None))
    self.label_rolreplication.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Replications : ", None))
    self.label_rolgestionschema.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "schema management : ", None))
    self.groupBoxAffichageRoleAttributGenerale.setTitle(QtWidgets.QApplication.translate("bibli_ihm_asgard", "General", None))
    self.groupBoxAffichageRoleAttributDroits.setTitle(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Rights", None))
    self.entete_GroupBoxAffichageRoleAppar_groupe = QtWidgets.QApplication.translate("bibli_ihm_asgard", "", None)
    self.entete_GroupBoxAffichageRoleAppar_role   =  QtWidgets.QApplication.translate("bibli_ihm_asgard", "", None)
    self.groupBoxAffichageRoleAppart.setTitle(self.entete_GroupBoxAffichageRoleAppar_groupe)
    #Translation
    
    #REMETTRE
    showHideCtrlSimpleComplet(self, self.case_simplecomplet.isChecked())
    return

#=========================
#=========================
def executeSqlRole(self, Dialog) :
        mode = self.mTreePostgresqlDroits.mode 
        if mode == "create" :
           mKeySql = bibli_asgard.dicListSql(self,'CreationRole')
           zMessGood = QtWidgets.QApplication.translate("asgard_general_ui", "Good you have a create rôle !!", None)
        elif mode == "update" :
           mKeySql = bibli_asgard.dicListSql(self,'ModificationRole')
           zMessGood = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Good you have a update rôle !!", None)
               
        mRolnameNewID, mRolnameOldID = self.Dialog.zone_rolnameID.text(), "#mRolnameID#"
        mRolnameNew, mRolnameOld = self.Dialog.zone_rolname.text(), "#mRolname#"
        mDescriptionNew, mDescriptionOld = self.Dialog.zone_description.toPlainText(), "#mDescription#"
        mMdpNew, mMdpOld = self.Dialog.zone_mdp.text(), "#mMdp#"
        mRolcreateroleNew, mRolcreateroleOld = (True if self.Dialog.case_rolcreaterole.isChecked() else False), "#mRolcreaterole#"
        mRolcreatedbNew, mRolcreatedbOld = (True if self.Dialog.case_rolcreatedb.isChecked() else False), "#mRolcreatedb#"
        mRolsuperNew, mRolsuperOld = (True if self.Dialog.case_rolsuper.isChecked() else False), "#mRolsuper#"
        mRolinheritNew, mRolinheritOld = (True if self.Dialog.case_rolinherit.isChecked() else False), "#mRolinherit#"
        mRolreplicationNew, mRolreplicationOld = (True if self.Dialog.case_rolreplication.isChecked() else False), "#mRolreplication#"
        mRolgestionschemaNew, mRolgestionschemaOld = (True if self.Dialog.case_rolgestionschema.isChecked() else False), "#mRolgestionschema#"
        mListeOut, mListeIn =  bibli_asgard.returnOutInListe(self )
        mListeOutNew, mListeOutOld = mListeOut, "#mListeOutNew#"
        mListeInNew, mListeInOld = mListeIn, "#mListeInNew#"
                                                                                        
        mContinue = True                                                              
        #Contrôles
        if mRolnameNew == '' and (mMdpNew == '' and self.Dialog.mTreePostgresqlDroits.mRolcanLogin and mode == "create") :
           zMess = QtWidgets.QApplication.translate("bibli_ihm_asgard", "name and password required", None) 
           mContinue = False
        elif mRolnameNew == '' : 
           zMess = QtWidgets.QApplication.translate("bibli_ihm_asgard", "name required", None) 
           mContinue = False
        elif mMdpNew == '' and self.Dialog.mTreePostgresqlDroits.mRolcanLogin and mode == "create" : 
           zMess = QtWidgets.QApplication.translate("bibli_ihm_asgard", "password required", None) 
           mContinue = False
        elif mRolnameNew in [ mName[0] for mName in self.Dialog.mTreePostgresqlDroits.ArraymRolesDeGroupe] :
           #Pas de ctrl pour update
           if mode == "create" :     
              zMess = QtWidgets.QApplication.translate("bibli_ihm_asgard", "The Name ", None) + mRolnameNew.upper() + QtWidgets.QApplication.translate("bibli_ihm_asgard", " already exists", None)
              mContinue = False
           elif mode == "update": 
             if mRolnameNew != self.mTreePostgresqlDroits.dicOldValueRole["mRolname"] :
                zMess = QtWidgets.QApplication.translate("bibli_ihm_asgard", "The Name ", None) + mRolnameNew.upper() + QtWidgets.QApplication.translate("bibli_ihm_asgard", " already exists", None)
                mContinue = False
        #------       
        if mContinue :
         #------
         if mode == "create" :
            pass
         elif mode == "update": 
           #Affichage si aucune valeur modifiée
           tId    = ('mRolnameID', 'mRolname', 'mDescription', 'mRolcreaterole', 'mRolcreatedb', 'mRolsuper', 'mRolinherit', 'mRolreplication', 'mRolgestionschema', 'mListeOut', 'mListeIn')
           tValue = (mRolnameNewID, mRolnameNew, mDescriptionNew, mRolcreateroleNew, mRolcreatedbNew, mRolsuperNew, mRolinheritNew, mRolreplicationNew, mRolgestionschemaNew, mListeOutNew, mListeInNew)
           self.dicNewValueRole = dict(zip(tId, tValue))
           dicOldValueRole =  self.mTreePostgresqlDroits.dicOldValueRole
           
           if not bibli_asgard.returnChange(dicOldValueRole, self.dicNewValueRole) and mMdpNew == '':           
              zMess  = QtWidgets.QApplication.translate("bibli_ihm_asgard", "No value changed", None)
              mContinue = False

        #------       
        if not mContinue :
           zTitre = QtWidgets.QApplication.translate("bibli_ihm_asgard", "ASGARD MANAGER : Warning", None)
           QMessageBox.warning(self, zTitre, zMess)
        else :
           #------ #Gestion des diff revoke et grant      
           if mode == "create" :
              mListeRevokeNew, mListeRevokeOld = [], "#mListeRevokeNew#"  #pas de Revoke pour Create
              mListeGrantNew,  mListeGrantOld  = mListeInNew,  "#mListeGrantNew#"
           elif mode == "update": 
              mListeRevoke =  [value for value in      dicOldValueRole["mListeIn"] if value not in self.dicNewValueRole["mListeIn"]]
              mListeGrant  =  [value for value in self.dicNewValueRole["mListeIn"] if value not in      dicOldValueRole["mListeIn"]]
              mListeRevokeNew, mListeRevokeOld = mListeRevoke, "#mListeRevokeNew#"
              mListeGrantNew,  mListeGrantOld  = mListeGrant,  "#mListeGrantNew#"

           dicReplace = {mRolnameOldID: mRolnameNewID, mRolnameOld: mRolnameNew, mDescriptionOld: mDescriptionNew, mMdpOld: mMdpNew, mRolcreateroleOld: mRolcreateroleNew, 
                         mRolcreatedbOld: mRolcreatedbNew, mRolsuperOld: mRolsuperNew, mRolinheritOld: mRolinheritNew, mRolreplicationOld: mRolreplicationNew,
                         mListeRevokeOld: mListeRevokeNew, mListeGrantOld: mListeGrantNew, mRolgestionschemaOld: mRolgestionschemaNew}

           #------ Substitution       
           for key, value in dicReplace.items():
               if key == "#mRolcreaterole#" :
                  mValue = ('CREATEROLE' if self.Dialog.case_rolcreaterole.isChecked() else 'NOCREATEROLE') 
               elif key == "#mRolcreatedb#" :
                  mValue = ('CREATEDB' if self.Dialog.case_rolcreatedb.isChecked() else 'NOCREATEDB') 
               elif key == "#mRolsuper#" :
                  mValue = ('SUPERUSER' if self.Dialog.case_rolsuper.isChecked() else 'NOSUPERUSER')
               elif key == "#mRolinherit#" :
                  mValue = ('INHERIT' if self.Dialog.case_rolinherit.isChecked() else 'NOINHERIT')
               elif key == "#mRolreplication#" :
                  mValue = ('REPLICATION' if self.Dialog.case_rolreplication.isChecked() else 'NOREPLICATION')
               elif key == "#mMdp#" :
                  if dicReplace[key] != '' :
                     mValue = "ENCRYPTED PASSWORD '" + str(value)  + "'"
                  else :
                     mValue =  ''
               else :
                  mValue = value
               dicReplace[key] = mValue
                 
           dicReplace["#mdpLogin#"] = ('NOLOGIN' if self.Dialog.mTreePostgresqlDroits.mRolcanLogin != True else 'LOGIN')   
           #-- Permet de controler si le compte est g_admin ou parent de g_admin avec CREATEROLE   SET ROLE;
           if self.role_g_admin_createrole != self.userConnecteEnCours :
              dicReplace['#Role_g_admin_createrole#'] = "SET ROLE " + str(self.role_g_admin_createrole) + ";"
              dicReplace['#ResetRole#'] = "RESET ROLE ;"
           else :
              dicReplace['#Role_g_admin_createrole#'] = ''
              dicReplace['#ResetRole#'] = ''
           dicReplace['#Rolgestionschema_cond1#'] = ''
           dicReplace['#Rolgestionschema_cond2#'] = ''
           #-
           #------                                        
           for key, value in dicReplace.items():
               if isinstance(value, bool) and key != '#mRolgestionschema#':   #Pour passer elif
                  mValue = str(value)
               elif (value is None) :
                  mValue = "''"
               else :
                  if key != "#mMdp#" :
                     #Gestion REVOKE, GRANT
                     mGConnexionOuGroupe = True if self.Dialog.mTreePostgresqlDroits.mRolcanLogin == True else False  #ConnexionOuGroupe
                     if key == '#mListeRevokeNew#': 
                        if len(dicReplace[key]) > 0 :
                            if mGConnexionOuGroupe :  #Connexion
                               value = 'REVOKE {}'.format(', '.join( [ '"' + str(l) + '"' for l in dicReplace[key] ] )) + ' FROM "' + str(dicReplace['#mRolname#']) + '" ;'
                            else :                    #Groupe
                               value = 'REVOKE "' + str(dicReplace['#mRolname#']) + '" FROM ' + '{}'.format(', '.join( [ '"' + str(l) + '"' for l in dicReplace[key] ] )) + ' ;'
                        else :
                           value = ''
                     elif key == '#mListeGrantNew#':   
                        if len(dicReplace[key]) > 0 :
                            if mGConnexionOuGroupe :  #Connexion
                              value = 'GRANT {}'.format(', '.join( [ '"' + str(l) + '"' for l in dicReplace[key] ] )) + ' TO "'   + str(dicReplace['#mRolname#']) + '" ;'
                            else :                    #Groupe
                              value = 'GRANT "'  + str(dicReplace['#mRolname#']) + '" TO '   + '{}'.format(', '.join( [ '"' + str(l) + '"' for l in dicReplace[key] ] )) + ' ;'
                        else :
                           value = ''   

                     #Gestion Gestion des schémas Case mRolgestionschema   self.asgardEditeur / self.dbName
                     elif key == '#mRolgestionschema#' : 

                       if not mGConnexionOuGroupe :  #Groupe
                          if mode == "create" :
                             if self.asgardEditeur != None :
                                if dicReplace[key] :   # Cochée
                                   value     = 'GRANT CREATE ON DATABASE "'  + str(self.dbName)        + '" TO "'   + str(dicReplace['#mRolname#']) + '" ;'
                                   dicReplace['#Rolgestionschema_cond1#'] = value
                                   if dicReplace['#mRolname#'] != self.asgardEditeur : # si Role courant différent du role de l'éditeur
                                      value = 'GRANT "'                     + str(self.asgardEditeur) + '" TO "'   + str(dicReplace['#mRolname#']) + '" ;'
                                      dicReplace['#Rolgestionschema_cond2#'] = value
                                else :                  #déCochée
                                   value = 'REVOKE CREATE ON DATABASE "' + str(self.dbName)        + '" FROM "' + str(dicReplace['#mRolname#']) + '" ;'
                                   dicReplace['#Rolgestionschema_cond1#'] = value
                                   if dicReplace['#mRolname#'] != self.asgardEditeur : # si Role courant différent du role de l'éditeur
                                      value = 'REVOKE "'                    + str(self.asgardEditeur) + '" FROM "' + str(dicReplace['#mRolname#']) + '" ;'
                                      dicReplace['#Rolgestionschema_cond2#'] = value
                             else :
                                value = ''
                          elif mode == "update" :
                             if (self.dicNewValueRole["mRolgestionschema"] != dicOldValueRole["mRolgestionschema"]) and mode == "update" : #si chgt de case
                                if dicReplace[key] :   # Cochée
                                   value     = 'GRANT CREATE ON DATABASE "'  + str(self.dbName)        + '" TO "'   + str(dicReplace['#mRolname#']) + '" ;'
                                   dicReplace['#Rolgestionschema_cond1#'] = value
                                   if dicReplace['#mRolname#'] != self.asgardEditeur : # si Role courant différent du role de l'éditeur
                                      value = 'GRANT "'                     + str(self.asgardEditeur) + '" TO "'   + str(dicReplace['#mRolname#']) + '" ;'
                                      dicReplace['#Rolgestionschema_cond2#'] = value
                                else :                  #déCochée
                                   value = 'REVOKE CREATE ON DATABASE "' + str(self.dbName)        + '" FROM "' + str(dicReplace['#mRolname#']) + '" ;'
                                   dicReplace['#Rolgestionschema_cond1#'] = value
                                   if dicReplace['#mRolname#'] != self.asgardEditeur : # si Role courant différent du role de l'éditeur
                                      value = 'REVOKE "'                    + str(self.asgardEditeur) + '" FROM "' + str(dicReplace['#mRolname#']) + '" ;'
                                      dicReplace['#Rolgestionschema_cond2#'] = value
                             else :
                                value = ''
                       else :
                          value = ''
                     else :
                        value = value.replace("'", "''") if value != '' else value
                       
                  mValue = str(value)
                  
               mKeySql = mKeySql.replace(key, mValue)
           #print(mKeySql)
           #------ 
           r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSqlNoReturn(Dialog, self.mBaseAsGard.mConnectEnCours, self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)

           if r != False :
              zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_ihm_asgard", "Information !!!", None)
              QMessageBox.information(self, zTitre, zMess) 
           else :
              #Géré en amont dans la fonction executeSqlNoReturn
              pass 

           self.Dialog.executeButtonRole.setVisible(False) 

        return 

#=========================
def showHideCtrlSimpleComplet(self, mFlags) : 
    if mFlags :
       mHauteurRoleAttribut       = 240
       mHauteurRoleAttributDroits = 105
    else :
       mHauteurRoleAttribut       = 185
       mHauteurRoleAttributDroits = 50

    self.groupBoxAffichageRoleAttribut.setGeometry(QtCore.QRect(5,5,self.Dialog.groupBoxAffichageRightDroits.width() - 10, mHauteurRoleAttribut))
    self.groupBoxAffichageRoleAttributDroits.setGeometry(QtCore.QRect(5, 130, 380 , mHauteurRoleAttributDroits))

    self.groupBoxAffichageRoleAppart.setGeometry(QtCore.QRect(10, self.groupBoxAffichageRoleAttribut.y() + self.groupBoxAffichageRoleAttribut.height() ,self.Dialog.groupBoxAffichageRoleAttributGenerale.width(), self.Dialog.groupBoxAffichageRightDroits.height() - self.groupBoxAffichageRoleAttribut.height() - 50))
    self.groupBoxAffichageRoleAppartOut.setGeometry(QtCore.QRect(2, 2,(self.groupBoxAffichageRoleAppart.width() /2) - 10 , self.groupBoxAffichageRoleAppart.height() - 4))
    self.groupBoxAffichageRoleAppartIn.setGeometry(QtCore.QRect((self.groupBoxAffichageRoleAppart.width() /2) + 10 , 2,(self.groupBoxAffichageRoleAppart.width() /2) - 12, self.groupBoxAffichageRoleAppart.height() - 4 ))


    if hasattr(self.Dialog, 'mTreePostgresqlMembresOut') :  #Pas d'affichage de l'instance Treeview
       self.mTreePostgresqlMembresOut.setGeometry(5, 5, self.groupBoxAffichageRoleAppartOut.width() - 10, self.groupBoxAffichageRoleAppartOut.height() - 10 )
    if hasattr(self.Dialog, 'mTreePostgresqlMembresIn') :  #Pas d'affichage de l'instance Treeview
       self.mTreePostgresqlMembresIn.setGeometry(5 ,5 , self.groupBoxAffichageRoleAppartIn.width() - 10, self.groupBoxAffichageRoleAppartIn.height() - 10 )

    self.executeDroits.setGeometry(QtCore.QRect(self.groupBoxAffichageRoleAppartOut.width() , (self.groupBoxAffichageRoleAppart.height()/2) - (self.executeDroits.height()/2) , 20, 60))
    self.executeButtonRole.setGeometry(QtCore.QRect((self.groupBoxAffichageRoleAppart.width() /2) - (self.executeButtonRole.width() /2) + self.groupBoxAffichageRoleAppart.x(), self.groupBoxAffichageRightDroits.height() - 33, 100,23))

    return   
#==================================================
# Gestion de l'IHM pour les schémas
#==================================================
    
def createIHMAffichage(self) :
    self.groupBoxAffichageRight = QtWidgets.QGroupBox(self.displayInformations)
    self.groupBoxAffichageRight.setGeometry(QtCore.QRect(((self.displayInformations.width() - 40)/2) + 30, 0, ((self.displayInformations.width() - 40)/2) + 10 ,self.displayInformations.height() - 0))
    self.groupBoxAffichageRight.setObjectName("groupBoxAffichageRight")
    self.groupBoxAffichageRight.setStyleSheet("QGroupBox {   \
                                border-style: outset;    \
                                border-width: 2px;       \
                                border-radius: 10px;     \
                                border-color: black;      \
                                font: bold 11px;         \
                                padding: 6px;            \
                                }") 
    self.groupBoxAffichageRight.setVisible(False)
                                
    #==================================================
    #Affichage Help
    self.groupBoxAffichageHelp = QtWidgets.QGroupBox(self.groupBoxAffichageRight)
    self.groupBoxAffichageHelp.setGeometry(QtCore.QRect(10, 10, self.Dialog.groupBoxAffichageRight.width() - 20, self.Dialog.groupBoxAffichageRight.height() - 20))
    self.groupBoxAffichageHelp.setObjectName("groupBoxAffichageHelp")
    self.groupBoxAffichageHelp.setStyleSheet("QGroupBox {   \
                                border-width: 0px;       \
                                border-color: blue;      \
                                }") 
    #Generation de l'aide
    genereAideDynamique(self,"CREATE", [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19])
    self.groupBoxAffichageHelp.setVisible(False)
    
    #==================================================
    #Option Schémas Niv 1
    self.groupBoxAffichageSchema = QtWidgets.QGroupBox(self.groupBoxAffichageRight)
    self.groupBoxAffichageSchema.setGeometry(QtCore.QRect(10,10,self.Dialog.groupBoxAffichageRight.width() - 10, 450))
    self.groupBoxAffichageSchema.setObjectName("groupBoxAffichageSchema")
    self.groupBoxAffichageSchema.setStyleSheet("QGroupBox {   \
                                border-width: 0px;       \
                                border-color: red;      \
                                }") 
    #--------  
    self.labelSchema = QtWidgets.QLabel(self.groupBoxAffichageSchema)     
    self.labelSchema.setGeometry(QtCore.QRect(0,24,118,18))
    self.labelSchema.setObjectName("labelSchema")
    self.labelSchema.setAlignment(Qt.AlignRight)
    #--------                            
    self.zoneSchema = QtWidgets.QLineEdit(self.groupBoxAffichageSchema)
    self.zoneSchema.setGeometry(QtCore.QRect(130,20,220,23))
    self.zoneSchema.setObjectName("zoneSchema")                                 
    self.groupBoxAffichageSchema.setVisible(False)
    #-------- 
    self.labelBloc = QtWidgets.QLabel(self.groupBoxAffichageSchema)     
    self.labelBloc.setGeometry(QtCore.QRect(0,54,118,18))
    self.labelBloc.setObjectName("labelBloc")
    self.labelBloc.setAlignment(Qt.AlignRight)
    #--------                                                                         
    self.comboBloc = QtWidgets.QComboBox(self.groupBoxAffichageSchema)
    self.comboBloc.setGeometry(QtCore.QRect(130,50,220,23))
    self.comboBloc.setObjectName("comboBloc")
    #-------- 
    self.labelActif = QtWidgets.QLabel(self.groupBoxAffichageSchema)     
    self.labelActif.setGeometry(QtCore.QRect(0,84,120,18))
    self.labelActif.setObjectName("labelActif")
    self.labelActif.setAlignment(Qt.AlignRight)
    
    self.labelActif.setStyleSheet("QLabel {   \
                                border-width: 1px;       \
                                border-color: red;      \
                                }") 
                                
    #---                            
    self.labelActifInfo = QtWidgets.QLabel(self.groupBoxAffichageSchema)     
    self.labelActifInfo.setGeometry(QtCore.QRect(150,84,220,18))
    self.labelActifInfo.setObjectName("labelActifInfo")
    self.labelActifInfo.setAlignment(Qt.AlignLeft)
    #--------                            
    self.caseActif = QtWidgets.QCheckBox(self.groupBoxAffichageSchema)    
    self.caseActif.setGeometry(QtCore.QRect(130,80,220,23))
    self.caseActif.setObjectName("caseActif")
    self.caseActif.setChecked(False)        
    #-------- 
    self.labelNomenclature = QtWidgets.QLabel(self.groupBoxAffichageSchema)     
    self.labelNomenclature.setGeometry(QtCore.QRect(0,109,120,18))
    self.labelNomenclature.setObjectName("labelNomenclature")
    self.labelNomenclature.setAlignment(Qt.AlignRight)
    #--------                            
    self.caseNomenclature = QtWidgets.QCheckBox(self.groupBoxAffichageSchema)    
    self.caseNomenclature.setGeometry(QtCore.QRect(130,105,200,23))
    self.caseNomenclature.setObjectName("caseNomenclature")
    self.caseNomenclature.setChecked(False)        
    #Option Droits
    self.groupBoxAffichageSchemaDroits = QtWidgets.QGroupBox(self.groupBoxAffichageSchema)
    self.groupBoxAffichageSchemaDroits.setGeometry(QtCore.QRect(0,135,350, 105))
    self.groupBoxAffichageSchemaDroits.setObjectName("groupBoxAffichageSchema")  
    self.groupBoxAffichageSchemaDroits.setStyleSheet("QGroupBox {   \
                                border-width: 2px;       \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                }")
    #--------  
    self.labelProd = QtWidgets.QLabel(self.groupBoxAffichageSchemaDroits)     
    self.labelProd.setGeometry(QtCore.QRect(20,19,100,18))
    self.labelProd.setObjectName("labelProd")
    self.labelProd.setAlignment(Qt.AlignRight)
    #--------                            
    self.comboProd = QtWidgets.QComboBox(self.groupBoxAffichageSchemaDroits)
    self.comboProd.setGeometry(QtCore.QRect(130,15,210,23))
    self.comboProd.setEditable(True)
    self.comboProd.setInsertPolicy(self.comboProd.InsertAtTop)
    self.comboProd.setObjectName("comboProd")
    #-------- 
    #-------- 
    self.labelEdit = QtWidgets.QLabel(self.groupBoxAffichageSchemaDroits)     
    self.labelEdit.setGeometry(QtCore.QRect(20,49,100,18))
    self.labelEdit.setObjectName("labelEdit")
    self.labelEdit.setAlignment(Qt.AlignRight)
    #--------                            
    self.comboEdit = QtWidgets.QComboBox(self.groupBoxAffichageSchemaDroits)
    self.comboEdit.setGeometry(QtCore.QRect(130,45,210,23))
    self.comboEdit.setEditable(True)
    self.comboEdit.setInsertPolicy(self.comboEdit.InsertAtTop)
    self.comboEdit.setObjectName("comboEdit")
    #-------- 
    #-------- 
    self.labelLect = QtWidgets.QLabel(self.groupBoxAffichageSchemaDroits)     
    self.labelLect.setGeometry(QtCore.QRect(20,79,100,18))
    self.labelLect.setObjectName("labelLect")
    self.labelLect.setAlignment(Qt.AlignRight)
    #--------                            
    self.comboLect = QtWidgets.QComboBox(self.groupBoxAffichageSchemaDroits)
    self.comboLect.setGeometry(QtCore.QRect(130,75,210,23))
    self.comboLect.setEditable(True)
    self.comboLect.setInsertPolicy(self.comboLect.InsertAtTop)
    self.comboLect.setObjectName("comboLect")
    #Option Arborescence
    self.groupBoxAffichageSchemaArbo = QtWidgets.QGroupBox(self.groupBoxAffichageSchema)
    self.groupBoxAffichageSchemaArbo.setGeometry(QtCore.QRect(0,255,350, 135))
    self.groupBoxAffichageSchemaArbo.setObjectName("groupBoxAffichageSchemaArbo")  
    self.groupBoxAffichageSchemaArbo.setStyleSheet("QGroupBox {   \
                                border-width: 2px;       \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                }")
    #-------- 
    self.labelNiv1 = QtWidgets.QLabel(self.groupBoxAffichageSchemaArbo)     
    self.labelNiv1.setGeometry(QtCore.QRect(0,19,120,18))
    self.labelNiv1.setObjectName("labelNiv1")
    self.labelNiv1.setAlignment(Qt.AlignRight)
    #--------                            
    self.zoneNiv1 = QtWidgets.QLineEdit(self.groupBoxAffichageSchemaArbo)
    self.zoneNiv1.setGeometry(QtCore.QRect(130,15,210,23))
    self.zoneNiv1.setObjectName("zoneNiv1") 
    #-------- 
    #--------  
    self.labelNiv1_abr = QtWidgets.QLabel(self.groupBoxAffichageSchemaArbo)     
    self.labelNiv1_abr.setGeometry(QtCore.QRect(0,49,120,18))
    self.labelNiv1_abr.setObjectName("labelNiv1_abr")
    self.labelNiv1_abr.setAlignment(Qt.AlignRight)
    self.labelNiv1_abr.setStyleSheet("QLabel {font: italic 10px;}")
    #--------                            
    self.zoneNiv1_abr = QtWidgets.QLineEdit(self.groupBoxAffichageSchemaArbo)
    self.zoneNiv1_abr.setGeometry(QtCore.QRect(130,45,210,23))
    self.zoneNiv1_abr.setObjectName("zoneNiv1_abr") 
    self.zoneNiv1_abr.setStyleSheet("QLineEdit {font: italic 10px;}")
    #--------  
    self.labelNiv2 = QtWidgets.QLabel(self.groupBoxAffichageSchemaArbo)     
    self.labelNiv2.setGeometry(QtCore.QRect(0,79,120,18))
    self.labelNiv2.setObjectName("labelNiv2")
    self.labelNiv2.setAlignment(Qt.AlignRight)
    #--------                            
    self.zoneNiv2 = QtWidgets.QLineEdit(self.groupBoxAffichageSchemaArbo)
    self.zoneNiv2.setGeometry(QtCore.QRect(130,75,210,23))
    self.zoneNiv2.setObjectName("zoneNiv2") 
    #--------  
    self.labelNiv2_abr = QtWidgets.QLabel(self.groupBoxAffichageSchemaArbo)     
    self.labelNiv2_abr.setGeometry(QtCore.QRect(0,104,120,18))
    self.labelNiv2_abr.setObjectName("labelNiv2_abr")
    self.labelNiv2_abr.setAlignment(Qt.AlignRight)
    self.labelNiv2_abr.setStyleSheet("QLabel {font: italic 10px;}")
    #--------                            
    self.zoneNiv2_abr = QtWidgets.QLineEdit(self.groupBoxAffichageSchemaArbo)
    self.zoneNiv2_abr.setGeometry(QtCore.QRect(130,100,210,23))
    self.zoneNiv2_abr.setObjectName("zoneNiv2_abr") 
    self.zoneNiv2_abr.setStyleSheet("QLineEdit {font: italic 10px;}")
    #--------      
    self.zoneSchema.setFocus(Qt.OtherFocusReason)                                     
    self.groupBoxAffichageSchema.setVisible(False)
    #------ 
    #Boutons  
    #------ 
    self.executeButtonSchema = QtWidgets.QPushButton(self.groupBoxAffichageSchema)
    self.executeButtonSchema.setGeometry(QtCore.QRect(150, 410, 100,23))
    self.executeButtonSchema.setObjectName("executeButtonSchema") 
    #Connections 
    self.executeButtonSchema.clicked.connect(lambda : self.executeSqlSchema(self)) 
    
    #Translation
    self.executeButtonSchema.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Apply", None))
    self.labelSchema.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Schema name : ", None))
    self.labelBloc.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Functional bloc : ", None))
    self.labelActif.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Actif : ", None))
    self.labelActifInfo.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Physical creation of the diagram", None))
    self.labelProd.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Producteur : ", None))
    self.labelEdit.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Editeur : ", None))
    self.labelLect.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Lecteur : ", None))

    self.labelNomenclature.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Nomenclature : ", None))
    self.labelNiv1.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Level 1 : ", None))
    self.labelNiv1_abr.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Level 1 (standard) : ", None))
    self.labelNiv2.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Level 2 : ", None))
    self.labelNiv2_abr.setText(QtWidgets.QApplication.translate("bibli_ihm_asgard", "Level 2 (standard) : ", None))
    self.groupBoxAffichageSchemaDroits.setTitle(QtWidgets.QApplication.translate("bibli_ihm_asgard", "privileges", None))
    self.groupBoxAffichageSchemaArbo.setTitle(QtWidgets.QApplication.translate("bibli_ihm_asgard", "tree structure", None))
    
#============================================        
def genereObjetImageHelp(self, mNameObjet, mName,mX, mY, mL, mH, mIcon, mNameObjetLib, mNameLib, mLibTitre, mLibelle, mHauteurLabel) :
    myPath = os.path.dirname(__file__)+"\\icons\\actions\\" + mIcon
    myDefPath = myPath.replace("\\","/")
    carIcon = QtGui.QImage(myDefPath)
    mNameObjet.setPixmap(QtGui.QPixmap.fromImage(carIcon))
    mNameObjet.setGeometry(QtCore.QRect(mX, mY + 20, mL, mH))
    mNameObjet.setObjectName(mName)    
    #---------------------
    mDeltaImgLib = 10 + 45
    mRatio = 0.14
    mLib = returnListeTexte(self, mLibelle, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
    mhauteur = (2 if len(mLib) == 1 else len(mLib))
    mNameObjetLib.setGeometry(QtCore.QRect(mX , mY -5, self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (mhauteur * 21) + 0))
    mNameObjetLib.setObjectName(mNameLib)
    mNameObjetLib.setText(mLibTitre + '<br>{}'.format('<br>'.join(mLib)))
    #mNameObjetLib.setStyleSheet("QLabel { border: 2px solid red;}") 
    return 
 
#============================================        
def genereObjetImageHelpDroits(self, mNameObjet, mName,mX, mY, mL, mH, mIcon, mNameObjetLib, mNameLib, mLibTitre, mLibelle, mHauteurLabel) :
    myPath = os.path.dirname(__file__)+"\\icons\\actions\\" + mIcon
    myDefPath = myPath.replace("\\","/")
    carIcon = QtGui.QImage(myDefPath)
    mNameObjet.setPixmap(QtGui.QPixmap.fromImage(carIcon))
    mNameObjet.setGeometry(QtCore.QRect(mX, mY + 20, mL, mH))
    mNameObjet.setObjectName(mName)    
    #---------------------
    mDeltaImgLib = 10 + 45
    mRatio = 0.14
    mLib = returnListeTexte(self, mLibelle, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
    mhauteur = (2 if len(mLib) == 1 else len(mLib))
    mNameObjetLib.setGeometry(QtCore.QRect(mX , mY -5, self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (mhauteur * 21) + 0))
    mNameObjetLib.setObjectName(mNameLib)
    mNameObjetLib.setText(mLibTitre + '<br>{}'.format('<br>'.join(mLib)))
    #mNameObjetLib.setStyleSheet("QLabel { border: 2px solid red;}") 
    return 
        
#============================================        
def genereObjets(self, mNameObjet, mName, mX, mY, mL, mH, mLibelle, mEtat) :
    mNameObjet.setGeometry(QtCore.QRect(mX, mY, mL, mH))
    mNameObjet.setObjectName(mName)
    mNameObjet.setText(mLibelle)
    mNameObjet.setChecked(mEtat)
    return 
    
#============================================        
def returnListeTexte(self, mText, mLongueur) :
    objTextWrap = textwrap.TextWrapper(mLongueur, break_long_words=True)
    mListLib = objTextWrap.wrap(mText)
    return mListLib   

#============================================        
def genereAideDynamiqueDroits(self, mAction, mListaffichage) :
  if mAction == "CREATE" :
    for i in mListaffichage :
        if i == 100 :
           self.img100, self.lib100 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits)
           mLibTitre100 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "New connexion", None) + "</b>"
           mLib100 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Creating a connexion with all of its attributes.", None)
           genereObjetImageHelpDroits(self, self.img100, "img100", 10, 5, 40, 40, "connexion_new.png", self.lib100, "lib100", mLibTitre100, mLib100, 50)
        elif i == 101 :
           self.img101, self.lib101 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre101 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "New group", None) + "</b>"
           mLib101 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Creating a group with all of its attributes.", None)
           genereObjetImageHelpDroits(self, self.img101, "img101", 10, 55, 40, 40, "groupe_new.png", self.lib101, "lib101", mLibTitre101, mLib101, 50)
        elif i == 102 :
           self.img102, self.lib102 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre102 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "removing the connexion role", None) + "</b>"
           mLib102 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "removing the connexion role.", None)
           genereObjetImageHelpDroits(self, self.img102, "img102", 10, 55, 40, 40, "supprime_role.png", self.lib102, "lib102", mLibTitre102, mLib102, 50)
        elif i == 103 :
           self.img103, self.lib103 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre103 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "removing the group role", None) + "</b>"
           mLib103 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "removing the group role.", None)
           genereObjetImageHelpDroits(self, self.img103, "img103", 10, 55, 40, 40, "supprime_groupe.png", self.lib103, "lib103", mLibTitre103, mLib103, 50)
        elif i == 104 :
           self.img104, self.lib104 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre104 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Revoke all rights of the role", None) + "</b>"
           mLib104 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Revokes all the rights of the role on the database objects, as well as its default privileges.", None)
           genereObjetImageHelpDroits(self, self.img104, "img104", 10, 55, 40, 40, "revoquer_role.png", self.lib104, "lib104", mLibTitre104, mLib104, 50)
        elif i == 105 :
           self.img105, self.lib105 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre105 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Revoke all rights of the groupe", None) + "</b>"
           mLib105 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Revokes all the rights of the groupe on the database objects, as well as its default privileges.", None)
           genereObjetImageHelpDroits(self, self.img105, "img105", 10, 55, 40, 40, "revoquer_groupe.png", self.lib105, "lib105", mLibTitre105, mLib105, 50)
        elif i == 106 :
           self.img106, self.lib106 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre106 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reassign rights / Cut", None) + "</b>"
           mLib106 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Transfers (Cut) all the rights of the role on the objects of the database, as well as its default privileges, for a designated role.", None)
           genereObjetImageHelpDroits(self, self.img106, "img106", 10, 55, 40, 40, "reaffecte_droits_depart.png", self.lib106, "lib106", mLibTitre106, mLib106, 50)
        elif i == 107 :
           self.img107, self.lib107 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre107 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reassign rights / Paste", None) + "</b>"
           mLib107 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Transfers (Paste) all the rights of the role in memory on the database objects, as well as its default privileges, to a designated role.", None)
           genereObjetImageHelpDroits(self, self.img107, "img107", 10, 55, 40, 40, "reaffecte_droits_arrivee.png", self.lib107, "lib107", mLibTitre107, mLib107, 50)
        elif i == 1060 :
           self.img1060, self.lib1060 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre1060 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reassign rights / Cut", None) + "</b>"
           mLib1060 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Transfers (Cut) all the rights of the role on the objects of the database, as well as its default privileges, for a designated role.", None)
           genereObjetImageHelpDroits(self, self.img1060, "img1060", 10, 55, 40, 40, "reaffecte_droits_depart_gr.png", self.lib1060, "lib1060", mLibTitre1060, mLib1060, 50)
        elif i == 1070 :
           self.img1070, self.lib1070 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre1070 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reassign rights / Paste", None) + "</b>"
           mLib1070 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Transfers (Paste) all the rights of the role in memory on the database objects, as well as its default privileges, to a designated role.", None)
           genereObjetImageHelpDroits(self, self.img1070, "img1070", 10, 55, 40, 40, "reaffecte_droits_arrivee_gr.png", self.lib1070, "lib1070", mLibTitre1070, mLib1070, 50)
        elif i == 108 :
           self.img108, self.lib108 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelpDroits) 
           mLibTitre108 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Cancel Reassign Rights / Cut ", None) + "</b>"
           mLib108 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Cancels the transfer of rights ", None)
           genereObjetImageHelpDroits(self, self.img108, "img108", 10, 55, 40, 40, "reaffecte_droits_annule.png", self.lib108, "lib108", mLibTitre108, mLib108, 50)
           
    self.mLibTitre100, self.mLibTitre101, self.mLibTitre102, self.mLibTitre103, self.mLibTitre104, self.mLibTitre105, self.mLibTitre106, self.mLibTitre107, self.mLibTitre108, self.mLibTitre1060, self.mLibTitre1070 = mLibTitre100, mLibTitre101, mLibTitre102, mLibTitre103, mLibTitre104, mLibTitre105, mLibTitre106, mLibTitre107, mLibTitre108, mLibTitre1060, mLibTitre1070
    self.mLib100, self.mLib101, self.mLib102, self.mLib103, self.mLib104, self.mLib105, self.mLib106, self.mLib107, self.mLib108, self.mLib1060, self.mLib1070 = mLib100, mLib101, mLib102, mLib103, mLib104, mLib105, mLib106, mLib107, mLib108, mLib1060, mLib1070
  elif mAction == "UPDATE" :
    self.Dialog.img100.hide()
    self.Dialog.lib100.hide()                                           
    self.Dialog.img101.hide()                                         
    self.Dialog.lib101.hide()
    self.Dialog.img102.hide()
    self.Dialog.lib102.hide()
    self.Dialog.img103.hide()
    self.Dialog.lib103.hide()
    self.Dialog.img104.hide()
    self.Dialog.lib104.hide()
    self.Dialog.img105.hide()
    self.Dialog.lib105.hide()
    self.Dialog.img106.hide()
    self.Dialog.lib106.hide()
    self.Dialog.img107.hide()
    self.Dialog.lib107.hide()
    self.Dialog.img1060.hide()
    self.Dialog.lib1060.hide()
    self.Dialog.img1070.hide()
    self.Dialog.lib1070.hide()
    self.Dialog.img108.hide()
    self.Dialog.lib108.hide()
        
    mX, mY, first = 10, 15, True
    for i in mListaffichage :
        if i == 100 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img100.show()
           self.Dialog.lib100.show()
           self.Dialog.img100.move(mX, mY)
           self.Dialog.lib100.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib100.height() + 10)
        elif i == 101 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img101.show()
           self.Dialog.lib101.show()
           self.Dialog.img101.move(mX, mY)
           self.Dialog.lib101.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib101.height() + 10)
        elif i == 102 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img102.show()
           self.Dialog.lib102.show()
           self.Dialog.img102.move(mX, mY)
           self.Dialog.lib102.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib102.height() + 10)
        elif i == 103 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img103.show()
           self.Dialog.lib103.show()
           self.Dialog.img103.move(mX, mY)
           self.Dialog.lib103.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib103.height() + 10)           
        elif i == 104 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img104.show()
           self.Dialog.lib104.show()
           self.Dialog.img104.move(mX, mY)
           self.Dialog.lib104.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib104.height() + 10) 
        elif i == 105 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img105.show()
           self.Dialog.lib105.show()
           self.Dialog.img105.move(mX, mY)
           self.Dialog.lib105.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib105.height() + 10) 
        elif i == 106 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img106.show()
           self.Dialog.lib106.show()
           self.Dialog.img106.move(mX, mY)
           self.Dialog.lib106.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib106.height() + 10) 
        elif i == 107 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img107.show()
           self.Dialog.lib107.show()
           self.Dialog.img107.move(mX, mY)
           self.Dialog.lib107.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib107.height() + 10) 
        elif i == 1060 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img1060.show()
           self.Dialog.lib1060.show()
           self.Dialog.img1060.move(mX, mY)
           self.Dialog.lib1060.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib1060.height() + 10) 
        elif i == 1070 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img1070.show()
           self.Dialog.lib1070.show()
           self.Dialog.img1070.move(mX, mY)
           self.Dialog.lib1070.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib1070.height() + 10) 
        elif i == 108 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img108.show()
           self.Dialog.lib108.show()
           self.Dialog.img108.move(mX, mY)
           self.Dialog.lib108.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib108.height() + 10) 
    return 
    
#============================================        
def genereAideDynamique(self, mAction, mListaffichage) :
  if mAction == "CREATE" :
    for i in mListaffichage :
        if i == 0 :
           pass
        elif i == 1 :
           self.img1, self.lib1 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)
           mLibTitre1 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "New schema", None) + "</b>"
           mLib1 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Defines a new schema, active (created in the database) or not.", None)
           genereObjetImageHelp(self, self.img1, "img1", 10, 5, 40, 40, "schema_new.png", self.lib1, "lib1", mLibTitre1, mLib1, 50)
        elif i == 2 :
           self.img2, self.lib2 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)   #
           mLibTitre2 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Move to trash", None) + "</b>"
           mLib2 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "An active schema put in the trash can be permanently deleted from the database.", None)
           genereObjetImageHelp(self, self.img2, "img2", 10, 55, 40, 40, "corbeille.png", self.lib2, "lib2", mLibTitre2, mLib2, 50)
        elif i == 3 :
           self.img3, self.lib3 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)   #
           mLibTitre3 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Dereferencing", None) + "</b>"
           mLib3 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Excludes the diagram from the scope of Asgard. All information entered in the form will be lost. The rights previously defined for the producer, the publisher and the reader are kept identically.", None)
           genereObjetImageHelp(self, self.img3, "img3", 10, 105, 40, 40, "dereferencer.png", self.lib3, "lib3",  mLibTitre3, mLib3, 80)
        elif i == 4 :
           self.img4, self.lib4 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)   #
           mLibTitre4 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Delete", None) + "</b>"
           mLib4 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Permanently clears information about the inactive schema from the Asgard management table.", None)
           genereObjetImageHelp(self, self.img4, "img4", 10, 155, 40, 40, "schema_efface.png", self.lib4, "lib4", mLibTitre4, mLib4, 50)
        elif i == 5 :
           self.img5, self.lib5 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)    #
           mLibTitre5 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Create in the database (make active)", None) + "</b>"
           mLib5 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Create the schema in the database. The schema will now appear as 'active'.", None)
           genereObjetImageHelp(self, self.img5, "img5", 10, 205, 40, 40, "schema_creer_base.png", self.lib5, "lib5", mLibTitre5, mLib5, 50)
        elif i == 6 :
           self.img6, self.lib6 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)    #
           mLibTitre6 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Empty the trash", None) + "</b>"
           mLib6 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Permanently remove all active schemas from the recycle bin, erase inactive schemas.", None)
           genereObjetImageHelp(self, self.img6, "img6", 10, 255, 40, 40, "corbeillevide.png", self.lib6, "lib6", mLibTitre6, mLib6, 50)
        elif i == 7 :
           self.img7, self.lib7 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)
           mLibTitre7 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Restore", None) + "</b>"
           mLib7 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Take the diagram out of the trash and place it back in its original block.", None)                        #
           genereObjetImageHelp(self, self.img7, "img7", 10, 305, 40, 40, "restaurer.png", self.lib7, "lib7", mLibTitre7, mLib7, 50)
        elif i == 8 :
           self.img8, self.lib8 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre8 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Delete from the database", None) + "</b>"
           mLib8 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Permanently deletes the schema and its contents from the database. The schema remains referenced by Asgard as an 'inactive' schema.", None)
           genereObjetImageHelp(self, self.img8, "img8", 10, 355, 40, 40, "supprimer_base.png", self.lib8, "lib8", mLibTitre8, mLib8, 80)
        elif i == 9 :
           self.img9, self.lib9 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre9 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reference", None) + "</b>"
           mLib9 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "The scheme will be supported by Asgard mechanisms. It is classified in the tree structure according to its prefix or, failing that, in the 'Others' block, The rights to the schema and its content are reset.", None)
           genereObjetImageHelp(self, self.img9, "img9", 10, 405, 40, 40, "referencer.png", self.lib9, "lib9", mLibTitre9, mLib9, 50)
        elif i == 10 :
           self.img10, self.lib10 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre10 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reset rights", None) + "</b>"
           mLib10 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Restores the standard rights of the producer, editor and reader to the diagram and the objects it contains.", None)
           genereObjetImageHelp(self, self.img10, "img10", 10, 455, 40, 40, "reinitialise_droits.png", self.lib10, "lib10", mLibTitre10, mLib10, 50)
        elif i == 11 :
           self.img11, self.lib11 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre11 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Move / Cut", None) + "</b>"
           mLib11 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Select an object to change schema.", None)
           genereObjetImageHelp(self, self.img11, "img11", 10, 505, 40, 40, "deplace_depart.png", self.lib11, "lib11", mLibTitre11, mLib11, 50)
        elif i == 12 :
           self.img12, self.lib12 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre12 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Move / Paste", None) + "</b>"
           mLib12 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Defines the new schema for the selected object. The rights are transferred from the producer, editor and reader of the starting schema to those of the target schema.", None)
           genereObjetImageHelp(self, self.img12, "img12", 10, 555, 40, 40, "deplace_arrivee.png", self.lib12, "lib12", mLibTitre12, mLib12, 50)
        elif i == 13 :
           self.img13, self.lib13 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre13 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Cancel \"Move / Cut\"", None) + "</b>"
           mLib13 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Cancels the movement of the selected object.", None)
           genereObjetImageHelp(self, self.img13, "img13", 10, 605, 40, 40, "deplace_annule.png", self.lib13, "lib13", mLibTitre13, mLib13, 50)
        elif i == 14 :
           self.img14, self.lib14 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre14 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Refer to ... ", None) + "</b>"
           mLib14 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "The scheme will be supported by ASGARD mechanisms. It is classified in the tree structure according to the choice of the active functional block in the submenu. The rights to the schema and its content are reset.", None)
           genereObjetImageHelp(self, self.img14, "img14", 10, 605, 40, 40, "", self.lib14, "lib14", mLibTitre14, mLib14, 50)
        elif i == 15 :
           self.img15, self.lib15 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre15 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Look for anomalies", None) + "</b>"
           mLib15 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Scans the schema and the objects it contains in search of missing or excess rights compared to the ASGARD standard.", None)
           genereObjetImageHelp(self, self.img15, "img15", 10, 605, 40, 40, "diagnostic.png", self.lib15, "lib15", mLibTitre15, mLib15, 50)
        elif i == 16 :
           self.img16, self.lib16 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre16 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Referencing while retaining the rights", None) + "</b>"
           mLib16 = QtWidgets.QApplication.translate("bibli_ihm_asgard", 'The scheme will be supported by Asgard mechanisms. It is classified in the tree structure according to its prefix or, failing that, in the "Others" block. The rights to the diagram and its content are retained.', None)
           genereObjetImageHelp(self, self.img16, "img16", 10, 405, 40, 40, "referencerconservedroits.png", self.lib16, "lib16", mLibTitre16, mLib16, 50)
        elif i == 17 :
           self.img17, self.lib17 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre17 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Reset rights", None) + "</b>"
           mLib17 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Restores standard producer, publisher and reader rights to the object. .", None)
           genereObjetImageHelp(self, self.img17, "img17", 10, 455, 40, 40, "reinitialise_droits.png", self.lib17, "lib17", mLibTitre17, mLib17, 50)
        elif i == 18 :
           self.img18, self.lib18 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre18 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Replica", None) + "</b>"
           mLib18 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Replicates the dataset for synchronization with the central database.", None)
           genereObjetImageHelp(self, self.img18, "img18", 10, 455, 40, 40, "repliquer.png", self.lib18, "lib18", mLibTitre18, mLib18, 50)
        elif i == 19 :
           self.img19, self.lib19 = QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp), QtWidgets.QLabel(self.Dialog.groupBoxAffichageHelp)      #
           mLibTitre19 = "<b>" + QtWidgets.QApplication.translate("bibli_ihm_asgard", "Dereplica", None) + "</b>"
           mLib19 = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Dereplicates the dataset for synchronization with the central database.", None)
           genereObjetImageHelp(self, self.img19, "img19", 10, 455, 40, 40, "derepliquer.png", self.lib19, "lib19", mLibTitre19, mLib19, 50)
           
    #--
    self.mLibTitre1, self.mLibTitre2, self.mLibTitre3, self.mLibTitre4, self.mLibTitre5, self.mLibTitre6, self.mLibTitre7, self.mLibTitre8, self.mLibTitre9, self.mLibTitre10, \
    self.mLibTitre11, self.mLibTitre12, self.mLibTitre13, self.mLibTitre14, self.mLibTitre15, self.mLibTitre16, self.mLibTitre17, self.mLibTitre18, self.mLibTitre19 = \
    mLibTitre1, mLibTitre2, mLibTitre3, mLibTitre4, mLibTitre5, mLibTitre6, mLibTitre7, mLibTitre8, mLibTitre9, mLibTitre10, \
    mLibTitre11, mLibTitre12, mLibTitre13, mLibTitre14, mLibTitre15, mLibTitre16, mLibTitre17, mLibTitre18, mLibTitre19
    #--
    self.mLib1, self.mLib2, self.mLib3, self.mLib4, self.mLib5, self.mLib6, self.mLib7, self.mLib8, self.mLib9, self.mLib10, \
    self.mLib11, self.mLib12, self.mLib13, self.mLib14, self.mLib15, self.mLib16, self.mLib17, self.mLib18, self.mLib19 = \
    mLib1, mLib2, mLib3, mLib4, mLib5, mLib6, mLib7, mLib8, mLib9, mLib10, \
    mLib11, mLib12, mLib13, mLib14, mLib15, mLib16, mLib17, mLib18, mLib19
    #--
  elif mAction == "UPDATE" :
    self.Dialog.img1.hide()
    self.Dialog.lib1.hide()
    self.Dialog.img2.hide()
    self.Dialog.lib2.hide()
    self.Dialog.img3.hide()
    self.Dialog.lib3.hide()
    self.Dialog.img4.hide()
    self.Dialog.lib4.hide()
    self.Dialog.img5.hide()
    self.Dialog.lib5.hide()
    self.Dialog.img6.hide()
    self.Dialog.lib6.hide()
    self.Dialog.img7.hide()
    self.Dialog.lib7.hide()
    self.Dialog.img8.hide()
    self.Dialog.lib8.hide()
    self.Dialog.img9.hide()
    self.Dialog.lib9.hide()
    self.Dialog.img10.hide()
    self.Dialog.lib10.hide()
    self.Dialog.img11.hide()
    self.Dialog.lib11.hide()
    self.Dialog.img12.hide()
    self.Dialog.lib12.hide()
    self.Dialog.img13.hide()
    self.Dialog.lib13.hide()
    self.Dialog.img14.hide()
    self.Dialog.lib14.hide()
    self.Dialog.img15.hide()
    self.Dialog.lib15.hide()
    self.Dialog.img16.hide()
    self.Dialog.lib16.hide()
    self.Dialog.img17.hide()
    self.Dialog.lib17.hide()
    self.Dialog.img18.hide()
    self.Dialog.lib18.hide()
    self.Dialog.img19.hide()
    self.Dialog.lib19.hide()
    mX, mY, first = 10, 15, True
    for i in mListaffichage :
        if i == 1 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img1.show()
           self.Dialog.lib1.show()
           self.Dialog.img1.move(mX, mY)
           self.Dialog.lib1.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib1.height() + 10)
        elif i == 2 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img2.show()
           self.Dialog.lib2.show()
           self.Dialog.img2.move(mX, mY)
           self.Dialog.lib2.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib2.height() + 10)
        elif i == 3:
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img3.show()
           self.Dialog.lib3.show()
           self.Dialog.img3.move(mX, mY)
           self.Dialog.lib3.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib3.height() + 10)
        elif i == 4 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img4.show()
           self.Dialog.lib4.show()
           self.Dialog.img4.move(mX, mY)
           self.Dialog.lib4.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib4.height() + 10)
        elif i == 5 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img5.show()
           self.Dialog.lib5.show()
           self.Dialog.img5.move(mX, mY)
           self.Dialog.lib5.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib5.height() + 10)
        elif i == 6 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img6.show()
           self.Dialog.lib6.show()
           self.Dialog.img6.move(mX, mY)
           self.Dialog.lib6.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib6.height() + 10)
        elif i == 7 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img7.show()
           self.Dialog.lib7.show()
           self.Dialog.img7.move(mX, mY)
           self.Dialog.lib7.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib7.height() + 10)
        elif i == 8 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img8.show()
           self.Dialog.lib8.show()
           self.Dialog.img8.move(mX, mY)
           self.Dialog.lib8.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib8.height() + 10)
        elif i == 9 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img9.show()
           self.Dialog.lib9.show()
           self.Dialog.img9.move(mX, mY)
           self.Dialog.lib9.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib9.height() + 10)
        elif i == 10 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img10.show()
           self.Dialog.lib10.show()
           self.Dialog.img10.move(mX, mY)
           self.Dialog.lib10.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib10.height() + 10)
        elif i == 11 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img11.show()
           self.Dialog.lib11.show()
           self.Dialog.img11.move(mX, mY)
           self.Dialog.lib11.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib11.height() + 10)
        elif i == 12 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img12.show()
           self.Dialog.lib12.show()
           self.Dialog.img12.move(mX, mY)
           self.Dialog.lib12.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib12.height() + 10)
        elif i == 13 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img13.show()
           self.Dialog.lib13.show()
           self.Dialog.img13.move(mX, mY)
           self.Dialog.lib13.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib13.height() + 10)
        elif i == 14 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img14.show()
           self.Dialog.lib14.show()
           self.Dialog.img14.move(mX, mY)
           self.Dialog.lib14.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib14.height() + 10)
        elif i == 15 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img15.show()
           self.Dialog.lib15.show()
           self.Dialog.img15.move(mX, mY)
           self.Dialog.lib15.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib15.height() + 10)
        elif i == 16 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img16.show()
           self.Dialog.lib16.show()
           self.Dialog.img16.move(mX, mY)
           self.Dialog.lib16.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib16.height() + 10)
        elif i == 17 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img17.show()
           self.Dialog.lib17.show()
           self.Dialog.img17.move(mX, mY)
           self.Dialog.lib17.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib17.height() + 10)
        elif i == 18 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img18.show()
           self.Dialog.lib18.show()
           self.Dialog.img18.move(mX, mY)
           self.Dialog.lib18.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib18.height() + 10)
        elif i == 19 :
           if first :
              mX, mY, first = 10, 15, False
           self.Dialog.img19.show()
           self.Dialog.lib19.show()
           self.Dialog.img19.move(mX, mY)
           self.Dialog.lib19.move(mX + 45, mY - 5)
           mY = mY + (self.Dialog.lib19.height() + 10)
    return 

#==================================================
# FIN
#==================================================
