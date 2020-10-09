#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:20:38 2020

@author: yannick
"""
###############################################################################
# 1- fonction qui liste des fichiers d'un répertoire
# 2- fonction qui ouvre un fichier et extrait les lignes de 528 à 543 nm ou de 592 à 608 nm
# 3- fonction qui crée un sous répertoire d'un certain nom passé en argument
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
# 5- faire une boucle sur la liste de fichiers
# 6- lire et regrouper les secondes collonnes (spectres) de ces nouveaux fichier
#    sous la forme d'un tableau tsv et sauver un seul fichier
###############################################################################

import sys,os,numpy
import LIBStick_echange_vars
import LIBStick_creation_tableau_norm
sys.path.insert(0,os.path.join(os.path.expanduser("~"),"Desktop"))
sys.path.insert(0,"./dossier_mes_modules/")

###############################################################################
# 1- fonction qui liste des fichiers *.asc d'un répertoire
###############################################################################
def creation_liste_fichiers(rep_travail):
    os.chdir(rep_travail)
    liste=[]
    for fichier in os.listdir():
        if (os.path.isfile(fichier) and fichier[-3:] == "asc") :
            liste.append(fichier)
    liste.sort()
    return liste

def creation_nom_echantillon(liste_fichiers):
    nom_echantillon=LIBStick_echange_vars.L_ext_liste_fichiers[0][0:-6]
    return nom_echantillon

###############################################################################
# 2- fonction qui ouvre un fichier et extrait les lignes de 528 à 543 nm ou de 592 à 608 nm
###############################################################################
def lit_fichier(fichier, bas, haut):
    document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
    document_tronc=numpy.zeros((0,2))
    for ligne in document :
        if (ligne[0]>=bas and ligne[0]<=haut) :
            document_tronc=numpy.row_stack((document_tronc,ligne))
            #document_tronc=numpy.vstack((document_tronc,ligne)) #idem ci-dessus
    return document_tronc

def lit_spectre(fichier):
    document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
    spectre=numpy.zeros((0,2))
    for ligne in document :
        if (ligne[0]<=1013) :
            spectre=numpy.row_stack((spectre,ligne))
    return spectre

###############################################################################
# 3- fonction qui crée un sous répertoire d'un certain nom passé en argument
###############################################################################
def repertoire_de_travail(rep_script,rep_travail_relatif):
    rep_travail=rep_script+"/"+rep_travail_relatif
    return rep_travail

def creation_sous_repertoire(rep_travail,tableau_bornes):
    if LIBStick_echange_vars.L_ext_flag_zone2 :
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1]))
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1]))
    if LIBStick_echange_vars.L_ext_flag_zone2 == 0 :
         if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1]))

###############################################################################
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###############################################################################
def enregistre_fichier(document,repertoire,nom_fichier):
    os.chdir(repertoire)
    nom_fichier=nom_fichier[0:-4] + "_" + repertoire[-7:] +".tsv"
    numpy.savetxt(nom_fichier,document, delimiter="\t")
     
###############################################################################
# programme principal
###############################################################################
def main(rep_travail, tableau_bornes) :
    rep_script=os.getcwd()
    print ("Flag 2 spectre : ")
    print (LIBStick_echange_vars.L_ext_flag_zone2)
    if LIBStick_echange_vars.L_ext_flag_zone2 == 0 :
        tableau_bornes=numpy.delete(tableau_bornes, (1), axis=0)
    creation_sous_repertoire(rep_travail,tableau_bornes)
    #LIBStick_echange_vars.L_ext_liste_fichiers=creation_liste_fichiers(rep_travail)
#    LIBStick_echange_vars.L_ext_nombre_fichiers=len(LIBStick_echange_vars.L_ext_liste_fichiers)
    LIBStick_echange_vars.L_ext_nom_echantillon=creation_nom_echantillon(LIBStick_echange_vars.L_ext_liste_fichiers)       
    for i in range(len(LIBStick_echange_vars.L_ext_liste_fichiers)) :
        for bornes in tableau_bornes :
            os.chdir(rep_travail)
            document=lit_fichier(LIBStick_echange_vars.L_ext_liste_fichiers[i], bornes[0], bornes[1])
            enregistre_fichier(document,rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1]) ,LIBStick_echange_vars.L_ext_liste_fichiers[i])
    for bornes in tableau_bornes :
        os.chdir(rep_script)
        LIBStick_creation_tableau_norm.main(rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1])+"/", LIBStick_echange_vars.L_ext_nom_echantillon,bornes)
    
