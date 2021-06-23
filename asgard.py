# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *

from PyQt5.QtWidgets import QAction, QMenu , QApplication, QMessageBox
from PyQt5.QtGui import QIcon

from qgis.core import *
from qgis.gui import *

import os

from . import doasgard_general_ui
from . import bibli_asgard
from .bibli_asgard import *
from . import doabout

class MainPlugin(object):
  def __init__(self, iface):
     self.name = "asgardmanager"
     self.iface = iface
    
     # Generation de la traduction selon la langue choisie   
     overrideLocale = QSettings().value("locale/overrideFlag", False)
     localeFullName = QLocale.system().name() if not overrideLocale else QSettings().value("locale/userLocale", "")
     if localeFullName == None :
        self.localePath = os.path.dirname(__file__) + "/i18n/asgard_fr.qm"
     else :
        self.localePath = os.path.dirname(__file__) + "/i18n/asgard_" + localeFullName[0:2] + ".qm"
     if QFileInfo(self.localePath).exists():
        self.translator = QTranslator()
        self.translator.load(self.localePath)
        QCoreApplication.installTranslator(self.translator)
     # Generation de la traduction selon la langue choisie   

  def initGui(self):
     #Construction du menu
     self.menu=QMenu("ASGARD")
     self.menu.setTitle(QtWidgets.QApplication.translate("asgard_main", "Asgard Manager") + "  (" + str(bibli_asgard.returnVersion()) + ")")

     menuIcon = bibli_asgard.getThemeIcon("asgard2.png")
     self.asgard2 = QAction(QIcon(menuIcon),"Asgard Manager (Automatic and Simplified GrAnting for Rights in Databases)" + "  (" + str(bibli_asgard.returnVersion()) + ")",self.iface.mainWindow())
     self.asgard2.setText(QtWidgets.QApplication.translate("asgard_main", "Asgard Manager (Automatic and Simplified GrAnting for Rights in Databases)") + "  (" + str(bibli_asgard.returnVersion()) + ")")
     self.asgard2.triggered.connect(self.clickIHMasgard2)
     
     menuIcon = bibli_asgard.getThemeIcon("about.png")
     self.about = QAction(QIcon(menuIcon), "About ...", self.iface.mainWindow())
     self.about.setText(QtWidgets.QApplication.translate("asgard_main", "About ..."))
     self.about.triggered.connect(self.clickAbout)
    
     #Construction du menu
     self.menu.addAction(self.asgard2)
     self.menu.addSeparator()
     self.menu.addAction(self.about)

     #=========================
     #-- Ajout du menu
     menuBar = self.iface.mainWindow().menuBar()    
     zMenu = menuBar
     for child in menuBar.children():
         if child.objectName()== "mPluginMenu" :
            zMenu = child
            break
     zMenu.addMenu(self.menu)

     #Ajouter une barre d'outils'
     self.toolBarName = QtWidgets.QApplication.translate("asgard_main", "My tool bar ASGARD MANAGER")
     self.toolbar = self.iface.addToolBar(self.toolBarName)
     # Pour faire une action
     self.toolbar.addAction(self.asgard2)
     #self.toolbar.addSeparator()
     #self.toolbar.addAction(self.about)
     #=========================
     
  def clickAbout(self):
      d = doabout.Dialog()
      d.exec_()

  def clickIHMasgard2(self):
      d = doasgard_general_ui.Dialog()
      d.exec_()

  def unload(self):
      pass  
       




  
