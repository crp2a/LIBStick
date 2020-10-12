#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:42:42 2020

@author: yannick
"""

import numpy,os
import LIBStick_echange_vars

###############################################################################
# 1- fonctions
###############################################################################
def extraction_spectres(tableau_norm):
    #tableau_extrait=LIBStick_creation_tableau_norm.tableau_norm.copy()
    tableau_extrait=tableau_norm.copy()
#    print ("format tableau initial : ")
#    print(tableau_extrait.shape)
    indice_premier=(LIBStick_echange_vars.L_ext_bornes_moyenne_spectres[0]-1)
    indice_dernier=(LIBStick_echange_vars.L_ext_bornes_moyenne_spectres[1]-1)
    cols_supprime_debut=list()
    cols_supprime_fin=list()
    if indice_premier > 0 :
        for i in range(0,indice_premier) :
            cols_supprime_debut.append(i)
    if indice_dernier < LIBStick_echange_vars.L_ext_nombre_fichiers :
        for i in range(indice_dernier+1, LIBStick_echange_vars.L_ext_nombre_fichiers):
            cols_supprime_fin.append(i)
    cols_supprime=cols_supprime_debut+cols_supprime_fin
#    print ("colonnes à supprimer : ")
#    print(cols_supprime)         
    tableau_extrait=numpy.delete(tableau_extrait, cols_supprime, axis=1)    
#    print ("format tableau extrait : ")
#    print(tableau_extrait.shape)    
    return tableau_extrait

def creation_spectre_moyen(tableau_extrait):
    spectre_moyen=tableau_extrait.sum(axis=1)
    spectre_moyen=spectre_moyen/tableau_extrait.shape[1]
#    print("format spectre moyen : ")
#    print(spectre_moyen.shape)
    return spectre_moyen

def enregistre_fichier(spectre_moyen, nom_echantillon, bornes):
    nom_fichier=nom_echantillon+"_spectre_moyen_"+ str(bornes[0])+"_"+str(bornes[1])+".mean"
    nom_fichier=str(numpy.char.replace(nom_fichier, " ", "_"))
    numpy.savetxt(nom_fichier,spectre_moyen,delimiter="\t", newline="\n")
#    print (nom_fichier)
    
###############################################################################
# programme principal
###############################################################################
def main (rep_travail,nom_echantillon, bornes) :
#    print("===========================================")
    os.chdir(rep_travail)
    tableau_norm=numpy.loadtxt("tableau_normalisé.txt",delimiter="\t",dtype=float,encoding="Latin-1")
    tableau_extrait=extraction_spectres(tableau_norm)
    spectre_moyen=creation_spectre_moyen(tableau_extrait)
    enregistre_fichier(spectre_moyen, nom_echantillon, bornes)
    return spectre_moyen
