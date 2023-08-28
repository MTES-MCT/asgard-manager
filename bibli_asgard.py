# (c) Didier  LECLERC 2020 CMSIG MTE-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen
# créé sept 2020

from PyQt5 import QtCore, QtGui, QtWidgets, QtSvg
from PyQt5.QtWidgets import (QAction, QMenu , QApplication, QMessageBox, QFileDialog, QTextEdit, QLineEdit,  QMainWindow, 
                            QTableView, QListView, QHeaderView, QTreeWidget, QTreeWidgetItem, QTreeWidgetItemIterator, QStyledItemDelegate, QStyleOptionButton, QStyle,
                            QVBoxLayout, QTabWidget, QWidget, QAbstractItemView, QScrollArea)
from PyQt5.QtWebKitWidgets import QWebView, QWebPage
from . import bibli_graph_asgard
from .bibli_graph_asgard import * 
from . import bibli_ihm_asgard
from .bibli_ihm_asgard import * 

from . import doerreur

import re
import csv
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
                     
from qgis.core import QgsProject, QgsMapLayer, QgsVectorLayerCache, QgsFeatureRequest, QgsSettings, QgsDataSourceUri, QgsCredentials
 
from qgis.utils import iface
import psycopg2

from qgis.gui import (QgsAttributeTableModel, QgsAttributeTableView, QgsLayerTreeViewMenuProvider, QgsAttributeTableFilterModel)
from qgis.utils import iface

from qgis.core import *
from qgis.gui import *
import qgis                              
import os                       
import datetime
import os.path
import time

#========================================================
#========================================================
def dicListSql(self, mKeySql):
    mDic_LH = bibli_asgard.returnAndSaveDialogParam(self, "Load")
    try :
      self.displayObjects = mDic_LH["displayObjects"] 
    except :
      self.displayObjects = ['all']

    mdicListSql = {}
    #------------------
    # REPLICATION
    #-----------------
    #Fonction Create Schéma, Séquence, Table News Replication 
    mdicListSql['Fonction_CreateSchemaTableReplication'] = ("""
                  CREATE SCHEMA IF NOT EXISTS z_replique
                      AUTHORIZATION postgres;
                      
                  CREATE SEQUENCE IF NOT EXISTS z_replique.replique_id_seq
                      INCREMENT 1
                      START 1
                      MINVALUE 1
                      MAXVALUE 2147483647
                      CACHE 1;
                  ALTER SEQUENCE z_replique.replique_id_seq
                      OWNER TO postgres;
    
                  CREATE TABLE IF NOT EXISTS z_replique.replique
                  (
                      nombase character varying(255) COLLATE pg_catalog."default",
                      schema character varying(255) COLLATE pg_catalog."default",
                      nomobjet character varying(255) COLLATE pg_catalog."default",
                      typeobjet character varying(100) COLLATE pg_catalog."default",
                      etat boolean,
                      id integer NOT NULL DEFAULT nextval('z_replique.replique_id_seq'::regclass),
                      CONSTRAINT replique_pkey PRIMARY KEY (id)
                  )
                  TABLESPACE pg_default;
                  ALTER TABLE z_replique.replique
                      OWNER to postgres;
                                          """) 
    #Fonction Select News Replication 
    mdicListSql['Fonction_Liste_Replication'] = ("""
                  SELECT nombase, schema, nomobjet, typeobjet, etat FROM z_replique.replique;
                                          """) 
    #Fonction Insert News Replication 
    mdicListSql['treeActionrepliquerInsert'] = ("""
                  INSERT INTO z_replique.replique(
	              nombase, schema, nomobjet, typeobjet, etat)
                  VALUES (#nom_base#, #nom_schema#, #nom_objet#, #type_objet#, #etat#);
                                          """) 
    #Fonction Update Replication 
    mdicListSql['treeActionrepliquerUpdate'] = ("""
                  UPDATE z_replique.replique
                  SET nombase=#nom_base#, schema=#nom_schema#, nomobjet=#nom_objet#, typeobjet=#type_objet#, etat=#etat#
                  WHERE nombase=#nom_base# and schema=#nom_schema# and nomobjet=#nom_objet#; 
                                          """) 
    #------------------
    # LAYER_STYLES
    #-----------------
    #Fonction d'application des droits pour la table layer_styles
    mdicListSql['Fonction_Layer_Styles_Droits'] = ("""
    SELECT z_asgard_admin.asgard_layer_styles(variante := #variante#) ;
                                          """) 
    #Fonction Si existe layer_styles + si propriétaire
    mdicListSql['Fonction_Layer_Styles'] = ("""
    SELECT
    count(*) = 1 AS ls_exists,
    coalesce(bool_and(pg_has_role(relowner, 'USAGE')), False) AS ls_isowner
    FROM pg_catalog.pg_class
    WHERE relnamespace = 'public'::regnamespace AND relname = 'layer_styles' ;
                                          """) 
    #-----------------
    #Fonctions de Contrôles à supprimer
    mdicListSql['Membre_G_admin'] = ("""SELECT pg_has_role('g_admin', 'USAGE')""")
    #Fonctions de Contrôles 
    #Attention utilisation de QUOTE_IDENT()
    mdicListSql['Membre_G_admin_ET_CreateRoleOuPas'] = (
                 """
                   SELECT pg_has_role('g_admin', 'USAGE'),
                   quote_ident((array_agg(rolname::text ORDER BY rolname = current_user DESC, rolname = 'g_admin' DESC ))[1]) AS parent_with_createrole, 
                   quote_ident(current_user) AS userConnecteEnCours,
                   coalesce(bool_or(rolsuper), false) AS is_superuser
                   FROM pg_roles
                   WHERE pg_has_role(rolname, 'MEMBER') AND rolcreaterole
                 """
                       )        
    mdicListSql['IsSuperUser'] = (
                 """
                   SELECT 
                   coalesce(bool_or(rolsuper), false) AS is_superuser
                   FROM pg_roles
                   WHERE pg_has_role(rolname, 'MEMBER') AND rolcreaterole
                 """
                       )        
    #------------------
                       
    #Liste des rôles editeurs et lecteurs
    mdicListSql['ListeRolesEditeursLecteurs'] = (
                       """
                       SELECT rolname::text AS n_role
                       FROM pg_catalog.pg_roles
                       WHERE NOT rolcanlogin
                       AND NOT rolname ~ '^pg_'
                       UNION
                       SELECT 'public'::text AS n_role
                       ORDER BY n_role   
                       """
                       )    
    #Liste des rôles producteur
    mdicListSql['ListeRolesProducteurs'] = (
                       """
                       WITH t AS (
                           SELECT
                               count(*) AS has_createrole
                               FROM pg_roles
                               WHERE pg_has_role(rolname, 'MEMBER') AND rolcreaterole AND rolinherit
                           )
                       SELECT rolname
                           FROM t, pg_catalog.pg_roles
                               LEFT JOIN information_schema.applicable_roles
                                   ON role_name = rolname
                           WHERE (
                               NOT rolcanlogin
                                   AND NOT rolname ~ '^pg_'
                                   AND (
                                       pg_has_role(rolname, 'USAGE'::text)
                                           AND pg_has_role('g_admin', rolname, 'USAGE'::text)
                                       OR has_createrole > 0
                                       OR is_grantable = 'YES'
                                   )
                               )
                               OR rolsuper AND pg_has_role(rolname, 'USAGE'::text)
                           ORDER BY rolname
                       """
                       )        
    #Liste des schémas
    mdicListSql['ListeSchema'] = (
                       """
                       SELECT nspname
                       FROM pg_namespace
                       WHERE nspname not ilike 'pg_%'
                       and nspname not in ('pg_catalog', 'information_schema', 'topology', 'tiger_data', 'tiger')
                       ORDER BY nspname
                       """
                       )
    #Liste des schémas PLUS
    mdicListSql['ListeSchemaBlocExiste'] = (
                       """
                       SELECT nom_schema, bloc , creation, nomenclature, producteur, editeur, lecteur, nomenclature, niv1, niv1_abr, niv2, niv2_abr
                       FROM z_asgard.gestion_schema_usr 
                       WHERE nom_schema not in ('topology', 'tiger_data', 'tiger')
                       ORDER BY  nom_schema
                       """
                       )                       
    #Liste des schémas et tables
    mdicListSql['ListeSchemaTable'] = ( 
                       """
                       SELECT pg_tables.schemaname, pg_tables.tablename FROM pg_catalog.pg_tables where pg_tables.schemaname in
                       (
                       SELECT nspname
                       FROM pg_namespace
                       WHERE nspname not ilike 'pg_%'
                       and nspname not in ('pg_catalog', 'information_schema')
                       ) 
                       ORDER BY pg_tables.tablename

                       """
                       )
    #-----Autre version                       
    #Liste des schémas et tables
    mdicListSql['ListeSchemaTable'] = ( 
                       """
                       SELECT table_schema as schemaname, table_name as tablename, table_type as tabletype FROM information_schema.tables 
                       ORDER BY table_schema
                       """
                       )
    #Liste de la vue gestion_schema_usr
    mdicListSql['ListeGestion_schema_usr'] = (
                       """
                       SELECT nspname
                       WHERE nspname not ilike 'pg_%'
                       and nspname not in ('pg_catalog', 'information_schema')
                       """
                       )
    #Fonction de sortie 
    mdicListSql['FONCTIONasgard_sortie_gestion_schema'] = ("""SELECT z_asgard_admin.asgard_sortie_gestion_schema(#nom_schema#)""")

    #Fonction qui retourne si l'extension est installée et les numéro des versions
    mdicListSql['ReturnInstalleEtVersion'] = ("""SELECT *, CURRENT_DATABASE() FROM pg_available_extensions WHERE name = 'asgard'""")
    #PLUME Fonction qui retourne si l'extension est installée et les numéro des versions
    mdicListSql['ReturnInstalleEtVersionPlume'] = ("""SELECT *, CURRENT_DATABASE() FROM pg_available_extensions WHERE name = 'plume_pg'""")
    #===================
    # Menu GESTION DE LA BASE
    #Fonction de maintenance générales  Réinitialiser tous les droits 
    mdicListSql['FONCTIONreinitAllSchemasFunction'] = ("""SELECT z_asgard_admin.asgard_initialise_all_schemas()""")
    #-
    mdicListSql['FONCTIONdiagnosticAsgard'] = ("""SELECT nom_schema, nom_objet, typ_objet, critique, anomalie FROM z_asgard_admin.asgard_diagnostic()""")
    #-
    mdicListSql['FONCTIONmembreGconsult'] = ("""SELECT z_asgard_admin.asgard_all_login_grant_role('g_consult')""")
    #-
    mdicListSql['FONCTIONnettoieRoles'] = ("""SELECT z_asgard.asgard_nettoyage_roles()""")
    #-
    mdicListSql['FONCTIONreferencerAllSchemasFunction'] = ("""SELECT z_asgard_admin.asgard_initialisation_gestion_schema()""")
    #-
    mdicListSql['FONCTIONimportNomenclature'] = ("""SELECT z_asgard_admin.asgard_import_nomenclature()""")
    #-
    mdicListSql['FONCTIONinstallerAsgard'] = ("""CREATE EXTENSION asgard""")
    #-
    mdicListSql['FONCTIONmajAsgard'] = ("""ALTER EXTENSION asgard UPDATE""")
    #-
    mdicListSql['FONCTIONdesinstallerAsgard'] = ("""DROP EXTENSION asgard""")
    #- For PLUME
    mdicListSql['FONCTIONinstallerPlume'] = ("""CREATE EXTENSION plume_pg CASCADE""")
    #-
    mdicListSql['FONCTIONmajPlume'] = ("""ALTER EXTENSION plume_pg UPDATE""")
    #-
    mdicListSql['FONCTIONdesinstallerPlume'] = ("""DROP EXTENSION plume_pg cascade""")
    #- For PLUME
    # Menu GESTION DE LA BASE
    #===================
    
    #Liste des libellés des niv1, niv1_abr, niv2, niv2_abvextensions du serveur la vue gestion_schema_usr   
    mdicListSql['ListeArboNiv1Niv2'] = ("""SELECT niv1, niv1_abr, niv2, niv2_abr FROM z_asgard."gestion_schema_usr";""")
    
    #Liste des extensions du serveur la vue gestion_schema_usr   
    mdicListSql['ListeExtension'] = ("""SELECT * FROM pg_available_extensions""")
    
    #Fonction de création d'un schéma 
    mdicListSql['CreationSchema'] = ("""CREATE SCHEMA "#mon_schema#" AUTHORIZATION "#role_groupe#" """)
    
    #Fonction de déplacement d'un objet
    mdicListSql['FONCTIONDeplaceObjet'] = ("""SELECT z_asgard.asgard_deplace_obj(#obj_schema#, #obj_nom#, #obj_typ#, #schema_cible#, 1)""")

    #Fonction de réaffectation des rôles ou transfert des droits
    mdicListSql['FONCTIONReaffecteRoles'] = ("""SELECT z_asgard_admin.asgard_reaffecte_role(n_role := '#nom_role#', n_role_cible := '#nom_role_cible#', b_hors_asgard := true, b_default_acl := true)""")

    #==============================================
    #Création de la requete de la liste des schémas, objets et type
    #Lecture et typage resultat
    mTypListINI = self.displayObjects if isinstance(self.displayObjects, list) else [ self.displayObjects ] 
 
    #---
    typlistOrigine = [        
    ["table", "pg_class", "rel", "relkind = ANY (ARRAY['r', 'p'])"],                  
    ["view", "pg_class", "rel", "relkind = 'v'"],
    ["materialized view", "pg_class", "rel", "relkind = 'm'"],
    ["foreign table", "pg_class", "rel", "relkind = 'f'"],
    ["sequence", "pg_class", "rel", "relkind = 'S'"],
    ["function", "pg_proc", "pro", "true"],
    ["type", "pg_type", "typ", "NOT typtype = 'd'"],
    ["domain", "pg_type", "typ", "typtype = 'd'"]
    ]

    #---
    #Construction dictionnaire pour  SQL
    #si all ou vide
    if len(mTypListINI) == 0  or (len(mTypListINI) == 1 and mTypListINI[0].upper() == 'ALL') : 
       typlist = list(typlistOrigine)
    else :
       mDicTypList = {}
       for elem in typlistOrigine :
           if elem[0] in mTypListINI : mDicTypList[elem[0]] = elem 
       #--- 
       typlist = [ value for value in mDicTypList.values() ] if len(mDicTypList) > 0 else typlistOrigine
    self.typlist = typlist   
    #---
    r = "" 
    for i in range(len(typlist)):                                 
        if r != "" : r += " UNION " 
        r += """SELECT
        nom_schema,
        CASE WHEN '{ref[0]}' = 'function'
            THEN quote_ident({ref[2]}name::text) || substring({ref[1]}.oid::regprocedure::text, '[(][^()]*[)]$')
            ELSE {ref[2]}name::text END AS objname,
        '{ref[0]}' AS objtype, '{ref[1]}' AS objcatalog
        FROM z_asgard.gestion_schema_etr
            LEFT JOIN pg_catalog.{ref[1]} ON oid_schema = {ref[2]}namespace
            LEFT JOIN pg_catalog.pg_depend ON objid = {ref[1]}.oid
        WHERE {ref[3]} AND NOT deptype = 'i'
        """.format(ref=typlist[i])

    r += " ORDER BY nom_schema, objtype, objname" 
    #---
    #Fonction de la liste des schémas, objets et type
    #nom_schema, objname, objtype
    mdicListSql['ListeSchemaObjets'] = (r) 
    #==============================================

    #Fonction de création d'une occurrence schéma                                                                
    mdicListSql['CreationSchemaLigne'] = ("""
                  INSERT INTO z_asgard.gestion_schema_usr (nom_schema, bloc, nomenclature, niv1, niv1_abr, niv2, niv2_abr, creation, producteur, editeur, lecteur)
                                                 	 VALUES (#nom_schema#, #bloc#, #nomenclature#, #niv1#, #niv1_abr#, #niv2#, #niv2_abr#, #creation#, #producteur#, #editeur#, #lecteur#)             
                                          """)
    #Fonction de modification d'une occurrence schéma 
    mdicListSql['ModificationSchemaLigne'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET nom_schema=#nom_schema#, bloc=#bloc#, nomenclature=#nomenclature#, niv1=#niv1#, niv1_abr=#niv1_abr#, niv2=#niv2#, niv2_abr=#niv2_abr#, 
                      creation=#creation#, producteur=#producteur#, editeur=#editeur#, lecteur=#lecteur#
                  WHERE nom_schema=#ID_nom_schema#
                                          """)
    #-----------------
    #Fonction de création d'un role                                                                
    # A conserver pour quand la gestion des profils sera opérationnelle                                                                
    #           #mRolsuper#
    #           #mRolreplication#
    mdicListSql['CreationRole'] = ("""
                #Role_g_admin_createrole#

                CREATE ROLE "#mRolname#" WITH
                #mdpLogin#
                #mRolinherit#
                #mRolcreatedb#
                #mRolcreaterole#
                #mMdp#;
                #mListeRevokeNew#
                #mListeGrantNew# 
                #mListeRevokeBISNew#
                #mListeGrantBISNew# 
                COMMENT ON ROLE "#mRolname#" IS '#mDescription#';
                
                #ResetRole#
                #Rolgestionschema_cond1#
                                          """)

    #Fonction de modification d'un role                                                              
    # A conserver pour quand la gestion des profils sera opérationnelle                                                                
    #           #mRolsuper#
    #           #mRolreplication#
    mdicListSql['ModificationRole'] = ("""
                #Role_g_admin_createrole#
    
                ALTER ROLE "#mRolname#" WITH
                #mdpLogin#
                #mRolinherit#
                #mRolcreatedb#
                #mRolcreaterole#
                #mMdp#;
                #mListeRevokeNew#
                #mListeGrantNew# 
                #mListeRevokeBISNew#
                #mListeGrantBISNew# 
                COMMENT ON ROLE "#mRolname#" IS '#mDescription#';
                
                #ResetRole#
                #Rolgestionschema_cond1#
                                          """)
    #Fonction de suppression d'un rôle
    mdicListSql['treeActionDeleteRole'] = ("""
                  #Role_g_admin_createrole#
    
                  DROP ROLE "#nom_role#";
                  
                  #ResetRole#
                                          """) 
    #Fonction de revoquer d'un rôle
    mdicListSql['treeActionRevoquerRole'] = ("""
    
                 SELECT z_asgard_admin.asgard_reaffecte_role(
                 n_role := '#nom_role#',
                 b_hors_asgard := true,
                 b_default_acl := true
                 )
                 
                  ;
                                          """) 
    #-----------------
    #-----------------
    # DRAG & Drop
    #Fonction de modification d'une occurrence schéma 
    mdicListSql['ModificationSchemaLigneDRAGDROP'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET bloc=#bloc#
                  WHERE nom_schema=#ID_nom_schema#
                                          """)
    # DRAG & Drop
    #-----------------
    #Fonction de mettre à la corbeille 
    mdicListSql['treeActionCorbeille'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET bloc=#bloc#
                  WHERE nom_schema=#ID_nom_schema#
                                          """) 
    #Fonction d'effacer l'enrg d'un non actifs de la vue gestion_schema_usr
    mdicListSql['treeActionSchema_efface'] = ("""
                  DELETE FROM z_asgard.gestion_schema_usr
                  WHERE nom_schema=#ID_nom_schema#  
                                          """)                                                                                                                              
    #Fonction de creer dans la base rendre actif 
    mdicListSql['treeActionSchema_creer_base'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET creation=#creation#
                  WHERE nom_schema=#ID_nom_schema#
                                          """) 
    #Fonction de vider la corbeille (deux etapes)
    mdicListSql['treeActionCorbeillevide_Un'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET creation=#creation#
                  WHERE bloc=#bloc#
                                          """) 
    mdicListSql['treeActionCorbeillevide_Deux'] = ("""
                  DELETE FROM z_asgard.gestion_schema_usr
                  WHERE bloc=#bloc#  
                                          """) 
    #Fonction de restauration  identique treeActionCorbeille
    mdicListSql['treeActionRestaurer'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET bloc=#bloc#
                  WHERE nom_schema=#ID_nom_schema#
                                          """) 
    #Fonction de Supprimer de la base  identique treeActionSchema_creer_base
    mdicListSql['treeActionSupprimer_base'] = ("""
                  UPDATE z_asgard.gestion_schema_usr
	                SET creation=#creation#
                  WHERE nom_schema=#ID_nom_schema#
                                          """) 
    #Fonction de referencement et NE conserve PAS les droits et les REINITIALISE
    mdicListSql['FONCTIONasgard_initialise_schema'] = ("""SELECT z_asgard.asgard_initialise_schema(#nom_schema#)""")
    #----------------------------------------------------------------------------------------------------------------
    #Fonction de referencement et CONSERVE les droits 
    mdicListSql['FONCTIONasgard_initialise_schemaConserveDroits'] = ("""SELECT z_asgard.asgard_initialise_schema(#nom_schema#, b_preserve := true)""")

    #Fonction de réinitialisation des droits ## Idem FONCTIONasgard_initialise_schema ce jour 
    mdicListSql['FONCTIONasgard_Reinitialisedroit'] = ("""SELECT z_asgard.asgard_initialise_schema(#nom_schema#)""")

    #Fonction de réinitialisation des droits sur un objet ## Rétablit les droits standards du producteur, de l’éditeur et du lecteur sur l’objet. 
    mdicListSql['FONCTIONasgard_initialise_obj'] = ("""SELECT z_asgard.asgard_initialise_obj(#nom_schema#, #nom_objet#, #type_objet#)""")

    #Fonction de diagnostic pour un schéma
    mdicListSql['FONCTIONasgard_DiagnosticSchema'] = ("""SELECT nom_schema, nom_objet, typ_objet, critique, anomalie FROM z_asgard_admin.asgard_diagnostic(ARRAY[#nom_schema#])""")

    # ROLES
    #-----------------
    #Liste des rôles de groupe
    mdicListSql['listeDesRolesDeGroupe'] = ("""
    SELECT row_number() OVER () AS oid,
    pg_roles.rolname::text AS rolname,
    pg_roles.oid AS oid_grp,
        CASE
            WHEN pg_shdescription.description ~ '^[A-z]'::text THEN pg_shdescription.description::name
            ELSE pg_roles.rolname
        END AS description
    FROM pg_roles
      LEFT JOIN pg_shdescription ON pg_shdescription.objoid = pg_roles.oid
    WHERE substr(pg_roles.rolname::text, 1, 2) <> 'pg'::text AND pg_roles.rolcanlogin = false
    UNION
    SELECT '-99'::bigint AS oid,
           'non renseigne'::text AS rolname,
           NULL::oid AS oid_grp,
           'Groupe non renseigné'::name AS description;
                                          """)
                                              
    #Liste des rôles de connexion et de groupe
    mdicListSql['listeDesRolesDeGroupeEtConnexions'] = ("""
    WITH
    roles_1 AS (
        SELECT
            -- informations génériques
            roles.rolname, roles.rolsuper, roles.rolinherit,
            roles.rolcreaterole, roles.rolcreatedb, roles.rolcanlogin, roles.rolreplication,
            roles.rolconnlimit, roles.rolpassword, roles.rolvaliduntil, roles.rolbypassrls,
            roles.rolconfig, roles.oid,
            -- commentaire sur le rôle
            shobj_description(roles.oid, 'pg_authid') AS description,
            -- gestion des schémas
            roles.rolsuper OR roles.oid IN (
                SELECT grantee
                    FROM pg_database, aclexplode(datacl)
                    WHERE datname = current_database()
                        AND privilege_type = 'CREATE'
                UNION
                SELECT datdba FROM pg_database
                    WHERE datname = current_database()
            ) AS db_create
            FROM pg_catalog.pg_roles AS roles
            WHERE NOT rolname ~ ANY (ARRAY['^pg_', '^postgres$'])
    ),
    roles_2 AS (
        SELECT
            roles_1.*,
            -- membres du rôles
            array_agg(DISTINCT membres.member ORDER BY membres.member) AS membres
            FROM roles_1 LEFT JOIN pg_catalog.pg_auth_members AS membres ON roles_1.oid = membres.roleid
            GROUP BY roles_1.rolname, roles_1.rolsuper, roles_1.rolinherit,
                roles_1.rolcreaterole, roles_1.rolcreatedb, roles_1.rolcanlogin, roles_1.rolreplication,
                roles_1.rolconnlimit, roles_1.rolpassword, roles_1.rolvaliduntil, roles_1.rolbypassrls,
                roles_1.rolconfig, roles_1.oid, roles_1.description, roles_1.db_create
        ),
    roles_3 AS (
        SELECT
            roles_2.*,
            -- rôles dont le rôle est membre
            array_agg(DISTINCT parents.roleid ORDER BY parents.roleid) AS parents
            FROM roles_2 LEFT JOIN pg_catalog.pg_auth_members AS parents ON roles_2.oid = parents.member
            GROUP BY roles_2.rolname, roles_2.rolsuper, roles_2.rolinherit,
                roles_2.rolcreaterole, roles_2.rolcreatedb, roles_2.rolcanlogin, roles_2.rolreplication,
                roles_2.rolconnlimit, roles_2.rolpassword, roles_2.rolvaliduntil, roles_2.rolbypassrls,
                roles_2.rolconfig, roles_2.oid, roles_2.description, roles_2.db_create, roles_2.membres
        ),
    roles_4 AS (
        SELECT
            roles_3.*,
            -- droits du rôle sur les schémas référencés par ASGARD
            array_agg(
                ARRAY[nom_schema, (asgardmanager_metadata.oid_lecteur = roles_3.oid)::text]
                ORDER BY asgardmanager_metadata.nom_schema
            ) FILTER (
                    WHERE pg_has_role(roles_3.oid, asgardmanager_metadata.oid_lecteur, 'USAGE')
                ) AS schema_lec,
            array_agg(
                ARRAY[nom_schema, (asgardmanager_metadata.oid_editeur = roles_3.oid)::text]
                ORDER BY asgardmanager_metadata.nom_schema
            ) FILTER (
                WHERE pg_has_role(roles_3.oid, asgardmanager_metadata.oid_editeur, 'USAGE')
                ) AS schema_edi,
            array_agg(
                ARRAY[nom_schema, (asgardmanager_metadata.oid_producteur = roles_3.oid)::text]
                ORDER BY asgardmanager_metadata.nom_schema
            ) FILTER (
                WHERE pg_has_role(roles_3.oid, asgardmanager_metadata.oid_producteur, 'USAGE')
                ) AS schema_pro
            FROM roles_3 LEFT JOIN  z_asgard.asgardmanager_metadata ON true
            GROUP BY roles_3.rolname, roles_3.rolsuper, roles_3.rolinherit,
                roles_3.rolcreaterole, roles_3.rolcreatedb, roles_3.rolcanlogin, roles_3.rolreplication,
                roles_3.rolconnlimit, roles_3.rolpassword, roles_3.rolvaliduntil, roles_3.rolbypassrls,
                roles_3.rolconfig, roles_3.oid, roles_3.description, roles_3.db_create, roles_3.membres,
                roles_3.parents
    )
    SELECT
        roles_4.rolname, roles_4.rolsuper, roles_4.rolinherit,
        roles_4.rolcreaterole, roles_4.rolcreatedb, roles_4.rolcanlogin, roles_4.rolreplication,
        roles_4.rolconnlimit, roles_4.rolpassword, roles_4.rolvaliduntil, roles_4.rolbypassrls,
        roles_4.rolconfig, roles_4.oid, roles_4.description, roles_4.membres, roles_4.parents,
        roles_4.schema_lec, roles_4.schema_edi, roles_4.schema_pro, roles_4.db_create,
        -- bases contenant des objets dépendants du rôle
        array_agg(
            DISTINCT pg_database.datname::text ORDER BY pg_database.datname::text
        ) FILTER (WHERE pg_database.datname IS NOT NULL) AS db_dependances
        FROM roles_4
            LEFT JOIN pg_catalog.pg_shdepend
                ON roles_4.oid = pg_shdepend.refobjid AND pg_shdepend.refclassid = 'pg_authid'::regclass
            LEFT JOIN pg_catalog.pg_database
                ON pg_shdepend.dbid = pg_database.oid
                    OR pg_shdepend.classid = 'pg_database'::regclass AND pg_shdepend.objid = pg_database.oid
        GROUP BY roles_4.rolname, roles_4.rolsuper, roles_4.rolinherit,
            roles_4.rolcreaterole, roles_4.rolcreatedb, roles_4.rolcanlogin, roles_4.rolreplication,
            roles_4.rolconnlimit, roles_4.rolpassword, roles_4.rolvaliduntil, roles_4.rolbypassrls,
            roles_4.rolconfig, roles_4.oid, roles_4.description, roles_4.db_create, roles_4.membres,
            roles_4.parents, roles_4.schema_lec, roles_4.schema_edi, roles_4.schema_pro
        ORDER BY roles_4.rolname ;                                                        """) 
    
    #Table de relation n à n roles/groupes
    mdicListSql['relationRolesGroupes'] = ("""
                 SELECT roleid, member, grantor, admin_option FROM pg_catalog.pg_auth_members;
                                                       """) 
    #Fontions Graphiques
    #-----------------
    mdicListSql["volumeDesBases"]        = bibli_graph_asgard.dicListSqlGraph("volumeDesBases")
    mdicListSql["volParBloc"]            = bibli_graph_asgard.dicListSqlGraph("volParBloc")

    return  mdicListSql[mKeySql]

#========================================================
#========================================================
def dicExpRegul(self, mPattern, mText):
    mDicExpRegul = {}
    #------------------
    #Find : [Un car au début plus '_' et Retour Un car au début, la chaine sans le préfixe)
    mDicExpRegul['Find_(FirstCar_)&Ret_FirstCar'] = ('^([A-Za-z])_')
    #------------------
    
    #Traitement Retourne une liste (bloc, chaine sans préfixe)          
    try :
      mRet = [ re.findall(mDicExpRegul[mPattern], mText)[0] , mText[2:] ] if re.findall(mDicExpRegul[mPattern], mText) else [ '' , mText]
    except :
      mRet = [ '' , '']
    return  mRet

#========================================================
#========================================================
def dicExisteExpRegul(self, mPattern, mText):
    mDicExisteExpRegul = {}
    #------------------
    mDicExisteExpRegul['Search_0'] = '[A-Z]{2,3}[1-9][0-9]*[.]'
    #------------------
    #Traitement Retourne une liste (bloc, chaine sans préfixe)
    try :
      mRet = True if re.search(mDicExisteExpRegul[mPattern], mText) != None else False
    except :
      mRet = False
    return  mRet
    
