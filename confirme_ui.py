# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT-Mer/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020 

import os.path
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

from . import asgard_general_ui
from .asgard_general_ui import * 
from . import bibli_asgard
from .bibli_asgard import *
import datetime
import os.path
import time

class Ui_Dialog_Confirme(object):
    def setupUiConfirme(self, DialogConfirme, mDialog, mBaseAsGard, mTypeAction, mKeySqlTransformee):
        self.mBaseAsGard = mBaseAsGard
        self.mDialog = mDialog
        self.mTypeAction = mTypeAction
        if mTypeAction == 'ExtensionPasInstallee' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "ASGARD extension not installed.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "The files required to install the ASGARD extension are missing. You have to install them manually.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\logo\\asgard2.png"
        elif mTypeAction == 'ExtensionPasInstalleePlume' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "PLUME extension not installed.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "The files required to install the PLUME extension are missing. You have to install them manually.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\logo\\plume.png"
        elif mTypeAction == 'FONCTIONreinitAllSchemasFunction' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Reset all rights.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "By continuing, you will restore the standard rights of the roles designated as producer, editor and reader to all referenced schemas ", None)
           zMessConfirme += QtWidgets.QApplication.translate("confirme_ui", "and the objects they contain. Excess rights will be revoked, missing rights reinstated. All rights assigned to other roles will be removed, ", None)
           zMessConfirme += QtWidgets.QApplication.translate("confirme_ui", "as well as any default privileges defined on the schemas. WARNING: this function can be slow (a few minutes, or even tens of minutes)", None)
           zMessConfirme += QtWidgets.QApplication.translate("confirme_ui", " on a base comprising a very large number of diagrams or objects.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\reinitialise_droits.png"
        elif mTypeAction == 'FONCTIONdiagnosticAsgard' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Find all anomalies.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Scans referenced schemas and the objects they contain for missing or excess rights over the ASGARD standard.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\diagnostic.png"
        elif mTypeAction == 'FONCTIONmembreGconsult' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Make all users members of g_consult.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "By continuing, you will make all login roles that aren't already a member of the g_consult role, as recommended for proper functioning of ASGARD. g_consult is a consult role, intended to have read-only access to all public data. The connection role of a user must imperatively belong to g_consult so that he can launch the AsgardMenu plugin.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\gconsult_roles.png"
        elif mTypeAction == 'FONCTIONTableauBord' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Dashboard.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Generates a dashboard from the diagrams and objects visible in the tree structure of the function blocks, taking the filter into account.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\tableaubord.png"
        elif mTypeAction == 'FONCTIONnettoieRoles' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Refresh the role names in the management table.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", 'By continuing, you will refresh the names of the roles listed in the ASGARD management table (as they appear in the "Schemas" tab). This action does not affect the rights in any way, it only allows you to view the correct names when a role has been renamed, or deleted without first launching the "Revoke all rights of the role / group" action.', None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\nettoyage_roles.png"
        elif mTypeAction == 'FONCTIONreferencerAllSchemasFunction' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Reference all the diagrams in the database.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "By continuing, you will proceed to the referencing of all the diagrams of the base still not supported by the mechanisms of ASGARD ", None)
           zMessConfirme += QtWidgets.QApplication.translate("confirme_ui", "(except system diagrams, public and, if it exists, topology). The diagrams will be classified in the tree structure according to their prefix or, ", None)
           zMessConfirme += QtWidgets.QApplication.translate("confirme_ui", 'failing that, in the "Others" block. The rights on the diagrams and the objects they contain will not be affected, you will then have the possibility ', None)
           zMessConfirme += QtWidgets.QApplication.translate("confirme_ui", "to use the functions of ASGARD to reset the rights.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\referencer.png"
        elif mTypeAction == 'FONCTIONimportNomenclature' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Import or repair the national nomenclature.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Imports national nomenclature schemas as inactive schemas. Repeating the operation restores the missing diagrams and resets the tree level labels for all the diagrams in the BOM.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\nomenclature.png"
        elif mTypeAction == 'FONCTIONinstallerAsgard' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Install ASGARD on the base.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "By continuing, you will install the PostgreSQL ASGARD extension, version ", None)
           zMessConfirme  += "<b>" + self.mDialog.asgardVersionDefaut + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", " on database ", None)
           zMessConfirme  += "<b>" + self.mDialog.dbName.upper() + "</b>"
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\installe_asgard.png"
        elif mTypeAction == 'FONCTIONmajAsgard' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Update the ASGARD extension.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Continuing on, you will update the PostgreSQL ASGARD extension (current version ", None)
           zMessConfirme  += "<b>" + self.mDialog.asgardInstalle + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ", target version", None)
           zMessConfirme  += "<b>" + self.mDialog.asgardVersionDefaut + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ") on database ", None)
           zMessConfirme  += "<b>" + self.mDialog.dbName.upper() + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ". This action is irreversible.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\maj_asgard.png"
        elif mTypeAction == 'FONCTIONdesinstallerAsgard' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Uninstall the ASGARD extension.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Continuing on, you will proceed to uninstall the PostgreSQL ASGARD extension on the database ", None)
           zMessConfirme  += "<b>" + self.mDialog.dbName.upper() + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ". This action does not affect the rights attributed to the diagrams and objects of the database, but the information stored in the ASGARD management table (readers and editors designated for the diagrams and tree levels) will be permanently lost.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\desinstalle_asgard.png"
           # For PLUME
        elif mTypeAction == 'FONCTIONinstallerPlume' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Install PLUME on the base.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "By continuing, you will install the PostgreSQL PLUME extension, version ", None)
           zMessConfirme  += "<b>" + self.mDialog.plumeVersionDefaut + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", " on database ", None)
           zMessConfirme  += "<b>" + self.mDialog.dbNamePlume.upper() + "</b>"
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\installe_plume.png"
        elif mTypeAction == 'FONCTIONmajPlume' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Update the PLUME extension.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Continuing on, you will update the PostgreSQL PLUME extension (current version ", None)
           zMessConfirme  += "<b>" + self.mDialog.plumeInstalle + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ", target version", None)
           zMessConfirme  += "<b>" + self.mDialog.plumeVersionDefaut + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ") on database ", None)
           zMessConfirme  += "<b>" + self.mDialog.dbNamePlume.upper() + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ". This action is irreversible.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\maj_plume.png"
        elif mTypeAction == 'FONCTIONdesinstallerPlume' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Uninstall the PLUME extension.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Continuing on, you will proceed to uninstall the PostgreSQL PLUME extension on the database ", None)
           zMessConfirme  += "<b>" + self.mDialog.dbNamePlume.upper() + "</b>"
           zMessConfirme  += QtWidgets.QApplication.translate("confirme_ui", ". This action does not affect the rights attributed to the diagrams and objects of the database, but the information stored in the PLUME management table (readers and editors designated for the diagrams and tree levels) will be permanently lost.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\desinstalle_plume.png"
           # For PLUME
        elif mTypeAction == 'FONCTIONasgard_DiagnosticSchema' :
           self.zMessTitle    =  QtWidgets.QApplication.translate("confirme_ui", "Look for anomalies.", None)
           zMessConfirme  = QtWidgets.QApplication.translate("confirme_ui", "Scans the schema and the objects it contains in search of missing or excess rights compared to the ASGARD standard.", None)
           myPath = os.path.dirname(__file__)+"\\icons\\actions\\diagnostic.png"


        self.mTypeAction = mTypeAction
        self.zMessConfirme =  QtWidgets.QApplication.translate("confirme_ui", zMessConfirme, None)
        if self.mTypeAction != 'ExtensionPasInstallee' and self.mTypeAction != 'ExtensionPasInstalleePlume':
           if mTypeAction == 'FONCTIONasgard_DiagnosticSchema' :
              mKeySql = mKeySqlTransformee # Chgt des paramètres : mKeySqlTransformee contient déjà la requête transformée
           elif self.mTypeAction == 'FONCTIONTableauBord' :
              mKeySql = "" #nécessaire pour la fonction executeFonctionGénérale
           else :
              mKeySql = bibli_asgard.dicListSql(self,mTypeAction)
        else :
           mKeySql = "ExtensionPasInstallee"  # juste pour renseigner la clé, non utilisée après aussi ExtensionPasInstalleePlume
        self.zMessGood = QtWidgets.QApplication.translate("confirme_ui", "Operation performed !!", None)

        DialogConfirme.setObjectName("DialogConfirme")
        DialogConfirme.resize(QtCore.QSize(QtCore.QRect(0,0,520,350).size()).expandedTo(DialogConfirme.minimumSizeHint()))
        iconSource = bibli_asgard.getThemeIcon("asgard2.png")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        DialogConfirme.setWindowIcon(icon)
        #----------
        self.labelImage = QtWidgets.QLabel(DialogConfirme)
        myDefPath = myPath.replace("\\","/")
        carIcon = QtGui.QImage(myDefPath)
        self.labelImage.setPixmap(QtGui.QPixmap.fromImage(carIcon))
        self.labelImage.setGeometry(QtCore.QRect(20, 0, 100, 100))
        self.labelImage.setObjectName("labelImage")
        #----------
        self.label_2 = QtWidgets.QLabel(DialogConfirme)
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
        self.textEdit = QtWidgets.QTextEdit(DialogConfirme)
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
        self.textEdit.height = 250
        self.textEdit.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.textEdit.setGeometry(QtCore.QRect(10, 90, 500, 200))
        #----------
        self.pushButton = QtWidgets.QPushButton(DialogConfirme)
        self.pushButton.setObjectName("pushButton")
        if self.mTypeAction != 'ExtensionPasInstallee' :
           self.pushButton.setGeometry(QtCore.QRect(int( DialogConfirme.width() / 2 ) - 100, 310, 80, 25))
        else :
           self.pushButton.setGeometry(QtCore.QRect(int( DialogConfirme.width() / 2 ) - 40, 310, 80, 25))
        self.pushButton.clicked.connect(lambda : self.executeFonctionGenerale(mKeySql))
        #----------
        self.pushButtonAnnuler = QtWidgets.QPushButton(DialogConfirme)
        self.pushButtonAnnuler.setObjectName("pushButtonAnnuler")
        self.pushButtonAnnuler.setGeometry(QtCore.QRect(int( DialogConfirme.width() / 2 ) + 20, 310, 80, 25))
        self.pushButtonAnnuler.clicked.connect(DialogConfirme.reject)
        if self.mTypeAction == 'ExtensionPasInstallee' :
           self.pushButtonAnnuler.setVisible(False) 
        #----------
        self.afficheUI(DialogConfirme)

    def afficheUI(self, DialogConfirme):
        self.zMessConfirme = returnListeTexte(self, self.zMessConfirme, 400)
        self.zMessConfirme = '<br>{}'.format('<br>'.join(self.zMessConfirme))
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
        mMessBefore = QtWidgets.QApplication.translate("confirme_ui", "Reminder of the definition of the action :", None)
        mMessAfter  = QtWidgets.QApplication.translate("confirme_ui", "Confirm its execution", None)
        MonHtml2 = "<br><u>"
        MonHtml2 += mMessBefore
        MonHtml2 += "</u><br>"
        MonHtml2 += self.zMessConfirme
        MonHtml2 += "<br><br><br><b>"
        if self.mTypeAction != 'ExtensionPasInstallee' :
           MonHtml2 += mMessAfter
        MonHtml2 += "</b><br>"
        MonHtml += MonHtml2
        MonHtml += "</i></p></body></html>"
        DialogConfirme.setWindowTitle("ASGARD Manager - (" + str(bibli_asgard.returnVersion()) + ")")
        self.textEdit.setHtml(QtWidgets.QApplication.translate("confirme_ui", MonHtml, None))
        self.label_2.setText(QtWidgets.QApplication.translate("confirme_ui", self.zMessTitle, None))
        self.pushButton.setText(QtWidgets.QApplication.translate("confirme_ui", "OK", None))
        self.pushButtonAnnuler.setText(QtWidgets.QApplication.translate("confirme_ui", "Cancel", None))
        
    def executeFonctionGenerale(self, mKeySql) :
        if self.mTypeAction == 'FONCTIONdesinstallerAsgard' or self.mTypeAction == 'ExtensionPasInstallee' or \
           self.mTypeAction == 'FONCTIONdesinstallerPlume'  or self.mTypeAction == 'ExtensionPasInstalleePlume' :
           self.mDialog.comboAdresse.setCurrentText("Aucun")
                                                            
        if self.mTypeAction != 'ExtensionPasInstallee' and self.mTypeAction != 'ExtensionPasInstalleePlume':
           if self.mTypeAction == 'FONCTIONdiagnosticAsgard' or self.mTypeAction == 'FONCTIONasgard_DiagnosticSchema' :
              r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSql(self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
           else :
              if self.mTypeAction != 'FONCTIONTableauBord' :
                 r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.mBaseAsGard.executeSqlNoReturn(self.mDialog, self.mBaseAsGard.mConnectEnCours, self.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
           #--
           if self.mTypeAction == 'FONCTIONdiagnosticAsgard' or self.mTypeAction == 'FONCTIONasgard_DiagnosticSchema' :
              if r != None :
                 if len(r) == 0 :
                    zMess, zTitre = self.zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
                    zMess += "<br><br><b>" + QtWidgets.QApplication.translate("confirme_ui", "No anomalies detected.", None).upper() + "</b>"
                    QMessageBox.information(self, zTitre, zMess)
                    self.close() 
                 else :
                    #Gestion des anomalies détectées
                    self.close()
                    self.afficheViewDiagnostic(r, self.mTypeAction)
                    try :
                       self.mDialog.tabWidget.setCurrentIndex(3)
                    except :
                       pass 
              else :
                 self.close() 
           #--
           elif self.mTypeAction == 'FONCTIONTableauBord' :
              #Gestion des anomalies détectées
              self.close()
              self.afficheViewTableauBord(self.mTypeAction)
              try :
                 self.mDialog.tabWidget.setCurrentIndex(4)
              except :
                 pass 
           #--
           else :
              if r != False :
                 zMess, zTitre = self.zMessGood, QtWidgets.QApplication.translate("confirme_ui", "Information !!!", None)
                 QMessageBox.information(self, zTitre, zMess)
                 self.close() 
              else :
                 self.close() 
        else :
           self.close() 
        return
        
    #=For Display DashBoard
    def afficheViewTableauBord(self, mTypeAction):
        #for CSV
        self.headerCSV = []
        self.dataCSV   = []
        #for CSV
        myPathIcon = os.path.dirname(__file__)+"\\icons\\"
        dicIcoObjets = {
                      "table"             : myPathIcon + "\\objets\\table.png",
                      "tablereplique"     : myPathIcon + "\\objets\\tablereplique.png",
                      "tabledereplique"   : myPathIcon + "\\objets\\tabledereplique.png",
                      "view"              : myPathIcon + "\\objets\\view.png",
                      "viewreplique"      : myPathIcon + "\\objets\\viewreplique.png",
                      "viewdereplique"    : myPathIcon + "\\objets\\viewdereplique.png",
                      "materialized view" : myPathIcon + "\\objets\\mview.png",
                      "materialized viewreplique"     : myPathIcon + "\\objets\\mviewreplique.png",
                      "materialized viewdereplique"   : myPathIcon + "\\objets\\mviewdereplique.png",
                      "foreign table"     : myPathIcon + "\\objets\\foreign_table.png",
                      "sequence"          : myPathIcon + "\\objets\\sequence.png",
                      "function"          : myPathIcon + "\\objets\\function.png",
                      "type"              : myPathIcon + "\\objets\\type.png",
                      "domain"            : myPathIcon + "\\objets\\domain.png"
                       }

        listBlocsExclus = ['Administrati', 'Corbeil'] 
        myPathImg1 = myPathIcon + "logo\\logo.png"
        mLigne =  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        mLigne +=  '<HTML xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">'
        mLigne +=  '<HEAD>'
        mLigne +=  '</HEAD>'
        mLigne +=  '<BODY>'
        if self.mDialog.zone_affichage_TableauBord.toPlainText() == '' :
           mLigne +=  "<p><img src='" + myPathImg1 + "' height='47' width='116'></p>"
        mDate  =   time.strftime("%d ") + zMyFrenchMonth(float(time.strftime("%m"))) + time.strftime(" %Y - %Hh %Mm %Ss") + "\n"
        if self.mTypeAction == 'FONCTIONTableauBord' :
           mTitre =   "Liste des schémas et objets pour la base de données <b>" + self.mDialog.dbName.upper() + "</b><br>" + mDate 
        mLigne +=  "<center><font color='#958B62' size='4' face = 'Comic sans serif'><b>" + mTitre + "</b><br></font><font color='#440128' size='2' face = 'Comic sans serif'></center>"
        mLigne +=  "<TABLE style='border-collapse:collapse' style='border-color:#958B62' border='1' style='border-style:solid' width=100%>"
        mLigne +=  "  <TR style='color:#FFFFFF' style='background-color:#958B62'>"
        if self.mDialog.ctrlReplication :
           #for CSV
           self.headerCSV = ['Répliqué', 'Blocs fonctionnels']
           #for CSV
           mLigne +=     '<TH width=5% >Répliqué</TH>'
           mLigne += '    <TH width=20% >Blocs fonctionnels</TH>'
        else :
           #for CSV
           self.headerCSV = ['Blocs fonctionnels']
           #for CSV
           mLigne += '    <TH width=25% >Blocs fonctionnels</TH>'
        #for CSV
        self.headerCSV.append('Schémas')
        self.headerCSV.append('Nom de l\'objet')
        self.headerCSV.append('Type de l\'objet')
        #for CSV

        mLigne +=     '<TH width=25% >Schémas</TH>'
        mLigne +=     '<TH width=35% >Nom de l\'objet</TH>'
        mLigne +=     '<TH width=15% >Type de l\'objet</TH>'
        mLigne += '  </TR>\n'

        mBloc, mCodeBloc = "", ""
        mSchema, actif   = "", False
        mObjet, mTypeObj, mReplique = "", "", False
        findElem = False
        listBlocsExclusFlags = False
        iterator = QTreeWidgetItemIterator(self.mDialog.mTreePostgresql)
        while iterator.value():
           dataListCSV = []
           itemValueText = iterator.value().text(0)
           
           #Blocs fonctionnels
           if not findElem :
              for elem in self.mDialog.mTreePostgresql.mListBlocs :
                  if itemValueText == elem[0] :
                     if mBloc != itemValueText and elem[0] not in listBlocsExclus : 
                        mBloc, mCodeBloc = elem[0],  elem[1]
                        listBlocsExclusFlags = False
                     else :
                        listBlocsExclusFlags = True
                     break

           if not listBlocsExclusFlags :
              #Schémas actifs
              if not findElem :
                 for elem in self.mDialog.mTreePostgresql.mListSchemaActifs :
                     if itemValueText == elem[0] :
                        if mSchema != itemValueText : 
                           mSchema, actif   = elem[0], True
                        else :
                           findElem = True
                        break
              #Schémas Non actifs
              if not findElem :
                 for elem in self.mDialog.mTreePostgresql.mListSchemaNonActifs :
                     if itemValueText == elem[0] :
                        if mSchema != itemValueText : 
                           mSchema, actif   = elem[0], False
                        else :
                           findElem = True
                        break
              #Schémas Objets types
              if not findElem :
                 for elem in self.mDialog.mTreePostgresql.mArraySchemasTables :
                     if itemValueText == elem[1] :
                        mObjet, mTypeObj, mReplique = elem[1], elem[2], False
                        findElem = True
                        break
           
           if findElem :
              mLigne += "  <TR style='color:#000000' ;vertical-align:middle'>\n"
              #For réplication
              existeDansMetadata, repliquerMetadata, objetIcon = self.mDialog.mTreePostgresql.returnReplique(mSchema, mObjet, mTypeObj, self.mDialog.mListeMetadata, self.mDialog.mTreePostgresql.mListeObjetArepliquer)
              if self.mDialog.ctrlReplication :
                 if existeDansMetadata and repliquerMetadata :
                    #for CSV
                    dataListCSV.append('Oui')
                    #for CSV
                    myPathiconImg = myPathIcon + "\\objets\\dashboardReplique.png"
                    mLigne +=     '<TD align=center><img src="' + myPathiconImg + '" height="15" width="15"></TD>'
                 else :   
                    #for CSV
                    dataListCSV.append('')
                    #for CSV
                    mLigne +=     '<TD></TD>'
              #--
              #for CSV
              dataListCSV.append(str(mBloc))
              dataListCSV.append(str(mSchema))
              dataListCSV.append(str(mObjet))
              dataListCSV.append(str(mTypeObj))
              #for CSV
              
              myPathiconImg = myPathIcon + "\\treeview\\" + str(mCodeBloc) + ".png"
              mLigne +=     '<TD style="text-indent:10px"><img src="' + myPathiconImg + '" height="15" width="15">   ' + str(mBloc) + '</TD>'
              myPathiconImg = myPathIcon + "\\objets\\schema_actif.png" if actif else myPathIcon + "\\objets\\schema_nonactif.png"
              mLigne +=     '<TD style="text-indent:10px"><img src="' + myPathiconImg + '" height="15" width="15">   ' + str(mSchema) + '</TD>'
              myPathiconTypeImg = mTypeObj + ("replique" if (existeDansMetadata and repliquerMetadata) else "") 
              mLigne +=     '<TD style="text-indent:10px"><img src="' + dicIcoObjets[myPathiconTypeImg] + '" height="15" width="15">   ' + str(mObjet) + '</TD>'
              mLigne +=     '<TD style="text-indent:10px">' + str(mTypeObj) + '</TD>'
              mLigne += '  </TR>\n'
              findElem = False
              listBlocsExclusFlags = False
              self.dataCSV.append(dataListCSV)
           iterator += 1

        mLigne += '</TABLE>\n'
        mLigne += '</BODY>\n'
        mLigne += '</HTML>'
        self.mDialog.contenuCSV = [ self.headerCSV, self.dataCSV ]
        """
        iterator = QTreeWidgetItemIterator(self.mDialog.mTreePostgresql)
        while iterator.value():
           itemValue = iterator.value()
           print("text %s" %(str(itemValue.text(0))))
           #----
           iterator += 1
        """
        
        if self.mDialog.zone_affichage_TableauBord.toPlainText() != '' :
           mLigne = self.mDialog.zone_affichage_TableauBord.toHtml() + "<center>------------------------------------------------------------------------</center>" + mLigne
        self.mDialog.zone_affichage_TableauBord.setHtml(mLigne)
        return

    #=For Display Diagnostics
    def afficheViewDiagnostic(self, resultat, mTypeAction):
        myPathImg1 = os.path.dirname(__file__) + "\\icons\\logo\\logo.png"
        mLigne =  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'
        mLigne +=  '<HTML xmlns="http://www.w3.org/1999/xhtml" xml:lang="fr">'
        mLigne +=  '<HEAD>'
        mLigne +=  '</HEAD>'
        mLigne +=  '<BODY>'
        if self.mDialog.zone_affichage_diagnostic.toPlainText() == '' :
           mLigne +=  "<p><img src='" + myPathImg1 + "' height='47' width='116'></p>"
        mDate  =   time.strftime("%d ") + zMyFrenchMonth(float(time.strftime("%m"))) + time.strftime(" %Y - %Hh %Mm %Ss") + "\n"
        if self.mTypeAction == 'FONCTIONdiagnosticAsgard' :
           mTitre =   "Anomalies détectées pour la base de données <b>" + self.mDialog.dbName.upper() + "</b><br>" + mDate 
        elif self.mTypeAction == 'FONCTIONasgard_DiagnosticSchema' :
           mTitre =   "Anomalies détectées pour le schéma " + str(self.mDialog.mTreePostgresql.nom_Schema_du_Diagnostic.upper()) + " de la base de données <b>" + str(self.mDialog.dbName.upper()) + "</b><br>" + mDate 
        mLigne +=  "<center><font color='#958B62' size='4' face = 'Comic sans serif'><b>" + mTitre + "</b><br></font><font color='#440128' size='2' face = 'Comic sans serif'></center>"
        mLigne +=  "<TABLE style='border-collapse:collapse' style='border-color:#958B62' border='1' style='border-style:solid' width=100%>"
        mLigne +=  "  <TR style='color:#FFFFFF' style='background-color:#958B62'>"
        mLigne += '    <TH width=15% >Nom du schéma</TH>'
        mLigne +=     '<TH width=15% >Nom de l\'objet</TH>'
        mLigne +=     '<TH width=10% >Type de l\'objet</TH>'
        mLigne +=     '<TH width=10% >Critique</TH>'
        mLigne +=     '<TH width=50% >Anomalie</TH>\n'
        mLigne += '  </TR>\n'
        for elem in resultat :
            if elem[3] != True :
               mLigne += "  <TR style='color:#000000' style='vertical-align:middle'>\n"
            else : 
               mLigne += "  <TR style='color:#FF0000' style='vertical-align:middle'>\n"
            mLigne += '    <TD style="text-indent:10px">' + str(elem[0]) + '</TD>'
            mLigne +=     '<TD style="text-indent:10px">' + str(elem[1]) + '</TD>'
            mLigne +=     '<TD align=center>' + str(elem[2]) + '</TD>'
            mLigne +=     '<TD align=center>' + str(elem[3]) + '</TD>'
            mLigne +=     '<TD style="text-indent:10px">' + str(elem[4]) + '</TD>\n'
            mLigne += '  </TR>\n'
        mLigne += '</TABLE>\n'
        mLigne += '</BODY>\n'
        mLigne += '</HTML>'
        if self.mDialog.zone_affichage_diagnostic.toPlainText() != '' :
           mLigne = self.mDialog.zone_affichage_diagnostic.toHtml() + "<center>------------------------------------------------------------------------</center>" + mLigne
        self.mDialog.zone_affichage_diagnostic.setHtml(mLigne)
        return
    
                                                    
