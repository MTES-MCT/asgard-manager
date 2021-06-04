# (c) Didier  LECLERC 2020 CMSIG MTES-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé mars 2020 version 1.0
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QAction, QMenu , QMenuBar, QApplication, QMessageBox, QFileDialog, QTextEdit, QMainWindow, 
                            QTableView, QDockWidget, QVBoxLayout, QTabWidget, QWidget, QAbstractItemView, QTreeWidgetItemIterator)
 
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from qgis.core import QgsSettings

from . import bibli_asgard
from .bibli_asgard import *
from . import docolorbloc

from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtQuick import QQuickItem, QQuickPaintedItem, QQuickView, QQuickWindow

from qgis.PyQt.QtCore import QUrl
import qgis                              
import os                       
import datetime
import os.path
import time

#===================
# QML 
#===================
#-----------------------------------

def executeGraphColorBloc(self):
    self.mDic_LH = bibli_asgard.returnAndSaveDialogParam(self, "Load")
    d = docolorbloc.Dialog()
    d.exec_() 
        
def executeGraphQml(self):
    self.mDic_LH = bibli_asgard.returnAndSaveDialogParam(self, "Load")
    mChoixGraph        = self.comboChoiceGraph.currentText()
    self.mChoiceGraph  = self.dicChoiceGraph[mChoixGraph][0]
    self.mTypeGraph    = "pie" if self.radioPie.isChecked() else "bar"
    today = datetime.datetime.now() 
    myPathHtmlGraph = os.path.dirname(__file__) + "\\qml\\" + self.dicChoiceGraph[mChoixGraph][1] + ".qml"
    myPathHtmlGraph = myPathHtmlGraph.replace("\\","/")

    #---- Parcours  pour non sélection 
    #Filtrer en fonction sélection TreeViewGraph
    mReturnItemTreeSchemasBlocs = []
    iterator = QTreeWidgetItemIterator(self.Dialog.mTreeGraphSchemasBlocs)
    while iterator.value():
       itemValue = iterator.value()
       #----
       if itemValue.parent() != None :
          if itemValue.checkState(0) == Qt.Checked :
             mReturnItemTreeSchemasBlocs.append(itemValue.text(0))
       iterator += 1
    #---- Parcours

    mContinue = (False if mChoixGraph == 'Aucun' else True )

    if mContinue and self.mChoiceGraph == "graph2" and len(mReturnItemTreeSchemasBlocs) == 0  :  # Aucune sélection dans TreeSelect mTreeGraphSchemasBlocs
       mContinue = False

    if self.mChoiceGraph == "graph3" :
       mTitre = QtWidgets.QApplication.translate("bibli_asgard", "Confirmation", None)
       mLib = QtWidgets.QApplication.translate("bibli_asgard", "The time for this processing takes a few minutes depending on the size of your database.", None)
       mLib1 = QtWidgets.QApplication.translate("bibli_asgard", "Are you sure you want to continue ?", None)

       if QMessageBox.question(None, mTitre, mLib + "<br><br>" + mLib1,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.No : 
          mContinue = False
       
    if mContinue :
       QApplication.instance().setOverrideCursor(Qt.WaitCursor)

       if self.mChoiceGraph == "graph1" or self.mChoiceGraph == "graph3" :
          graphVolumeDesBasesQml(self, myPathHtmlGraph)
       elif self.mChoiceGraph == "graph2" :
          graphSchemasParBlocsQml(self, myPathHtmlGraph)

       mUrlHtml = QUrl.fromLocalFile(myPathHtmlGraph)
       if not hasattr(self, 'mVisuWeb') :
          self.groupBoxAffichageGraphLayout = QVBoxLayout(self.groupBoxAffichageRightDash)
          self.mVisuWeb = VUEWEBQML(self.groupBoxAffichageGraphLayout)
          self.mVisuWeb.loadUrl(mUrlHtml, "ASGARD", self.dicChoiceGraph[mChoixGraph][1])
       else : 
          self.mVisuWeb.reloadUrl(mUrlHtml, self.dicChoiceGraph[mChoixGraph][1])
       QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
    return
    
#===================
# QML = Volumes des bases
#===================
def graphVolumeDesBasesQml(self, myPathHtmlGraph):
    #===================
    #-----------
    mChoixGraph = self.comboChoiceGraph.currentText()
    if self.dicChoiceGraph[mChoixGraph][0] ==  "graph1" :
       mKeySql = bibli_asgard.dicListSql(self,'volumeDesBases')
    elif self.dicChoiceGraph[mChoixGraph][0] ==  "graph3" :
       mKeySql = bibli_asgard.dicListSql(self,'volParBloc')
    mRequest = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)

    if mRequest == None :
       #Géré en amont dans la fonction executeSqlNoReturn
       pass 
    else :   
        mTitle = self.dicChoiceGraph[mChoixGraph][2] 
        mLarg, mHaut = self.Dialog.groupBoxAffichageRightDash.width(), self.Dialog.groupBoxAffichageRightDash.height()
        createQml(self, self.mChoiceGraph, myPathHtmlGraph, mRequest, mLarg, mHaut)           
    return
    
