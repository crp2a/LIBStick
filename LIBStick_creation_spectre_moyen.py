#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 14:42:42 2020

@author: yannick
"""

import numpy,os

###############################################################################
# 1- fonctions
###############################################################################
def creation_spectre_moyen_avec_x(tableau_norm, bornes_moyenne_spectres):
    tableau_abscisses=tableau_norm[:,0]
    tableau_extrait=tableau_norm[:,1:]
    indice_premier=(bornes_moyenne_spectres[0]-1)
    indice_dernier=(bornes_moyenne_spectres[1])
    tableau_extrait=tableau_extrait[:,indice_premier:indice_dernier]
    spectre_moyen=tableau_extrait.sum(axis=1)
    spectre_moyen=spectre_moyen/tableau_extrait.shape[1]
    spectre_moyen=numpy.column_stack((tableau_abscisses,spectre_moyen))
    return spectre_moyen

def enregistre_fichier(spectre_moyen, nom_echantillon, bornes):
    nom_fichier=nom_echantillon+"_spectre_moyen_"+ str(bornes[0])+"_"+str(bornes[1])+".mean"
    nom_fichier=str(numpy.char.replace(nom_fichier, " ", "_"))
    numpy.savetxt(nom_fichier,spectre_moyen,delimiter="\t", newline="\n")
    
###############################################################################
# programme principal
###############################################################################
def main (rep_travail,nom_echantillon, bornes, bornes_moyenne_spectres) :
    os.chdir(rep_travail)
    tableau_norm=numpy.loadtxt("tableau_normalisé_points.txt",delimiter="\t",dtype=float,encoding="Latin-1")
    spectre_moyen=creation_spectre_moyen_avec_x(tableau_norm, bornes_moyenne_spectres)
    enregistre_fichier(spectre_moyen, nom_echantillon, bornes)
    return spectre_moyen