#========================================================      
# Class pour le tree View Blocs Schémas Graphiques    
class TREEVIEWASGARDGRAPHOPTIONS(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["Paramètres"])
        self.header().setStyleSheet("font: bold ;")
        #self.setItemDelegate(DELEGATE())

    #===============================              
    def afficheGraphOptions(self, Dialog, myPathIcon): 
        self.Dialog = Dialog 
        mYOptions = 50
        mHOptions = (self.Dialog.groupBoxAffichageLeftDash.height()/2) - 50
        self.setGeometry(15, mYOptions, self.Dialog.groupBoxAffichageLeftDash.width() - 30, mHOptions)
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Dialog = Dialog 
        
        #============
        iconTree = returnIcon(myPathIcon + "\\treeview\\graph_options.png")
        self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ QtWidgets.QApplication.translate("bibli_asgard", "Options", None) ] ) ] )
        root = self.topLevelItem( 0 )
        root.setIcon(0, iconTree)
        #============
        #Instancie Options 1er Niveau 
        mListNiv1, mListNiv1Libelle, mListNiv1Icons = [], [], []
        dicListNiv1 = {"graph_type": "Type", "graph_etiquette": "Etiquettes", "graph_legende": "Légende", "graph_titre": "Titre", "graph_animation": "Animation"}
        for mKey, mValue in dicListNiv1.items() :
            mListNiv1.append([ mValue, mKey ])
            mListNiv1Libelle.append(mValue)
            mListNiv1Icons.append(returnIcon(myPathIcon + "\\treeview\\" + str(mKey) + ".png"))
        self.mListNiv1, self.mListNiv1Libelle, self.mListNiv1Icons = mListNiv1, mListNiv1Libelle, mListNiv1Icons 
        #============
        #Instancie Options 2ème Niveau 
        mListNiv2, mListNiv2Libelle, mListNiv2Icons = [], [], []
        dicListNiv2 = {"graph_type_cercle": ["graph_type", "Cercle"], "graph_type_barre": ["graph_type", "Barre"], \
                       "graph_etiquette_libelle": ["graph_etiquette", "Libellé"], "graph_etiquette_pourc": ["graph_etiquette", "Pourcentage"], "graph_etiquette_valeur": ["graph_etiquette", "Valeur"], \
                       "graph_legende_nord": ["graph_legende", "Nord"], "graph_legende_ouest": ["graph_legende", "Ouest"], "graph_legende_est": ["graph_legende", "Est"], "graph_legende_sud": ["graph_legende", "Sud"], \
                       "graph_type_cercle": ["graph_type", "Cercle"], "graph_type_barre": ["graph_type", "Barre"] \
                       }
        self.dicListNiv2 = dicListNiv2
        #------------ 
        #Affiche Options 1er Niveau
        i = 0
        while i in range(len(mListNiv1)) :
            mRootBlocs = mListNiv1[i][0]
            mRootChildNiv1 = QTreeWidgetItem(None, [ mRootBlocs ] )
            if mListNiv1[i][0] == "Type" or mListNiv1[i][0] == "Légende" or mListNiv1[i][0] == "Titre" :
               mRootChildNiv1.setFlags(mRootChildNiv1.flags() | Qt.NoItemFlags )
            elif mListNiv1[i][0] == "Etiquettes" :
               mRootChildNiv1.setFlags(mRootChildNiv1.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            else : 
               mRootChildNiv1.setCheckState(0, Qt.Checked)
               mRootChildNiv1.setFlags(mRootChildNiv1.flags() | Qt.ItemIsUserCheckable)
            mRootChildNiv1.setIcon(0, mListNiv1Icons[i])
            root.addChild( mRootChildNiv1 )
            #Gestion du titre
            if mListNiv1[i][0] == "Titre" :                      
               mLibelleTitre = "Mon titre à moi"
               #print(mLibelleTitre)
               mRootChildNiv2 = QTreeWidgetItem(None, [ mLibelleTitre ])
               mRootChildNiv2.setFlags(mRootChildNiv2.flags() | Qt.ItemIsEditable)               
               mRootChildNiv1.addChild( mRootChildNiv2 )
            #Autres
            #Affiche Options 2ème Niveau 
            mFirstCheck = True
            for mRootNiv2_Key, mRootNiv2_Value in self.dicListNiv2.items() :
                if mListNiv1[i][1] == mRootNiv2_Value[0] :
                   mRootChildNiv2 = QTreeWidgetItem(None, [ mRootNiv2_Value[1] ] )
                   mRootChildNiv2.setCheckState(0, Qt.Checked)
                   #un seul Check
                   if mFirstCheck : 
                      if mListNiv1[i][0] == "Type" or mListNiv1[i][0] == "Légende" :
                         mFirstCheck = False
                         mRootChildNiv2.setCheckState(0, Qt.Checked)
                   else :
                      mRootChildNiv2.setCheckState(0, Qt.Unchecked)
                   mRootChildNiv2.setFlags(mRootChildNiv2.flags() | Qt.ItemIsUserCheckable)
                   niv2Icon = returnIcon(myPathIcon + "\\treeview\\" + str(mRootNiv2_Key) + ".png")
                   mRootChildNiv1.addChild( mRootChildNiv2 )
            i += 1
        #===================   
        self.expandAll()
        self.itemDoubleClicked.connect(self.check_status)
        self.itemClicked.connect( self.clickItems ) 
                                                             
    #-------
    def check_status(self, item, column):
        if item.checkState(0) == Qt.Checked :
           item.setCheckState(0, Qt.Unchecked)
        else :
           item.setCheckState(0, Qt.Checked)
        return
    #-------    
    def clickItems(self, item, column):
        mItemValue = self.Dialog.mTreePostgresql.returnValueItem(item, column)
        mItemClic = item.data(column, Qt.DisplayRole)
        # actions Niv 2 type Radio
        mNivParent = item.parent()
        if mNivParent != None :
           mItemParent = item.parent().data(column, Qt.DisplayRole)
           #-------
           if mItemParent == "Type"  :
              if item.checkState(0) == Qt.Unchecked :
                 item.setCheckState(0, Qt.Checked) 
              for itemChild in range(mNivParent.childCount()):
                  if item != mNivParent.child(itemChild) :
                     if item.checkState(0) == Qt.Checked : 
                        mNivParent.child(itemChild).setCheckState(0, Qt.Unchecked)
           #-------
           if mItemParent == "Légende" :
               for itemChild in range(mNivParent.childCount()):
                   if item != mNivParent.child(itemChild) :
                      if item.checkState(0) == Qt.Checked : 
                         mNivParent.child(itemChild).setCheckState(0, Qt.Unchecked)
        return

#========================================================      
# Class DELEGATE pour le tree View Blocs Schémas Graphiques    
class DELEGATE(QStyledItemDelegate):
    """
    def paint(self, painter, option, index):
        if not index.parent().isValid():
            QStyledItemDelegate.paint(self, painter, option, index)
        else:
            widget = option.widget
            style = widget.style() if widget else QApplication.style()
            opt = QStyleOptionButton()
            opt.rect = option.rect
            opt.text = index.data()
            opt.state |= QStyle.State_On if index.data(Qt.CheckStateRole) else QStyle.State_Off
            style.drawControl(QStyle.CE_RadioButton, opt, painter, widget)
    """
    def editorEvent(self, event, model, option, index):
        value = QStyledItemDelegate.editorEvent(self, event, model, option, index)
        if value:
            if event.type() == QEvent.MouseButtonRelease:
                if index.data(Qt.CheckStateRole) == Qt.Checked:
                    parent = index.parent()
                    for i in range(model.rowCount(parent)):
                        if i != index.row():
                            ix = parent.child(i, 0)
                            model.setData(ix, Qt.Unchecked, Qt.CheckStateRole)

        return value

    
#========================================================      
# Class pour le tree View Blocs Schémas Graphiques    
class TREEVIEWASGARDGRAPHSCHEMASBLOCS(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["Blocs"])
        self.header().setStyleSheet("font: bold ;")
    #===============================              
    def afficheGraphSchemasBlocs(self, Dialog, myPathIcon, mSchemasBlocs): 
        self.Dialog = Dialog 
        mYBlocs = self.Dialog.groupBoxParametre.y() + self.Dialog.groupBoxParametre.height() + 10
        mHBlocs = (self.Dialog.groupBoxAffichageLeftDash.height() - (self.Dialog.groupBoxParametre.y() + self.Dialog.groupBoxParametre.height() + 50))
        self.setGeometry(15, mYBlocs, self.Dialog.groupBoxAffichageLeftDash.width() - 30, mHBlocs)                                                 
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.Dialog = Dialog 
        #============
        iconTree = returnIcon(myPathIcon + "\\logo\\asgard2.png")
        self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ QtWidgets.QApplication.translate("bibli_asgard", "Blocs", None) ] ) ] )
        root = self.topLevelItem( 0 )
        root.setCheckState(0, Qt.Checked)
        root.setFlags(root.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        root.setIcon(0, iconTree)
        root.setExpanded(True)
        #============
        #Affiche Blocs fonctionnels 
        dicListBlocs = returnLoadBlocParam()
        #Ajout des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings
        dicListBlocs = returnDicBlocUniquementNonReference(dicListBlocs, mSchemasBlocs)
        #Ajoute Schémas Hors Asgard 
        #dicListBlocs["horsasgard"] = QtWidgets.QApplication.translate("bibli_asgard", "Schemes outside Asgard", None)
        self.dicListBlocs = dicListBlocs

        mListBlocs, mListBlocsLibelle, mListBlocsIcons = [], [], []
        #Reverse List for Dict
        mKeysReverse = [key for key in dicListBlocs.keys()]
        #mKeysReverse.reverse() pas de reverse pour ce treeview
        for mCount in range(len(mKeysReverse)) :
            mKey   = mKeysReverse[mCount] 
            mValue = dicListBlocs[mKey] 
            mListBlocs.append([ mValue, mKey ])
            mListBlocsLibelle.append(mValue)
            if str(mKey) == 'horsasgard' :
               #Affiche Schémas Hors Asgard 
               iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
               mListBlocsIcons.append(iconGestion)
            else :
               mListBlocsIcons.append(returnIcon(myPathIcon + "\\treeview\\" + str(mKey) + ".png"))

        #Ajout des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings
        mListBlocs, mListBlocsLibelle, mListBlocsIcons =  returnDicBlocLibelleIconNonReference(mListBlocs, mListBlocsLibelle, mListBlocsIcons, mSchemasBlocs, myPathIcon)
        self.mListBlocs, self.mListBlocsLibelle, self.mListBlocsIcons = mListBlocs, mListBlocsLibelle, mListBlocsIcons 
        #============
        #------------ 
        #Affiche les blocs fonctionnels
        i = 0
        while i in range(len(mListBlocs)) :
            mRootBlocs = mListBlocs[i][0]
            mRootChild = QTreeWidgetItem(None, [ mRootBlocs ] )
            mRootChild.setCheckState(0, Qt.Checked)
            mRootChild.setFlags(mRootChild.flags() | Qt.ItemIsUserCheckable)
            mRootChild.setIcon(0, mListBlocsIcons[i])
            root.addChild( mRootChild )
            i += 1
        #===================   
        self.itemDoubleClicked.connect(self.check_status)

    def check_status(self, item, column):
        if item.checkState(0) == Qt.Checked :
           item.setCheckState(0, Qt.Unchecked)
        else :
           item.setCheckState(0, Qt.Checked)
           
#========================================================      
# Class pour le tree View Schéma LECTEUR    
class TREEVIEWASGARDSCHEMALECTEUR(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["Lecteur"])
        self.header().setStyleSheet("font: bold ;")
    #===============================              
    def afficheSchemaLecteur(self, Dialog, myPathIcon, mRolnameID, ArraymlisteDesRolesDeGroupeEtConnexions): 
        self.Dialog = Dialog 
        self.setGeometry(5, 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
   
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #[Name, réel Edit, Lect, Prod 
        mSchemaLect, mSchemaEdit, mSchemaProd = returnSchemaEditLectProd(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)

        if mSchemaLect != None :
           mHeaderFont = QFont()
           mSchemaLect = sorted(mSchemaLect, key=lambda colonnes: colonnes[2], reverse = True)

           while i in range(len(mSchemaLect)) :
              self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mSchemaLect[i][0]) ] ) ] )
              rootOut = self.topLevelItem( 0 )

              if mSchemaLect[i][1] == 'true': #Reel
                 mHeaderFont.setBold(True)           
                 rootOut.setToolTip(0, QtWidgets.QApplication.translate("bibli_asgard", "The role is designated reader for the schema", None).replace("LECTEUR", "<b>LECTEUR</b>") + " <b>" + str(mSchemaLect[i][0]).upper() + "</b>")
              else : 
                 mHeaderFont.setBold(False)
                 rootOut.setToolTip(0, QtWidgets.QApplication.translate("bibli_asgard", "Role is a member of the designated reader for the schema", None).replace("LECTEUR", "<b>LECTEUR</b>") + " <b>" + str(mSchemaLect[i][0]).upper() + "</b>")
              rootOut.setFont(0, mHeaderFont)              

              mLettre = "autre" #Robustesse
              for mActif in self.Dialog.mSchemasBlocs :
                  if mActif[0] == mSchemaLect[i][0] :#Bloc
                     mLettre = mActif[1] if mActif[1] != None else "autre"
              rootOut.setIcon(0, returnIcon(myPathIcon + "\\treeview\\" + str(mLettre) + ".png"))
              i += 1
           
#========================================================      
# Class pour le tree View Schéma EDITEUR    
class TREEVIEWASGARDSCHEMAEDITEUR(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["Editeur"])
        self.header().setStyleSheet("font:  bold;")
    #===============================              
    def afficheSchemaEditeur(self, Dialog, myPathIcon, mRolnameID, ArraymlisteDesRolesDeGroupeEtConnexions): 
        self.Dialog = Dialog 
        self.setGeometry(5, self.Dialog.groupBoxAffichageLeftDroits.height()/3 + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3 )
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
   
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #[Name, réel Edit, Lect, Prod 
        mSchemaLect, mSchemaEdit, mSchemaProd = returnSchemaEditLectProd(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)

        if mSchemaEdit != None :
           mHeaderFont = QFont()
           mSchemaEdit = sorted(mSchemaEdit, key=lambda colonnes: colonnes[2], reverse = True)

           while i in range(len(mSchemaEdit)) :
              self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mSchemaEdit[i][0]) ] ) ] )
              rootOut = self.topLevelItem( 0 )

              if mSchemaEdit[i][1] == 'true': #Reel
                 mHeaderFont.setBold(True)           
                 rootOut.setToolTip(0, QtWidgets.QApplication.translate("bibli_asgard", "The role is designated editor for the schema", None).replace("EDITEUR", "<b>EDITEUR</b>") + " <b>" + str(mSchemaEdit[i][0]).upper() + "</b>")
              else : 
                 mHeaderFont.setBold(False)
                 rootOut.setToolTip(0, QtWidgets.QApplication.translate("bibli_asgard", "Role is a member of the designated editor for the schema", None).replace("EDITEUR", "<b>EDITEUR</b>") + " <b>" + str(mSchemaEdit[i][0]).upper() + "</b>")
              rootOut.setFont(0, mHeaderFont)              

              mLettre = "autre" #Robustesse
              for mActif in self.Dialog.mSchemasBlocs :
                  if mActif[0] == mSchemaEdit[i][0] :#Bloc
                     mLettre = mActif[1] if mActif[1] != None else "autre"
              rootOut.setIcon(0, returnIcon(myPathIcon + "\\treeview\\" + str(mLettre) + ".png"))
              i += 1

#========================================================      
# Class pour le tree View Schéma PRODUCTEUR    
class TREEVIEWASGARDSCHEMAPRODUCTEUR(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["Producteur"])
        self.header().setStyleSheet("font: bold;")
    #===============================              
    def afficheSchemaProducteur(self, Dialog, myPathIcon, mRolnameID, ArraymlisteDesRolesDeGroupeEtConnexions): 
        self.Dialog = Dialog 
        self.setGeometry(5, ((self.Dialog.groupBoxAffichageLeftDroits.height()/3) *2) + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
   
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #[Name, réel Edit, Lect, Prod 
        mSchemaLect, mSchemaEdit, mSchemaProd = returnSchemaEditLectProd(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)
        if mSchemaProd != None :
           mHeaderFont = QFont()
           mSchemaProd = sorted(mSchemaProd, key=lambda colonnes: colonnes[2], reverse = True)
      
           while i in range(len(mSchemaProd)) :
              self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mSchemaProd[i][0]) ] ) ] )
              rootOut = self.topLevelItem( 0 )

              if mSchemaProd[i][1] == 'true': #Reel
                 mHeaderFont.setBold(True)           
                 rootOut.setToolTip(0, QtWidgets.QApplication.translate("bibli_asgard", "The role is designated producer for the schema", None).replace("PRODUCTEUR", "<b>PRODUCTEUR</b>") + " <b>" + str(mSchemaProd[i][0]).upper() + "</b>")
              else : 
                 mHeaderFont.setBold(False)
                 rootOut.setToolTip(0, QtWidgets.QApplication.translate("bibli_asgard", "Role is a member of the designated producer for the schema", None).replace("PRODUCTEUR", "<b>PRODUCTEUR</b>") + " <b>" + str(mSchemaProd[i][0]).upper() + "</b>")
              rootOut.setFont(0, mHeaderFont)              

              mLettre = "autre" #Robustesse
              for mActif in self.Dialog.mSchemasBlocs :
                  if mActif[0] == mSchemaProd[i][0] :#Bloc
                     mLettre = mActif[1] if mActif[1] != None else "autre"
              rootOut.setIcon(0, returnIcon(myPathIcon + "\\treeview\\" + str(mLettre) + ".png"))
              i += 1
              
#========================================================     
#========================================================     
# Class pour le tree View Membres OUT    
class TREEVIEWASGARDMEMBRESOUT(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["server"])
        self.setDragEnabled(False)
        self.setDropIndicatorShown(True)
        self.viewport().setAcceptDrops(False)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)  
        self.setSelectionMode(QAbstractItemView.ExtendedSelection	)  
    #===============================              
    def afficheDroitsOut(self, Dialog, myPathIcon, mServeurName, mRolnameID, mRolcanLogin, mConfigConnection,  ArraymlisteDesRolesDeGroupeEtConnexions):
        self.Dialog = Dialog 
        iconCursorInterdit = returnIcon(myPathIcon + "\\treeview\\cursor_interdit.png")
        iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
        iconRoleConnex = returnIcon(myPathIcon + "\\treeview\\connexion.png")
        iconRoleGroupe = returnIcon(myPathIcon + "\\treeview\\groupe.png")
        iconConnex = returnIcon(myPathIcon + "\\objets\\role.png")
        iconGroupe = returnIcon(myPathIcon + "\\objets\\groupe.png")
        zMessHeaderLabels = ""
        for t in  mConfigConnection : 
            if "password" not in t:
               zMessHeaderLabels += t + " / "
        self.setHeaderLabels([mServeurName])
        self.headerItem().setToolTip(0, zMessHeaderLabels[:-3])
        self.setGeometry(5, 5, self.Dialog.groupBoxAffichageRoleAppartOut.width() - 10, self.Dialog.groupBoxAffichageRoleAppartOut.height() -10 )
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #rolid + rolname + login + mOutIn 
        mBoucleMembre, mBoucleParent  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)

        if mRolcanLogin == False : #Membres
          while i in range(len(mBoucleMembre)) :
            if not mBoucleMembre[i][3] : # Out
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleMembre[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex)
            i += 1
        else : #Parents
          while i in range(len(mBoucleParent)) :
            if not mBoucleParent[i][3] : # Out
               if mBoucleParent[i][2] == False : #ROLANLOGIN
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleParent[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex)

                  #--Pour ToolTip
                  mTipID = mBoucleMembre[i][0]   # ID de l'Item ex : g_admin
                  mBoucleMembreTip, mBoucleParentTip  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, mTipID)
                  iListLabelToolTip, mListLabelToolTip = 0, []
                  while iListLabelToolTip in range(len(mBoucleMembreTip)) :
                     if mBoucleMembreTip[iListLabelToolTip][3] : # In
                        mListLabelToolTip.append(str(mBoucleMembreTip[iListLabelToolTip][1]))
                     iListLabelToolTip += 1
                  rootOut.setToolTip(0, "{}".format(", ".join(mListLabelToolTip)))    #pour chaque bloc
                  #--Pour ToolTip

            i += 1
            
        self.itemClicked.connect( self.ihmsDroitsOut ) 
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect( self.menuContextuelAsgardOut)

    #===============================              
    def afficheDroitsOutBIS(self, Dialog, myPathIcon, mServeurName, mRolnameID, mRolcanLogin, mConfigConnection,  ArraymlisteDesRolesDeGroupeEtConnexions):
        self.Dialog = Dialog 
        iconCursorInterdit = returnIcon(myPathIcon + "\\treeview\\cursor_interdit.png")
        iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
        iconRoleConnex = returnIcon(myPathIcon + "\\treeview\\connexion.png")
        iconRoleGroupe = returnIcon(myPathIcon + "\\treeview\\groupe.png")
        iconConnex = returnIcon(myPathIcon + "\\objets\\role.png")
        iconGroupe = returnIcon(myPathIcon + "\\objets\\groupe.png")
        zMessHeaderLabels = ""
        for t in  mConfigConnection : 
            if "password" not in t:
               zMessHeaderLabels += t + " / "
        self.setHeaderLabels([mServeurName])
        self.headerItem().setToolTip(0, zMessHeaderLabels[:-3])
        self.setGeometry(5, 5, self.Dialog.groupBoxAffichageRoleAppartOut.width() - 10, self.Dialog.groupBoxAffichageRoleAppartOut.height() -10 )
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #rolid + rolname + login + mOutIn 
        mBoucleMembre, mBoucleParent  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)
        
        #INVERSION membres Parents pour bouton Membres / Appartenance
        if mRolcanLogin == True : #Parents
          while i in range(len(mBoucleMembre)) :
            if not mBoucleMembre[i][3] : # Out
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleMembre[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex)
            i += 1
        else : #Membres
          while i in range(len(mBoucleParent)) :
            if not mBoucleParent[i][3] : # Out
               if mBoucleParent[i][2] == False : #ROLANLOGIN
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleParent[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex)

                  #--Pour ToolTip
                  mTipID = mBoucleMembre[i][0]   # ID de l'Item ex : g_admin
                  mBoucleMembreTip, mBoucleParentTip  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, mTipID)
                  iListLabelToolTip, mListLabelToolTip = 0, []
                  while iListLabelToolTip in range(len(mBoucleMembreTip)) :
                     if mBoucleMembreTip[iListLabelToolTip][3] : # In
                        mListLabelToolTip.append(str(mBoucleMembreTip[iListLabelToolTip][1]))
                     iListLabelToolTip += 1
                  rootOut.setToolTip(0, "{}".format(", ".join(mListLabelToolTip)))    #pour chaque bloc
                  #--Pour ToolTip

            i += 1
            
        self.itemClicked.connect( self.ihmsDroitsOut ) 
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect( self.menuContextuelAsgardOut)

    #-------------                                                    
    def menuContextuelAsgardOut(self, point):
        index = self.indexAt(point)
        if not index.isValid():
           return
        self.Dialog.executeDroits.setVisible(False)
        
        if self.Dialog.case_membreappartient.isChecked():         
           self.Dialog.labelOutIn.setText("OUT")
        else :
           self.Dialog.labelOutIn.setText("OUTBIS")
        
        self.treeMenu = QMenu(self)
        #-------   
        menuIcon = returnIcon(self.Dialog.myPathIcon + "\\treeview\\flechedroite.png")          
        self.treeActionSchema_new = QAction(QIcon(menuIcon), "Ajouter", self.treeMenu)
        self.treeMenu.addAction(self.treeActionSchema_new)
        self.treeActionSchema_new.triggered.connect( lambda : deplaceItemOutIn(self) )
        #-------
        self.treeMenu.exec_(self.mapToGlobal(point))
        
    #------         
    def ihmsDroitsOut(self, item, column): 
        mItemClic = item.data(column, Qt.DisplayRole)
        imgOut = os.path.dirname(__file__) + "\\icons\\" + "\\treeview\\flechedroite.png"
        img = imgOut.replace("\\","/")
        self.Dialog.executeDroits.setStyleSheet("background-image : url(" + img + ");")
        self.Dialog.executeDroits.setVisible(True)        

        if self.Dialog.case_membreappartient.isChecked():         
           self.Dialog.labelOutIn.setText("OUT")
        else :
           self.Dialog.labelOutIn.setText("OUTBIS")
        
#============     
#============ 
#Création GIF et Déplacement 
def addDeplaceGif(**kwargs) :
    if kwargs['_action'] == "ADD" :
       _movie = QtGui.QMovie(kwargs['_gif'])
       kwargs['_objet'].setMovie(_movie)
       _movie.start()
    kwargs['_objet'].setGeometry(QtCore.QRect(kwargs['_x'], kwargs['_y'], kwargs['_l'], kwargs['_h']))
    return

#============     
#============ 
#Déplace les items Buttons 
def deplaceItemOutIn(self ) :
    if self.Dialog.labelOutIn.text() == "OUT" :
       selectedItems = self.Dialog.mTreePostgresqlMembresOut.selectedItems()
       if len(selectedItems) < 1:
            return
    elif self.Dialog.labelOutIn.text() == "IN" :
       selectedItems = self.Dialog.mTreePostgresqlMembresIn.selectedItems()
       if len(selectedItems) < 1:
            return
    elif self.Dialog.labelOutIn.text() == "OUTBIS" :
       selectedItems = self.Dialog.mTreePostgresqlMembresOutBIS.selectedItems()
       if len(selectedItems) < 1:
            return
    elif self.Dialog.labelOutIn.text() == "INBIS" :
       selectedItems = self.Dialog.mTreePostgresqlMembresInBIS.selectedItems()
       if len(selectedItems) < 1:
            return
    #----
    if self.Dialog.labelOutIn.text() == "OUT" :
       #----
       mBoucleItemSelect = True 
       while mBoucleItemSelect :                 
          #----
          selectedItems = self.Dialog.mTreePostgresqlMembresOut.selectedItems()
          mItemWidgetID  = selectedItems[0]       #Id
          mItemWidgetLIB = mItemWidgetID.text(0)  #Lib
          #----
          mIndex = 0                              #pos
          while mIndex < self.Dialog.mTreePostgresqlMembresOut.topLevelItemCount() :
             if mItemWidgetLIB == self.Dialog.mTreePostgresqlMembresOut.topLevelItem(mIndex).text(0) :
                self.Dialog.mTreePostgresqlMembresOut.takeTopLevelItem(mIndex)
                self.Dialog.mTreePostgresqlMembresIn.insertTopLevelItem(0, mItemWidgetID)
                selectedItems = self.Dialog.mTreePostgresqlMembresOut.selectedItems()
                if len(selectedItems) < 1:
                   self.Dialog.executeDroits.setVisible(False)        
                break
             else :
                mIndex += 1
          if len(selectedItems) < 1:
             mBoucleItemSelect = False
       #----
    #----
    if self.Dialog.labelOutIn.text() == "IN" : 
       #----
       mBoucleItemSelect = True 
       while mBoucleItemSelect :                 
          #----
          selectedItems = self.Dialog.mTreePostgresqlMembresIn.selectedItems()
          mItemWidgetID  = selectedItems[0]       #Id
          mItemWidgetLIB = mItemWidgetID.text(0)  #Lib
          #----
          mIndex = 0                              #pos
          while mIndex < self.Dialog.mTreePostgresqlMembresIn.topLevelItemCount() :
             if mItemWidgetLIB == self.Dialog.mTreePostgresqlMembresIn.topLevelItem(mIndex).text(0) :
                self.Dialog.mTreePostgresqlMembresIn.takeTopLevelItem(mIndex)
                self.Dialog.mTreePostgresqlMembresOut.insertTopLevelItem(0, mItemWidgetID)
                selectedItems = self.Dialog.mTreePostgresqlMembresIn.selectedItems()
                if len(selectedItems) < 1:
                   self.Dialog.executeDroits.setVisible(False)        
                break
             else :
                mIndex += 1
          if len(selectedItems) < 1:
             mBoucleItemSelect = False
       #----
    #----
    if self.Dialog.labelOutIn.text() == "OUTBIS" :
       #----
       mBoucleItemSelect = True 
       while mBoucleItemSelect :                 
          #----
          selectedItems = self.Dialog.mTreePostgresqlMembresOutBIS.selectedItems()
          mItemWidgetID  = selectedItems[0]       #Id
          mItemWidgetLIB = mItemWidgetID.text(0)  #Lib
          #----
          mIndex = 0                              #pos
          while mIndex < self.Dialog.mTreePostgresqlMembresOutBIS.topLevelItemCount() :
             if mItemWidgetLIB == self.Dialog.mTreePostgresqlMembresOutBIS.topLevelItem(mIndex).text(0) :
                self.Dialog.mTreePostgresqlMembresOutBIS.takeTopLevelItem(mIndex)
                self.Dialog.mTreePostgresqlMembresInBIS.insertTopLevelItem(0, mItemWidgetID)
                selectedItems = self.Dialog.mTreePostgresqlMembresOutBIS.selectedItems()
                if len(selectedItems) < 1:
                   self.Dialog.executeDroits.setVisible(False)        
                break
             else :
                mIndex += 1
          if len(selectedItems) < 1:
             mBoucleItemSelect = False
       #----
    #----
    if self.Dialog.labelOutIn.text() == "INBIS" : 
       #----
       mBoucleItemSelect = True 
       while mBoucleItemSelect :                 
          #----
          selectedItems = self.Dialog.mTreePostgresqlMembresInBIS.selectedItems()
          mItemWidgetID  = selectedItems[0]       #Id
          mItemWidgetLIB = mItemWidgetID.text(0)  #Lib
          #----
          mIndex = 0                              #pos
          while mIndex < self.Dialog.mTreePostgresqlMembresInBIS.topLevelItemCount() :
             if mItemWidgetLIB == self.Dialog.mTreePostgresqlMembresInBIS.topLevelItem(mIndex).text(0) :
                self.Dialog.mTreePostgresqlMembresInBIS.takeTopLevelItem(mIndex)
                self.Dialog.mTreePostgresqlMembresOutBIS.insertTopLevelItem(0, mItemWidgetID)
                selectedItems = self.Dialog.mTreePostgresqlMembresInBIS.selectedItems()
                if len(selectedItems) < 1:
                   self.Dialog.executeDroits.setVisible(False)        
                break
             else :
                mIndex += 1
          if len(selectedItems) < 1:
             mBoucleItemSelect = False
       #----
    return    
 
#============ 
#Pour les Quatre Tree OUT et IN
# = return Listes  
def returnOutInListe(self ) :

    mListOut = []
    mIndexOUT = 0 
    while mIndexOUT < self.Dialog.mTreePostgresqlMembresOut.topLevelItemCount() :
       mListOut.append(self.Dialog.mTreePostgresqlMembresOut.topLevelItem(mIndexOUT).text(0))
       mIndexOUT += 1
    #---                   
    mListIn = []
    mIndexIN = 0 
    while mIndexIN < self.Dialog.mTreePostgresqlMembresIn.topLevelItemCount() :
       mListIn.append(self.Dialog.mTreePostgresqlMembresIn.topLevelItem(mIndexIN).text(0))
       mIndexIN += 1
       
    mListOutBIS = []
    mIndexOUTBIS = 0 
    while mIndexOUTBIS < self.Dialog.mTreePostgresqlMembresOutBIS.topLevelItemCount() :
       mListOutBIS.append(self.Dialog.mTreePostgresqlMembresOutBIS.topLevelItem(mIndexOUTBIS).text(0))
       mIndexOUTBIS += 1
    #---                   
    mListInBIS = []
    mIndexINBIS = 0 
    while mIndexINBIS < self.Dialog.mTreePostgresqlMembresInBIS.topLevelItemCount() :
       mListInBIS.append(self.Dialog.mTreePostgresqlMembresInBIS.topLevelItem(mIndexINBIS).text(0))
       mIndexINBIS += 1

    return mListOut, mListIn, mListOutBIS, mListInBIS      
       