#===================
# QML = Schémas par Blocs fonctionnels
#===================
def graphSchemasParBlocsQml(self, myPathHtmlGraph):
    dicListBlocs = bibli_asgard.returnLoadBlocParam()
    mConfigConnection = self.connectBaseAsgard[2].split()
    #self.dbName    = [ elem for elem in mConfigConnection if "dbname=" in elem ][0].split('=')[1]  #Nom de la base de données
    #print("graphSchemasParBlocsQml" + str(self.dbName))
    
    #Traitement Data 
    #Filtrer en fonction sélection TreeViewGraph
    mReturnItemTreeSchemasBlocs = []
    #---- Parcours
    iterator = QTreeWidgetItemIterator(self.Dialog.mTreeGraphSchemasBlocs)
    while iterator.value():
       itemValue = iterator.value()
       #----
       if itemValue.parent() != None :
          if itemValue.checkState(0) == Qt.Checked :
             mReturnItemTreeSchemasBlocs.append(itemValue.text(0))
       iterator += 1
    #---- Tri
    dicListBlocsSelection = {}
    for key, value in self.dicListBlocs.items() :
        if value in mReturnItemTreeSchemasBlocs :
           dicListBlocsSelection[key] = value
    #---- 
    mBlocs, mSchemas, mCenter = [], [], self.dbName
    mBlocIdTempo = ""
    mBlocsTempo = []
    mSchemasTempo = []
    lastmBlocsTempo = []
    compt = 0
    first = True

    for row in sorted(self.mSchemasBlocs, key=lambda colonnes: colonnes[1] if colonnes[1] != None else 'autre', reverse = False) :
      mKey = row[1] if row[1] != None else 'autre'
      if mKey in dicListBlocsSelection :  #Si dans la sélection 
        if first : 
           mBlocIdTempo  = row[1]
           mBlocsTemp    = dicListBlocsSelection[mKey]
           mBlocsKeyTemp = mKey
           first = False
           #compt += 1
          
        if mBlocIdTempo != row[1] :
           mBlocsTempo.append(mBlocsTemp)
           mBlocsTempo.append(compt)
           mBlocsTempo.append(mBlocsKeyTemp)
           #  - ajout
           mBlocs.append(mBlocsTempo)
           mSchemas.append( mSchemasTempo )
           # - réinit
           compt = 0
           mBlocsTempo = []
           mSchemasTempo = []
           mBlocIdTempo = row[1]
           mBlocsTemp = dicListBlocsSelection[mKey]
           mBlocsKeyTemp = mKey
           
        if row[2] :
           mSchemasTempo.append(row[0])
           mSchemasTempo.append(1)
           mSchemasTempo.append(mKey)
           compt += 1
        lastmBlocsTempo = []
        lastmBlocsTempo.append(mBlocsTemp)
        lastmBlocsTempo.append(compt)
        lastmBlocsTempo.append(mBlocsKeyTemp)
        lastmSchemas = compt
    #Last occurrence
    mBlocs.append(lastmBlocsTempo)   # Nom, Nombre, Id (lettre)}
    mSchemas.append( mSchemasTempo)  # Nom, Nombre = 1
    #Last occurrence

    mChoixGraph = self.comboChoiceGraph.currentText()
    mTitle      = self.dicChoiceGraph[mChoixGraph][2] 
    mLarg, mHaut = self.Dialog.groupBoxAffichageRightDash.width(), self.Dialog.groupBoxAffichageRightDash.height()

    mRequest = [ mBlocs, mSchemas ]
    if len(mBlocs[0]) > 0 :
       createQml(self, self.mChoiceGraph, myPathHtmlGraph, mRequest, mLarg, mHaut)           
    return
    
