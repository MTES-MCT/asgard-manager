# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT-Mer/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020 

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog
from qgis.core import *

from .confirme_ui import Ui_Dialog_Confirme

class Dialog(QDialog, Ui_Dialog_Confirme):
      def __init__(self, mDialog, mBaseAsGard, mTypeAction, mKeySqlTransformee):
          QDialog.__init__(self)
          self.mTypeAction = mTypeAction
          self.mKeySqlTransformee = mKeySqlTransformee
          self.setupUiConfirme(self, mDialog, mBaseAsGard, self.mTypeAction, self.mKeySqlTransformee)

		