#============ 
#Pour les deux Tree OUT et IN
# = return Out/In    
def returnOutInAppartNonappart(self, ArraymRolesDeGroupe, mIdFind) :
    #Create Lists for In Out
    # si bon item clic

    if self.Dialog.mTreePostgresqlDroits.mode == "update" :
       #Membre
       mListRoleGroupMembre = [mListRoleGroupMembre[14] for mListRoleGroupMembre in ArraymRolesDeGroupe if mListRoleGroupMembre[12] == mIdFind][0]
       #Parent
       mListRoleGroupParent = [mListRoleGroupMembre[15] for mListRoleGroupMembre in ArraymRolesDeGroupe if mListRoleGroupMembre[12] == mIdFind][0]
    elif self.Dialog.mTreePostgresqlDroits.mode == "create" : #ne tient pas compte de l'ID
       #Membre
       mListRoleGroupMembre = [mListRoleGroupMembre[14] for mListRoleGroupMembre in ArraymRolesDeGroupe][0]
       #Parent
       mListRoleGroupParent = [mListRoleGroupMembre[15] for mListRoleGroupMembre in ArraymRolesDeGroupe][0]
    
    #-------
    iBoucle, mListRoleGroupMembreComplet = 0, []
    while iBoucle in range(len(ArraymRolesDeGroupe)) :
       if self.Dialog.mTreePostgresqlDroits.mode == "update" : #ne tient pas compte de l'ID
          if ArraymRolesDeGroupe[iBoucle][12] != mIdFind :
             #rolid + rolname + login + mOutIn 
             mListTemp = []
             mListTemp.append(ArraymRolesDeGroupe[iBoucle][12])
             mListTemp.append(ArraymRolesDeGroupe[iBoucle][0])
             mListTemp.append(ArraymRolesDeGroupe[iBoucle][5])
             mListTemp.append(True if (ArraymRolesDeGroupe[iBoucle][12] in mListRoleGroupMembre) else False)
             mListRoleGroupMembreComplet.append(tuple(mListTemp))
       elif self.Dialog.mTreePostgresqlDroits.mode == "create" : #ne tient pas compte de l'ID
          #rolid + rolname + login + mOutIn 
          mListTemp = []
          mListTemp.append(ArraymRolesDeGroupe[iBoucle][12])
          mListTemp.append(ArraymRolesDeGroupe[iBoucle][0])
          mListTemp.append(ArraymRolesDeGroupe[iBoucle][5])
          #mListTemp.append(True if (ArraymRolesDeGroupe[iBoucle][0] == "g_consult" and self.Dialog.mTreePostgresqlDroits.mRolcanLogin) else False)       #Non Membres
          mListTemp.append(False)       #Non Parents #Modif 2021/08 pour ne pas avoir g_consult dans la liste des membres à la création
          mListRoleGroupMembreComplet.append(tuple(mListTemp))
       iBoucle += 1                
    #-------
    iBoucle, mListRoleGroupParentComplet = 0, []
    while iBoucle in range(len(ArraymRolesDeGroupe)) :
       if self.Dialog.mTreePostgresqlDroits.mode == "update" : #ne tient pas compte de l'ID
          if ArraymRolesDeGroupe[iBoucle][12] != mIdFind :
             #rolid + rolname + login + mOutIn 
             mListTemp = []
             mListTemp.append(ArraymRolesDeGroupe[iBoucle][12])
             mListTemp.append(ArraymRolesDeGroupe[iBoucle][0])
             mListTemp.append(ArraymRolesDeGroupe[iBoucle][5])
             mListTemp.append(True if (ArraymRolesDeGroupe[iBoucle][12] in mListRoleGroupParent) else False)
             mListRoleGroupParentComplet.append(tuple(mListTemp))
       elif self.Dialog.mTreePostgresqlDroits.mode == "create" : #ne tient pas compte de l'ID
          #rolid + rolname + login + mOutIn 
          mListTemp = []
          mListTemp.append(ArraymRolesDeGroupe[iBoucle][12])
          mListTemp.append(ArraymRolesDeGroupe[iBoucle][0])
          mListTemp.append(ArraymRolesDeGroupe[iBoucle][5])
          mListTemp.append(True if (ArraymRolesDeGroupe[iBoucle][0] == "g_consult"and self.Dialog.mTreePostgresqlDroits.mRolcanLogin) else False)       #Non Parents
          mListRoleGroupParentComplet.append(tuple(mListTemp))
       iBoucle += 1
    #-------
    #order by 
    mOrderByChoiceGroupe, mOrderByChoiceConnexion  = "1", "2"
    # A supprimer si Ok : llTempMembre = [ [ [(mOrderByChoiceGroupe if eee[1][2] else mOrderByChoiceConnexion) + eee[0][len(eee[0]) - 1 ] ], eee[1] ] for eee in [ [ee[1].split("."),ee] for ee in [ e for e in mListRoleGroupMembreComplet ] ] ]
    # A supprimer si Ok : mListRoleGroupMembreComplet = [l[1] for l in sorted(llTempMembre, key=lambda colonnes: colonnes[0], reverse = True)]
    mListRoleGroupMembreComplet = [l for l in sorted(mListRoleGroupMembreComplet, key=lambda colonnes: colonnes[1].lower(), reverse = True)]
    #------
    # A supprimer si Ok : llTempParent = [ [ [(mOrderByChoiceGroupe if eee[1][2] else mOrderByChoiceConnexion) + eee[0][len(eee[0]) - 1 ] ], eee[1] ] for eee in [ [ee[1].split("."),ee] for ee in [ e for e in mListRoleGroupParentComplet ] ] ]
    # A supprimer si Ok : mListRoleGroupParentComplet = [l[1] for l in sorted(llTempParent, key=lambda colonnes: colonnes[0], reverse = True)]

    mListRoleGroupParentComplet = [l for l in sorted(mListRoleGroupParentComplet, key=lambda colonnes: colonnes[1].lower(), reverse = True)]

    return mListRoleGroupMembreComplet, mListRoleGroupParentComplet   


#============ 
#Pour les trois Tree schema edit, lect, Prod
# = return Out/In    
def returnSchemaEditLectProd(self, ArraymRolesDeGroupe, mIdFind) :   
    mPattern = 'Find_(FirstCar_)&Ret_FirstCar' #Pour ordonner les autres
    mSchemaLect, mSchemaEdit, mSchemaProd = None, None, None

    #Lecteur  == Nom schéma, TrueFalse edit,lect,prod et prefixe bloc
    mSchemaLect = [mListRoleGroupMembre[16] for mListRoleGroupMembre in ArraymRolesDeGroupe if mListRoleGroupMembre[12] == mIdFind][0]
    if mSchemaLect != None :
       mTemp = []
       for mListRoleGroupMembre in mSchemaLect :
           mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mListRoleGroupMembre[0])[0] 
           if mPrefixe == '' :            
              mPrefixe = 'zz'    #autre
           else :
              for mCorbeille in self.Dialog.mSchemasBlocs :
                  if mCorbeille[0] == mListRoleGroupMembre[0] and mCorbeille[1] == 'd' : #Bloc Corbeille
                     mPrefixe = 'zzz'
                     break
           mTemp.append( mListRoleGroupMembre +  [ str(mPrefixe) + str(mListRoleGroupMembre[0]) ] )
       if mTemp :
          mSchemaLect = mTemp

    #Editeur
    mSchemaEdit = [mListRoleGroupMembre[17] for mListRoleGroupMembre in ArraymRolesDeGroupe if mListRoleGroupMembre[12] == mIdFind][0]
    if mSchemaEdit != None :
       mTemp = []
       for mListRoleGroupMembre in mSchemaEdit :
           mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mListRoleGroupMembre[0])[0] 
           if mPrefixe == '' :            
              mPrefixe = 'zz'    #autre
           else :
              for mCorbeille in self.Dialog.mSchemasBlocs :
                  if mCorbeille[0] == mListRoleGroupMembre[0] and mCorbeille[1] == 'd' : #Bloc Corbeille
                     mPrefixe = 'zzz'
                     break
           mTemp.append( mListRoleGroupMembre +  [ str(mPrefixe) + str(mListRoleGroupMembre[0]) ] )
       if mTemp :
          mSchemaEdit = mTemp    

    #Producteur
    mSchemaProd = [mListRoleGroupMembre[18] for mListRoleGroupMembre in ArraymRolesDeGroupe if mListRoleGroupMembre[12] == mIdFind][0]
    if mSchemaProd != None :
       mTemp = []
       for mListRoleGroupMembre in mSchemaProd :
           mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mListRoleGroupMembre[0])[0] 
           if mPrefixe == '' :            
              mPrefixe = 'zz'    #autre
           else :
              for mCorbeille in self.Dialog.mSchemasBlocs :
                  if mCorbeille[0] == mListRoleGroupMembre[0] and mCorbeille[1] == 'd' : #Bloc Corbeille
                     mPrefixe = 'zzz'
                     break
           mTemp.append( mListRoleGroupMembre +  [ str(mPrefixe) + str(mListRoleGroupMembre[0]) ] )
       if mTemp :
          mSchemaProd = mTemp
    return mSchemaLect, mSchemaEdit, mSchemaProd   
           
#========================================================
# Class pour le tree View Membres IN    
class TREEVIEWASGARDMEMBRESIN(QTreeWidget):
    customMimeType = "text/plain"   

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["server"])
        self.setDragEnabled(False)
        self.setDropIndicatorShown(True)
        self.viewport().setAcceptDrops(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)  
        self.setSelectionMode(QAbstractItemView.ExtendedSelection	)  
      
    #===============================
    def afficheDroitsIn(self, Dialog, myPathIcon, mServeurName, mRolnameID, mRolcanLogin, mConfigConnection, ArraymlisteDesRolesDeGroupeEtConnexions): 
        self.Dialog = Dialog 
        iconCursorInterdit = returnIcon(myPathIcon + "\\treeview\\cursor_interdit.png")
        iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
        iconRoleConnex = returnIcon(myPathIcon + "\\treeview\\connexion.png")
        iconRoleGroupe = returnIcon(myPathIcon + "\\treeview\\groupe.png")
        iconConnex = returnIcon(myPathIcon + "\\objets\\role.png")
        iconGroupe = returnIcon(myPathIcon + "\\objets\\groupe.png")
        zMessHeaderLabels = ""
        for t in  mConfigConnection : 
            if "password" not in t:
               zMessHeaderLabels += t + " / "
        self.setHeaderLabels([mServeurName])
        self.headerItem().setToolTip(0, zMessHeaderLabels[:-3])
        self.setGeometry(5,5, self.Dialog.groupBoxAffichageRoleAppartIn.width() - 10, self.Dialog.groupBoxAffichageRoleAppartIn.height() - 10 )
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #rolid + rolname + login + mOutIn 
        mBoucleMembre, mBoucleParent  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)
        if mRolcanLogin == False : #Membres
          while i in range(len(mBoucleMembre)) :
            if mBoucleMembre[i][3] : # In   
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleMembre[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex) 
            i += 1
        else : #Parents
          while i in range(len(mBoucleParent)) :
            if mBoucleParent[i][3] : # In
               if mBoucleParent[i][2] == False : #ROLANLOGIN
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleParent[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  #if self.Dialog.mTreePostgresqlDroits.mode == "create" :   #désactive la sélection
                  #   rootOut.setFlags(Qt.NoItemFlags)
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex)
               
                  #--Pour ToolTip
                  mTipID = mBoucleParent[i][0]   # ID de l'Item ex : g_admin
                  mBoucleMembreTip, mBoucleParentTip  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, mTipID)
                  iListLabelToolTip, mListLabelToolTip = 0, []
                  while iListLabelToolTip in range(len(mBoucleMembreTip)) :
                     if mBoucleMembreTip[iListLabelToolTip][3] : # In
                        mListLabelToolTip.append(str(mBoucleMembreTip[iListLabelToolTip][1]))
                     iListLabelToolTip += 1
                  rootOut.setToolTip(0, "{}".format(", ".join(mListLabelToolTip)))    #pour chaque bloc
                  #--Pour ToolTip

            i += 1
        #-----------
        self.itemClicked.connect( self.ihmsDroitsIn ) 
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect( self.menuContextuelAsgardIn)
      
    #===============================
    def afficheDroitsInBIS(self, Dialog, myPathIcon, mServeurName, mRolnameID, mRolcanLogin, mConfigConnection, ArraymlisteDesRolesDeGroupeEtConnexions): 
        self.Dialog = Dialog 
        iconCursorInterdit = returnIcon(myPathIcon + "\\treeview\\cursor_interdit.png")
        iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
        iconRoleConnex = returnIcon(myPathIcon + "\\treeview\\connexion.png")
        iconRoleGroupe = returnIcon(myPathIcon + "\\treeview\\groupe.png")
        iconConnex = returnIcon(myPathIcon + "\\objets\\role.png")
        iconGroupe = returnIcon(myPathIcon + "\\objets\\groupe.png")
        zMessHeaderLabels = ""
        for t in  mConfigConnection : 
            if "password" not in t:
               zMessHeaderLabels += t + " / "
        self.setHeaderLabels([mServeurName])
        self.headerItem().setToolTip(0, zMessHeaderLabels[:-3])
        self.setGeometry(5,5, self.Dialog.groupBoxAffichageRoleAppartIn.width() - 10, self.Dialog.groupBoxAffichageRoleAppartIn.height() - 10 )
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions
        #============
        i = 0
        #rolid + rolname + login + mOutIn 
        mBoucleMembre, mBoucleParent  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, Dialog.mTreePostgresqlDroits.mRolnameID)
        if mRolcanLogin == True : #Parents
          while i in range(len(mBoucleMembre)) :
            if mBoucleMembre[i][3] : # In   
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleMembre[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex) 
            i += 1
        else : #Membres
          while i in range(len(mBoucleParent)) :
            if mBoucleParent[i][3] : # In
               if mBoucleParent[i][2] == False : #ROLANLOGIN
                  self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ str(mBoucleParent[i][1]) ] ) ] )
                  rootOut = self.topLevelItem( 0 )
                  #if self.Dialog.mTreePostgresqlDroits.mode == "create" :   #désactive la sélection
                  #   rootOut.setFlags(Qt.NoItemFlags)
                  if mBoucleMembre[i][2] == False : #ROLANLOGIN
                     rootOut.setIcon(0, iconGroupe)
                  else :                                                                 
                     rootOut.setIcon(0, iconConnex)
               
                  #--Pour ToolTip
                  mTipID = mBoucleParent[i][0]   # ID de l'Item ex : g_admin
                  mBoucleMembreTip, mBoucleParentTip  = returnOutInAppartNonappart(self, self.ArraymRolesDeGroupe, mTipID)
                  iListLabelToolTip, mListLabelToolTip = 0, []
                  while iListLabelToolTip in range(len(mBoucleMembreTip)) :
                     if mBoucleMembreTip[iListLabelToolTip][3] : # In
                        mListLabelToolTip.append(str(mBoucleMembreTip[iListLabelToolTip][1]))
                     iListLabelToolTip += 1
                  rootOut.setToolTip(0, "{}".format(", ".join(mListLabelToolTip)))    #pour chaque bloc
                  #--Pour ToolTip

            i += 1
        #-----------
        self.itemClicked.connect( self.ihmsDroitsIn ) 
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect( self.menuContextuelAsgardIn)

    #-------------                                                    
    def menuContextuelAsgardIn(self, point):
        index = self.indexAt(point)
        if not index.isValid():
           return
        self.Dialog.executeDroits.setVisible(False) 
        
        if self.Dialog.case_membreappartient.isChecked():         
           self.Dialog.labelOutIn.setText("IN")
        else :
           self.Dialog.labelOutIn.setText("INBIS")
        
        self.treeMenu = QMenu(self)
        #-------   
        menuIcon = returnIcon(self.Dialog.myPathIcon + "\\treeview\\flechegauche.png")          
        self.treeActionSchema_new = QAction(QIcon(menuIcon), "Enlever", self.treeMenu)
        self.treeMenu.addAction(self.treeActionSchema_new)
        self.treeActionSchema_new.triggered.connect( lambda : deplaceItemOutIn(self) )
        #-------
        self.treeMenu.exec_(self.mapToGlobal(point))
                
    #------         
    def ihmsDroitsIn(self, item, column):
        mItemClic = item.data(column, Qt.DisplayRole)
        imgOut = os.path.dirname(__file__) + "\\icons\\" + "\\treeview\\flechegauche.png"
        img = imgOut.replace("\\","/")
        self.Dialog.executeDroits.setStyleSheet("background-image : url(" + img + ");")
        self.Dialog.executeDroits.setVisible(True) 

        if self.Dialog.case_membreappartient.isChecked():         
           self.Dialog.labelOutIn.setText("IN")
        else :
           self.Dialog.labelOutIn.setText("INBIS")