#-----------------------------------
def createQml(self, mChoiceGraph, myPathQml, mRequest, mLarg, mHaut):
    #Alimentation Paramètres
    dicOptionsGraph = {}
    dicOptionsGraph["mChoiceGraph"]       = mChoiceGraph
    dicOptionsGraph["radioPieBar"]        = "pie" if self.radioPie.isChecked() else "bar"
    dicOptionsGraph["spinBoxHole"]        = self.spinBoxHole.value()
    dicOptionsGraph["spinBoxMiddle"]      = self.spinBoxMiddle.value()
    dicOptionsGraph["spinBoxMax"]         = self.spinBoxMax.value()
    dicOptionsGraph["spinBoxMax"]         = self.spinBoxMax.value()
    dicOptionsGraph["boxBar"]             = "full" if self.radioBarFull.isChecked() else "auto"
    dicOptionsGraph["caseEtiGraph"]       = True if self.caseEtiGraph.isChecked() else False
    dicOptionsGraph["caseEtiLibelle"]     = True if self.caseEtiLibelle.isChecked() else False
    dicOptionsGraph["caseEtiPourc"]       = True if self.caseEtiPourc.isChecked() else False
    dicOptionsGraph["caseEtiValeur"]      = True if self.caseEtiValeur.isChecked() else False
    dicOptionsGraph["caseLegGraph"]       = True if self.caseLegGraph.isChecked() else False
    dicOptionsGraph["caseLegOrien"]       = "Nord" if self.caseLegNord.isChecked() else "Ouest" if self.caseLegOuest.isChecked() else "Est" if self.caseLegEst.isChecked() else "Sud"
    dicOptionsGraph["caseTitreGraph"]     = True if self.caseTitreGraph.isChecked() else False
    dicOptionsGraph["zoneTitre"]          = self.zoneTitre.text()
    dicOptionsGraph["caseAnimationGraph"] = True if self.caseAnimationGraph.isChecked() else False

    if dicOptionsGraph["mChoiceGraph"] == "graph1" or dicOptionsGraph["mChoiceGraph"] == "graph3" :
       QmlDeb = ""
       QmlDeb += "import QtCharts 2.2\n"
       QmlDeb += "import QtQuick 2.11\n"
       QmlDeb += "ChartView {\n"
       QmlDeb += "   id: chartview\n"
       #QmlDeb += "   theme: ChartView.ChartThemeHighContrast\n"          
       QmlDeb += "   width: " + str(mLarg) + "\n"
       QmlDeb += "   height: " + str(mHaut) + "\n"
       QmlDeb += "   antialiasing: true\n"
       
       if dicOptionsGraph["caseTitreGraph"] :
          QmlDeb += "   title: '" + dicOptionsGraph["zoneTitre"] + "'\n"
          QmlDeb += "   titleColor: 'black'\n"
          
       QmlDeb += "   backgroundColor: '#FFFFFF'\n"
       
       if dicOptionsGraph["caseAnimationGraph"] :
          QmlDeb += "   animationOptions: ChartView.AllAnimations\n"
          
       QmlDeb += "   localizeNumbers : true\n"
       
       if dicOptionsGraph["caseLegGraph"] :
          QmlDeb += "   legend.labelColor: 'black'\n"
          QmlDeb += "   legend.visible: true\n"
          if dicOptionsGraph["caseLegOrien"] == "Nord" :
             QmlDeb += "   legend.alignment: Qt.AlignTop\n"
          elif dicOptionsGraph["caseLegOrien"] == "Ouest" :
             QmlDeb += "   legend.alignment: Qt.AlignLeft\n"
          elif dicOptionsGraph["caseLegOrien"] == "Est" :
             QmlDeb += "   legend.alignment: Qt.AlignRight\n"
          elif dicOptionsGraph["caseLegOrien"] == "Sud" :
             QmlDeb += "   legend.alignment: Qt.AlignBottom\n"
          QmlDeb += "   legend.font: QFont('Arial', 14)\n\n"
       else :
          QmlDeb += "   legend.visible: false\n"

       QmlDeb += '   Image {                                 \n'
       QmlDeb += '      source: "../icons/logo/logoqml.png"       \n'
       QmlDeb += '      x: 0; y: 0                          \n'                                      
       QmlDeb += '      width: 116; height: 47             \n'
       QmlDeb += '     }                                       \n'
       
       if dicOptionsGraph["radioPieBar"] == "pie" :
          mSizeHole = dicOptionsGraph["spinBoxHole"]
          mSize     = dicOptionsGraph["spinBoxMax"]
          QmlDeb += "   PieSeries {\n"
          QmlDeb += "      id: pieSeries\n"
          QmlDeb += "      name: 'Noms'\n"
          QmlDeb += '      size: ' + str(mSize)             + '                                  \n'
          QmlDeb += '      holeSize: ' + str(mSizeHole)     + '                                  \n'
          #-
          QmlDeb += '      onDoubleClicked: {                                                              \n'
          QmlDeb += '          for ( var i = 0; i < pieSeries.count; i++ ) {                                   \n'
          QmlDeb += '              if (pieSeries.at(i).exploded == false)                                                             \n'
          QmlDeb += '                 pieSeries.at(i).exploded = true                                            \n'
          QmlDeb += '              else                                                             \n'
          QmlDeb += '                 pieSeries.at(i).exploded = false                                            \n'
          QmlDeb += '              }                                                                     \n'
          QmlDeb += '                }                                                               \n'

          #Gestion de la liste pour mapper le résultat graph3 en graph1
          if dicOptionsGraph["mChoiceGraph"] == "graph3" :
             mListeRequestGraph3 = [ [ ["", (elem[0] if elem[0] != None else "autre"), float(elem[1]) ] for elem in mRequest[0] ] ]
             mRequest = list(mListeRequestGraph3)

          mDiv = 1000000
          with open(myPathQml, "w",encoding="utf-8") as zFileQml :
               zFileQml.write(QmlDeb)
               # 
               mTotal = 0   
               for row in mRequest[0] :
                   mTotal += row[2]
               mTotal = mTotal / mDiv
               #
               #print(self.dicListBlocs)
               for row in mRequest[0] :
                   mEti = "<center>" 
                   if dicOptionsGraph["caseEtiLibelle"] :
                      if row[1] in self.dicListBlocs :
                         mEti += self.dicListBlocs[str(row[1])] + "<br>"
                      else :
                         mEti += str(row[1]) + "<br>"
                   if dicOptionsGraph["caseEtiPourc"] :
                      mEti += "<b>" + str(round((row[2]/mDiv/mTotal*100),2)) + " %</b>" + "<br>"
                   if dicOptionsGraph["caseEtiValeur"] :
                      mEti += str(round((row[2]/mDiv),2)) + "<br>"
                   try :
                      mEti =  mEti[:-4] if mEti[-4:] == "<br>" else mEti
                   except : pass
                   mEti += "</center>" 
                   #Gestion des couleurs pour mapper le résultat graph3 en graph1
                   if dicOptionsGraph["mChoiceGraph"] == "graph1" :
                      if str(row[1]).upper() == self.dbName.upper() :
                         varColor = "; color : '#958B62' "
                      else :
                         varColor = ""
                   elif dicOptionsGraph["mChoiceGraph"] == "graph3" :
                      if row[1] in self.mDic_LH :
                         varColor = ";color : " + str( self.mDic_LH[row[1]].split(',')[0] ) 
                      else :
                         varColor = ""
 
                   if dicOptionsGraph["caseEtiGraph"] :
                      if str(row[1]).upper() == self.dbName.upper() :
                         lineDataQml = "      PieSlice { label: '" + mEti + "'; value: " + str(round((row[2]/mDiv),3)) + " \
                         ; labelPosition : PieSlice.LabelOutside ;labelVisible : true; exploded : true " + varColor + "\
                         ; onClicked: { if (exploded == false) \
                                                {exploded = true } \
                                             else \
                                                {exploded = false } \
                                      }\
                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }\
                                                       }\n"
                      else :
                         lineDataQml = "      PieSlice { label: '" + mEti + "'; value: " + str(round((row[2]/mDiv),3)) + " \
                         ; labelPosition : PieSlice.LabelOutside ;labelVisible : true " + varColor + "\
                         ; onClicked: { if (exploded == false) \
                                                {exploded = true } \
                                             else \
                                                {exploded = false } \
                                      }\
                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }\
                                                       }\n"
                   else :
                      if str(row[1]).upper() == self.dbName.upper() : 
                         lineDataQml = "      PieSlice { label: '" + mEti + "'; value: " + str(round((row[2]/mDiv),3)) + " \
                         ; labelPosition : PieSlice.LabelOutside ; exploded : true" + varColor + "\
                         ; onClicked: { if (exploded == false) \
                                                {exploded = true } \
                                             else \
                                                {exploded = false } \
                                      }\
                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }\
                                                       }\n"
                      else :
                         lineDataQml = "      PieSlice { label: '" + mEti + "'; value: " + str(round((row[2]/mDiv),3)) + " \
                         ; labelPosition : PieSlice.LabelOutside " + varColor + "\
                         ; onClicked: { if (exploded == false) \
                                                {exploded = true } \
                                             else \
                                                {exploded = false } \
                                      }\
                          onHovered: { if (state) tooltip.visible=true; tooltip.text= 'MyToolTip.' }\
                                                       }\n"
                   zFileQml.write(lineDataQml) 
               #-------
               QmlFin = "   }\n"
               zFileQml.write(QmlFin)
               #-------
               QmlFin = "}\n"
               zFileQml.write(QmlFin)
               #-------
       elif dicOptionsGraph["radioPieBar"] == "bar" :
          #Gestion de la liste pour mapper le résultat graph3 en graph1
          if dicOptionsGraph["mChoiceGraph"] == "graph3" :
             mListeRequestGraph3 = [ [ ["", (elem[0] if elem[0] != None else "autre"), float(elem[1]) ] for elem in mRequest[0] ] ]
             mRequest = list(mListeRequestGraph3)
          #print(mRequest)
          QmlDeb += "   anchors.fill: parent\n\n"
          mDiv = 1000000
          with open(myPathQml, "w",encoding="utf-8") as zFileQml :
               QmlDeb += "   StackedBarSeries {\n"
               #QmlDeb += "  HorizontalStackedBarSeries {\n"

               QmlDeb += "      id: barSeries\n"
               #axeX
               lineAxeX = [ (row[1] if row[1] not in self.dicListBlocs else  self.dicListBlocs[str(row[1])] ) for row in mRequest[0] ]
               QmlDeb += "      axisX: BarCategoryAxis  { categories: " + str(lineAxeX) + "}\n"
               if dicOptionsGraph["boxBar"] == "full" : 
                  QmlDeb += "      axisY: ValueAxis { min: 0;max: 100; tickCount: 5  } \n"
               if dicOptionsGraph["caseEtiGraph"] :
                  QmlDeb += "      labelsVisible : true\n"
               QmlDeb += "      labelsPosition : AbstractBarSeries.LabelsInsideEnd \n"
               
               zFileQml.write(QmlDeb)
               # 
               mTotal = 0   
               for row in mRequest[0] :
                   mTotal += row[2]
               mTotal = mTotal / mDiv
               #    
               iLine = 0
               for row in mRequest[0] :
                   #Gestion des couleurs pour mapper le résultat graph3 en graph1
                   if dicOptionsGraph["mChoiceGraph"] == "graph1" :
                      if str(row[1]).upper() == self.dbName.upper() :
                         varColor = "; color : '#958B62' "
                      else :
                         varColor = ""
                   elif dicOptionsGraph["mChoiceGraph"] == "graph3" :
                      if row[1] in self.mDic_LH :
                         varColor = ";color : " + str( self.mDic_LH[row[1]].split(',')[0] ) 
                      else :
                         varColor = ""

                   iValue = 0
                   mListValue = []
                   while iValue < len(mRequest[0]) :
                      mEti = "<center>" 
                      if dicOptionsGraph["caseEtiLibelle"] :
                         if row[1] in self.dicListBlocs :
                            mEti += self.dicListBlocs[str(row[1])] + "<br>"
                         else :
                            mEti += str(row[1]) + "<br>"
                      if dicOptionsGraph["caseEtiPourc"] :
                         mEti += "<b>" + str(round((row[2]/mDiv/mTotal*100),2)) + " %</b>" + "<br>"
                      if dicOptionsGraph["caseEtiValeur"] :
                         mEti += str(round((row[2]/mDiv),2)) + "<br>"
                      try :
                         mEti =  mEti[:-4] if mEti[-4:] == "<br>" else mEti
                      except : pass
                      mEti += "</center>" 
                      mListValue.append(round((row[2]/mDiv/mTotal*100),2)) if iLine == iValue else mListValue.append(0)
                      iValue += 1
                   lineDataQml = "      BarSet { label: '" + mEti + "'; values: " + str(mListValue) +  varColor + "}\n"                
                   zFileQml.write(lineDataQml)
                   iLine += 1
  
               #-------
               QmlFin = "   }\n"
               zFileQml.write(QmlFin)
               #-------
               QmlFin = "}\n"
               zFileQml.write(QmlFin)
               #-------

    elif dicOptionsGraph["mChoiceGraph"] == "graph2" :
       #Filtrer en fonction sélection TreeViewGraph
       #---- Parcours
       mReturnItemTreeSchemasBlocs = []
       iterator = QTreeWidgetItemIterator(self.Dialog.mTreeGraphSchemasBlocs)
       while iterator.value():
          itemValue = iterator.value()
          #----
          if itemValue.parent() != None :
             if itemValue.checkState(0) == Qt.Checked :
                mReturnItemTreeSchemasBlocs.append(itemValue.text(0))
          iterator += 1
       #---- Tri
       dicListBlocsSelection = {}
       for key, value in self.dicListBlocs.items() :
           if value in mReturnItemTreeSchemasBlocs :
              dicListBlocsSelection[key] = value
       #---- 
       #---- Parcours

       QmlDeb = ""
       QmlDeb += "import QtCharts 2.0\n"
       QmlDeb += "import QtQuick 2.4\n"
       QmlDeb += "ChartView {\n"
       #QmlDeb += "   theme: ChartView.ChartThemeHighContrast\n"          
       QmlDeb += "   width: " + str(mLarg) + "\n"
       QmlDeb += "   height: " + str(mHaut) + "\n"
       QmlDeb += "   antialiasing: true\n"
       
       if dicOptionsGraph["caseTitreGraph"] :
          QmlDeb += "   title: '" + dicOptionsGraph["zoneTitre"] + "'\n"
          QmlDeb += "   titleColor: 'black'\n"
          
       QmlDeb += "   backgroundColor: '#FFFFFF'\n"
       if dicOptionsGraph["caseAnimationGraph"] :
          QmlDeb += "   animationOptions: ChartView.AllAnimations\n"

       if dicOptionsGraph["caseLegGraph"] :
          QmlDeb += "   legend.labelColor: 'black'\n"
          QmlDeb += "   legend.visible: true\n"
          if dicOptionsGraph["caseLegOrien"] == "Nord" :
             QmlDeb += "   legend.alignment: Qt.AlignTop\n"
          elif dicOptionsGraph["caseLegOrien"] == "Ouest" :
             QmlDeb += "   legend.alignment: Qt.AlignLeft\n"
          elif dicOptionsGraph["caseLegOrien"] == "Est" :
             QmlDeb += "   legend.alignment: Qt.AlignRight\n"
          elif dicOptionsGraph["caseLegOrien"] == "Sud" :
             QmlDeb += "   legend.alignment: Qt.AlignBottom\n"
          QmlDeb += "   legend.font: QFont('Arial', 14)\n\n"
       else :
          QmlDeb += "   legend.visible: false\n"

       mBlocs   = mRequest[0]
       mSchemas = mRequest[1]

       if dicOptionsGraph["radioPieBar"] == "pie" :
          mSizeHoleIn  = dicOptionsGraph["spinBoxHole"]
          mSizeHoleOut = dicOptionsGraph["spinBoxMiddle"]
          mSizeIn      = dicOptionsGraph["spinBoxMiddle"]
          mSizeOut     = dicOptionsGraph["spinBoxMax"]
          with open(myPathQml, "w",encoding="utf-8") as zFileQml :
               zFileQml.write(QmlDeb)
               lineDataQml = '      PieSeries {                                                                  \n'
               lineDataQml += '          id: pieIn                                                               \n'
               lineDataQml += '          size: ' + str(mSizeIn)             + '                                  \n'
               lineDataQml += '          holeSize: ' + str(mSizeHoleIn)     + '                                  \n'
               #-
               mTotal = 0   
               for mB in mBlocs :
                   mTotal += mB[1]
               mTotal = mTotal
               #
               for mB in mBlocs:
                   mEti = "<center>" 
                   if dicOptionsGraph["caseEtiLibelle"] :
                      mEti += str(mB[0]) + "<br>"
                   if dicOptionsGraph["caseEtiPourc"] :
                      mEti += "<b>" + str(round((mB[1]/mTotal*100),2)) + " %</b>" + "<br>"
                   if dicOptionsGraph["caseEtiValeur"] :
                      mEti += str(mB[1]) + "<br>"
                   try :
                      mEti =  mEti[:-4] if mEti[-4:] == "<br>" else mEti
                   except : pass
                   mEti += "</center>" 

                   lineDataQml += '          PieSlice { label : "' + mEti + '"; value : ' + str(mB[1]) + '; color : ' + str( self.mDic_LH[mB[2]].split(',')[0]) + ' } \n'
               lineDataQml += '      }                                                                           \n'
               #-
               lineDataQml += '      PieSeries {                                                                 \n'
               lineDataQml += '          id: pieOut                                                              \n'
               lineDataQml += '          size:       ' + str(mSizeOut)     + '                                   \n'
               lineDataQml += '          holeSize:   ' + str(mSizeHoleOut) + '                                   \n'
               #-

               for mS in mSchemas:
                   iSchem = 0
                   while iSchem < len(mS) :
                      mEti = "<center>" 
                      if dicOptionsGraph["caseEtiLibelle"] :
                         mEti += str(mS[iSchem]) + "<br>"
                      if dicOptionsGraph["caseEtiPourc"] :
                         mEti += "<b>" + str(round((mS[iSchem + 1]/mTotal*100),2)) + " %</b>" + "<br>"
                      if dicOptionsGraph["caseEtiValeur"] :
                         mEti += str(mS[iSchem + 1]) + "<br>"
                      try :
                         mEti =  mEti[:-4] if mEti[-4:] == "<br>" else mEti
                      except : pass
                      mEti += "</center>" 


                      lineDataQml += '          PieSlice { label : "' + str(mS[iSchem]) + '"; value : ' + str(mS[iSchem + 1]) + '; color : ' + str( self.mDic_LH[mS[iSchem + 2]].split(',')[1]) + ' } \n'
                      iSchem += 3
               lineDataQml += '      }                                                                           \n'
               #-
               zFileQml.write(lineDataQml)
               #-------
               QmlComponent =  "   Component.onCompleted: {                                       \n"
               QmlComponent += "   for (var i = 0; i < pieOut.count; i++) {                     \n"
               if dicOptionsGraph["caseEtiGraph"] :
                  QmlComponent += "       pieOut.at(i).labelPosition = PieSlice.LabelOutside;      \n"
                  QmlComponent += "       pieOut.at(i).labelVisible = true;                        \n"
               QmlComponent += "       pieOut.at(i).borderWidth = 3;                            \n"
               QmlComponent += "   }                                                              \n"
               QmlComponent += "   for (var i = 0; i < pieIn.count; i++) {                     \n"
               if dicOptionsGraph["caseEtiGraph"] :
                  QmlComponent += "       pieIn.at(i).labelPosition = PieSlice.LabelInsideNormal; \n"
                  QmlComponent += "       pieIn.at(i).labelVisible = true;                        \n"
               QmlComponent += "       pieIn.at(i).borderWidth = 2;                            \n"
               QmlComponent += "   }                                                              \n"
               QmlComponent += "   }                                                              \n"
               zFileQml.write(QmlComponent)
               #-------
               QmlFin = "}\n"
               zFileQml.write(QmlFin)
               #------- 

    return 


