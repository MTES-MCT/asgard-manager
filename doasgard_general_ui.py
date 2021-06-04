# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog
from qgis.core import *

from .asgard_general_ui import Ui_Dialog_Asgard
from . import bibli_ihm_asgard
from .bibli_ihm_asgard import *

class Dialog(QDialog, Ui_Dialog_Asgard):
      def __init__(self):
          QDialog.__init__(self)
          self.setupUi(self)

      def reject(self):
          try :
            self.mBaseAsGard.deconnectBase()
          except:
            pass

          bibli_asgard.returnAndSaveDialogParam(self, "Save")

          self.hide()        