#========================================================
# Class pour le tree View Droits    
class TREEVIEWASGARDDROITS(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["server"])
        
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.viewport().setAcceptDrops(True)
        self.setAcceptDrops(True)
        self.setDragDropMode(QAbstractItemView.NoDragDrop)
        self.mRolnameID = ""

    def afficheDroits(self, Dialog, myPathIcon, mServeurName, mConfigConnection, ArraymlisteDesRolesDeGroupeEtConnexions):
        self.Dialog, self.myPathIcon, self.mConfigConnection, self.ArraymlisteDesRolesDeGroupeEtConnexions = Dialog, myPathIcon, mConfigConnection, ArraymlisteDesRolesDeGroupeEtConnexions                                                                      
        iconCursorInterdit = returnIcon(myPathIcon + "\\treeview\\cursor_interdit.png")
        iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
        iconRoleConnex = returnIcon(myPathIcon + "\\treeview\\connexion.png")
        iconRoleGroupe = returnIcon(myPathIcon + "\\treeview\\groupe.png")
        iconConnex = returnIcon(myPathIcon + "\\objets\\role.png")
        iconGroupe = returnIcon(myPathIcon + "\\objets\\groupe.png")
        zMessHeaderLabels = ""
        self.mDepartTransfertDroitCouper, self.mDepartmGroupeRole = "", True
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)

        for t in  mConfigConnection : 
            if "password" not in t:
               zMessHeaderLabels += t + " / "
        self.setHeaderLabels([mServeurName])
        self.headerItem().setToolTip(0, zMessHeaderLabels[:-3])
        self.setGeometry(15, 15, self.Dialog.groupBoxAffichageLeftDroits.width() - 30, self.Dialog.groupBoxAffichageLeftDroits.height() - 30)
        
        #===============================
        #============
        self.ArraymRolesDeGroupe = ArraymlisteDesRolesDeGroupeEtConnexions

        #order by   
        mOrderByChoiceGroupe, mOrderByChoiceConnexion  = "1", "2"
        # A SUPPRIMER si OK : llTemp = [ [ [(mOrderByChoiceGroupe if eee[1][5] else mOrderByChoiceConnexion) + eee[0][len(eee[0]) - 1 ] ], eee[1] ] for eee in [ [ee[0].split("."),ee] for ee in [ e for e in self.ArraymRolesDeGroupe ] ] ]
        # A SUPPRIMER si OK : self.ArraymRolesDeGroupe = [l[1] for l in sorted(llTemp, key=lambda colonnes: colonnes[0], reverse = False)]
        self.ArraymRolesDeGroupe = [l for l in sorted(self.ArraymRolesDeGroupe, key=lambda colonnes: colonnes[0].lower(), reverse = False)]
        #order by
        #============
        #Affiche Droits 
        self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ QtWidgets.QApplication.translate("bibli_asgard", "Connection Roles", None) ] ) ] )
        rootConnex = self.topLevelItem( 0 )
        rootConnex.setIcon(0, iconRoleConnex)                                                                 
        i = 0
        while i in range(len(self.ArraymRolesDeGroupe)) :
            if self.ArraymRolesDeGroupe[i][5] == True : #ROLANLOGIN
               mRootConnex, mRootConnexIcons = self.ArraymRolesDeGroupe[i][0], iconConnex 
               node = QTreeWidgetItem(None, [ mRootConnex ] )
               node.setIcon(0, QIcon(mRootConnexIcons))
               rootConnex.addChild( node )
            i += 1
        #============ 
        self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ QtWidgets.QApplication.translate("bibli_asgard", "Group Roles", None) ] ) ] )
        rootGroup = self.topLevelItem( 0 )
        rootGroup.setIcon(0, iconRoleGroupe)
        i = 0
        while i in range(len(self.ArraymRolesDeGroupe)) :
            if self.ArraymRolesDeGroupe[i][5] != True : #ROLANLOGIN
               mRootGroup, mRootGroupIcons = self.ArraymRolesDeGroupe[i][0], iconGroupe 
               node = QTreeWidgetItem(None, [ mRootGroup ] )
               node.setIcon(0, QIcon(mRootGroupIcons))
               rootGroup.addChild( node )
            i += 1

        #===================   
        self.itemClicked.connect( self.ihmsDroits )                                                      
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuContextuelAsgardDroits)
        self.currentItemChanged.connect( self.ihmsDroitsCurrentIndexChanged )                                                      

    #-------------                                                    
    def menuContextuelAsgardDroits(self, point):
        index = self.indexAt(point)

        if not index.isValid():
           return                                                  

        item = self.itemAt(point)
        mNameEnCours = item.text(0) 
        self.mNameEnCours = mNameEnCours

        #GroupeOuRole 
        for i in range(len(self.ArraymRolesDeGroupe)) :
            if mNameEnCours == self.ArraymRolesDeGroupe[i][0] : 
               mGroupeRole     = True if self.ArraymRolesDeGroupe[i][5] else False
               self.mGroupeRole = mGroupeRole
               mRolDependances =  True if self.ArraymRolesDeGroupe[i][20] == None else False
               self.mRolDependances = mRolDependances
               mListeRolDependances =  self.ArraymRolesDeGroupe[i][20] if self.ArraymRolesDeGroupe[i][20] != None  else []
               break

        self.Dialog.groupBoxAffichageRoleAttribut.setVisible(False)
        self.Dialog.groupBoxAffichageRoleAppart.setVisible(False)
        self.Dialog.executeDroits.setVisible(False) 
        self.Dialog.executeButtonRole.setVisible(False) 
        self.Dialog.groupBoxAffichageHelpDroits.setVisible(False)
        
        self.Dialog.groupBoxAffichageRightDroits.setVisible(True)
        self.Dialog.groupBoxAffichageHelpDroits.setVisible(True)
        self.Dialog.groupBoxAffichageRightDroitsSchemas.setVisible(False)

        if mNameEnCours == "Rôles de connexion" : 
           bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [100])
           self.treeMenu = QMenu(self)
           #-------   
           menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\connexion_new.png")          
           self.treeActionConnexion_new = QAction(QIcon(menuIcon), "Nouveau rôle de connexion", self.treeMenu)
           self.treeMenu.addAction(self.treeActionConnexion_new)
           self.treeActionConnexion_new.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionConnexion_new"))
           #-------
           self.treeMenu.exec_(self.mapToGlobal(point))
        elif mNameEnCours == "Rôles de groupe" :
           bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [101])
           self.treeMenu = QMenu(self)
           #-------
           menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\groupe_new.png")           
           self.treeActionGroupe_New = QAction(QIcon(menuIcon), "Nouveau rôle de groupe", self.treeMenu)
           self.treeMenu.addAction(self.treeActionGroupe_New)
           self.treeActionGroupe_New.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionGroupe_New"))
           #-------
           self.treeMenu.exec_(self.mapToGlobal(point))
        else : #groupe et rôle      
           self.treeMenu = QMenu(self)
           #------- Revoquer Rôle
           #-------
           if mGroupeRole :
              if self.mDepartTransfertDroitCouper == "" :
                 bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [104,102,106,108])
              else :
                 bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [104,102,107,108])
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\revoquer_role.png")           
              self.treeActionRevoquerRole = QAction(QIcon(menuIcon), "Révoquer tous les droits du rôle", self.treeMenu)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\supprime_role.png")           
              self.treeActionDeleteRole = QAction(QIcon(menuIcon), "Supprimer le rôle de connexion", self.treeMenu)
           else :
              if self.mDepartTransfertDroitCouper == "" :
                 bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [105,103,1060,108])
              else :
                 bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [105,103,1070,108])
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\revoquer_groupe.png")           
              self.treeActionRevoquerRole = QAction(QIcon(menuIcon), "Révoquer tous les droits du groupe", self.treeMenu)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\supprime_groupe.png")           
              self.treeActionDeleteRole = QAction(QIcon(menuIcon), "Supprimer le rôle de groupe", self.treeMenu)
           #-------
           self.treeMenu.addAction(self.treeActionRevoquerRole)
           self.treeMenu.addAction(self.treeActionDeleteRole)
           #-------
           self.treeActionDeleteRole.setEnabled(True if mRolDependances else False)
           if not mRolDependances :
              self.treeMenu.setToolTipsVisible(True)
              self.treeActionDeleteRole.setToolTip("{}".format(", ".join(mListeRolDependances)))
                         
           #-------
           self.treeMenu.addSeparator()
           #-------
           if self.mDepartTransfertDroitCouper == "" :
              if mGroupeRole :
                 menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reaffecte_droits_depart.png")
              else :           
                 menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reaffecte_droits_depart_gr.png")
              self.treeActionTransfertDroitCouper = QAction(QIcon(menuIcon), "Réaffecter les droits / Couper", self.treeMenu)
              self.treeMenu.addAction(self.treeActionTransfertDroitCouper)
              self.treeActionTransfertDroitCouper.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionTransfertDroitCouper"))
           #-------
           if self.mDepartTransfertDroitCouper != "" :
              if mGroupeRole :
                 menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reaffecte_droits_arrivee.png")           
              else :           
                 menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reaffecte_droits_arrivee_gr.png")           
              self.treeActionTransfertDroitColler = QAction(QIcon(menuIcon), "Réaffecter les droits / Coller", self.treeMenu)
              self.treeMenu.addAction(self.treeActionTransfertDroitColler)
              self.treeActionTransfertDroitColler.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionTransfertDroitColler"))
           #-------
           menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reaffecte_droits_annule.png")           
           self.treeActionTransfertDroitAnnuler = QAction(QIcon(menuIcon), "Annuler le Réaffecter les droits / Couper", self.treeMenu)
           self.treeMenu.addAction(self.treeActionTransfertDroitAnnuler)
           self.treeActionTransfertDroitAnnuler.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionTransfertDroitAnnuler"))
           #-------
           self.treeActionRevoquerRole.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionRevoquerRole"))
           self.treeActionDeleteRole.triggered.connect(lambda : self.actionFonctionTreeRoleGroupe(item, "treeActionDeleteRole"))
           #-------
           self.fonctionAfficheTransfertDroiteAll(mNameEnCours)
           self.treeMenu.exec_(self.mapToGlobal(point))

        return

    #**********************
    def fonctionAfficheTransfertDroiteAll(self, mGetItem):
        if hasattr(self,'treeActionTransfertDroitCouper')  : self.treeActionTransfertDroitCouper.setEnabled(False)
        if hasattr(self,'treeActionTransfertDroitColler')  : self.treeActionTransfertDroitColler.setEnabled(False)
        if hasattr(self,'treeActionTransfertDroitAnnuler') : self.treeActionTransfertDroitAnnuler.setEnabled(False)
        #------
        if self.mDepartTransfertDroitCouper != "" :
           if hasattr(self,'treeActionTransfertDroitAnnuler') : self.treeActionTransfertDroitAnnuler.setEnabled(True)
           if self.mGroupeRole == self.mDepartmGroupeRole : #Coller un role sur un groupe ou son contraire interdit 
              if self.mDepartTransfertDroitCouper != mGetItem :
                 # si type objet dans la liste des types d'objets
                 if hasattr(self,'treeActionTransfertDroitColler')  : self.treeActionTransfertDroitColler.setEnabled(True)
        else :
           if hasattr(self,'treeActionTransfertDroitCouper')  : self.treeActionTransfertDroitCouper.setEnabled(True)
           #-
           if hasattr(self,'treeActionTransfertDroitAnnuler')  : self.treeActionTransfertDroitAnnuler.setEnabled(True)
        
        #------
        # ToolTip
        if hasattr(self,'treeMenu') :
           self.treeMenu.setToolTipsVisible(True) 
           if self.mDepartTransfertDroitCouper != "" :
              mToolTip = "Nom : " + str(self.mDepartTransfertDroitCouper)  + " == Rôle de " + ("connexion" if self.mDepartmGroupeRole else "groupe")
           else :
              mToolTip = ""
           if hasattr(self,'treeActionTransfertDroitCouper')     : self.treeActionTransfertDroitCouper.setToolTip(mToolTip)
           if hasattr(self,'treeActionTransfertDroitColler')     : self.treeActionTransfertDroitColler.setToolTip(mToolTip)

        return        

    #**********************
    def actionFonctionTreeRoleGroupe(self,mNode, mAction):
        mGetItem = mNode.text(0)
       
        self.Dialog.groupBoxAffichageHelpDroits.setVisible(False)
        self.Dialog.groupBoxAffichageRoleAttribut.setVisible(True)
        self.Dialog.groupBoxAffichageRoleAppart.setVisible(True)
        self.Dialog.executeButtonRole.setVisible(True) 
        self.Dialog.groupBoxAffichageRightDroits.setVisible(True)
        #**********************
        if mAction == "treeActionConnexion_new" or mAction == "treeActionGroupe_New" :

           if mAction == "treeActionConnexion_new" :
              mRolcanLogin = True
              mServeurNameOut = QtWidgets.QApplication.translate("bibli_asgard", "Does not belong to :", None)
              mServeurNameIn = QtWidgets.QApplication.translate("bibli_asgard", "Belongs to group :", None)    
              self.Dialog.zone_mdp.setEnabled(True)
              self.Dialog.case_rolgestionschema.setVisible(False)
              self.Dialog.label_rolgestionschema.setVisible(False)
           elif mAction == "treeActionGroupe_New" :
              mRolcanLogin = False
              mServeurNameOut = QtWidgets.QApplication.translate("bibli_asgard", "Non-member role :", None)
              mServeurNameIn = QtWidgets.QApplication.translate("bibli_asgard", "Group member roles :", None)
              self.Dialog.zone_mdp.setEnabled(False)
              self.Dialog.case_rolgestionschema.setVisible(True)
              self.Dialog.label_rolgestionschema.setVisible(True)

           self.mRolcanLogin    = mRolcanLogin  # pour le create ventilation groupe/connexion
           self.mode = "create"
           self.mRolnameID      = 0   # Gestion pour le Where
           self.mRolname        = ''
           self.mDescription    = ''
           self.mMdp            = ''
           self.mRolcreaterole  = False
           self.mRolcreatedb    = False
           self.mRolsuper       = False
           self.mRolinherit     = True
           self.mRolreplication = False
           self.mRolbypassrls   = False
           self.mRollogin       = True if self.mRolcanLogin else False
           self.mRolgestionschema = False
           self.Dialog.case_membreappartient.setChecked(True)
           
           #Gestion du libellé du bouton appartenance/Membres quand Create
           mtextMembre  = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Members", None)
           mtextAppartient = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Membership", None)
           if self.mRolcanLogin :   
              self.Dialog.button_membreappartient.setText(mtextMembre     if self.Dialog.case_membreappartient.isChecked() else mtextAppartient)
           else :
              self.Dialog.button_membreappartient.setText(mtextAppartient if self.Dialog.case_membreappartient.isChecked() else mtextMembre)
           #Gestion du libellé du bouton appartenance/Membres

           self.initIhmDroits(self.Dialog, self.mode, mServeurNameOut, mServeurNameIn, self.mRolnameID, self.mRolname, mRolcanLogin, self.mDescription, self.mMdp, self.mRolcreaterole, self.mRolcreatedb, self.mRolsuper, self.mRolinherit, self.mRolreplication, self.mRolbypassrls, self.mRollogin, self.mRolgestionschema)
           #Essentiel passage si clic sur rôle (g ou c) et bascule membres/appartenance et apr_s NEW ROLE 
           bibli_ihm_asgard.showHideCtrlBascule_Normal_A_Bis(self.Dialog, True, mRolCanLogin = self.mRolcanLogin)
           #

        else :
           mCont = False
           
           if mAction == "treeActionDeleteRole" :
              mTitre = QtWidgets.QApplication.translate("bibli_asgard", "Confirmation", None)
              mLib = QtWidgets.QApplication.translate("bibli_asgard", "Are you sure you want to delete this role ?", None)
              if not self.Dialog.displayMessage or QMessageBox.question(None, mTitre, mLib,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.Yes : 
                 mCont = True
                 mKeySql = dicListSql(self,mAction)
                 mRoleNewID, mRoleOldID = mGetItem, "#nom_role#" 
                 dicReplace = {mRoleOldID: mRoleNewID}

                 #-- Permet de controler si le compte est g_admin ou parent de g_admin avec CREATEROLE   SET ROLE;
                 if self.Dialog.role_g_admin_createrole != self.Dialog.userConnecteEnCours :
                    dicReplace['#Role_g_admin_createrole#'] = "SET ROLE " + str(self.Dialog.role_g_admin_createrole) + ";"
                    dicReplace['#ResetRole#'] = "RESET ROLE ;"
                 else :
                    dicReplace['#Role_g_admin_createrole#'] = ''
                    dicReplace['#ResetRole#'] = ''

                 #------       
                 zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "role deletion", None) + " " + mGetItem.upper()
                 zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           elif mAction == "treeActionRevoquerRole" :
              mTitre = QtWidgets.QApplication.translate("bibli_asgard", "Confirmation", None)
              mLib = QtWidgets.QApplication.translate("bibli_asgard", "Are you sure you want to revoke all rights for the role ?", None)
              if not self.Dialog.displayMessage or QMessageBox.question(None, mTitre, mLib,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.Yes : 
                 mCont = True
                 mKeySql = dicListSql(self,mAction)
                 mRoleNewID, mRoleOldID = mGetItem, "#nom_role#" 
                 dicReplace = {mRoleOldID: mRoleNewID}
                 #------       
                 zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "All rights of the role ", None) + " " + mGetItem.upper()  + "\n" + QtWidgets.QApplication.translate("bibli_asgard", "on the base ", None)
                 zMessGood += " " + str(self.Dialog.dbName.upper()) + " " + QtWidgets.QApplication.translate("bibli_asgard", "database have been revoked.", None)
 
                 if not self.mRolDependances :
                    zMessGood += "\n\n" + QtWidgets.QApplication.translate("bibli_asgard", "This role still has rights on the following bases: ", None) + "\n" + str(self.treeActionDeleteRole.toolTip().upper())
                 zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)

           elif mAction == "treeActionTransfertDroitCouper" or mAction == "treeActionTransfertDroitColler" or mAction == "treeActionTransfertDroitAnnuler":
              #--- 
              if mAction == "treeActionTransfertDroitCouper" :
                 self.mDepartTransfertDroitCouper, self.mDepartmGroupeRole = mGetItem, self.mGroupeRole
                 self.ihmsDroits(mNode,0)                                                      
              #--- 
              elif mAction == "treeActionTransfertDroitColler" :
               if self.mDepartTransfertDroitCouper != mGetItem :
                 mCont = True
                 mObjetOriNew,  mObjetOriOld      = self.mDepartTransfertDroitCouper, "#nom_role#"
                 mObjetCibleNew,  mObjetCibleOld  = mGetItem, "#nom_role_cible#"
                 mKeySql = dicListSql(self,'FONCTIONReaffecteRoles')
                 dicReplace = {mObjetOriOld: mObjetOriNew, mObjetCibleOld: mObjetCibleNew}
                 #------       
                 zMessGood = QtWidgets.QApplication.translate("bibli_asgard","Transfer of rights from ", None)
                 zMessGood += str(self.mDepartTransfertDroitCouper.upper())
                 zMessGood += QtWidgets.QApplication.translate("bibli_asgard"," to ", None)
                 zMessGood += str(mGetItem.upper())
                 zMessGood += QtWidgets.QApplication.translate("bibli_asgard"," successful", None)
                 zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
                 self.ihmsDroits(mNode,0)                                                      
              #--- 
              elif mAction == "treeActionTransfertDroitAnnuler": 
                   self.mDepartTransfertDroitCouper, self.mDepartmGroupeRole = "", True
                   self.ihmsDroits(mNode,0)                                                      

           #**********************
           if mCont :
              for key, value in dicReplace.items():
                  if isinstance(value, bool) :
                     mValue = str(value)
                  elif (value is None) :
                     mValue = "''"
                  else :
                     value = value.replace("'", "''")
                     mValue =  str(value) 
                  mKeySql = mKeySql.replace(key, mValue)
              #print(mKeySql)
              #==============================
              r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSqlNoReturn(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
              if r != False :
                 bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
                 #QMessageBox.information(self, zTitre, zMess)  
              else :
                 pass 
           #==============================
        return  

        #----------------------


    #-------------                                                    
    def ihmsDroitsCurrentIndexChanged(self, itemCurrent, itemPrevious):
        self.ihmsDroits( itemCurrent, self.currentColumn() )
        return

    #**********************
    def ihmsDroits(self, item, column): 
        mItemValue = self.Dialog.mTreePostgresql.returnValueItem(item, column)
        #print("mItemValue %s " %(str(mItemValue)))
        mItemClic = item.data(column, Qt.DisplayRole)
        #print("mItemClic %s " %(str(mItemClic)))
        self.Dialog.groupBoxAffichageRightDroits.setVisible(True)
        self.Dialog.groupBoxAffichageRoleAttribut.setVisible(False)
        self.Dialog.groupBoxAffichageRoleAppart.setVisible(False)
        self.Dialog.executeDroits.setVisible(False) 
        self.Dialog.executeButtonRole.setVisible(False) 
        self.Dialog.groupBoxAffichageHelpDroits.setVisible(False)
        self.Dialog.groupBoxAffichageRightDroitsSchemas.setVisible(False)
          
        for mGetItem in mItemValue :
               iParcours = 0
               while iParcours in range(len(self.ArraymRolesDeGroupe)) :
                     if mGetItem == self.ArraymRolesDeGroupe[iParcours][0] :
                        # Désactive le bouton appliquer si G_admin_ext
                        self.Dialog.executeButtonRole.setEnabled(False if mGetItem.upper() == "G_ADMIN_EXT" else True)
                        self.Dialog.executeButtonRole.setToolTip(QtWidgets.QApplication.translate("bibli_asgard", "You do not have the right to modify 'g_admin_ext'", None) if mGetItem.upper() == "G_ADMIN_EXT"else "")
                        #-----
                        self.Dialog.groupBoxAffichageRightDroits.setVisible(True)
                        self.Dialog.groupBoxAffichageRoleAttribut.setVisible(True)
                        self.Dialog.groupBoxAffichageRoleAppart.setVisible(True)
                        self.Dialog.executeButtonRole.setVisible(True) 
                        self.Dialog.groupBoxAffichageRightDroitsSchemas.setVisible(True)

                        self.mode = "update"
                        self.mRolnameID      = self.ArraymRolesDeGroupe[iParcours][12]   # Gestion pour le Where
                        self.mRolname        = self.ArraymRolesDeGroupe[iParcours][0]
                        self.mDescription    = "" if self.ArraymRolesDeGroupe[iParcours][13] == None else self.ArraymRolesDeGroupe[iParcours][13] 
                        #self.mMdp            = self.ArraymRolesDeGroupe[iParcours][8]
                        self.mMdp = ''
                        self.mRolcreaterole  = self.ArraymRolesDeGroupe[iParcours][3]
                        self.mRolcreatedb    = self.ArraymRolesDeGroupe[iParcours][4]
                        self.mRolsuper       = self.ArraymRolesDeGroupe[iParcours][1]
                        self.mRolinherit     = self.ArraymRolesDeGroupe[iParcours][2]
                        self.mRolreplication = self.ArraymRolesDeGroupe[iParcours][6]
                        
                        self.mRolbypassrls   = self.ArraymRolesDeGroupe[iParcours][10]
                        self.mRollogin       = self.ArraymRolesDeGroupe[iParcours][5] 
                        
                        self.mRolgestionschema = True if self.ArraymRolesDeGroupe[iParcours][19] else False
                        #self.mDbCreate         = True if self.ArraymRolesDeGroupe[iParcours][19]  else False   # Attention à la confusion avec mRolcreatedb
                        self.mRolDependances = self.ArraymRolesDeGroupe[iParcours][20]
                                    
                        #---- Gestion ToolTip for "gestion schémas" 
                        mMessToolTipTexte = self.returnToolTipGestionSchemas()
                                 
                        mCondDisabled_case_rolgestionschema = (self.mRolsuper == True or self.mRolname == "g_admin")
                        if mCondDisabled_case_rolgestionschema :  #Désactive la case gestion schéma for conditions
                           self.Dialog.case_rolgestionschema.setEnabled(False)
                        else :
                           self.Dialog.case_rolgestionschema.setEnabled(True)

                        self.Dialog.label_rolgestionschema.setToolTip("{}".format('\n'.join(bibli_asgard.returnListeTexte(self, mMessToolTipTexte, 50))))           
                        self.Dialog.case_rolgestionschema.setToolTip( "{}".format('\n'.join(bibli_asgard.returnListeTexte(self, mMessToolTipTexte, 50))))
                        #----           
                        
                        if self.ArraymRolesDeGroupe[iParcours][5] != True : #ROLANLOGIN
                           self.Dialog.groupBoxAffichageRoleAppart.setTitle(self.Dialog.entete_GroupBoxAffichageRoleAppar_groupe)
                           mServeurNameOut = QtWidgets.QApplication.translate("bibli_asgard", "Non-member role :", None)
                           mServeurNameIn = QtWidgets.QApplication.translate("bibli_asgard", "Group member roles :", None)
                           self.Dialog.zone_mdp.setEnabled(False) 
                           self.Dialog.case_rolgestionschema.setVisible(True)
                           self.Dialog.label_rolgestionschema.setVisible(True)
                        else : 
                           self.Dialog.groupBoxAffichageRoleAppart.setTitle(self.Dialog.entete_GroupBoxAffichageRoleAppar_role)
                           mServeurNameOut = QtWidgets.QApplication.translate("bibli_asgard", "Does not belong to :", None)
                           mServeurNameIn = QtWidgets.QApplication.translate("bibli_asgard", "Belongs to group :", None)    
                           self.Dialog.zone_mdp.setEnabled(True)
                           self.Dialog.case_rolgestionschema.setVisible(False)
                           self.Dialog.label_rolgestionschema.setVisible(False)
                           
                        self.mRolcanLogin = self.ArraymRolesDeGroupe[iParcours][5]
                        self.Dialog.case_membreappartient.setChecked(True)
                        self.initIhmDroits(self.Dialog, self.mode, mServeurNameOut, mServeurNameIn, self.mRolnameID, self.mRolname, self.ArraymRolesDeGroupe[iParcours][5], self.mDescription, self.mMdp, self.mRolcreaterole, self.mRolcreatedb, self.mRolsuper, self.mRolinherit, self.mRolreplication, self.mRolbypassrls, self.mRollogin, self.mRolgestionschema)
                        bibli_ihm_asgard.showHideCtrlBascule_Normal_A_Bis(self.Dialog, True, mRolCanLogin = self.ArraymRolesDeGroupe[iParcours][5])
                        #Affichage si aucune valeur modifiée
                        #--Save Old value Out In
                        self.mListeOutOld, self.mListeInOld, self.mListeOutBISOld, self.mListeInBISOld =  bibli_asgard.returnOutInListe(self )
                        #--
                        tId    = ('mRolnameID', 'mRolname', 'mDescription', 'mRolcreaterole', 'mRolcreatedb', 'mRolsuper', 'mRolinherit', 'mRolreplication', 'mRolbypassrls', 'mRollogin', 'mRolgestionschema', 'mListeOut', 'mListeIn', 'mListeOutBIS', 'mListeInBIS')
                        tValue = (str(self.mRolnameID), self.mRolname, self.mDescription, self.mRolcreaterole, self.mRolcreatedb, self.mRolsuper, self.mRolinherit, self.mRolreplication, self.mRolbypassrls, self.mRollogin, self.mRolgestionschema, self.mListeOutOld, self.mListeInOld, self.mListeOutBISOld, self.mListeInBISOld)
                        self.dicOldValueRole = dict(zip(tId, tValue))
                        break
                     iParcours += 1
        return

    #------ 
    def initIhmDroits(self, Dialog, mode,  mServeurNameOut, mServeurNameIn, mRolnameID, mRolname, mRolcanLogin, mDescription, mMdp, mRolcreaterole, mRolcreatedb, mRolsuper, mRolinherit, mRolreplication, mRolbypassrls, mRollogin, mRolgestionschema) :
        Dialog.zone_rolnameID.setText(str(mRolnameID))
        Dialog.zone_rolname.setText(mRolname)
        Dialog.zone_description.setText(mDescription)
        Dialog.zone_mdp.setText(mMdp)
        Dialog.case_rolcreaterole.setChecked(mRolcreaterole)
        Dialog.case_rolcreatedb.setChecked(mRolcreatedb)
        Dialog.case_rolsuper.setChecked(mRolsuper)
        Dialog.case_rolinherit.setChecked(mRolinherit)
        Dialog.case_rolreplication.setChecked(mRolreplication) 
        Dialog.case_rolBYPASSRLS.setChecked(mRolbypassrls) 
        Dialog.case_rollogin.setChecked(mRollogin)
        Dialog.case_rolgestionschema.setChecked(mRolgestionschema)

        mHeader_A = QtWidgets.QApplication.translate("bibli_asgard", "Non-member role :", None)
        mHeader_B = QtWidgets.QApplication.translate("bibli_asgard", "Group member roles :", None)
        #-
        mHeader_C = QtWidgets.QApplication.translate("bibli_asgard", "Does not belong to :", None)
        mHeader_D = QtWidgets.QApplication.translate("bibli_asgard", "Belongs to group :", None)    
        #-
        mServeurNameOutBIS = mHeader_A if mRolcanLogin else mHeader_C
        mServeurNameInBIS  = mHeader_B if mRolcanLogin else mHeader_D
        
        # Tree Out
        Dialog.mTreePostgresqlMembresOut.clear()
        Dialog.mTreePostgresqlMembresOut.afficheDroitsOut(self.Dialog, self.myPathIcon, mServeurNameOut, mRolnameID, mRolcanLogin, self.mConfigConnection, self.ArraymlisteDesRolesDeGroupeEtConnexions)
        Dialog.mTreePostgresqlMembresOut.show()
        Dialog.mTreePostgresqlMembresOut.setGeometry(5, 5, self.Dialog.groupBoxAffichageRoleAppartOut.width() - 10, self.Dialog.groupBoxAffichageRoleAppartOut.height() - 10 )
        #-
        Dialog.mTreePostgresqlMembresOutBIS.clear()
        Dialog.mTreePostgresqlMembresOutBIS.afficheDroitsOutBIS(self.Dialog, self.myPathIcon, mServeurNameOutBIS, mRolnameID, mRolcanLogin, self.mConfigConnection, self.ArraymlisteDesRolesDeGroupeEtConnexions)
        Dialog.mTreePostgresqlMembresOutBIS.show()
        Dialog.mTreePostgresqlMembresOutBIS.setGeometry(5, 5, self.Dialog.groupBoxAffichageRoleAppartOut.width() - 10, self.Dialog.groupBoxAffichageRoleAppartOut.height() - 10 )
        # Tree In
        Dialog.mTreePostgresqlMembresIn.clear()
        Dialog.mTreePostgresqlMembresIn.afficheDroitsIn(self.Dialog, self.myPathIcon, mServeurNameIn, mRolnameID, mRolcanLogin, self.mConfigConnection, self.ArraymlisteDesRolesDeGroupeEtConnexions)
        Dialog.mTreePostgresqlMembresIn.show()
        Dialog.mTreePostgresqlMembresIn.setGeometry(5 ,5 , self.Dialog.groupBoxAffichageRoleAppartIn.width() - 10, self.Dialog.groupBoxAffichageRoleAppartIn.height() - 10 )
        #-
        Dialog.mTreePostgresqlMembresInBIS.clear()
        Dialog.mTreePostgresqlMembresInBIS.afficheDroitsInBIS(self.Dialog, self.myPathIcon, mServeurNameInBIS, mRolnameID, mRolcanLogin, self.mConfigConnection, self.ArraymlisteDesRolesDeGroupeEtConnexions)
        Dialog.mTreePostgresqlMembresInBIS.show()
        Dialog.mTreePostgresqlMembresInBIS.setGeometry(5 ,5 , self.Dialog.groupBoxAffichageRoleAppartIn.width() - 10, self.Dialog.groupBoxAffichageRoleAppartIn.height() - 10 )

        #mServeurNameIn = QtWidgets.QApplication.translate("bibli_asgard", "Belongs to group :", None)    

        # Tree Schémas
        Dialog.mTreePostgresqlSchemaLecteur.clear()
        Dialog.mTreePostgresqlSchemaEditeur.clear()
        Dialog.mTreePostgresqlSchemaProducteur.clear()
        if self.mode == "update" :
           Dialog.mTreePostgresqlSchemaLecteur.afficheSchemaLecteur(self.Dialog, self.myPathIcon, mRolnameID, self.ArraymlisteDesRolesDeGroupeEtConnexions)
           Dialog.mTreePostgresqlSchemaLecteur.show()
           Dialog.mTreePostgresqlSchemaLecteur.setGeometry(5, ((self.Dialog.groupBoxAffichageLeftDroits.height()/3) *2) + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)
           #Dialog.mTreePostgresqlSchemaLecteur.setGeometry(5, 5, self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10 , (self.Dialog.groupBoxAffichageRightDroitsSchemas.height() - 20)/3)
 
           Dialog.mTreePostgresqlSchemaEditeur.afficheSchemaEditeur(self.Dialog, self.myPathIcon, mRolnameID, self.ArraymlisteDesRolesDeGroupeEtConnexions)
           Dialog.mTreePostgresqlSchemaEditeur.show()
           Dialog.mTreePostgresqlSchemaEditeur.setGeometry(5, self.Dialog.groupBoxAffichageLeftDroits.height()/3 + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)

           Dialog.mTreePostgresqlSchemaProducteur.afficheSchemaProducteur(self.Dialog, self.myPathIcon, mRolnameID, self.ArraymlisteDesRolesDeGroupeEtConnexions)
           Dialog.mTreePostgresqlSchemaProducteur.show()
           Dialog.mTreePostgresqlSchemaProducteur.setGeometry(5, 5, self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10 , (self.Dialog.groupBoxAffichageRightDroitsSchemas.height() - 20)/3)
           #Dialog.mTreePostgresqlSchemaProducteur.setGeometry(5, ((self.Dialog.groupBoxAffichageLeftDroits.height()/3) *2) + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)

        return
        
    #---- Gestion ToolTip for "gestion schémas" 
    def returnToolTipGestionSchemas(self) :
        if self.mRolsuper or self.mRolname == "g_admin":
            mMessToolTipTexte = QtWidgets.QApplication.translate("bibli_ihm_asgard", "Le rôle g_admin et les super-utilisateurs sont toujours habilités à gérer les schémas.", None)
        elif self.mRolgestionschema:
            mMessToolTipTexte = QtWidgets.QApplication.translate("bibli_ihm_asgard", 'En désactivant cette option, vous retirez au rôle le privilège CREATE sur la base.', None)
        else:
            mMessToolTipTexte = QtWidgets.QApplication.translate("bibli_ihm_asgard", 'En activant cette option, vous conférez au rôle le privilège CREATE sur la base.', None)
        return mMessToolTipTexte
        
#========================================================
#========================================================
# Class pour le tree View exploration    
class TREEVIEWASGARD(QTreeWidget):
    customMimeType = "text/plain"

    def __init__(self, *args):
        QTreeWidget.__init__(self, *args)
        self.setColumnCount(1)
        self.setHeaderLabels(["server"])
        
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setDragEnabled(True)
        self.viewport().setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)
        self.setAcceptDrops(True)
        #---
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        #mModel = QTreeWidget.Model()

    def mimeTypes(self):
        mimetypes = QTreeWidget.mimeTypes(self)
        mimetypes.append(TREEVIEWASGARD.customMimeType)
        return mimetypes


    def startDrag(self, supportedActions):
        drag = QDrag(self)
        mimedata = self.model().mimeData(self.selectedIndexes())
        mimedata.setData(TREEVIEWASGARD.customMimeType, QByteArray())
        drag.setMimeData(mimedata)
        drag.exec_(supportedActions)

    def dragEnterEvent(self, event):    #//DEPART
        self.mDepart = [None,None]
        selectedItems = self.selectedItems()
        if len(selectedItems) < 1:
            return
        mItemWidget = selectedItems[0].text(0)
        #
        # [Interdiction des Drag&Drop si racine = Administration]
        mListDepart = self.returnValueItem(selectedItems[0], 0)
        if len(mListDepart) > 0 :
           if mListDepart[-1] == "Administration" : return 
        # [Interdiction des Drag&Drop si racine = Administration]
        #
        if event.mimeData().hasFormat('text/plain'):
           #-----------
           if schemaExiste(mItemWidget, self.mListSchemaActifs) :
              self.mDepart = [mItemWidget, "SCHEMA_ACTIF"]
              event.accept()
           #-----------
           elif schemaExiste(mItemWidget, self.mListSchemaNonActifs) :
              self.mDepart = [mItemWidget, "SCHEMA_NONACTIF"]
              event.accept()
           #----------- 
           else:
            if selectedItems[0].parent() != None : #Pas les blocs
              # si type objet dans la liste des types d'objets
              #
              # [Interdiction des Drag&Drop si racine = schémas externes à Asgard]
              if str(selectedItems[0].parent().data(0, Qt.DisplayRole)) == QtWidgets.QApplication.translate("bibli_asgard", "Schemes outside Asgard", None) : return 
              # [Interdiction des Drag&Drop si racine = schémas externes à Asgard]
              #
              for mNameObjet in self.mArraySchemasTables  :
                  mSchemaDepart = self.returnValueItem(self.currentItem(), 0)[2] if self.Dialog.arboObjet else self.returnValueItem(self.currentItem(), 0)[1] # Hyper important si noms objets identiques dans schéma diff.
                  #Meme Type
                  if (self.returnTypeObjeEtAsgard(mItemWidget)[0] == mNameObjet[2])  :
                     # et Meme Nom
                     if mItemWidget == mNameObjet[1] and mSchemaDepart == mNameObjet[0] :
                        # Nom de l'objet et type de l'objet et schéma
                        self.mDepart = [mItemWidget, self.returnTypeObjeEtAsgard(mItemWidget)[0], mSchemaDepart]
                        event.accept()
                        break 
                     else :  
                        event.ignore()
                  else:
                     event.ignore()
           #-----------
           
    def dragMoveEvent(self, event):    #//EN COURS
        index = self.indexAt(event.pos())  

        try :
          r = self.itemFromIndex(index).text(0)
          #print("%s %s VUE ou TABLE '%s'" %("EN COURS dragMoveEvent r", str(r), str(self.returnTypeObjeEtAsgard(r)[0])  ))
          #self.mListBlocs pour                    : Blocs fonctionnels y compris Corbeille
          #self.mListSchemaActifs pour             : Actifs
          #self.mListSchemaNonActifs pour          : Non Actifs
          #self.mListSchemaCorbeilleActifs pour    : Actifs corbeille
          #self.mListSchemaCorbeilleNonActifs pour : Non Actifs corbeille
          #self.mListSchemaExistants pour          : Hors Asgard
 
          if self.mDepart[1] == "SCHEMA_ACTIF" or self.mDepart[1] == "SCHEMA_NONACTIF":
             if schemaExiste(r, self.mListBlocs) :
                #Prendre le code du bloc fonctionnel Test pour ne pas déplacer un schéma qui existe déjà dans un autre bloc
                for mBloc in self.mListBlocs :
                    if r == mBloc[0] :
                       mCodeBloc = mBloc[1]
                       break
                    else :
                       mCodeBloc ="d" #ne devrait pas arriver (robu)
                mTestExisteSchema = mCodeBloc + "_" + self.mDepart[0][2:]
                
                mFindSchemaKillPrefixe = True if dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', self.mDepart[0])[0] != '' else False
                mChaine =  dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', self.mDepart[0])[1]
                mTestExisteSchema = (mCodeBloc  + "_" + mChaine) if (mCodeBloc != None and mCodeBloc != 'autre') else mChaine
                #print("mListSchemaActifs %s" %(str(self.mListSchemaActifs))) 
                #print("mListSchemaNonActifs %s" %(str(self.mListSchemaNonActifs))) 
                #print("mListSchemaExistants %s" %(str(self.mListSchemaExistants))) 
                
                if not schemaExiste(mTestExisteSchema, self.mListSchemaActifs) :
                   if not schemaExiste(mTestExisteSchema, self.mListSchemaNonActifs) :
                      if not schemaExiste(mTestExisteSchema, self.mListSchemaExistants) :
                         event.accept()
                      else :
                        event.ignore()
                        # Restaure si mTestExisteSchema(Depart) dans corbeille
                        #if returnSchemaExisteAndName(mTestExisteSchema, self.mListSchemaExistants, 'd')[0] :
                        #   event.accept()
                        #else :
                        #   event.ignore()
                   else :
                     event.ignore()
                     # Restaure si mTestExisteSchema(Depart) dans corbeille
                     #if returnSchemaExisteAndName(mTestExisteSchema, self.mListSchemaNonActifs, 'd')[0] :
                     #   event.accept()
                     #else :
                     #   event.ignore()
                else :
                   event.ignore()
                  # Restaure si mTestExisteSchema(Depart) dans corbeille
                  #print("mTestExisteSchema {}".format(str(mTestExisteSchema)))
                  #print("self.mListSchemaActifs {}".format(str(self.mListSchemaActifs)))
                  #print(returnSchemaExisteAndName(mTestExisteSchema, self.mListSchemaActifs, 'd'))
                  #if returnSchemaExisteAndName(mTestExisteSchema, self.mListSchemaActifs, 'd')[0] :
                  #   event.ignore()
                  #else :
                  #   event.accept()

                #Prendre le code du bloc fonctionnel Test pour ne pas déplacer un schéma qui existe déjà dans un autre bloc
             else :                                                            
                event.ignore()
          #-----------
          else:
             if schemaExiste(r, self.mListSchemaActifs) :
                # si type objet dans la liste des types d'objets
                for mNameObjet in self.mArraySchemasTables  :
                    # si même nom d'objet et schéma identique
                    if (self.mDepart[0] == mNameObjet[1] and r == mNameObjet[0]) :
                       event.ignore()
                       break    
                    else:
                       event.accept()
             else: # Pas schémas actifs
                event.ignore()
          #----------- 
        except :
          event.ignore()

    def dropEvent(self, event):  #//ARRIVEE
        index = self.indexAt(event.pos())
        mArrivee = self.itemFromIndex(index).text(0)
        if self.mDepart[0] != None :
           if self.mDepart[1] == "SCHEMA_ACTIF" or self.mDepart[1] == "SCHEMA_NONACTIF":
              mTitre = QtWidgets.QApplication.translate("bibli_asgard", "Confirmation", None)
              mLib = QtWidgets.QApplication.translate("bibli_asgard", "Are you sure you want to move this diagram?", None)
              #▬if QMessageBox.question(None, mTitre, mLib,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.Yes : 
              if not self.Dialog.displayMessage or QMessageBox.question(None, mTitre, mLib,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.Yes : 
                 mDicListBlocs = returnLoadBlocParam()
                 #Ajout des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings
                 mDicListBlocs = returnDicBlocUniquementNonReference(mDicListBlocs, self.mSchemasBlocs)
                 for key, value in mDicListBlocs.items() :
                     if mArrivee == value : 
                        mBlocNewTemp = key if key != 'autre' else ''
                        break
                 mBlocNew, mBlocOld = mBlocNewTemp  , "#bloc#" 
                 mSchemaNew, mSchemaOld = self.mDepart[0], "#ID_nom_schema#"
                 dicReplace = {mSchemaOld: mSchemaNew, mBlocOld: mBlocNew}
                 mKeySql = dicListSql(self,'ModificationSchemaLigneDRAGDROP')
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
                 #------ 
                 r = self.Dialog.mBaseAsGard.executeSqlNoReturnDragDrop(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
                 if r != False :
                    zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "Good, you have moved your diagram", None)
                    zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
                    bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
                    #QMessageBox.information(self, zTitre, zMess) 
                 else :
                    #Géré en amont dans la fonction executeSqlNoReturnDragDrop
                    pass 
           # si type objet dans la liste des types d'objets
           else : #(self.mDepart[1] == [mNameObjet[2] for mNameObjet in self.mArraySchemasTables][0])  :
              mSchemaOriNew, mSchemaOriOld     = self.mDepart[2], "#obj_schema#"
              mObjetOriNew,  mObjetOriOld      = self.mDepart[0], "#obj_nom#"
              mTypeNew,      mTypeOld          = self.mDepart[1], "#obj_typ#"
              mSchemaCibleNew, mSchemaCibleOld = mArrivee, "#schema_cible#"
              mVarNew, mVarOld = "1", "#variante#"
              mKeySql = dicListSql(self,'FONCTIONDeplaceObjet')
              dicReplace = {mSchemaOriOld: mSchemaOriNew, mObjetOriOld: mObjetOriNew, mTypeOld: mTypeNew, mSchemaCibleOld: mSchemaCibleNew, mVarOld: mVarNew}
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
              #------ 
              #print(mKeySql)
              r = self.Dialog.mBaseAsGard.executeSqlNoReturnDragDrop(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
              if r != False :
                 zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "Good, you have moved your objet", None)
                 zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
                 bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
                 #QMessageBox.information(self, zTitre, zMess) 
              else :
                 #Géré en amont dans la fonction executeSqlNoReturnDragDrop
                 pass 
     
    #-------------
    #-------------
    def affiche(self, Dialog, myPathIcon, mServeurName, mConfigConnection, mArraySchemas, mArraySchemasTables, mSchemasBlocs, mArrayRolesEditeursLecteurs, ArraymRolesProducteurs, filtreActif = "", listeDesArbos = None): 
        self.Dialog = Dialog 
        self.listeDesArbos = listeDesArbos
        
        iconCursorInterdit = returnIcon(myPathIcon + "\\treeview\\cursor_interdit.png")
        iconGestion = returnIcon(myPathIcon + "\\treeview\\racine.png")
        iconRole = returnIcon(myPathIcon + "\\treeview\\roles.png")
        iconSchema = returnIcon(myPathIcon + "\\objets\\schema.png")
        iconSchemaactif = returnIcon(myPathIcon + "\\objets\\schema_actif.png")
        iconSchemanonactif = returnIcon(myPathIcon + "\\objets\\schema_nonactif.png")
        iconGroupe = returnIcon(myPathIcon + "\\objets\\groupe.png")
        iconConnex = returnIcon(myPathIcon + "\\objets\\connexion.png")
        iconGraph  = returnIcon(myPathIcon + "\\objets\\dash.png")
        iconPie    = returnIcon(myPathIcon + "\\objets\\pie.png")
        iconHisto  = returnIcon(myPathIcon + "\\objets\\histo.png")
        dicIcoObjets = {
                      "table"             : returnIcon(myPathIcon + "\\objets\\table.png"),
                      "tablereplique"     : returnIcon(myPathIcon + "\\objets\\tablereplique.png"),
                      "tabledereplique"   : returnIcon(myPathIcon + "\\objets\\tabledereplique.png"),
                      "view"              : returnIcon(myPathIcon + "\\objets\\view.png"),
                      "viewreplique"      : returnIcon(myPathIcon + "\\objets\\viewreplique.png"),
                      "viewdereplique"    : returnIcon(myPathIcon + "\\objets\\viewdereplique.png"),
                      "materialized view" : returnIcon(myPathIcon + "\\objets\\mview.png"),
                      "materialized viewreplique"     : returnIcon(myPathIcon + "\\objets\\mviewreplique.png"),
                      "materialized viewdereplique"   : returnIcon(myPathIcon + "\\objets\\mviewdereplique.png"),
                      "foreign table"     : returnIcon(myPathIcon + "\\objets\\foreign_table.png"),
                      "sequence"          : returnIcon(myPathIcon + "\\objets\\sequence.png"),
                      "function"          : returnIcon(myPathIcon + "\\objets\\function.png"),
                      "type"              : returnIcon(myPathIcon + "\\objets\\type.png"),
                      "domain"            : returnIcon(myPathIcon + "\\objets\\domain.png")
                       }
        dicIcoObjetsTraduction = {
                      "table"             : "Tables",
                      "tablereplique"     : "Tables",
                      "tabledereplique"   : "Tables",
                      "view"              : "Vues",
                      "viewreplique"      : "Vues",
                      "viewdereplique"    : "Vues",
                      "materialized view" : "Vues matérialisées",
                      "materialized viewreplique"     : "Vues matérialisées",
                      "materialized viewdereplique"   : "Vues matérialisées",
                      "foreign table"     : "Tables étrangères",
                      "sequence"          : "Séquences",
                      "function"          : "Fonctions",
                      "type"              : "Types",
                      "domain"            : "Domaines"
                       }
        #For layer_styles
        self.mNameLayerStyles = "layer_styles"  # Nommage de la table layer_styles
        self.dicIcoMenuLayerStyles = {
                      "var0"             : ("Variante 0 « g_admin »",    returnIcon(myPathIcon + "\\actions\\layerstyles_var0.png"), 0),
                      "var1"             : ("Variante 1 « producteur »", returnIcon(myPathIcon + "\\actions\\layerstyles_var1.png"), 1),
                      "var2"             : ("Variante 2 « éditeur »",    returnIcon(myPathIcon + "\\actions\\layerstyles_var2.png"), 2),
                      "var3"             : ("Variante 3 « éditeur+ »",   returnIcon(myPathIcon + "\\actions\\layerstyles_var3.png"), 3),
                      "var4"             : ("Variante 4 « éditeur++ »",  returnIcon(myPathIcon + "\\actions\\layerstyles_var4.png"), 4),
                      "var5"             : ("Variante 5 « lecteur »",    returnIcon(myPathIcon + "\\actions\\layerstyles_var5.png"), 5),
                      "varRemove"        : ("Réinitialisation",          returnIcon(myPathIcon + "\\actions\\layerstyles_varRemove.png"), 6)
                       }
        #=====
        if self.Dialog.ctrlReplication : 
           self.mListeObjetArepliquer = ['table', 'view', 'materialized view']
        else :
           self.mListeObjetArepliquer = []   #Rend inactif tous les menus contextuels dédiés à la réplication
        #=====
        zMessHeaderLabels = ""
        mL = ["password", "sslmode"]
        for t in  mConfigConnection : 
            if (mL[0] not in t and mL[1] not in t) :
               zMessHeaderLabels += t + " / "
        #--
        try :
           mTempServeurName = [ str([mServeurName][0]) + " ** Extension version : " + str(Dialog.asgardInstalle) + " **" ]
        except :
           mTempServeurName = [mServeurName]
        #--
        self.setHeaderLabels(mTempServeurName)
        self.headerItem().setToolTip(0, zMessHeaderLabels[:-3])
        y = 35  # 15
        self.setGeometry(15, y, self.Dialog.groupBoxAffichageLeft.width() - 30, self.Dialog.groupBoxAffichageLeft.height() - 50)
        self.mDepartCouper = ''
        
        # FILTRE
        self.filtreActifSensitive = (True if self.Dialog.caseZoneFilter.isChecked() else False)
        if self.Dialog.ctrlReplication : 
           self.filtreActifReplique = (True if self.Dialog.caseZoneFilterRepliquer.isChecked() else False)
           self.filtreActifDereplique = (True if self.Dialog.caseZoneFilterDerepliquer.isChecked() else False)
        else :
           self.filtreActifReplique = False
           self.filtreActifDereplique = False
        #--
        #--
        #Prise en compte des deux cases à cocher pour la réplication
        if self.Dialog.ctrlReplication :
           listTemp = []
           for elem in mArraySchemasTables : 
               _addElem = False
               existeDansMetadata, repliquerMetadata, objetIcon = self.returnReplique(elem[0], elem[1], elem[2], self.Dialog.mListeMetadata, self.mListeObjetArepliquer)
               # si case cochée Répliquer ET Dérépliquer
               if self.filtreActifReplique and self.filtreActifDereplique : 
                  if existeDansMetadata : 
                     _addElem = True
                  else :
                     if elem[2] in self.mListeObjetArepliquer :  
                        _addElem = True
               # si case cochée Répliquer
               elif self.filtreActifReplique : 
                  if existeDansMetadata : 
                     if repliquerMetadata :
                        _addElem = True
               elif self.filtreActifDereplique : 
               # si case cochée Dérépliquer
                  if existeDansMetadata : 
                     if not repliquerMetadata :
                        _addElem = True
                  else :
                     if elem[2] in self.mListeObjetArepliquer :  
                        _addElem = True
               else :
                  _addElem = True
               #--
               if _addElem : listTemp.append(elem)  
           mArraySchemasTables = listTemp

           # si case cochée Répliquer OU Dérépliquer
           if self.filtreActifReplique or self.filtreActifDereplique : 
              #--
              if len(mArraySchemasTables) != 0 :
                 listTemp = []
                 for elem in mArraySchemas :
                     for elemTemp in  mArraySchemasTables :
                         if elem[0] == elemTemp[0] or elem[0].upper()=='PUBLIC' :
                            listTemp.append(elem)
                            break
                 mArraySchemas = listTemp
              else :
                 mArraySchemas = []
              #--
              if len(mArraySchemasTables) != 0 :
                 listTemp = []
                 for elem in mSchemasBlocs :
                     for elemTemp in  mArraySchemasTables :
                         if elem[0] == elemTemp[0] or elem[0].upper()=='PUBLIC':
                            listTemp.append(elem)
                            break
                 mSchemasBlocs = listTemp
              else :
                 mSchemasBlocs = []
        #--
        #--
        #Prise en compte du FILTRE
        if filtreActif != "" :
           mArraySchemasTables = ([ elem for elem in mArraySchemasTables if ((re.search(filtreActif,elem[0],flags = re.IGNORECASE) if not self.filtreActifSensitive else re.search(filtreActif,elem[0])) != None or elem[0].upper()=='PUBLIC') or (re.search(filtreActif,elem[1],flags = re.IGNORECASE) if not self.filtreActifSensitive else re.search(filtreActif,elem[1])) != None ])
           #--
           if len(mArraySchemasTables) != 0 :
              listTemp = []
              for elem in mArraySchemas :
                  for elemTemp in  mArraySchemasTables :
                      if elem[0] == elemTemp[0] :
                         listTemp.append(elem)
                         break
                      else :
                         if ((re.search(filtreActif,elem[0],flags = re.IGNORECASE) if not self.filtreActifSensitive else re.search(filtreActif,elem[0])) != None or elem[0].upper()=='PUBLIC') :
                            listTemp.append(elem)
                            break
              mArraySchemas = listTemp
           else :
              mArraySchemas = ([ elem for elem in mArraySchemas if ((re.search(filtreActif,elem[0],flags = re.IGNORECASE) if not self.filtreActifSensitive else re.search(filtreActif,elem[0])) != None or elem[0].upper()=='PUBLIC') ])
           #--
           if len(mArraySchemasTables) != 0 :
              listTemp = []
              for elem in mSchemasBlocs :
                  for elemTemp in  mArraySchemasTables :
                      if elem[0] == elemTemp[0] :
                         listTemp.append(elem)
                         break
                      else :
                         if ((re.search(filtreActif,elem[0],flags = re.IGNORECASE) if not self.filtreActifSensitive else re.search(filtreActif,elem[0])) != None or elem[0].upper()=='PUBLIC') :
                            listTemp.append(elem)
                            break
              mSchemasBlocs = listTemp
           else :
              mSchemasBlocs = ([ elem for elem in mSchemasBlocs if ((re.search(filtreActif,elem[0],flags = re.IGNORECASE) if not self.filtreActifSensitive else re.search(filtreActif,elem[0])) != None or elem[0].upper()=='PUBLIC') ])
           
        if len(mArraySchemasTables) == 0 and (len(mArraySchemas) == 0 or (len(mArraySchemas) == 1 and mArraySchemas[0][0].upper() == 'PUBLIC')) and len(mSchemasBlocs) == 0 : 
           #Affiche info si pas de filtre correspondant
           zTitle = QtWidgets.QApplication.translate("bibli_asgard", "Information !!", None)            
           zMess = QtWidgets.QApplication.translate("bibli_asgard", "Please delete or enter another filter.", None)            
           self.Dialog.barInfo.pushMessage(zTitle, zMess, Qgis.Info, duration = self.Dialog.durationBarInfo)        
           return  
        # FILTRE

        #===============================
        #Create List obj (nom, type)
        referenceObjNameTypeAsgard = []   # [nomObjet, typeObjet, Asgard(True, False)]
        # nom_schema, bloc , creation, nomenclature, producteur, editeur, lecteur, nomenclature, niv1, niv1_abr, niv2, niv2_abr
        for mValue in mSchemasBlocs :
            referenceObjNameTypeAsgard.append([str(mValue[0]), "SCHEMA", True])

        # SELECT nspname Tous les schémas de la base
        for mValue in mArraySchemas :
            if str(mValue[0]) not in [ libObjet[0] for libObjet in referenceObjNameTypeAsgard] :
               referenceObjNameTypeAsgard.append([str(mValue[0]), "SCHEMA", False])

        # NomSchéma, Nom objet , type
        for mValue in mArraySchemasTables :
            referenceObjNameTypeAsgard.append([str(mValue[1]), str(mValue[2]),True])

        #===============================
        #===============================
        #============
        #Alimentation des schemas actifs, non actifs et existants en dehors d asgard 
        mListSchemaActifs, mListSchemaNonActifs, mListSchemaExistants, mListObjetsType = [], [], [], []
        mListSchemaCorbeilleActifs, mListSchemaCorbeilleNonActifs = [], [] 
        for mSchema in mArraySchemas : #sur tous les schémas de la bdd
            mExistAsgard = False
            for mBlocs in mSchemasBlocs : 
                if mSchema[0].strip() == mBlocs[0].strip() :
                   mExistAsgard = True
            if not mExistAsgard :
               mListSchemaExistants.append(mSchema)
        #-----------
        for mBlocs in mSchemasBlocs : #sur tous les schémas de la vue gestion_schema_usr
            if mBlocs[2] :  #Actif dans asgard ?
               mListSchemaActifs.append([ mBlocs[0],"autre" if mBlocs[1] == None else mBlocs[1] ])    # If pour Cas pour gestion de "autre" 
               if mBlocs[1] == "d" :
                  mListSchemaCorbeilleActifs.append([ mBlocs[0], mBlocs[1] ])
            else :
               mListSchemaNonActifs.append([mBlocs[0],"autre" if mBlocs[1] == None else mBlocs[1] ])  # If pour Cas pour gestion de "autre"
               if mBlocs[1] == "d" :
                  mListSchemaCorbeilleNonActifs.append([ mBlocs[0], mBlocs[1] ])
                  
        self.mListSchemaActifs, self.mListSchemaNonActifs, self.mSchemasBlocs, self.mListSchemaExistants, self.mArraySchemasTables, self.referenceObjNameTypeAsgard = \
             mListSchemaActifs,      mListSchemaNonActifs,      mSchemasBlocs,      mListSchemaExistants,      mArraySchemasTables,      referenceObjNameTypeAsgard
        self.mListSchemaCorbeilleActifs, self.mListSchemaCorbeilleNonActifs = mListSchemaCorbeilleActifs, mListSchemaCorbeilleNonActifs
        self.ArraymRolesProducteurs, self.mArraySchemas = ArraymRolesProducteurs, mArraySchemas
        #============
        #===============================
        #print("Schémas actifs == %s" %(str(self.mListSchemaActifs)))
        #print("Schémas NON actifs == %s" %(str(self.mListSchemaNonActifs)))
        #print("Schémas Existants == %s" %(str(self.mListSchemaExistants)))
        #============ 
        #Retoune la liste des blocs objets non vides
        #============
        #Affiche Schémas Hors Asgard 
        self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ QtWidgets.QApplication.translate("bibli_asgard", "Schemes outside Asgard", None) ] ) ] )
        root = self.topLevelItem( 0 )
        root.setIcon(0, iconGestion)
        mListHorsAsgard, mListHorsAsgardsIcons = mListSchemaExistants , iconSchema
        root.setToolTip(0, "{}".format(",".join(mListHorsAsgard[0])))
        iListHorsAsgard = 0
        while iListHorsAsgard in range(len(mListHorsAsgard)) :
            mRootHorsAsgard, mRootHorsAsgardIcons = mListHorsAsgard[iListHorsAsgard], mListHorsAsgardsIcons 
            nodeHorsAsgard = QTreeWidgetItem(None, [ mRootHorsAsgard[0] ] )
            nodeHorsAsgard.setIcon(0, mListHorsAsgardsIcons)
            root.addChild( nodeHorsAsgard )
            #Affiche Tables dans Public si layer_styles existe
            if self.Dialog.mLayerStyles[0][0]  and mListHorsAsgard[iListHorsAsgard][0].lower() == "public" :
               mRootTable, mRootTableIcon = self.mNameLayerStyles, dicIcoObjets["tabledereplique"]
               nodeTable = QTreeWidgetItem(None, [mRootTable] )
               nodeTable.setIcon(0, mRootTableIcon)
               nodeHorsAsgard.addChild( nodeTable )                                                 
            iListHorsAsgard += 1                 

        #============
        #Affiche Blocs fonctionnels 
        dicListBlocs = returnLoadBlocParam()
        #Ajout des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings
        dicListBlocs = returnDicBlocUniquementNonReference(dicListBlocs, mSchemasBlocs)
        self.dicListBlocs = dicListBlocs

        mListBlocs, mListBlocsLibelle, mListBlocsIcons = [], [], []
        #Reverse List for Dict
        mKeysReverse = [key for key in dicListBlocs.keys()]
        mKeysReverse.reverse()
        #Reverse List for Dict
        
        for mCount in range(len(mKeysReverse)) :
            mKey   = mKeysReverse[mCount] 
            mValue = dicListBlocs[mKey] 
            mListBlocs.append([ mValue, mKey ])
            mListBlocsLibelle.append(mValue)
            mListBlocsIcons.append(returnIcon(myPathIcon + "\\treeview\\" + str(mKey) + ".png"))

        #Ajout des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings
        mListBlocs, mListBlocsLibelle, mListBlocsIcons =  returnDicBlocLibelleIconNonReference(mListBlocs, mListBlocsLibelle, mListBlocsIcons, self.mSchemasBlocs, myPathIcon)
        self.mListBlocs, self.mListBlocsLibelle, self.mListBlocsIcons = mListBlocs, mListBlocsLibelle, mListBlocsIcons 
        #============
        #------------ 
        #Affiche les blocs fonctionnels
        i = 0
        while i in range(len(mListBlocs)) :
            mRootBlocs, labelToolTip = mListBlocs[i][0], []
            self.insertTopLevelItems( 0, [ QTreeWidgetItem(None, [ mRootBlocs ] ) ] )
            nodeBlocs = self.topLevelItem( 0 )
            nodeBlocs.setIcon(0, mListBlocsIcons[i])
            #============
            #Affiche Schémas actifs        
            mListSchemaActifs, mListSchemaActifsIcons = mListSchemaActifs , iconSchemaactif
            iListSchemaActifs = 0
            mDicArboObjet_TypeQTreeWidgetItem = {} #Dictionnaire type objet = QTreeWidgetItem en cours au fur et à mesure si il existe
            
            while iListSchemaActifs in range(len(mListSchemaActifs)) :
                mSchemaActif, mListSchemaActifsIcons = mListSchemaActifs[iListSchemaActifs], mListSchemaActifsIcons
                if (mListBlocs[i][1] == mSchemaActif[1]) :
                   nodeSchemaActif = QTreeWidgetItem(None, [ mSchemaActif[0] ])
                   nodeSchemaActif.setIcon(0, mListSchemaActifsIcons)
                   nodeBlocs.addChild( nodeSchemaActif )
                   labelToolTip.append(mSchemaActif[0])

                   #Affiche Tables       
                   # Si arborescence des objets
                   ## print(self.mArraySchemasTables)
                   if self.Dialog.arboObjet :                   
                      for mRootTable in self.mArraySchemasTables :
                          if mSchemaActif[0] == mRootTable[0] :
                             #Replication iconographie
                             existeDansMetadata, repliquerMetadata, objetIcon = self.returnReplique(mSchemaActif[0], mRootTable[1], mRootTable[2], self.Dialog.mListeMetadata, self.mListeObjetArepliquer)
                             #-
                             if objetIcon[-10:] == "dereplique" :
                                objetNoeud = objetIcon[0:-10]
                             elif objetIcon[-8:] == "replique" :
                                objetNoeud = objetIcon[0:-8]
                             else :
                                objetNoeud = objetIcon

                             if (str(mRootBlocs) + "_" + str(mSchemaActif[0]) + "_" + str(objetNoeud)) not in mDicArboObjet_TypeQTreeWidgetItem : #Création de l'arbre si il n'existe pas
                                nodeArbo = QTreeWidgetItem(None, [ dicIcoObjetsTraduction[objetNoeud] ] )
                                mDicArboObjet_TypeQTreeWidgetItem[ str(mRootBlocs) + "_" + str(mSchemaActif[0]) + "_" + str(objetNoeud) ] = nodeArbo
                                #"""
                                #si regroupement, prendre l'icone par defaut
                                if existeDansMetadata : 
                                   if repliquerMetadata :
                                      objetIconNoeud = objetIcon[0:-8] if objetIcon[-8:] == "replique" else objetIcon
                                      nodeArbo.setIcon(0, dicIcoObjets[objetIconNoeud ])
                                   else :
                                      nodeArbo.setIcon(0, dicIcoObjets[objetIcon ])
                                else :
                                   nodeArbo.setIcon(0, dicIcoObjets[objetIcon ])
                                #"""
                                nodeSchemaActif.addChild( nodeArbo )
                             #--
                             nodeTable = QTreeWidgetItem(None, [mRootTable[1]] )
                             nodeTable.setIcon(0, dicIcoObjets[objetIcon ])
                             #--
                             mDicArboObjet_TypeQTreeWidgetItem[(str(mRootBlocs) + "_" + str(mSchemaActif[0]) + "_" + str(objetNoeud))].addChild( nodeTable )
                   else :                   
                      for mRootTable in self.mArraySchemasTables :
                          if mSchemaActif[0] == mRootTable[0] :
                             nodeTable = QTreeWidgetItem(None, [mRootTable[1]] )
                             #--
                             #Replication iconographie
                             existeDansMetadata, repliquerMetadata, objetIcon = self.returnReplique(mSchemaActif[0], mRootTable[1], mRootTable[2], self.Dialog.mListeMetadata, self.mListeObjetArepliquer)
                             nodeTable.setIcon(0, dicIcoObjets[objetIcon ])
                             #--
                             nodeSchemaActif.addChild( nodeTable )


                iListSchemaActifs += 1
            nodeBlocs.setToolTip(0, "{}".format(",".join(labelToolTip)))    #pour chaque bloc
            #============
            #Affiche Schémas non actifs
            nodeSchemaNoActivegroup = QTreeWidgetItem(None,[ QtWidgets.QApplication.translate("bibli_asgard", "No Active Schemas", None) ])
            nodeSchemaNoActivegroup.setIcon(0, iconSchemanonactif)
            firstNodeSchemaNoActivegroup =True
            #------------  
            mListSchemaNonActifs, mListSchemaNonActifsIcons = mListSchemaNonActifs , iconSchemanonactif
            iListSchemaNonActifs = 0
            while iListSchemaNonActifs in range(len(mListSchemaNonActifs)) :
                mSchemaNonActif, mListSchemaNonActifsIcons = mListSchemaNonActifs[iListSchemaNonActifs], mListSchemaNonActifsIcons
                if (mListBlocs[i][1] == mSchemaNonActif[1]) :
                   #--Gestion de l'affichage si le groupe est vide
                   if firstNodeSchemaNoActivegroup :
                      nodeBlocs.addChild( nodeSchemaNoActivegroup )
                      firstNodeSchemaNoActivegroup = False
                   #--Gestion de l'affichage si le groupe est vide
                   nodeSchemaNonActif = QTreeWidgetItem(None, [ mSchemaNonActif[0] ])
                   nodeSchemaNonActif.setIcon(0, mListSchemaNonActifsIcons)
                   nodeSchemaNoActivegroup.addChild( nodeSchemaNonActif )
                   #Affiche Tables       
                   for mRootTable in self.mArraySchemasTables :
                       if mSchemaNonActif[0] == mRootTable[0] :
                          nodeTable = QTreeWidgetItem(None, [mRootTable[1]] )
                          if mRootTable[2] in dicIcoObjets : nodeTable.setIcon(0, dicIcoObjets[mRootTable[2]])
                          nodeSchemaNonActif.addChild( nodeTable )
                iListSchemaNonActifs += 1
            i += 1
        #===================   
        self.itemDoubleClicked.connect( self.processItem )                        
        self.itemClicked.connect( self.ihms )                                                      
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuContextuelAsgard)
        self.currentItemChanged.connect( self.ihmsCurrentIndexChanged )                                                      

    #-------------                                                    
    def menuContextuelAsgard(self, point):
        index = self.indexAt(point)
        if not index.isValid():
           return
        item = self.itemAt(point)
        self.item = item
        mNameEnCours = item.text(0) 
        self.mNameEnCours = mNameEnCours
        self.Dialog.groupBoxAffichageSchema.setVisible(False)
        self.Dialog.groupBoxAffichageHelp.setVisible(True)
       
        #Blocs fonctionnels y compris Corbeille
        if mNameEnCours in [ libZoneActive[0] for libZoneActive in self.mListBlocs] : 
           if mNameEnCours != "Corbeille" :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [1])
              self.treeMenuSchema_new  = QMenu(self)
              #-------   
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\schema_new.png")          
              self.treeActionSchema_new = QAction(QIcon(menuIcon), "Nouveau schéma", self.treeMenuSchema_new)
              self.treeMenuSchema_new.addAction(self.treeActionSchema_new)
              self.treeActionSchema_new.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionSchema_new"))
              #-------
              self.treeMenuSchema_new.exec_(self.mapToGlobal(point))
           else :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [6])
              self.treeMenu = QMenu(self)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\corbeillevide.png")           
              self.treeActionCorbeillevide = QAction(QIcon(menuIcon), "Vider la corbeille", self.treeMenu)
              self.treeMenu.addAction(self.treeActionCorbeillevide)
              self.treeActionCorbeillevide.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionCorbeillevide"))
              #-------
              self.treeMenu.exec_(self.mapToGlobal(point))

        #Actifs
        elif mNameEnCours in [ libZoneActive[0] for libZoneActive in self.mListSchemaActifs] : 
           if mNameEnCours not in [ libZoneActive[0] for libZoneActive in self.mListSchemaCorbeilleActifs] : 
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [2,3,10,15,12,13])
              self.treeMenu = QMenu(self)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\corbeille.png")           
              self.treeActionCorbeille = QAction(QIcon(menuIcon), "Mettre à la corbeille", self.treeMenu)
              self.treeMenu.addAction(self.treeActionCorbeille)
              self.treeActionCorbeille.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionCorbeille"))
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\dereferencer.png")           
              self.treeActionDereferencer = QAction(QIcon(menuIcon), "Déréférencer", self.treeMenu)
              self.treeMenu.addAction(self.treeActionDereferencer)
              self.treeActionDereferencer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDereferencer"))
              #-------
              self.treeMenu.addSeparator()
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reinitialise_droits.png")           
              self.treeActionReinitDroits = QAction(QIcon(menuIcon), "Réinitialiser les droits", self.treeMenu)
              self.treeMenu.addAction(self.treeActionReinitDroits)
              self.treeActionReinitDroits.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionReinitialisedroit"))
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\diagnostic.png")           
              self.treeActionDiagnostic = QAction(QIcon(menuIcon), "Rechercher les anomalies", self.treeMenu)
              self.treeMenu.addAction(self.treeActionDiagnostic)   
              self.treeActionDiagnostic.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDiagnostic"))
              #-------
              self.treeMenu.addSeparator()
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\deplace_arrivee.png")           
              self.treeActionDeplaceColler = QAction(QIcon(menuIcon), "Déplacer / Coller", self.treeMenu)
              self.treeMenu.addAction(self.treeActionDeplaceColler)
              self.treeActionDeplaceColler.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDeplaceColler"))
              #-------
              #self.treeMenu.addSeparator()
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\deplace_annule.png")           
              self.treeActionDeplaceAnnuler = QAction(QIcon(menuIcon), "Annuler le \"Déplacer / Couper\"", self.treeMenu)
              self.treeMenu.addAction(self.treeActionDeplaceAnnuler)
              self.treeActionDeplaceAnnuler.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDeplaceAnnuler"))
              #-------
              self.fonctionAfficheDeplaceAll(mNameEnCours)
              self.treeMenu.exec_(self.mapToGlobal(point))
           else :
              #Corbeille Actifs
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [7,8,12,13])
              self.treeMenu = QMenu(self)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\restaurer.png")           
              self.treeActionRestaurer = QAction(QIcon(menuIcon), "Restaurer", self.treeMenu)
              self.treeMenu.addAction(self.treeActionRestaurer)
              self.treeActionRestaurer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionRestaurer"))
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\supprimer_base.png")           
              self.treeActionSupprimer_base = QAction(QIcon(menuIcon), "Supprimer de la base de donnée", self.treeMenu)
              self.treeMenu.addAction(self.treeActionSupprimer_base)
              self.treeActionSupprimer_base.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionSupprimer_base"))
              #-------
              self.treeMenu.addSeparator()
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\deplace_arrivee.png")           
              self.treeActionDeplaceColler = QAction(QIcon(menuIcon), "Déplacer / Coller", self.treeMenu)
              self.treeMenu.addAction(self.treeActionDeplaceColler)
              self.treeActionDeplaceColler.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDeplaceColler"))
              #-------
              #self.treeMenu.addSeparator()
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\deplace_annule.png")           
              self.treeActionDeplaceAnnuler = QAction(QIcon(menuIcon), "Annuler le \"Déplacer / Couper\"", self.treeMenu)
              self.treeMenu.addAction(self.treeActionDeplaceAnnuler)
              self.treeActionDeplaceAnnuler.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDeplaceAnnuler"))
              #-------
              self.fonctionAfficheDeplaceAll("")
              self.treeMenu.exec_(self.mapToGlobal(point))           
           
        #Non Actifs
        elif mNameEnCours in [ libZoneActive[0] for libZoneActive in self.mListSchemaNonActifs] : 
           if mNameEnCours not in [ libZoneActive[0] for libZoneActive in self.mListSchemaCorbeilleNonActifs] : 
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [4,5])
              self.treeMenu = QMenu(self)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\schema_efface.png")           
              self.treeActionSchema_efface = QAction(QIcon(menuIcon), "Effacer", self.treeMenu)
              self.treeMenu.addAction(self.treeActionSchema_efface)
              self.treeActionSchema_efface.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionSchema_efface"))
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\schema_creer_base.png")           
              self.treeActionSchema_creer_base = QAction(QIcon(menuIcon), "Créer dans la base (rendre actif)", self.treeMenu)
              self.treeMenu.addAction(self.treeActionSchema_creer_base)
              self.treeActionSchema_creer_base.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionSchema_creer_base"))
              #-------
              self.treeMenu.exec_(self.mapToGlobal(point))
           else :
              #Corbeille Non Actifs
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [7,4])
              self.treeMenu = QMenu(self)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\restaurer.png")           
              self.treeActionRestaurer = QAction(QIcon(menuIcon), "Restaurer", self.treeMenu)
              self.treeMenu.addAction(self.treeActionRestaurer)
              self.treeActionRestaurer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionRestaurer"))
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\schema_efface.png")           
              self.treeActionSchema_efface = QAction(QIcon(menuIcon), "Effacer", self.treeMenu)
              self.treeMenu.addAction(self.treeActionSchema_efface)
              self.treeActionSchema_efface.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionSchema_efface"))
              #-------
              self.treeMenu.exec_(self.mapToGlobal(point))           
           
        #Existant (Hors asgard)
        elif mNameEnCours in [ libZoneActive[0] for libZoneActive in self.mListSchemaExistants] :
           if mNameEnCours == "public" :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [0])
           else : 
              """
              Suite à Redmine SPS 106411
              """
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [9, 16, 14])
              #bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [9,12,13])
              self.treeMenu = QMenu(self)
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\referencer.png")           
              self.treeActionReferencer = QAction(QIcon(menuIcon), "Référencer et réinitialiser les droits", self.treeMenu)
              self.treeMenu.addAction(self.treeActionReferencer)
              self.treeActionReferencer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionReferencer"))
              #-------
              menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\referencerconservedroits.png")           
              self.treeActionReferencerConserveDroits = QAction(QIcon(menuIcon), "Référencer en conservant les droits", self.treeMenu)
              self.treeMenu.addAction(self.treeActionReferencerConserveDroits)
              self.treeActionReferencerConserveDroits.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionReferencerConserveDroits"))
              #-------
              self.treeMenu.addSeparator()
              #-------
              #-------
              mTitreSousMenu = QtWidgets.QApplication.translate("bibli_asgard", "Refer to ...", None)
              self.treeSousMenu = QMenu(mTitreSousMenu)
              #Affiche les blocs fonctionnels
              #Reverse List for Dict
              mListBlocsReverse, mListBlocsLibelleReverse, mListBlocsIconsReverse = self.mListBlocs[::-1], self.mListBlocsLibelle[::-1], self.mListBlocsIcons[::-1]
              self.mListBlocsReverse= mListBlocsReverse
           
              listBlocsExclure = self.fonctionAfficheVersBloc(mNameEnCours)
              i = 0
              while i in range(len(mListBlocsReverse)-1) :
                 if mListBlocsReverse[i][1] != "d" and mListBlocsReverse[i][1] != "autre" : #J'enlève corbeille et Autre
                    menuIcon = mListBlocsIconsReverse[i]         
                    treeActionReferencerSousMenu = QAction(QIcon(menuIcon), mListBlocsLibelleReverse[i], self.treeSousMenu)
                    treeActionReferencerSousMenu.setObjectName(mListBlocsReverse[i][1])  
                    self.treeSousMenu.addAction(treeActionReferencerSousMenu)
                    treeActionReferencerSousMenu.triggered.connect(lambda : self.actionFonctionTreeVersBloc(item, "treeActionReferencerVersBloc", mListBlocsReverse[i][1]))
                    if mListBlocsReverse[i][1] in listBlocsExclure:
                       treeActionReferencerSousMenu.setEnabled(False)
                 i += 1
              self.treeMenu.addMenu(self.treeSousMenu)
              self.treeMenu.exec_(self.mapToGlobal(point))
        #Tous les objets d'un schéma
        elif mNameEnCours in [ mNameObjet[1] for mNameObjet in self.mArraySchemasTables] : 
             # si type objet dans la liste des types d'objets
             for mNameObjet in self.mArraySchemasTables  :
                 # et Meme Nom
                 if mNameEnCours == mNameObjet[1] :
                    #-------
                    #bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13])
                    self.treeMenu = QMenu(self)
                    menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\reinitialise_droits.png")           
                    self.treeActionReinitDroitsObjets = QAction(QIcon(menuIcon), "Réinitialiser les droits", self.treeMenu)
                    self.treeMenu.addAction(self.treeActionReinitDroitsObjets)
                    self.treeActionReinitDroitsObjets.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionReinitDroitsObjets"))
                    #-------
                    self.treeMenu.addSeparator()
                    #-------
                    menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\deplace_depart.png")           
                    self.treeActionDeplaceCouper = QAction(QIcon(menuIcon), "Déplacer / Couper", self.treeMenu)
                    self.treeMenu.addAction(self.treeActionDeplaceCouper)
                    self.treeActionDeplaceCouper.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDeplaceCouper"))
                    #-------
                    menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\deplace_annule.png")           
                    self.treeActionDeplaceAnnuler = QAction(QIcon(menuIcon), "Annuler le \"Déplacer / Couper\"", self.treeMenu)
                    self.treeMenu.addAction(self.treeActionDeplaceAnnuler)
                    self.treeActionDeplaceAnnuler.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDeplaceAnnuler"))
                    #-------
                    self.treeMenu.addSeparator()
                    #-------
                    #-------
                    mReturnValueItemTemp = self.returnValueItem(item, 0)
                   # Si arborescence des objets
                    mSchemaClic = mReturnValueItemTemp[2] if self.Dialog.arboObjet else mReturnValueItemTemp[1]
                    mObjetClic  = mReturnValueItemTemp[0]
                    #----
                    for mNameObjet in self.mArraySchemasTables  :
                       # et Meme Nom
                       if mObjetClic == mNameObjet[1] and mSchemaClic == mNameObjet[0] :
                          # Nom objet, type objet et schema de l'objet
                          self.mReturnValueItemTemp = [mNameObjet[1], mNameObjet[2], mNameObjet[0]]
                          break
                    #----
                    if self.mReturnValueItemTemp[1] in self.mListeObjetArepliquer : #si les obkets sont Table, vue et vue mat
                       existeDansMetadata, repliquerMetadata, objetIcon = self.returnReplique(self.mReturnValueItemTemp[2],self.mReturnValueItemTemp[0], self.mReturnValueItemTemp[1], self.Dialog.mListeMetadata, self.mListeObjetArepliquer)
                       if existeDansMetadata : 
                          if repliquerMetadata :
                             bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13, 19])
                             menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\derepliquer.png")           
                             self.treeActionDerepliquer = QAction(QIcon(menuIcon), "Dérépliquer", self.treeMenu)
                             self.treeMenu.addAction(self.treeActionDerepliquer)
                             self.treeActionDerepliquer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionDerepliquer"))
                          else :
                             bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13, 18])
                             menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\repliquer.png")           
                             self.treeActionRepliquer = QAction(QIcon(menuIcon), "Répliquer", self.treeMenu)
                             self.treeMenu.addAction(self.treeActionRepliquer)
                             self.treeActionRepliquer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionRepliquer"))
                       else :
                          bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13, 18])
                          menuIcon = returnIcon(self.Dialog.myPathIcon + "\\actions\\repliquer.png")           
                          self.treeActionRepliquer = QAction(QIcon(menuIcon), "Répliquer", self.treeMenu)
                          self.treeMenu.addAction(self.treeActionRepliquer)
                          self.treeActionRepliquer.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionRepliquer"))
                    else :
                       bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13])
                        
                    #-------
                    #-------
                    self.fonctionAfficheDeplaceAll("")
                    self.treeMenu.exec_(self.mapToGlobal(point))
                    break 
        # ** For layer_styles **
        elif mNameEnCours == self.mNameLayerStyles :
             zMessToolTip = QtWidgets.QApplication.translate("bibli_asgard", "You must be both a member of g_admin and the owner of the layer_styles table to manage permissions on it.", None)
             bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [200, 20, 21, 22, 23, 24, 25, 26])
             self.treeMenu = QMenu(self)
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["var0"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["var0"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "var0"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["var1"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["var1"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "var1"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["var2"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["var2"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "var2"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["var3"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["var3"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "var3"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["var4"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["var4"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "var4"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["var5"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["var5"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "var5"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             self.treeMenu.addSeparator()
             #-------
             menuIcon = self.dicIcoMenuLayerStyles["varRemove"][1]           
             self.treeActionLayerStyles = QAction(QIcon(menuIcon), self.dicIcoMenuLayerStyles["varRemove"][0], self.treeMenu)
             self.treeMenu.addAction(self.treeActionLayerStyles)
             self.treeActionLayerStyles.triggered.connect(lambda : self.actionFonctionTree(item, "treeActionLayerStyles", "varRemove"))
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setEnabled(False)
             if not self.Dialog.mLayerStyles[0][1] : self.treeActionLayerStyles.setToolTip(zMessToolTip)
             #-------
             if not self.Dialog.mLayerStyles[0][1] : self.treeMenu.setToolTipsVisible(True)
             self.treeMenu.exec_(self.mapToGlobal(point))
             #-------
        else : 
          bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [0])
          pass

        return

    #**********************
    #**********************
    def fonctionAfficheVersBloc(self, mGetItem):
        #------
        mFindSchemaKillPrefixe = True if dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem) != '' else False
        mChaine =  dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem)[1] 
        mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem)[0]
        """
        print("self.mListBlocs  %s" %(str(self.mListBlocs)))
        print("mChaine  %s" %(str(mChaine)))
        print("mPrefixe  %s" %(str(mPrefixe)))
        print("self.mListSchemaActifs  %s" %(str(self.mListSchemaActifs)))
        print("self.mListSchemaNonActifs  %s" %(str(self.mListSchemaNonActifs)))
        print("self.mListSchemaCorbeilleActifs  %s" %(str(self.mListSchemaCorbeilleActifs)))
        print("self.mListSchemaCorbeilleNonActifs  %s" %(str(self.mListSchemaCorbeilleNonActifs)))
        """
        listBlocsExclure = []
        for mBloc in self.mListBlocs :
            mCodeBloc = mBloc[1]
            if mCodeBloc != "d" :
               mTestExisteSchema = (mCodeBloc  + "_" + mChaine) if (mCodeBloc != None and mCodeBloc != 'autre') else mChaine
               #-----------
               if not schemaExiste(mTestExisteSchema, self.mListSchemaActifs) :
                  if not schemaExiste(mTestExisteSchema, self.mListSchemaNonActifs) :
                     pass
                  else :
                     listBlocsExclure.append(mCodeBloc)
               else :
                  listBlocsExclure.append(mCodeBloc)
               #-----------
               if not schemaExiste(mTestExisteSchema, self.mListSchemaCorbeilleActifs) :
                  if not schemaExiste(mTestExisteSchema, self.mListSchemaCorbeilleNonActifs) :
                     pass
                  else :
                     listBlocsExclure.append(mCodeBloc)
               else :
                  listBlocsExclure.append(mCodeBloc)
        return listBlocsExclure      

    #**********************
    #**********************
    def fonctionAfficheDeplaceAll(self, mGetItem):
        #------
        if hasattr(self,'treeActionDeplaceColler')     : self.treeActionDeplaceColler.setEnabled(False)
        if hasattr(self,'treeActionDeplaceAnnuler')    : self.treeActionDeplaceAnnuler.setEnabled(False)
        #------
        if self.mDepartCouper != "" :
           if hasattr(self,'treeActionDeplaceAnnuler') : self.treeActionDeplaceAnnuler.setEnabled(True)
           if self.mDepartCouper[2] != mGetItem :
              # si type objet dans la liste des types d'objets
              if hasattr(self,'treeActionDeplaceColler')  : self.treeActionDeplaceColler.setEnabled(True)
              for mNameObjet in self.mArraySchemasTables  :
                  # si même nom d'objet et schéma diff
                  if (self.mDepartCouper[0] == mNameObjet[1] and mGetItem == mNameObjet[0]) :
                     if hasattr(self,'treeActionDeplaceColler')  : self.treeActionDeplaceColler.setEnabled(False)
                     break 
        #------
        # ToolTip
        if hasattr(self,'treeMenu') :
           self.treeMenu.setToolTipsVisible(True) 
           mToolTip = ("Nom : " + str(self.mDepartCouper[0]) + " = Type : " + str(self.mDepartCouper[1])) if self.mDepartCouper != "" else ""
           if hasattr(self,'treeActionDeplaceCouper')     : self.treeActionDeplaceCouper.setToolTip(mToolTip)
           if hasattr(self,'treeActionDeplaceColler')     : self.treeActionDeplaceColler.setToolTip(mToolTip)

        return        
 
    #**********************
    #********************** Pour le référencement des shcémas externes vers un bloc spécifique
    def actionFonctionTreeVersBloc(self,mNode, mAction, mItem):
        self.Dialog.groupBoxAffichageSchema.setVisible(False)
        self.Dialog.groupBoxAffichageHelp.setVisible(True)
        mGetItem = mNode.text(0)
        mItemClic = self.sender().text()
        #Prendre le code du bloc fonctionnel Test pour ne pas déplacer un schéma qui existe déjà dans un autre bloc
        for mBloc in self.mListBlocs :
            if mItemClic == mBloc[0] and mBloc[1] != "autre" :
               mCodeBloc = mBloc[1]
               break
            else :
               mCodeBloc ="" #ne devrait pas arriver (robu)
               
        #print("mGetItem  %s" %(str(mGetItem)))
        #print("mItemClic  %s" %(str(mItemClic)))
        #print("code bloc  %s" %(str(mCodeBloc)))
        #----------------------
        if mAction == "treeActionReferencerVersBloc" : 
           mKeySql = dicListSql(self,"FONCTIONasgard_initialise_schema")
           mFindSchemaKillPrefixe = True if dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem) != '' else False
           mChaine =  dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem)[1] 
           mPrefixe = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem)[0]
           mSchemaNewID, mSchemaOldID = mGetItem, "#nom_schema#" 
           dicReplace = {mSchemaOldID: mSchemaNewID}
           #------       
           zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just referenced your diagram !!", None) + " " + mGetItem.upper() + " ==> " + str(mItemClic)
           zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)

           #**********************
           for key, value in dicReplace.items():
               if isinstance(value, bool) :
                  mValue = str(value)
               elif (value is None) :
                  mValue = "''"
               else :
                  value = value.replace("'", "''")
                  mValue = "'" + str(value) + "'"
               mKeySql = mKeySql.replace(key, mValue)
           mKeySqlFirst = mKeySql
           #==============================
           mBlocNew, mBlocOld = mCodeBloc  , "#bloc#" 
           mSchemaNew, mSchemaOld = mGetItem, "#ID_nom_schema#"
           dicReplace = {mSchemaOld: mSchemaNew, mBlocOld: mBlocNew}
           mKeySql = dicListSql(self,'ModificationSchemaLigneDRAGDROP')
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
           mKeySqlSecond = mKeySql
           #------ Concatene les deux instructions
           mKeySql  = mKeySqlFirst + ";" + mKeySqlSecond
           r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSqlNoReturn(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
           if r != False :
              bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
              #QMessageBox.information(self, zTitre, zMess) 
           else :
              #Géré en amont dans la fonction executeSqlNoReturnDragDrop
              pass 

        else :
           pass 
        return 
         
    #**********************
    #**********************
    def actionFonctionTree(self,mNode, mAction, mOption = ""):
        self.Dialog.groupBoxAffichageSchema.setVisible(False)
        self.Dialog.groupBoxAffichageHelp.setVisible(True)
        mGetItem = mNode.text(0)
        
        #**********************
        if mAction == "treeActionSchema_new" :
           iParcours = 0
           while iParcours in range(len(self.mListBlocs)) :
                 if mGetItem == self.mListBlocs[iParcours][0] :
                    self.Dialog.groupBoxAffichageSchema.setVisible(True)
                    self.Dialog.groupBoxAffichageHelp.setVisible(False)
                    self.mode = "create"
                    self.mSchemaID = "nouveau_schema" #ne sert que pour ne pas bloquer le dicreplace
                    self.mSchema = "nouveau_schema"
                    mBlocTemp = self.mListBlocs[iParcours][1] if self.mListBlocs[iParcours][1] != None else "autre"
                    self.mBloc   = "(" + str(mBlocTemp) + ") " + str(self.dicListBlocs[mBlocTemp])          
                    self.mActif  = False
                    self.mProd   = ""
                    self.mEdit   = "Aucun"
                    self.mLect   = "Aucun"
                    self.mNomenclature  = False
                    self.mNiv1          = ""
                    self.mNiv1_abr      = ""
                    self.mNiv2          = ""
                    self.mNiv2_abr      = ""
                    self.initIhmSchema(self.Dialog, self.mode, self.mSchema, self.mBloc, self.mActif, self.mProd, self.mEdit, self.mLect, self.mNomenclature, self.mNiv1, self.mNiv1_abr, self.mNiv2, self.mNiv2_abr, self.listeDesArbos)
                    break
                 iParcours += 1
        #----------------------
        elif mAction == "treeActionCorbeillevide" : 
           mTitre = QtWidgets.QApplication.translate("bibli_asgard", "Confirmation", None)
           mLib = QtWidgets.QApplication.translate("bibli_asgard", "Are you sure you want to empty your recycle bin ?", None)
           if not self.Dialog.displayMessage or QMessageBox.question(None, mTitre, mLib,QMessageBox.Yes|QMessageBox.No) ==  QMessageBox.Yes : 
             mKeySqlUn = dicListSql(self,"treeActionCorbeillevide_Un")
             mcreationNew, mcreationOld = False, "#creation#"
             mBlocNew, mBlocOld         = 'd', "#bloc#" 
             dicReplaceUn = {mcreationOld: mcreationNew, mBlocOld: mBlocNew}
             #------       
             mKeySqlDeux = dicListSql(self,"treeActionCorbeillevide_Deux")
             mBlocNew, mBlocOld         = 'd', "#bloc#" 
             dicReplaceDeux = {mBlocOld: mBlocNew}
             #**********************
             for key, value in dicReplaceUn.items():
                 if isinstance(value, bool) :
                    mValue = str(value)
                 elif (value is None) :
                    mValue = "''"
                 else :
                    mValue = "'" + str(value) + "'"
                 mKeySqlUn = mKeySqlUn.replace(key, mValue)
             #------ 
             for key, value in dicReplaceDeux.items():
                 if isinstance(value, bool) :
                    mValue = str(value)
                 elif (value is None) :
                    mValue = "''"
                 else :
                    mValue = "'" + str(value) + "'"
                 mKeySqlDeux = mKeySqlDeux.replace(key, mValue)
             #==============================
             r1, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSqlNoReturn(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySqlUn)
             if r1 != False :
                r2, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSqlNoReturn(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySqlDeux)
                if r2 != False :
                   zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just emptied your trash !!", None)
                   zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
                   bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
                   #QMessageBox.information(self, zTitre, zMess) 
                else :
                   #Géré en amont dans la fonction executeSqlNoReturn
                   pass
             else :
                #Géré en amont dans la fonction executeSqlNoReturn
                pass
             #==============================                                          

        #**********************
        elif mAction == "treeActionDeplaceCouper" or mAction == "treeActionDeplaceColler" or mAction == "treeActionDeplaceAnnuler":
           #--- 
           if mAction == "treeActionDeplaceCouper" :
             # Si arborescence des objets
             #mSchemaDepart = self.returnValueItem(mNode, 0)[1]  # Hyper important si noms objets identiques dans schéma diff.
             mSchemaDepart = self.returnValueItem(mNode, 0)[2] if self.Dialog.arboObjet else self.returnValueItem(mNode, 0)[1] # Hyper important si noms objets identiques dans schéma diff.

             for mNameObjet in self.mArraySchemasTables  :
                 # et Meme Nom
                 if mGetItem == mNameObjet[1] and mSchemaDepart == mNameObjet[0] :
                    # Nom objet, type objet et schema de l'objet
                    self.mDepartCouper = [mGetItem, mNameObjet[2], mNameObjet[0]]
                    break
           #--- 
           elif mAction == "treeActionDeplaceColler" :
            if self.mDepartCouper != "" : # Robus
              mSchemaOriNew, mSchemaOriOld     = self.mDepartCouper[2], "#obj_schema#"
              mObjetOriNew,  mObjetOriOld      = self.mDepartCouper[0], "#obj_nom#"
              mTypeNew,      mTypeOld          = self.mDepartCouper[1], "#obj_typ#"
              mSchemaCibleNew, mSchemaCibleOld = mGetItem             , "#schema_cible#"
              mVarNew, mVarOld = "1", "#variante#"
              mKeySql = dicListSql(self,'FONCTIONDeplaceObjet')
              dicReplace = {mSchemaOriOld: mSchemaOriNew, mObjetOriOld: mObjetOriNew, mTypeOld: mTypeNew, mSchemaCibleOld: mSchemaCibleNew, mVarOld: mVarNew}
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
              r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSqlNoReturn(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
              if r != False :
                 zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "Good, you have moved your objet", None)
                 zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
                 bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
                 #QMessageBox.information(self, zTitre, zMess) 
              else :
                 #Géré en amont dans la fonction executeSqlNoReturnDragDrop
                 pass 
           #--- 
           elif mAction == "treeActionDeplaceAnnuler": 
                self.mDepartCouper = ""

           self.fonctionAfficheDeplaceAll(mGetItem)
        
        #**********************
        else :
           if mAction == "treeActionCorbeille" :
                mKeySql = dicListSql(self,mAction)
                mSchemaNewID, mSchemaOldID = mGetItem, "#ID_nom_schema#" 
                mBlocNew, mBlocOld         = 'd', "#bloc#" 
                dicReplace = {mSchemaOldID: mSchemaNewID, mBlocOld: mBlocNew}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "your diagram is in the trash !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionDereferencer" :
                mKeySql = dicListSql(self,"FONCTIONasgard_sortie_gestion_schema")
                mSchemaNewID, mSchemaOldID = mGetItem, "#nom_schema#" 
                dicReplace = {mSchemaOldID: mSchemaNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just deferenced your diagram !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionRestaurer" :
                mKeySql = dicListSql(self,mAction)
                mSchemaNewID, mSchemaOldID = mGetItem, "#ID_nom_schema#" 
                #----
                mBlocNewTemp = dicExpRegul(self, 'Find_(FirstCar_)&Ret_FirstCar', mGetItem)[0]
                #----
                mBlocNew, mBlocOld = mBlocNewTemp, "#bloc#" 
                dicReplace = {mSchemaOldID: mSchemaNewID, mBlocOld: mBlocNew}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just restored your diagram !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionSupprimer_base" :
                mKeySql = dicListSql(self,mAction)
                mSchemaNewID, mSchemaOldID = mGetItem, "#ID_nom_schema#" 
                mcreationNew, mcreationOld = False, "#creation#"
                dicReplace = {mSchemaOldID: mSchemaNewID, mcreationOld: mcreationNew}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You just deleted your schema !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionSchema_efface" :
                mKeySql = dicListSql(self,mAction)
                mSchemaNewID, mSchemaOldID = mGetItem, "#ID_nom_schema#" 
                dicReplace = {mSchemaOldID: mSchemaNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just deleted a non-active diagram !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------           #----------------------
           elif mAction == "treeActionSchema_creer_base" :
                mKeySql = dicListSql(self,mAction)
                mSchemaNewID, mSchemaOldID = mGetItem, "#ID_nom_schema#" 
                mcreationNew, mcreationOld = True, "#creation#"
                dicReplace = {mSchemaOldID: mSchemaNewID, mcreationOld: mcreationNew}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just created the schema in the database (made active) !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionReferencer" : 
                mKeySql = dicListSql(self,"FONCTIONasgard_initialise_schema")
                mSchemaNewID, mSchemaOldID = mGetItem, "#nom_schema#" 
                dicReplace = {mSchemaOldID: mSchemaNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just referenced your diagram !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionReferencerConserveDroits" : 
                mKeySql = dicListSql(self,"FONCTIONasgard_initialise_schemaConserveDroits")
                mSchemaNewID, mSchemaOldID = mGetItem, "#nom_schema#" 
                dicReplace = {mSchemaOldID: mSchemaNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just referenced your schema while retaining the rights !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionReinitialisedroit" : 
                mKeySql = dicListSql(self,"FONCTIONasgard_Reinitialisedroit")
                mSchemaNewID, mSchemaOldID = mGetItem, "#nom_schema#" 
                dicReplace = {mSchemaOldID: mSchemaNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just restored the standard rights of the producer, editor and reader on the diagram !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionDiagnostic" : 
                mKeySql = dicListSql(self,"FONCTIONasgard_DiagnosticSchema")
                mSchemaNewID, mSchemaOldID = mGetItem, "#nom_schema#"
                self.nom_Schema_du_Diagnostic = mGetItem 
                dicReplace = {mSchemaOldID: mSchemaNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just restored the standard rights of the producer, editor and reader on the diagram !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionReinitDroitsObjets" : 
                # Si arborescence des objets
                #mSchemaDepart = self.returnValueItem(mNode, 0)[1]  # Hyper important si noms objets identiques dans schéma diff.
                mSchemaDepart = self.returnValueItem(mNode, 0)[2] if self.Dialog.arboObjet else  self.returnValueItem(mNode, 0)[1] # Hyper important si noms objets identiques dans schéma diff.

                for mNameObjet in self.mArraySchemasTables  :
                    # et Meme Nom
                    if mGetItem == mNameObjet[1] and mSchemaDepart == mNameObjet[0] :
                       # Nom objet, type objet et schema de l'objet
                       self.mDepartObjetTypeSchema = [mGetItem, mNameObjet[2], mNameObjet[0]]
                       break

                mKeySql = dicListSql(self,"FONCTIONasgard_initialise_obj")
                mSchemaNewID, mSchemaOldID       = self.mDepartObjetTypeSchema[2], "#nom_schema#" 
                mObjetNewID, mObjetOldID         = self.mDepartObjetTypeSchema[0], "#nom_objet#" 
                mTypeObjetNewID, mTypeObjetOldID = self.mDepartObjetTypeSchema[1], "#type_objet#" 
                dicReplace = {mSchemaOldID: mSchemaNewID, mObjetOldID: mObjetNewID, mTypeObjetOldID: mTypeObjetNewID}
                #------       
                zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just restored the standard rights of the producer, editor and reader on the objet !!", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionRepliquer" or mAction == "treeActionDerepliquer" :
                mReturnValueItemTemp = self.returnValueItem(mNode, 0)
                # Si arborescence des objets
                mSchemaClic = mReturnValueItemTemp[2] if self.Dialog.arboObjet else mReturnValueItemTemp[1]
                mObjetClic  = mReturnValueItemTemp[0]
                #----
                for mNameObjet in self.mArraySchemasTables  :
                    # et Meme Nom
                    if mObjetClic == mNameObjet[1] and mSchemaClic == mNameObjet[0] :
                       # Nom objet, type objet et schema de l'objet
                       self.mReturnValueItemTemp = [mNameObjet[1], mNameObjet[2], mNameObjet[0]]
                       break
                #----
                existeDansMetadata, repliquerMetadata, objetIcon = self.returnReplique(self.mReturnValueItemTemp[2],self.mReturnValueItemTemp[0], self.mReturnValueItemTemp[1], self.Dialog.mListeMetadata, self.mListeObjetArepliquer)
                if existeDansMetadata : 
                   mKeySql = dicListSql(self,"treeActionrepliquerUpdate")
                else :
                   mKeySql = dicListSql(self,"treeActionrepliquerInsert")
                #--
                if mAction == "treeActionRepliquer" :
                   mEtat = True
                elif mAction == "treeActionDerepliquer" :
                   mEtat = False

                mNewID, mOldID = "100", "#ID#"
                mBaseNewID, mBaseOldID = self.Dialog.mBaseAsGard.database, "#nom_base#"
                mSchemaNewID, mSchemaOldID =  mNameObjet[0], "#nom_schema#"
                mObjetNewID, mObjetOldID   = mNameObjet[1], "#nom_objet#"
                mTypeNewID, mTypeOldID     = mNameObjet[2], "#type_objet#"
                mEtatNewID, mEtatOldID     = mEtat, "#etat#"
                dicReplace = {mOldID: mNewID, mBaseOldID: mBaseNewID, mSchemaOldID: mSchemaNewID, mObjetOldID: mObjetNewID,mTypeOldID: mTypeNewID, mEtatOldID: mEtatNewID}
                #------       
                if mAction == "treeActionRepliquer" :
                   zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "you have just replicated the dataset for synchronization with the central database", None) + " " + mGetItem.upper()
                elif mAction == "treeActionDerepliquer" :
                   zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "you have just dereplicated the dataset for synchronization with the central database", None) + " " + mGetItem.upper()
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)
           #----------------------
           elif mAction == "treeActionLayerStyles" :
                mKeySql = dicListSql(self,"Fonction_Layer_Styles_Droits")
                mVarianteNewID, mVarianteOldID = self.dicIcoMenuLayerStyles[mOption][2], "#variante#"
                dicReplace = {mVarianteOldID: mVarianteNewID}
                #------  
                if self.dicIcoMenuLayerStyles[mOption][2] != 6 :     
                   zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just applied new rights to the layer_styles table   !!", None) + " variante : " + str(self.dicIcoMenuLayerStyles[mOption][0] )
                else :
                   zMessGood = QtWidgets.QApplication.translate("bibli_asgard", "You have just reinitailized the rights on the layer_styles table   !!", None)
                zMess, zTitre = zMessGood, QtWidgets.QApplication.translate("bibli_asgard", "Information !!!", None)

           #**********************
           for key, value in dicReplace.items():
               if isinstance(value, bool) :
                  mValue = str(value)
               elif (value is None) :
                  mValue = "''"
               elif isinstance(value, int) :
                  mValue = str(value)
               else :
                  value = value.replace("'", "''")
                  mValue = "'" + str(value) + "'"
               mKeySql = mKeySql.replace(key, mValue)
           #**********************
           if mAction == "treeActionDiagnostic" : #map vers la boite de confirmation avec substitution de la variable schéma
              # Attention chgt des paramètres envoyé 
              self.Dialog.dialogueConfirmationAction(self.Dialog, self.Dialog.mBaseAsGard, 'FONCTIONasgard_DiagnosticSchema', mKeySql)
           else :
              #==============================
              r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSqlNoReturn(self.Dialog, self.Dialog.mBaseAsGard.mConnectEnCours, self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
              if r != False :
                 bibli_asgard.displayMess(self.Dialog, (2 if self.Dialog.displayMessage else 1), zTitre, zMess, Qgis.Info, self.Dialog.durationBarInfo)
                 #QMessageBox.information(self, zTitre, zMess) 
              else :
                 pass 
              #==============================
        return  
        
    #-------------                                                    
    def ihmsCurrentIndexChanged(self, itemCurrent, itemPrevious):
        self.ihms( itemCurrent, self.currentColumn() )
        return

    #-------------                                                    
    def ihms(self, item, column):
        mItemValue = self.returnValueItem(item, column)
        
        #self.itemEnCours = mItemValue  # Pour mémoriser l'expand
        self.Dialog.groupBoxAffichageSchema.setVisible(False)
        self.Dialog.groupBoxAffichageHelp.setVisible(False)
        mItemClic = item.data(column, Qt.DisplayRole)
        self.returnItemClic = mItemClic

        if self.returnTypeObjeEtAsgard(mItemClic)[0] == "SCHEMA" :
           for mGetItem in mItemValue :
               iParcours = 0
               while iParcours in range(len(self.mSchemasBlocs)) :
                     if mGetItem == self.mSchemasBlocs[iParcours][0] :
                        self.Dialog.groupBoxAffichageSchema.setVisible(True)
                        self.Dialog.groupBoxAffichageHelp.setVisible(False)
                        self.mode = "update"
                        self.mSchemaID = self.mSchemasBlocs[iParcours][0]   # Gestion pour le Where
                        self.mSchema = self.mSchemasBlocs[iParcours][0]
                        mBlocTemp = self.mSchemasBlocs[iParcours][1] if self.mSchemasBlocs[iParcours][1] != None else "autre"
                        self.mBloc   = "(" + str(mBlocTemp) + ") " + str(self.dicListBlocs[mBlocTemp])          
                        self.mActif  = self.mSchemasBlocs[iParcours][2]
                        self.mProd   = self.mSchemasBlocs[iParcours][4] if self.mSchemasBlocs[iParcours][4] != None else "Aucun"
                        self.mEdit   = self.mSchemasBlocs[iParcours][5] if self.mSchemasBlocs[iParcours][5] != None else "Aucun"
                        self.mLect   = self.mSchemasBlocs[iParcours][6] if self.mSchemasBlocs[iParcours][6] != None else "Aucun"
                        self.mNomenclature  = self.mSchemasBlocs[iParcours][7]
                        self.mNiv1          = self.mSchemasBlocs[iParcours][8]  if self.mSchemasBlocs[iParcours][8] != None else ""
                        self.mNiv1_abr      = self.mSchemasBlocs[iParcours][9]  if self.mSchemasBlocs[iParcours][9] != None else ""
                        self.mNiv2          = self.mSchemasBlocs[iParcours][10] if self.mSchemasBlocs[iParcours][10] != None else ""
                        self.mNiv2_abr      = self.mSchemasBlocs[iParcours][11] if self.mSchemasBlocs[iParcours][11] != None else ""
                        self.initIhmSchema(self.Dialog, self.mode, self.mSchema, self.mBloc, self.mActif, self.mProd, self.mEdit, self.mLect, self.mNomenclature, self.mNiv1, self.mNiv1_abr, self.mNiv2, self.mNiv2_abr, self.listeDesArbos)
                        #Affichage si aucune valeur modifiée
                        tId    = ('id_schema', 'id_bloc', 'id_actif', 'id_producteur', 'id_editeur', 'id_lecteur', 'id_nomenclature', 'id_niv1', 'id_niv1_abr', 'id_niv2', 'id_Niv2_abr')
                        tValue = (self.mSchemaID, mBlocTemp, self.mActif, self.mProd, self.mEdit, self.mLect, self.mNomenclature, self.mNiv1, self.mNiv1_abr, self.mNiv2, self.mNiv2_abr)
                        self.dicOldValueSchema = dict(zip(tId, tValue))
                     iParcours += 1
        return
        
    #------ 
    def initIhmSchema(self, Dialog, mode, mSchema, mBloc, mActif, mProd, mEdit, mLect, mNomenclature, mNiv1, mNiv1_abr, mNiv2, mNiv2_abr, listeDesArbos) :
        Dialog.zoneSchema.setText(mSchema)
        #Delete Corbeille
        if self.mode == "create" :
           for mIndexBloc in range(Dialog.comboBloc.count()) :
               if Dialog.comboBloc.model().item(mIndexBloc,1).text() =='d' :
                  Dialog.comboBloc.view().setRowHidden(mIndexBloc, True)
           #------------
           Dialog.comboProd.clear()
           Dialog.comboProd.addItems(self.ArraymRolesProducteurs)
        Dialog.comboBloc.setCurrentText(mBloc)

        if mActif : 
           Dialog.caseActif.setEnabled(False)
           Dialog.labelActif.setEnabled(False)  
           Dialog.labelActifInfo.setStyleSheet("QLabel { color: grey; }")    
        else :                               
           Dialog.caseActif.setEnabled(True)
           Dialog.labelActif.setEnabled(True)
           Dialog.labelActifInfo.setStyleSheet("QLabel { color: red; }")    
            
        Dialog.caseActif.setChecked(mActif)
        #Complete en mode modif le rôle du producteur du schéma même si le role  de connexion n'a pas se rôle
        if self.mode == "update" :
           Dialog.comboProd.clear()
           Dialog.comboProd.addItems(self.ArraymRolesProducteurs)
           for mSchemaFind in self.mSchemasBlocs :
               if self.mSchemaID == mSchemaFind[0] :
                  if mSchemaFind[4] not in self.ArraymRolesProducteurs :
                     Dialog.comboProd.addItem(mSchemaFind[4])
                     break

        #------------
        Dialog.zoneNiv1.clear()
        Dialog.zoneNiv1_abr.clear()
        Dialog.zoneNiv2.clear()
        Dialog.zoneNiv2_abr.clear()
        #-
        Dialog.zoneNiv1.addItems(listeDesArbos[0])
        mCompleter = QCompleter(listeDesArbos[0], Dialog)
        mCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        mCompleter.setCompletionMode(QCompleter.UnfilteredPopupCompletion)
        Dialog.zoneNiv1.setCompleter(mCompleter)
        #-
        Dialog.zoneNiv1_abr.addItems(listeDesArbos[1])
        mCompleter = QCompleter(listeDesArbos[1], Dialog)
        mCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        Dialog.zoneNiv1_abr.setCompleter(mCompleter)
        #-
        Dialog.zoneNiv2.addItems(listeDesArbos[2])
        mCompleter = QCompleter(listeDesArbos[2], Dialog)
        mCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        Dialog.zoneNiv2.setCompleter(mCompleter)
        #-
        Dialog.zoneNiv2_abr.addItems(listeDesArbos[3])
        mCompleter = QCompleter(listeDesArbos[3], Dialog)
        mCompleter.setCaseSensitivity(Qt.CaseInsensitive)
        Dialog.zoneNiv2_abr.setCompleter(mCompleter)
        #------------
        Dialog.comboProd.setCurrentText(mProd)
        Dialog.comboEdit.setCurrentText(mEdit) 
        Dialog.comboLect.setCurrentText(mLect)
        Dialog.caseNomenclature.setChecked(mNomenclature)
        Dialog.zoneNiv1.setCurrentText(mNiv1)
        Dialog.zoneNiv1_abr.setCurrentText(mNiv1_abr)
        Dialog.zoneNiv2.setCurrentText(mNiv2)
        Dialog.zoneNiv2_abr.setCurrentText(mNiv2_abr)
        return
              
    #-------------
    def processItem(self, item, column):
        #self.Dialog.groupBoxAffichagesetVisible(False)
        if item == None : return None 
        mItemValue = self.returnValueItem(item, column)
        mText = ">>>  j'ai cliqué sur : "
        for mGetItem in mItemValue:
            mText += mGetItem + " / "
        print(mText[:-2])
        return
    #-------------
    def returnValueItem(self, item, column):
        if item == None : return None 
        mReturnValueItem, mItem = [], item
        while True :
           mReturnValueItem.append(mItem.data(column, Qt.DisplayRole))
           mParentItem = mItem.parent()
           if mParentItem != None :
              mItem = mParentItem
           else :
              break
        return mReturnValueItem
    #-------------
    def returnTypeObjeEtAsgard(self, mName):
        mRet = ("", "") 
        for libObjet in self.referenceObjNameTypeAsgard :
            if mName == libObjet[0] :
               mRet = (libObjet[1], libObjet[2])
               break
        return mRet
    #-------------
    
    def returnReplique(self, schema, objet, typeobjet, mListeMetadata, mListeObjetArepliquer):
        # schema sélectionné, 
        # objet sélectionné, 
        # typeobjet sélectionné, 
        # mListeMetadata Liste des objets dans metadata 
        #--
        #Réplication iconographie
        existeDansMetadata, repliquerMetadata, objetIcon = False, False, ""
        if len(mListeMetadata) != 0 :
           for elemMetadata in  mListeMetadata :
               if schema == elemMetadata[1] and objet == elemMetadata[2] :
                  tempmRootTable = typeobjet + ("replique" if elemMetadata[4] else "dereplique")  
                  existeDansMetadata, repliquerMetadata, objetIcon = True, elemMetadata[4], tempmRootTable
                  break
               else :
                  #Pas dans la table des Réplication
                  tempmRootTable = typeobjet + ("dereplique" if typeobjet in mListeObjetArepliquer else  '')  
                  existeDansMetadata, repliquerMetadata, objetIcon = False, False, tempmRootTable
        else :
           #Pas dans la table des Réplication
           tempmRootTable = typeobjet + ("dereplique" if typeobjet in mListeObjetArepliquer else  '')  
           existeDansMetadata, repliquerMetadata, objetIcon = False, False, tempmRootTable
           #--
           #Retourne Existe dans la table metadata, si elle existe replique ou pas, clé nom icone
        return existeDansMetadata, repliquerMetadata, objetIcon 
#========================================================
class BASEPOSTGRES :
    #----------------------
    def __init__(self, nameBase):
        self.nameBase = nameBase
        
        #===========================
        if returnSiVersionQgisSuperieureOuEgale("3.10") : 
           #modification pour permettre d'utiliser les configurations du passwordManager (QGIS >=3.10)
           metadata = QgsProviderRegistry.instance().providerMetadata('postgres')

           if nameBase not in metadata.connections(False) :
              QMessageBox.critical(self, "Error", "new : There is no defined database connection for " + nameBase)
              mListConnectBase = []
           #modification pour permettre d'utiliser les configurations du passwordManager (QGIS >=3.10)

           #modification pour permettre d'utiliser les configurations du passwordManager (QGIS >=3.10)
           uri = QgsDataSourceUri(metadata.findConnection(nameBase).uri())
           #modification pour permettre d'utiliser les configurations du passwordManager (QGIS >=3.10)
           self.service = uri.service() or os.environ.get('PGSERVICE')
           self.host = uri.host() or os.environ.get('PGHOST')
           self.port = uri.port() or os.environ.get('PGPORT')
           self.database = uri.database() or os.environ.get('PGDATABASE')
           self.username = uri.username() or os.environ.get('PGUSER') or os.environ.get('USER')
           self.password = uri.password() or os.environ.get('PGPASSWORD')
           self.sslmode = uri.sslMode() or os.environ.get('PGSSLMODE')
        else :
           # mListConnectBase  === ['', 'localhost', '5432', 'geobase_snum', 'etienne.lousteau', ''],
           # mConfigConnection === "host=localhost port=5432 dbname=geobase_snum user=etienne.lousteau password='' sslmode=2", 
           # uri               === <QgsDataSourceUri: dbname='geobase_snum' host=localhost port=5432 user='etienne.lousteau' sslmode=allow>]
           mSettings = QgsSettings()
           self.mConnectionSettingsKey = "/PostgreSQL/connections/{}".format(self.nameBase)
           mSettings.beginGroup(self.mConnectionSettingsKey)
           if not mSettings.contains("database") :
              QMessageBox.critical(self, "Error", "There is no defined database connection")
              mListConnectBase = []
           else :
              uri = QgsDataSourceUri()
              settingsList = ["service", "host", "port", "database", "username", "password"]
              self.service, self.host, self.port, self.database, self.username, self.password = map(lambda x: mSettings.value(x, "", type=str), settingsList)
              mListConnectBase = [self.service, self.host, self.port, self.database, self.username, self.password ]
              useEstimatedMetadata = mSettings.value("estimatedMetadata", False, type=bool)
              self.sslmode = mSettings.enumValue("sslmode", uri.SslPrefer)
           mSettings.endGroup()

           if self.service:
              mConfigConnection = "service{0} dbname={1} user={2} password='{3}' sslmode={4}".format(self.service, self.database, self.username, self.password, self.sslmode)
              uri.setConnection(self.service, self.database, self.username, self.password, self.sslmode)
           else:
              mConfigConnection = "host={0} port={1} dbname={2} user={3} password='{4}' sslmode={5}".format(self.host, self.port, self.database, self.username, self.password, self.sslmode)
              uri.setConnection(self.host, self.port, self.database, self.username, self.password, self.sslmode)

           uri.setUseEstimatedMetadata(useEstimatedMetadata)
        

        mListConnectBase = [self.service, self.host, self.port, self.database, self.username, self.password ]
        if self.service:
           mConfigConnection = "service{0} dbname={1} user={2} password='{3}' sslmode={4}".format(self.service, self.database, self.username, self.password, self.sslmode)
        else:
           mConfigConnection = "host={0} port={1} dbname={2} user={3} password='{4}' sslmode={5}".format(self.host, self.port, self.database, self.username, self.password, self.sslmode)


        self.nameBasemListConnectBase, self.mConfigConnection, self.uri = mListConnectBase, mConfigConnection, uri

    #----------------------
    def connectBase(self) :
        return self.mTestConnect(self.mConfigConnection, self.uri)
          
    #----------------------
    def mTestConnect(self, mConfigConnection, uri) :
        retUser, retPassword, mTestConnect, okConnect = self.username, self.password, True, False
        mMessAuth = QtWidgets.QApplication.translate("bibli_asgard", "Authentication problem, check your password in particular.", None)
        connInfoUri = uri.connectionInfo()

        while mTestConnect :
           try :
              mConnectEnCours = psycopg2.connect(uri.connectionInfo(), application_name="Asgard Manager")
              mTestConnect, okConnect = False, True
           except :
              (retSuccess, retUser, retPassword) = QgsCredentials.instance().get(connInfoUri, retUser, retPassword, mMessAuth)
              if not retSuccess : #Annuler 
                 mTestConnect, okConnect = False, False
              else :
                 uri.setUsername(retUser)     if retUser else ''
                 uri.setPassword(retPassword) if retPassword else ''
        #--------
        if okConnect :
           QgsCredentials.instance().put(connInfoUri, retUser, retPassword) 
           self.mConnectEnCours = mConnectEnCours
           self.mConnectEnCoursPointeur = mConnectEnCours.cursor()
           return True, self.mConnectEnCours, mConfigConnection
        else : 
           return False, None, ""    
                   
    #----------------------
    def executeSqlNoReturnDragDrop(self, Dialog, pointeurConnection, pointeurBase, mSql) :
       ret = True
       QApplication.instance().setOverrideCursor(Qt.WaitCursor)
       try :
          pointeurBase.execute(mSql)
          pointeurConnection.commit()

          if hasattr(Dialog, 'mTreePostgresql') :
             mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresql, "", "")
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresqlDroits, "", "")
          Dialog.initGeneral(Dialog)
          if hasattr(Dialog, 'mTreePostgresql') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)

       except Exception as err: 
          ret = False
          QApplication.instance().setOverrideCursor(Qt.ArrowCursor) 
          zMessError_Code   = (str(err.pgcode) if hasattr(err, 'pgcode') else '')
          zMessError_Erreur = (str(err.pgerror) if hasattr(err, 'pgerror') else '')
          zMessError_Erreur = cleanMessError(zMessError_Erreur)
          
          mListeErrorCode = ["42501", "P0000", "P0001", "P0002", "P0003", "P0004"] 
          if zMessError_Code in [ mCodeErreur for mCodeErreur in mListeErrorCode] :   #Erreur Asgard
             mTypeErreur = "ASGARDGEREE" if dicExisteExpRegul(self, 'Search_0', zMessError_Erreur) else "ASGARDNONGEREE"
          else : 
             mTypeErreur = "ASGARDMANAGER"
          dialogueMessageError(mTypeErreur, zMessError_Erreur ) 
          #-------------
          self.deconnectBase()  

          if hasattr(Dialog, 'mTreePostgresql') :
             mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresql, "", "")
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresqlDroits, "", "")
          Dialog.initGeneral(Dialog)
          if hasattr(Dialog, 'mTreePostgresql') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)

          #-------------
       QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
       return ret

    #----------------------
    def executeSqlNoReturn(self, Dialog, pointeurConnection, pointeurBase, mSql) :
        ret, zMessError_Code, zMessError_Erreur, zMessError_Diag = True, '', '', ''
        QApplication.instance().setOverrideCursor(Qt.WaitCursor) 

        try :
          pointeurBase.execute(mSql)
          pointeurConnection.commit()
          if hasattr(Dialog, 'mTreePostgresql') :
             mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresql, "", "")
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresqlDroits, "", "")
          Dialog.initGeneral(Dialog)
          if hasattr(Dialog, 'mTreePostgresql') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)

        except Exception as err:
          QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
          ret = False
          zMessError_Code   = (str(err.pgcode) if hasattr(err, 'pgcode') else '')
          zMessError_Erreur = (str(err.pgerror) if hasattr(err, 'pgerror') else '')
          print("err.pgcode = %s" %(zMessError_Code))
          print("err.pgerror = %s" %(zMessError_Erreur))
          zMessError_Erreur = cleanMessError(zMessError_Erreur)
          
          mListeErrorCode = ["42501", "P0000", "P0001", "P0002", "P0003", "P0004","2BP01"] 
          if zMessError_Code in [ mCodeErreur for mCodeErreur in mListeErrorCode] :   #Erreur Asgard
             mTypeErreur = "ASGARDGEREE" if dicExisteExpRegul(self, 'Search_0', zMessError_Erreur) else "ASGARDNONGEREE"
          else : 
             mTypeErreur = "ASGARDMANAGER"
             
          #Modif 10/02/2021 pour fichiers Extension n'existent pas et réinstalle sans fermer AM
          if zMessError_Code == '' and zMessError_Erreur == '' and mSql == "CREATE EXTENSION asgard" :
             pass # pas d'affichage de la boite de dialogue des erreurs
          else :
             dialogueMessageError(mTypeErreur, zMessError_Erreur ) 
          #-------------
          self.deconnectBase()  

          if hasattr(Dialog, 'mTreePostgresql') :
             mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresql, "", "")
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresqlDroits, "", "")
          Dialog.initGeneral(Dialog)
          if hasattr(Dialog, 'mTreePostgresql') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)
          #-------------
        QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
        return ret, zMessError_Code, zMessError_Erreur, zMessError_Diag      

    #----------------------
    def executeSqlCreate(self, Dialog, pointeurConnection, pointeurBase, mSql) :
        ret, zMessError_Code, zMessError_Erreur, zMessError_Diag = True, '', '', ''
        QApplication.instance().setOverrideCursor(Qt.WaitCursor) 

        try :
          pointeurBase.execute(mSql)
          pointeurConnection.commit()

        except Exception as err:
          QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
          ret = False
          zMessError_Code   = (str(err.pgcode) if hasattr(err, 'pgcode') else '')
          zMessError_Erreur = (str(err.pgerror) if hasattr(err, 'pgerror') else '')
          print("err.pgcode = %s" %(zMessError_Code))
          print("err.pgerror = %s" %(zMessError_Erreur))
          zMessError_Erreur = cleanMessError(zMessError_Erreur)
          
          mListeErrorCode = ["42501", "P0000", "P0001", "P0002", "P0003", "P0004","2BP01"] 
          if zMessError_Code in [ mCodeErreur for mCodeErreur in mListeErrorCode] :   #Erreur Asgard
             mTypeErreur = "ASGARDGEREE" if dicExisteExpRegul(self, 'Search_0', zMessError_Erreur) else "ASGARDNONGEREE"
          else : 
             mTypeErreur = "ASGARDMANAGER"
             
          #Modif 10/02/2021 pour fichiers Extension n'existent pas et réinstalle sans fermer AM
          if zMessError_Code == '' and zMessError_Erreur == '' and mSql == "CREATE EXTENSION asgard" :
             pass # pas d'affichage de la boite de dialogue des erreurs
          else :
             dialogueMessageError(mTypeErreur, zMessError_Erreur ) 
          #-------------
          self.deconnectBase()  

          if hasattr(Dialog, 'mTreePostgresql') :
             mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresql, "", "")
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresqlDroits, "", "")
          Dialog.initGeneral(Dialog)
          if hasattr(Dialog, 'mTreePostgresql') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
          if hasattr(Dialog, 'mTreePostgresqlDroits') :
             Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)
          #-------------
        QApplication.instance().setOverrideCursor(Qt.ArrowCursor)
        return ret, zMessError_Code, zMessError_Erreur, zMessError_Diag      

    #----------------------           
    def executeSql(self,pointeurBase, mSql) :
        zMessError_Code, zMessError_Erreur, zMessError_Diag = '', '', ''
        QApplication.instance().setOverrideCursor(Qt.WaitCursor) 
        try :
          pointeurBase.execute(mSql)
          result = pointeurBase.fetchall()
          
        except Exception as err:
          QApplication.instance().setOverrideCursor(Qt.ArrowCursor) 
          result = None
          zMessError_Code   = (str(err.pgcode) if hasattr(err, 'pgcode') else '')
          zMessError_Erreur = (str(err.pgerror) if hasattr(err, 'pgerror') else '')
          print("err.pgcode = %s" %(zMessError_Code))
          print("err.pgerror = %s" %(zMessError_Erreur))
          zMessError_Erreur = cleanMessError(zMessError_Erreur)
          mListeErrorCode = ["42501", "P0000", "P0001", "P0002", "P0003", "P0004"] 
          if zMessError_Code in [ mCodeErreur for mCodeErreur in mListeErrorCode] :   #Erreur Asgard
             mTypeErreur = "ASGARDGEREE" if dicExisteExpRegul(self, 'Search_0', zMessError_Erreur) else "ASGARDNONGEREE"
          else : 
             mTypeErreur = "ASGARDMANAGER"
          dialogueMessageError(mTypeErreur, zMessError_Erreur )   
          #-------------
          self.deconnectBase() 
           
          try :  #Cas où Dialog n'est pas istancié (début #Membre de g_admin asgard_general_ui ligne 396)
             if hasattr(Dialog, 'mTreePostgresql') :
                mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresql, "", "")
             if hasattr(Dialog, 'mTreePostgresqlDroits') :
                mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect = Dialog.returnItemTreePostgresql("LOAD", Dialog.mTreePostgresqlDroits, "", "")
             Dialog.initGeneral(Dialog)
             if hasattr(Dialog, 'mTreePostgresql') :
                Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresql, mReturnItemTreePostgresql, mReturnItemTreePostgresqlSelect)
             if hasattr(Dialog, 'mTreePostgresqlDroits') :
                Dialog.returnItemTreePostgresql("RESTORE", Dialog.mTreePostgresqlDroits, mReturnItemTreePostgresqlDroits, mReturnItemTreePostgresqlDroitsSelect)
          except :
             pass 
          #-------------

        QApplication.instance().setOverrideCursor(Qt.ArrowCursor) 
        return result, zMessError_Code, zMessError_Erreur, zMessError_Diag

     #----------------------
    def deconnectBase(self) :
        self.mConnectEnCours.commit()
        self.mConnectEnCoursPointeur.close()
        self.mConnectEnCours.close()
        return 
     #----------------------
    def layerPostgresql(self, mName, mSchema, mSource, mSql, mProvider ) :
        #try :
           if self.service :
              QMessageBox.warning(None,"ASGARD MANAGER : Connection","the connection is impossible")
              return False, None
           else:
              uri = QgsDataSourceUri()             
              uri.setConnection(self.host, self.port, self.database, self.username, self.password)
              uri.setDataSource(mSchema, mSource, "geom",mSql)
              vlayer = QgsVectorLayer(uri.uri(), mName, mProvider)
              return True, vlayer        
        #except :
           QMessageBox.warning(None,"ASGARD MANAGER : Connection","the connection is impossible")
           return False, None