#========================================================
# Class pour les DashBoard      
class VUEWEBQML():
                                                                                        
    def __init__(self,mFrame):
        self.tabWidgetGraph = QTabWidget()
        mFrame.addWidget(self.tabWidgetGraph)
        #Menu contextuel QTabWidget for graph
        self.tabWidgetGraph.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabWidgetGraph.customContextMenuRequested.connect(self.menuContextuelGraph) 

    #-------------                                                    
    def menuContextuelGraph(self, point):
        self.graphMenu = QMenu(self.tabWidgetGraph)
        #-------   
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\graph_print.png")          
        zTitleMenu = QtWidgets.QApplication.translate("bibli_graph_asgard", "Graphics: Print preview", None)
        self.treeActionGraphPrint = QAction(QIcon(menuIcon), zTitleMenu, self.graphMenu)
        self.graphMenu.addAction(self.treeActionGraphPrint)
        self.treeActionGraphPrint.triggered.connect( lambda : self.printView())
        self.graphMenu.addSeparator()
        #-------
        menuIcon = bibli_asgard.returnIcon(os.path.dirname(__file__) + "\\icons\\actions\\graph_save.png")          
        zTitleMenu = QtWidgets.QApplication.translate("bibli_graph_asgard", "Graphics: Save image", None)
        self.treeActionGraphSave = QAction(QIcon(menuIcon), zTitleMenu, self.graphMenu)
        self.graphMenu.addAction(self.treeActionGraphSave)
        self.treeActionGraphSave.triggered.connect( lambda : self.saveFileName(self.nameGraph))
        #-------
        if hasattr(self, 'view') :
           if self.view.source().isEmpty() :
              self.treeActionGraphPrint.setEnabled(False)
              self.treeActionGraphSave.setEnabled(False)
           else :
              self.treeActionGraphPrint.setEnabled(True)
              self.treeActionGraphSave.setEnabled(True)
        #-------
        self.graphMenu.exec_(self.tabWidgetGraph.mapToGlobal(point))
        #--
        
    def loadUrl(self, mQurl = None, label ="Blank", nameGraph = ""): 
        self.nameGraph = nameGraph
        self.view = QQuickView()     
        self.contentContainer = QWidget.createWindowContainer(self.view)
        self.view.setResizeMode(QQuickView.SizeRootObjectToView)

        if self.view.status() == QQuickView.Error:
           print("Erreur QQuickView")
           for error in self.view.errors():
               QgsMessageLog.logMessage(error.description())
               print("Message d'erreur :  " + str(error.description()))
        else:
           self.view.engine().clearComponentCache()
           self.view.setSource(mQurl)

        i = self.tabWidgetGraph.addTab(self.contentContainer, label) 
        self.tabWidgetGraph.setCurrentIndex(i)  
        return
        
    def reloadUrl(self, mQurl, nameGraph):
        self.nameGraph = nameGraph
        self.view.engine().clearComponentCache()
        self.view.setSource(mQurl)
        return

    def effaceContenu(self):
        self.view.engine().clearComponentCache()
        self.view.setSource(QUrl(''))
        self.view.source().clear()
        return

    #=For Printer
    def printView(self):
        printer = QPrinter()
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOrientation(QPrinter.Portrait)
        printer.setOutputFormat(QPrinter.NativeFormat)
        #-
        printDialog = QPrintPreviewDialog(printer)
        zTitle = QtWidgets.QApplication.translate("bibli_graph_asgard", "ASGARD MANAGER Graphics", None)
        printDialog.setWindowTitle(zTitle)
        printDialog.setWindowState(Qt.WindowNoState)
        #-
        myGraphView = QTextEdit(self.tabWidgetGraph)
        path = os.path.dirname(__file__) + "\\qml"
        pathFileHtml  = path + "\\graph_printer.html"
        pathFileImage = path + "\\graph_printer.jpg"
        #-
        mLigne = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">'
        mLigne += '<HTML>'
        mLigne += '<HEAD>'
        mLigne += '	<META HTTP-EQUIV="CONTENT-TYPE" CONTENT="text/html; charset=windows-1252">'
        mLigne += '</HEAD>'
        mLigne += '<BODY>'
        mLigne += '<img  src="file:///' + pathFileImage + '" width="' + str(self.tabWidgetGraph.width() * 0.75) + '"  />'
        mLigne += '</BODY>'
        mLigne += '</HTML>'
        #-
        self.saveGraph(pathFileImage)
        myGraphView.setAcceptRichText(True)
        myGraphView.setHtml(mLigne)
        printDialog.paintRequested.connect(myGraphView.print_)
        printDialog.exec_() 
        return

    def saveGraph(self, pathFileImage): 
        mImageGraph = self.view.grabWindow()
        mImageGraph.save(pathFileImage)               
        return 

    def saveFileName(self, mFileSaveInit):
        #Sauvegarde de la boite de dialogue Fichiers
        InitDir = mFileSaveInit
        TypeList = QtWidgets.QApplication.translate("bibli_graph_asgard", "Graphiques Asgard Manager", None) + " (*.jpg)"
        fileName = QFileDialog.getSaveFileName(None,QtWidgets.QApplication.translate("bibli_graph_asgard", "Asgard Manager Charts", None),InitDir,TypeList)
        if fileName[0] != "" : self.saveGraph(fileName[0]) 
        return 
    #=For Printer
  
