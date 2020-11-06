#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:12:06 2020

@author: yannick
"""

###############################################################################
###############################################################################
# fonctions générales de gestion des repertoires, fichiers et création de DataFrames
###############################################################################
###############################################################################

import numpy,os,pandas


###############################################################################
# fonctions générales de gestion des repertoires et fichiers
###############################################################################

def repertoire_de_travail(rep_script,rep_travail_relatif):
    rep_travail=rep_script+"/"+rep_travail_relatif
    return rep_travail

def creation_liste_fichiers(rep_travail,type_fichier):
    os.chdir(rep_travail)
    liste=[]
    if type_fichier == ".mean" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-4:] == "mean") :
                liste.append(fichier)
    if type_fichier == ".tsv" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "tsv") :
                liste.append(fichier)
    if type_fichier == ".asc" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "asc") :
                liste.append(fichier)
    liste.sort()
    return liste

def lit_spectre(fichier,type_fichier):
    if type_fichier == ".mean" :
        spectre=numpy.loadtxt(fichier,delimiter="\t",dtype=float,encoding="Latin-1")
    if type_fichier == ".tsv" :
        spectre=numpy.loadtxt(fichier,delimiter="\t",dtype=float,encoding="Latin-1")
    if type_fichier == ".asc" :
        document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
        spectre=numpy.zeros((0,2))
        for ligne in document :
            if (ligne[0]<=1013) :
                spectre=numpy.row_stack((spectre,ligne))
    return spectre


###############################################################################
# fonctions générales de création de DataFrame
###############################################################################

# creation tableau avec lambda (1ere colonne) et spectres dans le colonnes suivantes
def creer_tableau_avec_x_colonne1(liste):
    i=0
    for fichier in liste :
        if i==0 :
            tableau=numpy.loadtxt(fichier, delimiter="\t")
        else :
            fichier_entree=numpy.loadtxt(fichier, delimiter="\t", usecols=[1])
            tableau=numpy.column_stack((tableau,fichier_entree))
        i=i+1
    return tableau

# creation tableau avec lambda (1ere ligne) et spectres dans les lignes suivantes
def creer_tableau_avec_x_ligne1(liste):
    i=0
    for fichier in liste :
        if i==0 :
            tableau=numpy.loadtxt(fichier, delimiter="\t")
        else :
            fichier_entree=numpy.loadtxt(fichier, delimiter="\t", usecols=[1])
            tableau=numpy.column_stack((tableau,fichier_entree))
        i=i+1
    tableau=numpy.transpose(tableau)
    return tableau

# creation d'un DFataFrame avec lambda en nom des colonnes et le nom des fichiers en index des lignes        
def creer_DataFrame_x_tableau_en_colonnes(tableau_en_colonnes, liste) :
#    liste[0:0] = ["Lambda (nm)"]
    df=pandas.DataFrame(numpy.transpose(tableau_en_colonnes[:,1:]), index=liste, columns=tableau_en_colonnes[:,0])
    return df

# creation d'un DFataFrame avec lambda en nom des colonnes et le nom des fichiers en index des lignes        
def creer_DataFrame_x_tableau_en_lignes(tableau_en_lignes, liste) :
#    liste[0:0] = ["Lambda (nm)"]
    df=pandas.DataFrame(numpy.transpose(tableau_en_lignes[1:,:]), index=liste, columns=tableau_en_lignes[0,:])
    return df