#========================================================
def listBase(self):
    mSettings = QgsSettings()
    mSettings.beginGroup("/PostgreSQL/connections")
    mListeBase = mSettings.childGroups()
    mSettings.endGroup()
    return mListeBase
           

#==================================================
#Schéma existe
#==================================================
def schemaExiste(mNameSchema, mTypeSchemaRecherche) :
    #self.mListBlocs pour                    : Blocs fonctionnels y compris Corbeille
    #self.mListSchemaActifs pour             : Actifs
    #self.mListSchemaNonActifs pour          : Non Actifs
    #self.mListSchemaCorbeilleActifs pour    : Actifs corbeille
    #self.mListSchemaCorbeilleNonActifs pour : Non Actifs corbeille
    #self.mListSchemaExistants pour          : Hors Asgard
    return (True if mNameSchema in [ libZoneActive[0] for libZoneActive in mTypeSchemaRecherche] else False) 

#==================================================
#Schéma existe
#==================================================
def returnSchemaExisteAndName(mNameSchema, mTypeSchemaRecherche, mCodeBloc) :
    mReturnSchemaExisteAndName = [False, '']
    for libZoneActive in mTypeSchemaRecherche :
        if (mNameSchema == libZoneActive[0] and mCodeBloc == libZoneActive[1]) :
           mReturnSchemaExisteAndName = [True, mNameSchema]
           break
    return mReturnSchemaExisteAndName
            