#========================================================
#========================================================
def dicListSqlGraph(mKeySql):
    mdicListSqlGraph = {}

    #Volume des bases
    mdicListSqlGraph['volumeDesBases'] = ("""
    SELECT row_number() OVER () AS oid,
    pg_database.datname::text AS nom,
    pg_database_size(pg_database.datname) AS taille_en_octets,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS taille
    FROM pg_database
    WHERE pg_database.datistemplate = false
    ORDER BY (pg_database_size(pg_database.datname)) DESC;
                                          """)     
    #Volume par bloc
    mdicListSqlGraph['volParBloc'] = ("""
    SELECT
    bloc,
    coalesce(sum(pg_table_size(pg_class.oid::regclass)), 0) AS table_size,
    pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass))) AS table_size_pretty,
    coalesce(sum(pg_total_relation_size(pg_class.oid::regclass)), 0) AS total_relation_size,
    pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass))) AS total_relation_pretty
    FROM z_asgard.gestion_schema_etr
        LEFT JOIN pg_catalog.pg_class ON relnamespace = oid_schema
    GROUP BY bloc ;
                                          """)     
    #Volume par bloc ancien
    mdicListSqlGraph['volParBloc_ancien'] = ("""
    SELECT a.volume,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'c'::text)::text::integer, 0)
            ELSE 0
        END AS cons_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'c'::text))
            ELSE NULL::text
        END AS cons_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'c'::text)::text::integer, 0)
            ELSE 0
        END AS cons_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'c'::text))
            ELSE NULL::text
        END AS cons_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'w'::text)::text::integer, 0)
            ELSE 0
        END AS travail_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'w'::text))
            ELSE NULL::text
        END AS travail_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'w'::text)::text::integer, 0)
            ELSE 0
        END AS travail_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'w'::text))
            ELSE NULL::text
        END AS travail_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 's'::text)::text::integer, 0)
            ELSE 0
        END AS geo_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 's'::text))
            ELSE NULL::text
        END AS geo_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 's'::text)::text::integer, 0)
            ELSE 0
        END AS geo_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 's'::text))
            ELSE NULL::text
        END AS geo_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'p'::text)::text::integer, 0)
            ELSE 0
        END AS appli_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'p'::text))
            ELSE NULL::text
        END AS appli_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'p'::text)::text::integer, 0)
            ELSE 0
        END AS appli_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'p'::text))
            ELSE NULL::text
        END AS appli_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'r'::text)::text::integer, 0)
            ELSE 0
        END AS ref_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'r'::text))
            ELSE NULL::text
        END AS ref_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'r'::text)::text::integer, 0)
            ELSE 0
        END AS ref_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'r'::text))
            ELSE NULL::text
        END AS ref_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'k'::text)::text::integer, 0)
            ELSE 0
        END AS nc_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'k'::text))
            ELSE NULL::text
        END AS nc_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'k'::text)::text::integer, 0)
            ELSE 0
        END AS nc_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'k'::text))
            ELSE NULL::text
        END AS nc_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'x'::text)::text::integer, 0)
            ELSE 0
        END AS conf_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'x'::text))
            ELSE NULL::text
        END AS conf_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'x'::text)::text::integer, 0)
            ELSE 0
        END AS conf_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'x'::text))
            ELSE NULL::text
        END AS conf_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'e'::text)::text::integer, 0)
            ELSE 0
        END AS ext_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'e'::text))
            ELSE NULL::text
        END AS ext_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'e'::text)::text::integer, 0)
            ELSE 0
        END AS ext_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'e'::text))
            ELSE NULL::text
        END AS ext_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'z'::text)::text::integer, 0)
            ELSE 0
        END AS adm_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'z'::text))
            ELSE NULL::text
        END AS adm_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'z'::text)::text::integer, 0)
            ELSE 0
        END AS adm_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'z'::text))
            ELSE NULL::text
        END AS adm_total_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'd'::text)::text::integer, 0)
            ELSE 0
        END AS corb_data,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_table_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'd'::text))
            ELSE NULL::text
        END AS corb_data_pretty,
        CASE
            WHEN a.volume ~ 'volume'::text THEN COALESCE(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'd'::text)::text::integer, 0)
            ELSE 0
        END AS corb_total,
        CASE
            WHEN a.volume ~ 'volume'::text THEN pg_size_pretty(sum(pg_total_relation_size(pg_class.oid::regclass)) FILTER (WHERE gestion_schema.bloc::text = 'd'::text))
            ELSE NULL::text
        END AS corb_total_pretty
 
    FROM pg_class
        JOIN z_asgard_admin.gestion_schema ON pg_class.relnamespace = gestion_schema.oid_schema,
        unnest(ARRAY['volume'::text]) a(volume)
        GROUP BY a.volume; 
                                          """)     

    return  mdicListSqlGraph[mKeySql]

#==================================================
# FIN
#==================================================
