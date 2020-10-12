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

import sys,os
import numpy

import LIBStick_creation_tableau_norm

sys.path.insert(0,os.path.join(os.path.expanduser("~"),"Desktop"))
sys.path.insert(0,"./dossier_mes_modules/")

###############################################################################
# 1- fonction qui liste des fichiers *.asc d'un répertoire
###############################################################################
def creation_liste_fichiers(rep_travail, type_fichier):
    os.chdir(rep_travail)
    liste=[]
    if type_fichier == ".asc" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "asc") :
                liste.append(fichier)
    if type_fichier == ".tsv" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "tsv") :
                liste.append(fichier)
    liste.sort()
    return liste

def creation_nom_echantillon(liste_fichiers):
    nom_echantillon=liste_fichiers[0][0:-6]
    return nom_echantillon

###############################################################################
# 2- fonction qui ouvre un fichier et extrait les lignes de 528 à 543 nm ou de 592 à 608 nm
###############################################################################
def lit_fichier(fichier, bas, haut, type_fichier):
    document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
    document_tronc=numpy.zeros((0,2))
    for ligne in document :
        if (ligne[0]>=bas and ligne[0]<=haut) :
            document_tronc=numpy.row_stack((document_tronc,ligne))
            #document_tronc=numpy.vstack((document_tronc,ligne)) #idem ci-dessus
    return document_tronc

def lit_spectre(fichier, type_fichier):
    if type_fichier == ".asc" :
        document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
        spectre=numpy.zeros((0,2))
        for ligne in document :
            if (ligne[0]<=1013) :
                spectre=numpy.row_stack((spectre,ligne))
    if type_fichier == ".tsv" :
        spectre=numpy.loadtxt(fichier,delimiter="\t",usecols=[0,1],dtype=float,encoding="Latin-1")
    return spectre

###############################################################################
# 3- fonction qui crée un sous répertoire d'un certain nom passé en argument
###############################################################################
def repertoire_de_travail(rep_script,rep_travail_relatif):
    rep_travail=rep_script+"/"+rep_travail_relatif
    return rep_travail

def creation_sous_repertoire(rep_travail,tableau_bornes, flag_zone2):
    if flag_zone2 :
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1]))
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1]))
    if flag_zone2 == 0 :
         if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1]))

###############################################################################
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###############################################################################
def enregistre_fichier(document,repertoire,nom_fichier):
    os.chdir(repertoire)
    nom_fichier=nom_fichier[0:-4] + "_" + repertoire[-11:] +".tsv"
    numpy.savetxt(nom_fichier,document, delimiter="\t")
     
###############################################################################
# programme principal
###############################################################################
def main(rep_travail, tableau_bornes, type_fichier, liste_fichiers, flag_zone2, flag_2D, flag_3D) :
    rep_script=os.getcwd()
    if flag_zone2 == 0 :
        tableau_bornes=numpy.delete(tableau_bornes, (1), axis=0)
    creation_sous_repertoire(rep_travail,tableau_bornes, flag_zone2)
    nom_echantillon=creation_nom_echantillon(liste_fichiers)       
    for i in range(len(liste_fichiers)) :
        for bornes in tableau_bornes :
            os.chdir(rep_travail)
            document=lit_fichier(liste_fichiers[i], bornes[0], bornes[1], type_fichier)
            enregistre_fichier(document,rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1]) ,liste_fichiers[i])
    for bornes in tableau_bornes :
        os.chdir(rep_script)
        tableau_abscisses = LIBStick_creation_tableau_norm.main(rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1])+"/", nom_echantillon,bornes, flag_2D, flag_3D)
    return nom_echantillon
    