#==================================================
#Fichier existe
#==================================================
def FileExiste(FileName):
    try:
       with open(FileName): pass
       ExisteFile = True
    except IOError:
       ExisteFile = False
    return ExisteFile

#==================================================
#Dossier existe
#==================================================
def createFolder(mFolder):
    try:
       os.makedirs(mFolder)
    except OSError:
       pass
    return mFolder

#==================================================
#Ajout des blocs, Libelles et Icons qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings 
#==================================================
def returnDicBlocLibelleIconNonReference(mParamListBlocs, mParamListBlocsLibelle, mParamListBlocsIcons, mParamSchemasBlocs, mParamMyPathIcon) :
    mListCodeBloc = []
    for mListCode in mParamListBlocs :
        mListCodeBloc.append(mListCode[1])
    for mIndexKey in range(len(mParamSchemasBlocs)) :
        if mParamSchemasBlocs[mIndexKey][0][0:1] not in mListCodeBloc and mParamSchemasBlocs[mIndexKey][0][1:2] == "_" :
           mListCodeBloc.append(mParamSchemasBlocs[mIndexKey][0][0:1]) #Ajouter sinon, doublons etc ....
           mPos = len(mParamListBlocs) - 1
           mParamListBlocs.insert(mPos , [ "BLOC Non référencé (" + str(mParamSchemasBlocs[mIndexKey][0][0:1]).upper() + ")", mParamSchemasBlocs[mIndexKey][0][0:1] ])
           mParamListBlocsLibelle.insert(mPos ,mParamSchemasBlocs[mIndexKey][0][0:1])
           mParamListBlocsIcons.insert(mPos ,returnIcon(mParamMyPathIcon + "\\treeview\\" + str(mParamSchemasBlocs[mIndexKey][0][0:1]) + ".png"))
    return mParamListBlocs, mParamListBlocsLibelle, mParamListBlocsIcons
    
