# (c) Didier  LECLERC 2021 CMSIG MTE-MCTRCT-Mer/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2021 

import os.path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from . import asgard_general_ui
from .asgard_general_ui import * 
from . import bibli_asgard
from .bibli_asgard import *
from qgis.core import  QgsSettings

class Ui_Dialog_ColorBloc(object):
    def setupUiColorBloc(self, DialogColorBloc):
        self.DialogColorBloc = DialogColorBloc
        self.zMessTitle    =  QtWidgets.QApplication.translate("colorbloc_ui", "Changing the colors of function blocks.", None)
        myPath = os.path.dirname(__file__)+"\\icons\\actions\\color_blocs.png"

        DialogColorBloc.setObjectName("DialogConfirme")
        DialogColorBloc.setFixedSize(810,460)
        iconSource = bibli_asgard.getThemeIcon("asgard2.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogColorBloc.setWindowIcon(icon)
        #----------
        self.labelImage = QtWidgets.QLabel(DialogColorBloc)
        myDefPath = myPath.replace("\\","/")
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        self.labelImage.setGeometry(QtCore.QRect(20, 0, 100, 100))
        self.labelImage.setObjectName("labelImage")
        #----------
        self.label_2 = QtWidgets.QLabel(DialogColorBloc)
        self.label_2.setGeometry(QtCore.QRect(100, 30, 430, 30))
        self.label_2.setAlignment(Qt.AlignLeft)        
        font = QtGui.QFont()
        font.setPointSize(12) 
        font.setWeight(50) 
        font.setBold(True)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")
        
        #========
        self.mDic_LH = bibli_asgard.returnAndSaveDialogParam(self, "Load")
        self.dicListBlocs = bibli_asgard.returnLoadBlocParam() 
        self.dicListLettre = { 0:"c",  1:"w",  2:"s",  3:"p",  4:"r",  5:"x",  6 :"e",  7:"z", 8:"autre", 9:"d",\
                         10:"a", 11:"b", 12:"f", 13:"g", 14:"h", 15:"i", 16:"j", 17:"k", 18:"l",    19:"m",\
                         20:"n", 21:"o", 22:"q", 23:"t", 24:"u", 25:"v", 26:"y"}
        #========
        self.groupBoxAll = QtWidgets.QGroupBox(DialogColorBloc)
        self.groupBoxAll.setGeometry(QtCore.QRect(10,90,DialogColorBloc.width() - 20, DialogColorBloc.height() - 150))
        self.groupBoxAll.setObjectName("groupBoxAll")
        self.groupBoxAll.setStyleSheet("QGroupBox {   \
                                border-style: dashed; border-width: 1px;       \
                                border-color: #958B62;      \
                                font: bold 11px;         \
                                }")
        #-
        self.tabWidgetColor = QTabWidget(self.groupBoxAll)
        self.tabWidgetColor.setGeometry(QtCore.QRect(0, 0, self.groupBoxAll.width() ,self.groupBoxAll.height()))
        #--------------------------
        self.tabWidgetColor_premier = QWidget()
        self.tabWidgetColor_premier.setObjectName("tabWidgetColor_premier")
        labelTabWidgetColor_premier = QtWidgets.QApplication.translate("colorbloc_ui", "  first plan  ", None)
        self.tabWidgetColor.addTab(self.tabWidgetColor_premier,labelTabWidgetColor_premier)
         #--------------------------
        self.tabWidgetColor_second = QWidget()
        self.tabWidgetColor_second.setObjectName("tabWidgetColor_second")
        labelTabWidgetColor_second = QtWidgets.QApplication.translate("colorbloc_ui", "  second plan  ", None)
        self.tabWidgetColor.addTab(self.tabWidgetColor_second,labelTabWidgetColor_second)

        #---First Plan-------
        button_0, img_0, reset_0 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_0, img_0, reset_0, "button_0", "img_0", "reset_0", 0)
        button_1, img_1, reset_1 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_1, img_1, reset_1, "button_1", "img_1", "reset_1", 1)
        button_2, img_2, reset_2 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_2, img_2, reset_2, "button_2", "img_2", "reset_2", 2)
        #-
        button_3, img_3, reset_3 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_3, img_3, reset_3, "button_3", "img_3", "reset_3", 3)
        button_4, img_4, reset_4 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_4, img_4, reset_4, "button_4", "img_4", "reset_4", 4)
        button_5, img_5, reset_5 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_5, img_5, reset_5, "button_5", "img_5", "reset_5", 5)
        #-
        button_6, img_6, reset_6 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_6, img_6, reset_6, "button_6", "img_6", "reset_6", 6)
        button_7, img_7, reset_7 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_7, img_7, reset_7, "button_7", "img_7", "reset_7", 7)
        button_8, img_8, reset_8 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_8, img_8, reset_8, "button_8", "img_8", "reset_8", 8)
        #-
        button_9, img_9, reset_9 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_9, img_9, reset_9, "button_9", "img_9", "reset_9", 9)
        button_10, img_10, reset_10 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_10, img_10, reset_10, "button_10", "img_10", "reset_10", 10)
        button_11, img_11, reset_11 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_11, img_11, reset_11, "button_11", "img_11", "reset_11", 11)
        #-
        button_12, img_12, reset_12 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_12, img_12, reset_12, "button_12", "img_12", "reset_12", 12)
        button_13, img_13, reset_13 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_13, img_13, reset_13, "button_13", "img_13", "reset_13", 13)
        button_14, img_14, reset_14 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_14, img_14, reset_14, "button_14", "img_14", "reset_14", 14)
        #-
        button_15, img_15, reset_15 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_15, img_15, reset_15, "button_15", "img_15", "reset_15", 15)
        button_16, img_16, reset_16 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_16, img_16, reset_16, "button_16", "img_16", "reset_16", 16)
        button_17, img_17, reset_17 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_17, img_17, reset_17, "button_17", "img_17", "reset_17", 17)
        #-
        button_18, img_18, reset_18 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_18, img_18, reset_18, "button_18", "img_18", "reset_18", 18)
        button_19, img_19, reset_19 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_19, img_19, reset_19, "button_19", "img_19", "reset_19", 19)
        button_20, img_20, reset_20 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_20, img_20, reset_20, "button_20", "img_20", "reset_20", 20)
        #-
        button_21, img_21, reset_21 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_21, img_21, reset_21, "button_21", "img_21", "reset_21", 21)
        button_22, img_22, reset_22 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_22, img_22, reset_22, "button_22", "img_22", "reset_22", 22)
        button_23, img_23, reset_23 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_23, img_23, reset_23, "button_23", "img_23", "reset_23", 23)
        #-
        button_24, img_24, reset_24 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_24, img_24, reset_24, "button_24", "img_24", "reset_24", 24)
        button_25, img_25, reset_25 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_25, img_25, reset_25, "button_25", "img_25", "reset_25", 25)
        button_26, img_26, reset_26 = QtWidgets.QPushButton(self.tabWidgetColor_premier), QtWidgets.QLabel(self.tabWidgetColor_premier), QtWidgets.QPushButton(self.tabWidgetColor_premier)
        self.genereButtonAction(button_26, img_26, reset_26, "button_26", "img_26", "reset_26", 26)

        #---Second Plan-------
        button_second_0, img_second_0, reset_second_0 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_0, img_second_0, reset_second_0, "button_second_0", "img_second_0", "reset_second_0", 0)
        button_second_1, img_second_1, reset_second_1 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_1, img_second_1, reset_second_1, "button_second_1", "img_second_1", "reset_second_1", 1)
        button_second_2, img_second_2, reset_second_2 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_2, img_second_2, reset_second_2, "button_second_2", "img_second_2", "reset_second_2", 2)
        #-
        button_second_3, img_second_3, reset_second_3 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_3, img_second_3, reset_second_3, "button_second_3", "img_second_3", "reset_second_3", 3)
        button_second_4, img_second_4, reset_second_4 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_4, img_second_4, reset_second_4, "button_second_4", "img_second_4", "reset_second_4", 4)
        button_second_5, img_second_5, reset_second_5 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_5, img_second_5, reset_second_5, "button_second_5", "img_second_5", "reset_second_5", 5)
        #-
        button_second_6, img_second_6, reset_second_6 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_6, img_second_6, reset_second_6, "button_second_6", "img_second_6", "reset_second_6", 6)
        button_second_7, img_second_7, reset_second_7 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_7, img_second_7, reset_second_7, "button_second_7", "img_second_7", "reset_second_7", 7)
        button_second_8, img_second_8, reset_second_8 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_8, img_second_8, reset_second_8, "button_second_8", "img_second_8", "reset_second_8", 8)
        #-
        button_second_9, img_second_9, reset_second_9 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_9, img_second_9, reset_second_9, "button_second_9", "img_second_9", "reset_second_9", 9)
        button_second_10, img_second_10, reset_second_10 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_10, img_second_10, reset_second_10, "button_second_10", "img_second_10", "reset_second_10", 10)
        button_second_11, img_second_11, reset_second_11 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_11, img_second_11, reset_second_11, "button_second_11", "img_second_11", "reset_second_11", 11)
        #-
        button_second_12, img_second_12, reset_second_12 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_12, img_second_12, reset_second_12, "button_second_12", "img_second_12", "reset_second_12", 12)
        button_second_13, img_second_13, reset_second_13 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_13, img_second_13, reset_second_13, "button_second_13", "img_second_13", "reset_second_13", 13)
        button_second_14, img_second_14, reset_second_14 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_14, img_second_14, reset_second_14, "button_second_14", "img_second_14", "reset_second_14", 14)
        #-
        button_second_15, img_second_15, reset_second_15 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_15, img_second_15, reset_second_15, "button_second_15", "img_second_15", "reset_second_15", 15)
        button_second_16, img_second_16, reset_second_16 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_16, img_second_16, reset_second_16, "button_second_16", "img_second_16", "reset_second_16", 16)
        button_second_17, img_second_17, reset_second_17 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_17, img_second_17, reset_second_17, "button_second_17", "img_second_17", "reset_second_17", 17)
        #-
        button_second_18, img_second_18, reset_second_18 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_18, img_second_18, reset_second_18, "button_second_18", "img_second_18", "reset_second_18", 18)
        button_second_19, img_second_19, reset_second_19 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_19, img_second_19, reset_second_19, "button_second_19", "img_second_19", "reset_second_19", 19)
        button_second_20, img_second_20, reset_second_20 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_20, img_second_20, reset_second_20, "button_second_20", "img_second_20", "reset_second_20", 20)
        #-
        button_second_21, img_second_21, reset_second_21 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_21, img_second_21, reset_second_21, "button_second_21", "img_second_21", "reset_second_21", 21)
        button_second_22, img_second_22, reset_second_22 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_22, img_second_22, reset_second_22, "button_second_22", "img_second_22", "reset_second_22", 22)
        button_second_23, img_second_23, reset_second_23 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_23, img_second_23, reset_second_23, "button_second_23", "img_second_23", "reset_second_23", 23)
        #-
        button_second_24, img_second_24, reset_second_24 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_24, img_second_24, reset_second_24, "button_second_24", "img_second_24", "reset_second_24", 24)
        button_second_25, img_second_25, reset_second_25 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_25, img_second_25, reset_second_25, "button_second_25", "img_second_25", "reset_second_25", 25)
        button_second_26, img_second_26, reset_second_26 = QtWidgets.QPushButton(self.tabWidgetColor_second), QtWidgets.QLabel(self.tabWidgetColor_second), QtWidgets.QPushButton(self.tabWidgetColor_second)
        self.genereButtonAction(button_second_26, img_second_26, reset_second_26, "button_second_26", "img_second_26", "reset_second_26", 26)

        #========
        self.pushButton = QtWidgets.QPushButton(DialogColorBloc)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setGeometry(QtCore.QRect(DialogColorBloc.width() / 2 - 100, DialogColorBloc.height() - 50, 80, 25))
        self.pushButton.clicked.connect(lambda : self.functionSaveColor())
        #----------
        self.pushButtonAnnuler = QtWidgets.QPushButton(DialogColorBloc)
        self.pushButtonAnnuler.setObjectName("pushButtonAnnuler")
        self.pushButtonAnnuler.setGeometry(QtCore.QRect(DialogColorBloc.width() / 2 + 20, DialogColorBloc.height() - 50, 80, 25))
        self.pushButtonAnnuler.clicked.connect(DialogColorBloc.reject)
        #----------
        DialogColorBloc.setWindowTitle("ASGARD Manager - (" + str(bibli_asgard.returnVersion()) + ")")
        self.label_2.setText(QtWidgets.QApplication.translate("colorbloc_ui", self.zMessTitle, None))
        self.pushButton.setText(QtWidgets.QApplication.translate("colorbloc_ui", "OK", None))
        self.pushButtonAnnuler.setText(QtWidgets.QApplication.translate("colorbloc_ui", "Cancel", None))
        
    #========
    def genereButtonAction(self, mButton, mImage, mReset, mButtonName, mImageName, mResetName, compt): 
        for i in range(27) :
            if i <= 2:
               ii = i
               mX1, mY1 = (ii * 260) +  20, 10 
               mX2, mY2 = (ii * 260) + 165, 10
               mX3, mY3 = (ii * 260) + 210, 10
               if i == compt : break
            if i <= 5:
               ii = i - 3
               mX1, mY1 = (ii * 260) +  20, 40 
               mX2, mY2 = (ii * 260) + 165, 40
               mX3, mY3 = (ii * 260) + 210, 40
               if i == compt : break
            if i <= 8:
               ii = i - 6
               mX1, mY1 = (ii * 260) +  20, 70 
               mX2, mY2 = (ii * 260) + 165, 70
               mX3, mY3 = (ii * 260) + 210, 70
               if i == compt : break
            if i <= 11:
               ii = i - 9
               mX1, mY1 = (ii * 260) +  20, 100 
               mX2, mY2 = (ii * 260) + 165, 100
               mX3, mY3 = (ii * 260) + 210, 100
               if i == compt : break
            if i <= 14:
               ii = i - 12
               mX1, mY1 = (ii * 260) +  20, 130 
               mX2, mY2 = (ii * 260) + 165, 130
               mX3, mY3 = (ii * 260) + 210, 130
               if i == compt : break
            if i <= 17:
               ii = i - 15
               mX1, mY1 = (ii * 260) +  20, 160 
               mX2, mY2 = (ii * 260) + 165, 160
               mX3, mY3 = (ii * 260) + 210, 160
               if i == compt : break
            if i <= 20:
               ii = i - 18
               mX1, mY1 = (ii * 260) +  20, 190 
               mX2, mY2 = (ii * 260) + 165, 190
               mX3, mY3 = (ii * 260) + 210, 190
               if i == compt : break
            if i <= 23:
               ii = i - 21
               mX1, mY1 = (ii * 260) +  20, 220 
               mX2, mY2 = (ii * 260) + 165, 220
               mX3, mY3 = (ii * 260) + 210, 220
               if i == compt : break
            if i <= 26:
               ii = i - 24
               mX1, mY1 = (ii * 260) +  20, 250 
               mX2, mY2 = (ii * 260) + 165, 250
               mX3, mY3 = (ii * 260) + 210, 250
               if i == compt : break
        #
        mButton.setGeometry(QtCore.QRect(mX1, mY1, 140, 20))
        mButton.setObjectName(mButtonName)
        mButton.setText(self.dicListBlocs[self.dicListLettre[i]]) if self.dicListLettre[i] in self.dicListBlocs else mButton.setText(self.dicListLettre[i])
        #
        mImage.setGeometry(QtCore.QRect(mX2, mY2, 40, 20))
        mImage.setObjectName(mImageName)      
        if self.dicListLettre[i] in self.mDic_LH :
           if "second" in mButtonName :
              varColor = str( self.mDic_LH[self.dicListLettre[i]].split(',')[1] ) 
           else :
              varColor = str( self.mDic_LH[self.dicListLettre[i]].split(',')[0] ) 
           zStyleBackground = "QLabel { background-color : "  + varColor + "; }"
           mImage.setStyleSheet(zStyleBackground)
        #
        mReset.setGeometry(QtCore.QRect(mX3, mY3, 40, 20))
        mReset.setObjectName(mResetName)
        mReset.setText("Reset")
        #
        mButton.clicked.connect(lambda : self.functionColor(mImage, i))
        mReset.clicked.connect(lambda : self.functionResetColor(mImage, i, mButtonName))
        return 

    #========
    def functionSaveColor(self):
        mSettings = QgsSettings()
        mTitre = QtWidgets.QApplication.translate("colorbloc_ui", "Confirmation", None)
        mLib = QtWidgets.QApplication.translate("colorbloc_ui", "You will save all your changes..", None)
        mLib1 = QtWidgets.QApplication.translate("colorbloc_ui", "Are you sure you want to continue ?", None)

        if QMessageBox.question(None, mTitre, mLib + "<br><br>" + mLib1,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.Yes :
           mChild_premier = [mObj for mObj in self.tabWidgetColor_premier.children()] 
           mChild_second  = [mObj for mObj in self.tabWidgetColor_second.children()] 

           mLettre, mColorFirst, mColorSecond, mDicSaveColor = "", None, None, {}  
           for mObj in mChild_premier :
               for i in range(27) :
                   if mObj.objectName() == "img_" + str(i) :
                      mLettre      = str(self.dicListLettre[i])
                      mColor       = mObj.palette().color(QPalette.Window)
                      mColorFirst  = mColor.name()
                      mDicSaveColor[mLettre] = mColorFirst
                      break
           for mObj in mChild_second :
               for ii in range(27) :
                   if mObj.objectName() == "img_second_" + str(ii) :
                      mLettre      = str(self.dicListLettre[ii])                     
                      mColor       = mObj.palette().color(QPalette.Window)          
                      mColorSecond = mColor.name()
                      mDicSaveColor[mLettre] =  "'" + (mDicSaveColor[mLettre] + "','" + mColorSecond + "'")  if mLettre in mDicSaveColor else mColorSecond
                      break
           #-
           mSettings.beginGroup("ASGARD_MANAGER")
           mSettings.beginGroup("DashBoard")
           mSettings.beginGroup("BlocsColor")
           for key, value in mDicSaveColor.items():
               mSettings.setValue(key, value)
           mSettings.endGroup()
           mSettings.endGroup()
           mSettings.endGroup()    
           zMess, zTitre = QtWidgets.QApplication.translate("colorbloc_ui", "Colors saved.", None), QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           QMessageBox.information(self, zTitre, zMess) 
        return 

    #========
    def functionColor(self, mImage, i):
        mColor = mImage.palette().color(QPalette.Window)
        mColorInit = QColor(mColor.name())
        zMess = "%s %s" %(QtWidgets.QApplication.translate("colorbloc_ui", "Choose a color for the block : ", None), \
                          str(self.dicListBlocs[self.dicListLettre[i]]) if self.dicListLettre[i] in self.dicListBlocs else str(self.dicListLettre[i]))
        zColor = QColorDialog.getColor(mColorInit, self, zMess)
        if zColor.isValid():
           zStyleBackground = "QLabel { background-color : " + zColor.name() + " }"
           mImage.setStyleSheet(zStyleBackground)
        return 
        
    #========
    def functionResetColor(self, mImage, i, mButtonName):
        listBlocsKey = [
                "c",
                "w",
                "s",
                "p",
                "r",
                "x",
                "e",
                "z",
                "autre",
                "d",
                "a", "b","f", "g", "h", "i", "j", "k", "l", "m","n", "o", "q", "t", "u", "v",  "y"
                ]
        listBlocsValue = [
                "'#ff8d7e','#ffe3df'",
                "'#ff9940','#ffe6cf'",
                "'#fdcf41','#fff3d0'",
                "'#5770BE','#d5dbef'",
                "'#91ae4f','#e4ebd3'",
                "'#484D7A','#d1d3de'",          
                "'#00AC8C','#bfeae2'",
                "'#7D4E5B','#bea7ad'",
                "'#808080','#bfbfbf'",
                "'#958B62','#e5e2d8'" ,
                "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'",
                "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'",
                "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'", "'#808080','#bfbfbf'",
                "'#808080','#bfbfbf'", "'#808080','#bfbfbf'"
                ] 
        mDicDashBoard = dict(zip(listBlocsKey, listBlocsValue))
 
        if self.dicListLettre[i] in self.mDic_LH :
           if "second" in mButtonName :
              varColor = str( mDicDashBoard[self.dicListLettre[i]].split(',')[1] )
           else :               
              varColor = str( mDicDashBoard[self.dicListLettre[i]].split(',')[0] )
           zStyleBackground = "QLabel { background-color : "  + varColor + "; }"
           mImage.setStyleSheet(zStyleBackground)
        return                                                     