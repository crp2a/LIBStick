#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 13:14:38 2020

@author: yannick
"""

import pandas, os


rep_travail="./"

def creation_liste_fichiers(rep_travail):
    os.chdir(rep_travail)
    liste=[]
    for fichier in os.listdir():
        if (os.path.isfile(fichier) and fichier[-3:] == "csv") :
            liste.append(fichier)
    liste.sort()
    return liste

def lit_fichier(rep_travail, fichier) :
#    print(rep_travail)
#    print(fichier)
#    print(rep_travail+fichier)
    DataFrame_element= pandas.read_table(fichier)
    return DataFrame_element

def ajoute_colonne_I_relative(DataFrame_element):
    #DataFrame_element["I relative"]
    #DataFrame_element.insert(3)
    print(DataFrame_element)
    maxi= DataFrame_element["Intensité"].max()
    i=0
    for I in DataFrame_element["Intensité"] :
        DataFrame_element.iloc[i, 3]=I*100/maxi
        i=i+1
    return DataFrame_element

def sauvegarde_element(fichier,DataFrame_element):
    DataFrame_element.to_csv(fichier, sep='\t')
 
    
    
liste=creation_liste_fichiers(rep_travail)
for fichier in liste :
    print(fichier)
    DataFrame_element=lit_fichier(rep_travail, fichier)
    DataFrame_element=ajoute_colonne_I_relative(DataFrame_element)
    print(DataFrame_element)
    sauvegarde_element(fichier,DataFrame_element)