#==================================================
#Ajout uniquement des blocs qui sont dans gestion_schema_usr mais pas dans le qgis_global_settings 
#==================================================
def returnDicBlocUniquementNonReference(mParamListBlocs, mParamSchemasBlocs) :
    mListCodeBloc = []
    for mListCode in mParamListBlocs :
        mListCodeBloc.append(mListCode)                                                   
    for mIndexKey in range(len(mParamSchemasBlocs)) :
        if mParamSchemasBlocs[mIndexKey][0][0:1] not in mListCodeBloc and mParamSchemasBlocs[mIndexKey][0][1:2] == "_" :
           mListCodeBloc.append(mParamSchemasBlocs[mIndexKey][0][0:1]) #Ajouter sinon, doublons etc ....
           if 'd' in mParamListBlocs : 
              del mParamListBlocs['d'] 
           mParamListBlocs[mParamSchemasBlocs[mIndexKey][0][0:1]] = "BLOC Non référencé (" + str(mParamSchemasBlocs[mIndexKey][0][0:1]).upper() + ")"
           if 'd' not in mParamListBlocs : mParamListBlocs['d'] = 'Corbeille'
    #mParamListBlocs = redresseBlocs(mParamListBlocs)
    return mParamListBlocs
    
def redresseBlocs(mDic) :
    mListKeyRedresse = ['autre']
    for mKeyList in mListKeyRedresse :
        for mKeyDic in mDic.keys():
            if mKeyList == mKeyDic :
               del mDic[mKeyList] 
               if mKeyList not in mDic :
                  mDic[''] = 'Autres'
    
    return mDic
    
#==================================================
#Lecture du fichier ini
#==================================================
def returnLoadBlocParam():
    mDic = {}
    mSettings = QgsSettings()
    mSettings.beginGroup("ASGARD_MANAGER")
    #Ajouter si nouveau bloc fonctionnel
    listBlocsKey = [
                "c",
                "w",
                "s",
                "p",
                "r",
                "x",
                "e",
                "z"
                ]
    listBlocsValue = [
                "Consultation",
                "Données travail",
                "Géostandards",
                "Données thématiques",
                "Référentiels",
                "Données confidentielles",
                "Données extérieures",
                "Administration"
                ] 
    dicBlocAutre = {"autre":"Autres", "d":"Corbeille"}  # Gestion des Schémas à Null sur Bloc Autres et gestion Corbeille
                 
    mSettings.beginGroup("Blocs")
    for iBlocs in range(len(listBlocsKey)) :
        if len(listBlocsKey[iBlocs]) ==  1 : #Clé autorisée sur un caractère
           if not mSettings.contains(listBlocsKey[iBlocs]) :
              mSettings.setValue(str(listBlocsKey[iBlocs].lower()), str(listBlocsValue[iBlocs]))
           mDic[listBlocsKey[iBlocs]] = mSettings.value(listBlocsKey[iBlocs])           

    #---------------------
    for keyGroupBloc in mSettings.allKeys():
        if len(keyGroupBloc) ==  1 : #Clé autorisée sur un caractère
           if keyGroupBloc not in mDic :  #Conserver l'ordre du DicBlocs
              mDic[keyGroupBloc.lower()] = mSettings.value(keyGroupBloc)
    #Ajout de Autre à la fin du TreeView
    for key, value in dicBlocAutre.items():
        mDic[key] = value
    mSettings.endGroup()
    mSettings.endGroup()    
    return mDic

#==================================================
#Sauvegarde uniquement du paramètre DashBord affichage onglet stats
#==================================================
def saveParamDashBoard():
    mDicAutre = {}
    mSettings = QgsSettings()
    mSettings.beginGroup("ASGARD_MANAGER")
    mSettings.beginGroup("Generale")
    
    mDicAutre["dashBoard"] = "false"
                 
    for key, value in mDicAutre.items():
        mSettings.setValue(key, value)

    mSettings.endGroup()
    mSettings.endGroup()    
    return 
        
   
#==================================================
#Lecture du fichier ini pour dimensions Dialog
#==================================================
def returnAndSaveDialogParam(self, mAction):
    mDicAutre = {}
    mSettings = QgsSettings()
    mSettings.beginGroup("ASGARD_MANAGER")
    mSettings.beginGroup("Generale")
    
    if mAction == "Load" :
       #Ajouter si autre param
       valueDefautL = 810
       valueDefautH = 640
       valueDefautDisplayObject = "all"
       valueDefautDashBoard = "true"
       valueDefautDisplayMessage = "dialogBox"
       valueDefautArboObjet = "true"
       valueDefautFileHelp  = "html"
       valueDefautFileHelpPdf   = "https://snum.scenari-community.org/Asgard/PDF/GuideAsgardManager"
       valueDefautFileHelpHtml  = "https://snum.scenari-community.org/Asgard/Documentation/#SEC_AsgardManager"
       valueDefautDurationBarInfo = 10
       mDicAutre["dialogLargeur"]  = valueDefautL
       mDicAutre["dialogHauteur"]  = valueDefautH
       mDicAutre["displayObjects"] = valueDefautDisplayObject
       mDicAutre["dashBoard"]      = valueDefautDashBoard
       mDicAutre["displayMessage"] = valueDefautDisplayMessage
       mDicAutre["arboObjet"]      = valueDefautArboObjet
       mDicAutre["fileHelp"]       = valueDefautFileHelp
       mDicAutre["fileHelpPdf"]    = valueDefautFileHelpPdf
       mDicAutre["fileHelpHtml"]   = valueDefautFileHelpHtml
       mDicAutre["durationBarInfo"]= valueDefautDurationBarInfo

       for key, value in mDicAutre.items():
           if not mSettings.contains(key) :
              mSettings.setValue(key, value)
           else :
              mDicAutre[key] = mSettings.value(key)           
       #-dashBoard
       #-
       mSettings.endGroup()
       mSettings.beginGroup("DashBoard")
       mSettings.beginGroup("BlocsColor")
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
       for key, value in mDicDashBoard.items():
           if not mSettings.contains(key) :
              mSettings.setValue(key, value)
           else :
              mDicDashBoard[key] = mSettings.value(key)           
       #-dashBoard
       mDicAutre = {**mDicAutre, **mDicDashBoard}          
    elif mAction == "Save" :
       mDicAutre["dialogLargeur"] = self.Dialog.width()
       mDicAutre["dialogHauteur"] = self.Dialog.height()
                 
       for key, value in mDicAutre.items():
           mSettings.setValue(key, value)

    mSettings.endGroup()
    mSettings.endGroup()
    mSettings.endGroup()    
    return mDicAutre

#==================================================
#Lecture du fichier ini pour sauvegarde connection
#==================================================
def returnAndSaveConnectionParam(self, mAction):
    mDicAutreConnect = {}
    mSettings = QgsSettings()
    mSettings.beginGroup("ASGARD_MANAGER")
    mSettings.beginGroup("Generale")
    
    if mAction == "Load" :
       #Ajouter si autre param
       valueDefautUrlConnect = 'Aucun'
       mDicAutreConnect["urlConnect"] = valueDefautUrlConnect
                 
       for key, value in mDicAutreConnect.items():
           if not mSettings.contains(key) :
              mSettings.setValue(key, value)
           else :
              mDicAutreConnect[key] = mSettings.value(key)           
    elif mAction == "Save" :
       mIndex = self.comboAdresse.currentText()
       mDicAutreConnect["urlConnect"] = self.comboAdresse.currentText()
                 
       for key, value in mDicAutreConnect.items():
           mSettings.setValue(key, value)

    mSettings.endGroup()
    mSettings.endGroup()    
    return mDicAutreConnect        
#==================================================
#Lecture du fichier paramètre
#==================================================
def loadFichierParam(monFichierParam, mBlocs):
    #Ajouter si nouveau bloc fonctionnel
    listBlocs = {
                "c":"Consultation",
                "w":"Données travail",
                "s":"Géostandards",
                "p":"Données thématiques",
                "r":"Référentiels",
                "x":"Données Confidentielles",
                "e":"Données extérieures",
                "z":"Administration"
                }
    carDebut, carFin = '[', ']'
    dicWithValue = listBlocs
    if not FileExiste(monFichierParam) :
       createParam(monFichierParam, dicWithValue, mBlocs, carDebut, carFin)

    return loadParam(monFichierParam, mBlocs, carDebut, carFin)
    
#==================================================
def loadParam(monFichierParam, mBlocs, carDebut, carFin):
    #Génération du dic
    sVar_bonne_ligne = mBlocs
    sChaineDebut, sChaineFin, dicoValue = carDebut, carFin, {}
    zFileParam = open(monFichierParam, "r",encoding="utf-8")

    for zFileParamLigne in zFileParam :

        if sVar_bonne_ligne in zFileParamLigne :
           posinf = zFileParamLigne.index(sChaineDebut)
           possup = zFileParamLigne.index(sChaineFin)
           sdic_IveVariables = zFileParamLigne[posinf + 1:possup]

           for sCouple in sdic_IveVariables.split(",") :
               sMyCle   = sCouple[0:sCouple.index(":")].strip()
               sMyValue = sCouple[sCouple.index(":") + 1:].strip()
               dicoValue[sMyCle] = sMyValue
               
    zFileParam.close()
    return dicoValue

#==================================================
#Creation du fichier paramètre
#==================================================
def createParam(monFichierParam, dicWithValue, mBlocs,  carDebut, carFin) :

    if not FileExiste(monFichierParam) :
       carSep = "#"
       zFileParam = open(monFichierParam, "w",encoding="utf-8")
       zContenu = u"# (c) Didier  LECLERC 2020 CMSIG MTES-MCTRCT/SG/SNUM/UNI/DRC Site de Rouen\n"
       zContenu += u"# créé le " + time.strftime("%d ") + zMyFrenchMonth(float(time.strftime("%m"))) + time.strftime(" %Y - %Hh%Mm%Ss") + "\n"
       zContenu += "\n"
       zContenu += mBlocs + " = " + carDebut

       for key, value in dicWithValue.items():
           zContenu += str(key) + ":" + str(value) + ","
       zContenu = zContenu[:len(zContenu)-1] + carFin + "\n"
       zFileParam.write(zContenu)
       zFileParam.close()
       return    

#==================================================
def returnVersion() : return "version 1.3.4"

#==================================================
def returnSiVersionQgisSuperieureOuEgale(_mVersTexte) :
    _mVersMax = 1000000  #Valeur max arbitraire
    try :
       _mVers = qgis.utils.Qgis.QGIS_VERSION_INT
    except : 
       _mVers = _mVersMax
    if _mVersTexte == "3.4.5" :
       _mBorne = 30405
       _mMess = "_mVers >= '3.4.5'"                    
    elif _mVersTexte == "3.10" : 
       _mBorne = 31006
       _mMess = "_mVers >= '3.10'" 
    elif _mVersTexte == "3.16" : 
       _mBorne = 31605
       _mMess = "_mVers >= '3.16'" 
    elif _mVersTexte == "3.18" : 
       _mBorne = 31801
       _mMess = "_mVers >= '3.18'"
    elif _mVersTexte == "3.20" : 
       _mBorne = 32002
       _mMess = "_mVers >= '3.20'"
    elif _mVersTexte == "3.21" : 
       _mBorne = 33000
       _mMess = "_mVers >= '3.21'"

    return True if _mVers >= _mBorne else False

#==================================================
def returnInstalleEtVersionPlume(self) :
    mKeySql = dicListSql(self,'ReturnInstalleEtVersionPlume')
    r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSql(self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
    installeVersion = None
    defautVersion   = None
    dbName = None
    if len(r) != 0 : # Cas où les fichiers d'installation de l'extension sont absents
       if r != None :
          installeVersion = r[0][2]     # Version installée ou None si pas installée
          defautVersion   = r[0][1]     # Version par défaut 
          dbName          = r[0][4]     # Nom de la base 
       else :
          #Géré en amont dans la fonction executeSqlNoReturn
          pass
    #else :
    #   self.Dialog.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'ExtensionPasInstalleePlume', '')
    return installeVersion, defautVersion, dbName

#==================================================
def etatMenuGestionDeLaBasePlume(self, installe_error_plume) :
    #Affichage mess d'informations
    zTitlePlume = QtWidgets.QApplication.translate("bibli_asgard", 'Warning !!!') 
    zTitlePlume = "<font color=\"#0026FF\">" + zTitlePlume + "</font>  "
    zMessPlume = QtWidgets.QApplication.translate("bibli_asgard", 'An update is available for the PLUME extension.')
    zMessPlume += " ==== " + QtWidgets.QApplication.translate("bibli_asgard", 'The option is available in the "Database management" menu.')
    zMessPlume ="<b><font color=\"#0026FF\";>" + zMessPlume + "</font></b>"
    
    if installe_error_plume : 
       if self.isSuperUser :
          if self.plumeVersionDefaut :
             self.installerPlume.setVisible(True)
             self.installerPlume.setEnabled(True)
          else :
             self.installerPlume.setVisible(False)
             self.installerPlume.setEnabled(False)
       else :
          self.installerPlume.setVisible(True)
          self.installerPlume.setEnabled(False)
       #-
       self.majPlume.setVisible(False)
       self.majPlume.setEnabled(False)
       #-
       self.desinstallerPlume.setVisible(False)
       self.desinstallerPlume.setEnabled(False)
    else :
       self.installerPlume.setVisible(False)
       self.installerPlume.setEnabled(False)
       #-
       self.majPlume.setVisible(True)
       #-
       self.desinstallerPlume.setVisible(True)
       #-
       #self.labelInfo.clear()
       if self.isSuperUser :
          if self.plumeVersionDefaut != self.plumeInstalle :
             self.majPlume.setEnabled(True)
             #Affiche info si MAJ version 
             self.barInfo.pushMessage(zTitlePlume, zMessPlume, Qgis.Info, duration = self.durationBarInfo)        
          else :
             self.majPlume.setEnabled(False)
          #-
          self.desinstallerPlume.setEnabled(True)
       else :
          self.majPlume.setEnabled(False)
          #-
          self.desinstallerPlume.setEnabled(False)
    return  

#==================================================
def returnInstalleEtVersionAsgard(self) :
    mKeySql = dicListSql(self,'ReturnInstalleEtVersion')
    r, zMessError_Code, zMessError_Erreur, zMessError_Diag = self.Dialog.mBaseAsGard.executeSql(self.Dialog.mBaseAsGard.mConnectEnCoursPointeur, mKeySql)
    installeVersion = None
    defautVersion   = None
    dbName = None
    if len(r) != 0 : # Cas où les fichiers d'installation de l'extension sont absents
       if r != None :
          installeVersion = r[0][2]     # Version installée ou None si pas installée
          defautVersion   = r[0][1]     # Version par défaut 
          dbName          = r[0][4]     # Nom de la base 
       else :
          #Géré en amont dans la fonction executeSqlNoReturn
          pass
    else :
       self.Dialog.dialogueConfirmationAction(self.Dialog, self.mBaseAsGard, 'ExtensionPasInstallee', '')
    return installeVersion, defautVersion, dbName
     
#==================================================
def etatMenuGestionDeLaBase(self, installe_error) :
    #installe_error
    self.reinitAllSchemas.setEnabled(False if installe_error else True)
    self.diagnosticAsgard.setEnabled(False if installe_error else True)
    self.membreGconsult.setEnabled(False if installe_error else True)
    self.nettoieRoles.setEnabled(False if installe_error else True)
    self.referencerAllSchemas.setEnabled(False if installe_error else True)
    self.importNomenclature.setEnabled(False if installe_error else True)
    self.tableauBord.setEnabled(False if installe_error else True)
    #Affichage mess d'informations
    zTitle = QtWidgets.QApplication.translate("bibli_asgard", 'Warning !!!') 
    zTitle = "<font color=\"#0026FF\">" + zTitle + "</font>  "
    zMess = QtWidgets.QApplication.translate("bibli_asgard", 'An update is available for the ASGARD extension.')
    zMess += " ==== " + QtWidgets.QApplication.translate("bibli_asgard", 'The option is available in the "Database management" menu.')
    zMess ="<b><font color=\"#0026FF\";>" + zMess + "</font></b>"

    if installe_error : 
       if self.isSuperUser :
          if self.asgardVersionDefaut :
             self.installerAsgard.setVisible(True)
             self.installerAsgard.setEnabled(True)
          else :
             self.installerAsgard.setVisible(False)
             self.installerAsgard.setEnabled(False)
       else :
          self.installerAsgard.setVisible(True)
          self.installerAsgard.setEnabled(False)
       #-
       self.majAsgard.setVisible(False)
       self.majAsgard.setEnabled(False)
       #-
       self.desinstallerAsgard.setVisible(False)
       self.desinstallerAsgard.setEnabled(False)
    else :
       self.installerAsgard.setVisible(False)
       self.installerAsgard.setEnabled(False)
       #-
       self.majAsgard.setVisible(True)
       #-
       self.desinstallerAsgard.setVisible(True)
       #-
       #self.labelInfo.clear()
       if self.isSuperUser :
          if self.asgardVersionDefaut != self.asgardInstalle :
             self.majAsgard.setEnabled(True)
             #Affiche info si MAJ version 
             self.barInfo.pushMessage(zTitle, zMess, Qgis.Info, duration = self.durationBarInfo)        
          else :
             self.majAsgard.setEnabled(False)
          #-
          self.desinstallerAsgard.setEnabled(True)
       else :
          self.majAsgard.setEnabled(False)
          #-
          self.desinstallerAsgard.setEnabled(False)
       
    # pour F5
    for a in self.mMenuDialog.children() :
        if a.text() == "Actualiser" :
           a.setEnabled(False if installe_error else True)
           break
           
    #- For PLUME
    etatMenuGestionDeLaBasePlume(self, self.installe_error_plume)

    return  
#==================================================
def zMyFrenchMonth(zNumberMonth):
    aMyFrenchMonth = {1:"Janvier", 2:"Février", 3:"Mars",4:"Avril",5:"Mai",6:"Juin",7:"Juillet",8:"Août",9:"Septembre",10:"Octobre",11:"Novembre",12:"Décembre"}
    return aMyFrenchMonth[zNumberMonth]

#==================================================
def returnChange(dicOld, dicNew) : 
    mReturnChange = False
    for key in dicOld.keys():
        if dicOld[key] != dicNew[key] :
           mReturnChange = True
           break
    return mReturnChange        

#==================================================
def cleanMessError(mMess) :
    mContext = "CONTEXT:"
    mErreur  = "ERREUR:"  
    mHint    = "HINT:"  
    mDetail  = "DETAIL:"
    mMess = mMess[0:mMess.find(mContext)].lstrip() if mMess.find(mContext) != -1 else mMess
    mMess = mMess[0:mMess.find(mErreur)].lstrip() + mMess[mMess.find(mErreur) + len(mErreur):].lstrip() if mMess.find(mErreur) != -1 else mMess
    mMess = mMess[0:mMess.find(mHint)].lstrip() + "<br><br>" + mMess[mMess.find(mHint) + len(mHint):].lstrip() if mMess.find(mHint) != -1 else mMess
    mMess = mMess[0:mMess.find(mDetail)].lstrip() + "<br><br>" + mMess[mMess.find(mDetail) + len(mDetail):].lstrip() if mMess.find(mDetail) != -1 else mMess
    return mMess 
 
#==================================================
def dialogueMessageError(mTypeErreur, zMessError_Erreur):
    d = doerreur.Dialog(mTypeErreur, zMessError_Erreur)
    d.exec_()
        
#==================================================
def returnIcon( iconAdress) :
    iconSource = iconAdress
    iconSource = iconSource.replace("\\","/")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(iconSource), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    icon.actualSize(QSize(15, 15))
    return icon 

#==================================================
def resizeIhm(self, l_Dialog, h_Dialog) :
    self.Dialog.tabWidget.setGeometry(QtCore.QRect(10, 70, l_Dialog -20 ,h_Dialog - 130))
    self.Dialog.displayInformations.setGeometry(QtCore.QRect(10, 10, self.Dialog.tabWidget.width() -20 ,self.Dialog.tabWidget.height() - 40))
    self.groupBoxAffichageLeft.setGeometry(QtCore.QRect(0,0,(self.Dialog.displayInformations.width() - 40)/2,self.Dialog.displayInformations.height() - 0))
    #----
    self.Dialog.displayInformationsDroits.setGeometry(QtCore.QRect(10, 10, self.Dialog.tabWidget.width() -20 ,self.Dialog.tabWidget.height() - 40))
    self.groupBoxAffichageLeftDroits.setGeometry(QtCore.QRect(0,0,(self.Dialog.displayInformationsDroits.width() - 10) * self.Dialog.mSectionGauche,self.Dialog.displayInformationsDroits.height() - 0))
    #----
    self.groupBoxDown.setGeometry(QtCore.QRect(10,h_Dialog - 50,l_Dialog -20,40))    
    self.okhButton.setGeometry(QtCore.QRect(((self.Dialog.displayInformations.width() -200) / 3) + 100 + ((self.Dialog.displayInformations.width() -200) / 3), 10, 100,23))
    self.helpButton.setGeometry(QtCore.QRect((self.Dialog.displayInformations.width() -200) / 3, 10, 100,23))
    #----
    self.groupBoxAffichageRight.setGeometry(QtCore.QRect(((self.Dialog.displayInformations.width() - 40)/2) + 20, 0, ((self.Dialog.displayInformations.width() - 40)/2) + 20 ,self.displayInformations.height() - 0))
    self.groupBoxAffichageSchema.setGeometry(QtCore.QRect(10,10,self.groupBoxAffichageRight.width() - 20, 450))
    #----
    self.groupBoxAffichageRightDroits.setGeometry(QtCore.QRect(self.groupBoxAffichageLeftDroits.width() + 10, 0, 400, self.displayInformationsDroits.height() - 0))
    #----
    mX = self.groupBoxAffichageRightDroits.x() + self.groupBoxAffichageRightDroits.width() + 10
    mY = 0
    mL = self.displayInformationsDroits.width() - self.groupBoxAffichageLeftDroits.width() - self.groupBoxAffichageRightDroits.width() - 25
    mH = self.displayInformationsDroits.height() - 0
    self.groupBoxAffichageRightDroitsSchemasZone.setGeometry(QtCore.QRect(mX, mY, mL, mH))
    self.groupBoxAffichageRightDroitsSchemas.setGeometry(QtCore.QRect(2, 2, self.groupBoxAffichageRightDroitsSchemasZone.width() - 4, self.groupBoxAffichageRightDroitsSchemasZone.height() - 4))
    #----
    self.groupBoxAffichageRoleAttribut.setGeometry(QtCore.QRect(0,0,self.Dialog.groupBoxAffichageRightDroits.width() , self.Dialog.groupBoxAffichageRightDroits.height()/2 - 5))
    self.groupBoxAffichageRoleAppart.setGeometry(QtCore.QRect(0, self.Dialog.groupBoxAffichageRightDroits.height()/2 + 5,self.Dialog.groupBoxAffichageRightDroits.width() , self.Dialog.groupBoxAffichageRightDroits.height()/2 - 5))
    self.groupBoxAffichageRoleAppartOut.setGeometry(QtCore.QRect(0, 0 + self.y_button_membreappartient, (self.groupBoxAffichageRoleAppart.width() /2) - 10 , self.groupBoxAffichageRoleAppart.height()))
    self.groupBoxAffichageRoleAppartOutBIS.setGeometry(QtCore.QRect(0, 0 + self.y_button_membreappartient, (self.groupBoxAffichageRoleAppart.width() /2) - 10 , self.groupBoxAffichageRoleAppart.height()))
    self.groupBoxAffichageRoleAppartIn.setGeometry(QtCore.QRect((self.groupBoxAffichageRoleAppart.width() /2) + 10 , 0 + self.y_button_membreappartient, (self.groupBoxAffichageRoleAppart.width() /2) - 10, self.groupBoxAffichageRoleAppart.height() ))
    self.groupBoxAffichageRoleAppartInBIS.setGeometry(QtCore.QRect((self.groupBoxAffichageRoleAppart.width() /2) + 10 , 0 + self.y_button_membreappartient, (self.groupBoxAffichageRoleAppart.width() /2) - 10, self.groupBoxAffichageRoleAppart.height() ))
    #----
    self.Dialog.displayInformationsDash.setGeometry(QtCore.QRect(10, 10, self.Dialog.tabWidget.width() -20 ,self.Dialog.tabWidget.height() - 40))
    self.groupBoxAffichageLeftDash.setGeometry(QtCore.QRect(0,0,(self.displayInformationsDash.width() - 10) * self.mSectionGauche,self.displayInformationsDash.height() - 0))
    #----
    self.Dialog.displayInformationsDiagnostic.setGeometry(QtCore.QRect(10, 10, self.Dialog.tabWidget.width() -20 ,self.Dialog.tabWidget.height() - 40))
    self.zone_affichage_diagnostic.setGeometry(QtCore.QRect(10, 10, self.displayInformationsDiagnostic.width() -20 ,self.displayInformationsDiagnostic.height() - 20))
    #----
    self.Dialog.displayInformationsTableauBord.setGeometry(QtCore.QRect(10, 10, self.Dialog.tabWidget.width() -20 ,self.Dialog.tabWidget.height() - 40))
    self.zone_affichage_TableauBord.setGeometry(QtCore.QRect(10, 10, self.displayInformationsTableauBord.width() -20 ,self.displayInformationsTableauBord.height() - 20))
    #----

    self.groupBoxParametre.setGeometry(QtCore.QRect(10,50,self.groupBoxAffichageLeftDash.width() - 20, 235))
    self.groupBoxRadioPieBar.setGeometry(QtCore.QRect(10,50,self.groupBoxAffichageLeftDash.width() - 20, 45))
    self.groupBoxCheckEtiquette.setGeometry(QtCore.QRect(10,95,self.groupBoxAffichageLeftDash.width() - 20, 65))
    self.groupBoxCheckLegende.setGeometry(QtCore.QRect(10,160,self.groupBoxAffichageLeftDash.width() - 20, 80))
    self.groupBoxCheckTitreAnim.setGeometry(QtCore.QRect(10,240,self.groupBoxAffichageLeftDash.width() - 20, 55))
    self.zoneTitre.setGeometry(QtCore.QRect(50,2,self.groupBoxAffichageLeftDash.width() - 75,20))

    #-
    mX = self.groupBoxAffichageLeftDash.width() + 10
    mY = 0
    mL = self.displayInformationsDash.width() - self.groupBoxAffichageLeftDash.width() - 10
    mH = self.displayInformationsDash.height() - 0
    self.groupBoxAffichageRightDash.setGeometry(QtCore.QRect(mX, mY, mL, mH))
    self.labelChoiceGraph.setGeometry(QtCore.QRect(10,10,self.groupBoxAffichageLeftDash.width() - 20,20))
    self.comboChoiceGraph.setGeometry(QtCore.QRect(10,30,self.groupBoxAffichageLeftDash.width() - 20,23))
 
    self.executeButtonGraphColor.setGeometry(QtCore.QRect((self.groupBoxAffichageLeftDash.width() - 200) / 3, self.groupBoxAffichageLeftDash.height() - 30, 100,23))
    self.executeButtonGraph.setGeometry(QtCore.QRect(((self.groupBoxAffichageLeftDash.width() - 200) / 3 * 2) + 100, self.groupBoxAffichageLeftDash.height() - 30, 100,23))

    if hasattr(self.Dialog, 'mTreeGraphSchemasBlocs') :  #Pas d'affichage de l'instance Treeview
       mYBlocs = self.groupBoxParametre.y() + self.groupBoxParametre.height() + 10
       mHBlocs = (self.groupBoxAffichageLeftDash.height() - (self.groupBoxParametre.y() + self.groupBoxParametre.height() + 50))
       self.mTreeGraphSchemasBlocs.setGeometry(15, mYBlocs, self.groupBoxAffichageLeftDash.width() - 30, mHBlocs)                                                 
    #----
    #----
    self.groupBoxAffichageHelp.setGeometry(QtCore.QRect(10, 10, self.groupBoxAffichageRight.width() - 20, self.groupBoxAffichageRight.height() - 20))
    self.groupBoxAffichageHelpDroits.setGeometry(QtCore.QRect(10, 10, self.groupBoxAffichageRightDroits.width() - 20, self.groupBoxAffichageRightDroits.height() - 20))
    #----

    if hasattr(self.Dialog, 'mTreePostgresql') :  #Pas d'affichage de l'instance Treeview
       y = 35  # 15
       self.mTreePostgresql.setGeometry(15, y, self.groupBoxAffichageLeft.width() - 30, self.groupBoxAffichageLeft.height() - 50)
    if hasattr(self.Dialog, 'mTreePostgresqlDroits') :  #Pas d'affichage de l'instance Treeview
       self.mTreePostgresqlDroits.setGeometry(15, 15, self.groupBoxAffichageLeftDroits.width() - 30, self.groupBoxAffichageLeftDroits.height() - 30)
    if hasattr(self.Dialog, 'mTreePostgresqlSchemaLecteur') :  #Pas d'affichage de l'instance Treeview
       self.mTreePostgresqlSchemaLecteur.setGeometry(5, ((self.Dialog.groupBoxAffichageLeftDroits.height()/3) *2) + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)
       #self.mTreePostgresqlSchemaLecteur.setGeometry(5, 5,  self.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.groupBoxAffichageLeftDroits.height() - 20)/3)
    if hasattr(self.Dialog, 'mTreePostgresqlSchemaEditeur') :  #Pas d'affichage de l'instance Treeview
       self.mTreePostgresqlSchemaEditeur.setGeometry(5, self.Dialog.groupBoxAffichageLeftDroits.height()/3 + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)
    if hasattr(self.Dialog, 'mTreePostgresqlSchemaProducteur') :  #Pas d'affichage de l'instance Treeview
       self.mTreePostgresqlSchemaProducteur.setGeometry(5, 5,  self.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.groupBoxAffichageLeftDroits.height() - 20)/3)
       #self.mTreePostgresqlSchemaProducteur.setGeometry(5, ((self.Dialog.groupBoxAffichageLeftDroits.height()/3) *2) + 5,  self.Dialog.groupBoxAffichageRightDroitsSchemas.width() - 10, (self.Dialog.groupBoxAffichageLeftDroits.height() - 20)/3)

    #----
    bibli_asgard.showHideCtrlSimpleComplet(self, self.case_simplecomplet.isChecked())    
    #---- Aide générique DROITS
    if hasattr(self.Dialog, 'mTreePostgresqlDroits') :  #Pas d'affichage de l'instance Treeview
     if hasattr(self.Dialog.mTreePostgresqlDroits, 'mNameEnCours'):
        mDeltaImgLib = 10 + 45
        mRatio = 0.14
        if self.Dialog.mTreePostgresqlDroits.mNameEnCours == "Rôles de connexion" : 
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib100, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib100.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib100.setText(self.mLibTitre100 + '<br>{}'.format('<br>'.join(mLib)))
          bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [100])
        elif self.Dialog.mTreePostgresqlDroits.mNameEnCours == "Rôles de groupe"  :
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib101, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib101.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib101.setText(self.mLibTitre101 + '<br>{}'.format('<br>'.join(mLib)))
          bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [101])
        else :
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib102, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib102.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib102.setText(self.mLibTitre102 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib103, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib103.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib103.setText(self.mLibTitre103 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib104, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib104.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib104.setText(self.mLibTitre104 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib105, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib105.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib105.setText(self.mLibTitre105 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib106, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib106.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib106.setText(self.mLibTitre106 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib107, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib107.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib107.setText(self.mLibTitre107 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib1060, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib1060.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib1060.setText(self.mLibTitre1060 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib1070, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib1070.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib1070.setText(self.mLibTitre1070 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib108, self.Dialog.groupBoxAffichageHelpDroits.width() * mRatio)
          mhauteur = (2 if len(mLib) == 1 else len(mLib))
          self.lib108.resize(self.Dialog.groupBoxAffichageHelpDroits.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
          self.lib108.setText(self.mLibTitre108 + '<br>{}'.format('<br>'.join(mLib)))
          #---------
          if hasattr(self.Dialog, 'mTreePostgresql') :  #Pas d'affichage de l'instance Treeview
             if hasattr(self.Dialog.mTreePostgresql, 'mNameEnCours'):
                if hasattr(self, 'ArraymRolesDeGroupe'):
                   if self.Dialog.mTreePostgresql.mNameEnCours in [ elem[0] for elem in self.ArraymRolesDeGroupe if elem[5]== True ] :
                      mRG = 'connexion' 
                   elif self.Dialog.mTreePostgresql.mNameEnCours in [ elem[0] for elem in self.ArraymRolesDeGroupe if elem[5]== False ] :
                      mRG = 'groupe' 
                   #---------
                   if mRG == 'connexion' : 
                      if self.Dialog.mTreePostgresqlDroits.mDepartTransfertDroitCouper == "" :
                        bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [104,102,106,108])
                      else :
                        bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [104,102,107,108])
                   elif mRG == 'groupe' :
                      if self.Dialog.mTreePostgresqlDroits.mDepartTransfertDroitCouper == "" :
                        bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [105,103,106,108])
                      else :
                        bibli_ihm_asgard.genereAideDynamiqueDroits(self,"UPDATE", [105,103,107,108])

    #----  Aide générique
    if hasattr(self.Dialog, 'mTreePostgresql') :  #Pas d'affichage de l'instance Treeview
     if hasattr(self.Dialog.mTreePostgresql, 'mNameEnCours'):
        mDeltaImgLib = 10 + 45
        mRatio = 0.14
        #---------
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib1, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib1.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib1.setText(self.mLibTitre1 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib2, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib2.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib2.setText(self.mLibTitre2 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib3, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib3.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib3.setText(self.mLibTitre3 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib4, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib4.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib4.setText(self.mLibTitre4 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib5, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib5.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib5.setText(self.mLibTitre5 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib6, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib6.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib6.setText(self.mLibTitre6 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib7, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib7.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib7.setText(self.mLibTitre7 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib8, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib8.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib8.setText(self.mLibTitre8 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib9, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib9.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib9.setText(self.mLibTitre9 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib10, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib10.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib10.setText(self.mLibTitre10 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib11, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib11.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib11.setText(self.mLibTitre11 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib12, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib12.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib12.setText(self.mLibTitre12 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib13, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib13.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib13.setText(self.mLibTitre13 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib14, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib14.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib14.setText(self.mLibTitre14 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib15, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib15.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib15.setText(self.mLibTitre15 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib16, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib16.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib16.setText(self.mLibTitre16 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib17, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib17.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib17.setText(self.mLibTitre17 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib18, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib18.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib18.setText(self.mLibTitre18 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib19, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib19.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib19.setText(self.mLibTitre19 + '<br>{}'.format('<br>'.join(mLib)))

        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib20, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib20.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib20.setText(self.mLibTitre20 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib21, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib21.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib21.setText(self.mLibTitre21 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib22, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib22.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib22.setText(self.mLibTitre22 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib23, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib23.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib23.setText(self.mLibTitre23 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib24, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib24.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib24.setText(self.mLibTitre24 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib25, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib25.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib25.setText(self.mLibTitre25 + '<br>{}'.format('<br>'.join(mLib)))
        #-
        mLib = bibli_ihm_asgard.returnListeTexte(self, self.mLib26, self.Dialog.groupBoxAffichageHelp.width() * mRatio)
        mhauteur = (2 if len(mLib) == 1 else len(mLib))
        self.lib26.resize(self.Dialog.groupBoxAffichageHelp.width() - mDeltaImgLib, (  mhauteur * 21) + 0)
        self.lib26.setText(self.mLibTitre26 + '<br>{}'.format('<br>'.join(mLib)))
        #---------

        #Blocs fonctionnels y compris Corbeille
        if self.Dialog.mTreePostgresql.mNameEnCours in [ libZoneActive[0] for libZoneActive in self.Dialog.mTreePostgresql.mListBlocs] : 
           if self.Dialog.mTreePostgresql.mNameEnCours != "Corbeille" :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [1])
           else :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [6])
        #Actifs
        elif self.Dialog.mTreePostgresql.mNameEnCours in [ libZoneActive[0] for libZoneActive in self.Dialog.mTreePostgresql.mListSchemaActifs] : 
           if self.Dialog.mTreePostgresql.mNameEnCours not in [ libZoneActive[0] for libZoneActive in self.Dialog.mTreePostgresql.mListSchemaCorbeilleActifs] : 
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [2,3,10,15,12,13])
           else :
              #Corbeille Actifs
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [7,8,12,13])
        #Non Actifs
        elif self.Dialog.mTreePostgresql.mNameEnCours in [ libZoneActive[0] for libZoneActive in self.Dialog.mTreePostgresql.mListSchemaNonActifs] : 
           if self.Dialog.mTreePostgresql.mNameEnCours not in [ libZoneActive[0] for libZoneActive in self.Dialog.mTreePostgresql.mListSchemaCorbeilleNonActifs] : 
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [4,5])
           else :
              #Corbeille Non Actifs
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [7,4])
        #Existant (Hors asgard)
        elif self.Dialog.mTreePostgresql.mNameEnCours in [ libZoneActive[0] for libZoneActive in self.Dialog.mTreePostgresql.mListSchemaExistants] :
           if self.Dialog.mTreePostgresql.mNameEnCours == "public" :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [0])
           else :
              bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [9, 16, 14])
              #bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [9,12,13])
        #Tous les objets d'un schéma
        elif self.Dialog.mTreePostgresql.mNameEnCours in [ mNameObjet[1] for mNameObjet in self.Dialog.mTreePostgresql.mArraySchemasTables] : 
             mReturnValueItemTemp = self.Dialog.mTreePostgresql.returnValueItem(self.Dialog.mTreePostgresql.item, 0)
             mSchemaClic, mObjetClic = mReturnValueItemTemp[1], mReturnValueItemTemp[0]
             #----
             for mNameObjet in self.Dialog.mTreePostgresql.mArraySchemasTables  :
                # et Meme Nom
                if mObjetClic == mNameObjet[1] and mSchemaClic == mNameObjet[0] :
                   # Nom objet, type objet et schema de l'objet
                   mReturnValueItemTemp = [mNameObjet[1], mNameObjet[2], mNameObjet[0]]
                   break

             if mReturnValueItemTemp[1] in self.Dialog.mTreePostgresql.mListeObjetArepliquer : #si les objets sont Table, vue et vue mat
                existeDansMetadata, repliquerMetadata, objetIcon = self.Dialog.mTreePostgresql.returnReplique(mReturnValueItemTemp[2], mReturnValueItemTemp[0], mReturnValueItemTemp[1], self.Dialog.mListeMetadata, self.mTreePostgresql.mListeObjetArepliquer)
                if existeDansMetadata : 
                   if repliquerMetadata :
                      bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13, 19])
                   else :
                      bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13, 18])
                else :
                   bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17, 11, 13, 18])
             else :
                bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [17,11,13])

        # ** For layer_styles **
        elif self.Dialog.mTreePostgresql.mNameEnCours == self.Dialog.mTreePostgresql.mNameLayerStyles :
             bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [200, 20, 21, 22, 23, 24, 25, 26])
        else : 
          bibli_ihm_asgard.genereAideDynamique(self,"UPDATE", [0])
    #Réinit les dimensions de l'IHM
    bibli_asgard.returnAndSaveDialogParam(self, "Save")
    mDic_LH = bibli_asgard.returnAndSaveDialogParam(self, "Load")
    self.Dialog.lScreenDialog, self.Dialog.hScreenDialog = int(mDic_LH["dialogLargeur"]), int(mDic_LH["dialogHauteur"])
    #----
    return  
    
#=For Printer
def printViewDiagnostic(self, Dialog):
    printer = QPrinter()
    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageSize(QPrinter.A4)
    printer.setOrientation(QPrinter.Landscape)
    printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter )    
    printer.setOutputFormat(QPrinter.NativeFormat)
    #-
    printDialog = QPrintPreviewDialog(printer)
    printDialog.setWindowModality(QtCore.Qt.WindowModal)
    printDialog.setModal(True)
    zTitle = QtWidgets.QApplication.translate("confirme_ui", "ASGARD MANAGER : Anomalies detected", None)
    printDialog.setWindowTitle(zTitle)
    printDialog.setWindowState(Qt.WindowNoState)
    #-
    printDialog.paintRequested.connect(Dialog.zone_affichage_diagnostic.print_)
    printDialog.exec_() 
    return

#--------
def deletetViewDiagnostic(self, Dialog):
    Dialog.zone_affichage_diagnostic.setHtml('')
    return
    
#--------
def printViewTableauBord(self, Dialog):
    printer = QPrinter()
    printer = QPrinter(QPrinter.HighResolution)
    printer.setPageSize(QPrinter.A4)
    printer.setOrientation(QPrinter.Landscape)
    printer.setPageMargins(10, 10, 10, 10, QPrinter.Millimeter )    
    printer.setOutputFormat(QPrinter.NativeFormat)
    #-
    printDialog = QPrintPreviewDialog(printer)
    printDialog.setWindowModality(QtCore.Qt.WindowModal)
    printDialog.setModal(True)
    zTitle = QtWidgets.QApplication.translate("confirme_ui", "ASGARD MANAGER : Dashboard", None)
    printDialog.setWindowTitle(zTitle)
    printDialog.setWindowState(Qt.WindowNoState)
    #-
    printDialog.paintRequested.connect(Dialog.zone_affichage_TableauBord.print_)
    printDialog.exec_() 
    return

#--------
def csvTableauBord(self, Dialog):
    #Sauvegarde de la boite de dialogue Fichiers
    InitDir = os.path.dirname(__file__) + "\\" + "AM_Export_Csv_" + time.strftime("%Y%m%d_%Hh%Mm%S") + ".csv"
    TypeList = QtWidgets.QApplication.translate("bibli_graph_asgard", "Dashboard Export CSV", None) + " (*.csv)"
    fileName = QFileDialog.getSaveFileName(None,QtWidgets.QApplication.translate("bibli_graph_asgard", "Asgard Manager Dashboard Export CSV", None),InitDir,TypeList)
    if fileName[0] != "" : 
       # csv header
       header = self.Dialog.contenuCSV[0]
       data = self.Dialog.contenuCSV[1]
       with open(fileName[0], 'w', encoding='utf-8', newline='') as f:
           writer = csv.writer(f, delimiter=";")
           writer.writerow(header)
           writer.writerows(data)
    return        

#--------
def deletetViewTableauBord(self, Dialog):
    Dialog.zone_affichage_TableauBord.setHtml('')
    return        
#==================================================
#Execute Pdf 
#==================================================
def execPdf(nameciblePdf):
    paramGlob = nameciblePdf            
    os.startfile(paramGlob)

    return            
#==================================================
def getThemeIcon(theName):
    myPath = CorrigePath(os.path.dirname(__file__))
    myDefPathIcons = myPath + "\\icons\\logo\\"
    myDefPath = myPath.replace("\\","/")+ theName
    myDefPathIcons = myDefPathIcons.replace("\\","/")+ theName
    myCurThemePath = QgsApplication.activeThemePath() + "/plugins/" + theName
    myDefThemePath = QgsApplication.defaultThemePath() + "/plugins/" + theName
    myQrcPath = "python/plugins/asgardmanager/" + theName
    if QFile.exists(myDefPath): return myDefPath
    elif QFile.exists(myDefPathIcons): return myDefPathIcons
    elif QFile.exists(myCurThemePath): return myCurThemePath
    elif QFile.exists(myDefThemePath): return myDefThemePath
    elif QFile.exists(myQrcPath): return myQrcPath
    else: return theName

#==================================================
def CorrigePath(nPath):
    nPath = str(nPath)
    a = len(nPath)
    subC = "/"
    b = nPath.rfind(subC, 0, a)
    if a != b : return (nPath + "/")
    else: return nPath

def transformeBorneXml(zText) :
    zText = zText.replace("@@",">") 
    zText = zText.replace("@","<")
    return zText
    
#==================================================
#==================================================
#==================================================
#==================================================
def displayMess(mDialog, type,zTitre,zMess, level=Qgis.Critical, duration = 10):
    #type 1 = MessageBar
    #type 2 = QMessageBox
    if type == 1 :
       mDialog.barInfo.clearWidgets()
       mDialog.barInfo.pushMessage(zTitre, zMess, level=level, duration = duration)
    else :
       QMessageBox.information(None,zTitre,zMess)
    return  
#--
def debugMess(type,zTitre,zMess, level=Qgis.Critical):
    #type 1 = MessageBar
    #type 2 = QMessageBox
    if type == 1 :
       qgis.utils.iface.messageBar().pushMessage(zTitre, zMess, level=level)
    else :
       QMessageBox.information(None,zTitre,zMess)
    return  

#==================================================
# FIN
#==================================================
