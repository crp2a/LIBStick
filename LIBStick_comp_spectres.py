#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:31:54 2020

@author: yannick
"""

import numpy,os,pandas
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3d
import LIBStick_outils

limites_zone1=[534.5 , 535.8]
limites_zone2=[528.0 , 543.0]
limites_spectre=[528.0, 543.0]

###############################################################################
# fonctions création tableaux et DataFrame
###############################################################################
def creer_tableau_avec_x(liste,type_fichier, type_traitement): # données en colonnes
    print(type_fichier)
    if type_traitement == 0 :   # On ne normalise pas les spectres
        tableau=LIBStick_outils.creer_tableau_avec_x_colonne1(liste,type_fichier)
    if type_traitement == 1 :   # On normalise tous les spectres
        tableau=LIBStick_outils.creer_tableau_avec_x_colonne1(liste,type_fichier)
        tableau=LIBStick_outils.normalise_tableau_x_aire(tableau)
    return tableau    

def creer_DataFrame_resultats(DataFrame_comparatif, limites_zone1,limites_zone2,flag_denominateur):
    if flag_denominateur == 1 :
        DataFrame_tableau_calculs=pandas.DataFrame()
        Sous_DataFrame = DataFrame_comparatif.loc[ : , limites_zone1[0]:limites_zone1[1]]
        DataFrame_tableau_calculs["Somme zone 1"] = Sous_DataFrame.sum(axis=1)
        Sous_DataFrame = DataFrame_comparatif.loc[ : , limites_zone2[0]:limites_zone2[1]]
        DataFrame_tableau_calculs["Somme zone 2"] = Sous_DataFrame.sum(axis=1)
        DataFrame_tableau_calculs["Rapport"]=DataFrame_tableau_calculs["Somme zone 1"] / DataFrame_tableau_calculs["Somme zone 2"]
    if flag_denominateur == 0 :
        DataFrame_tableau_calculs=pandas.DataFrame()
        Sous_DataFrame = DataFrame_comparatif.loc[ : , limites_zone1[0]:limites_zone1[1]]
        DataFrame_tableau_calculs["Somme zone 1"] = Sous_DataFrame.sum(axis=1)
    return DataFrame_tableau_calculs

def convertir_Dataframe_resultats_tableau(DataFrame_comparatif):
    tableau=DataFrame_comparatif.values
    tableau= numpy.delete(tableau, -1 , axis=1)
    return tableau

def enregistre_DataFrame_resultats(DataFrame_resultats):
#    DataFrame_resultats.to_csv("Resultat_fichiers_classes.csv")
    DataFrame_resultats.to_excel("Resultat_fichiers_classes.xls")
    DataFrame_resultats.to_csv("Resultat_fichiers_classes.txt", sep='\t', decimal=",")

###############################################################################
# fonctions d'affichage graphique du tableau de résultats
###############################################################################    
def tableau_256gris(tableau_norm):
    tableau8bits=tableau_norm*255
    tableau8bits=tableau8bits.astype(int) 
    return tableau8bits
    
def graphique_creation(tableau8bits,nom_echantillon,limites_spectre):
    #fig=plt.figure()
    fig, ax=plt.subplots()
    #plt.imshow(tableau8bits, cmap="gray", extent=[limites_spectre[0],limites_spectre[1],tableau8bits.shape[0],0], aspect="auto")
    plt.imshow(tableau8bits, cmap="inferno", extent=[limites_spectre[0],limites_spectre[1],tableau8bits.shape[0],0], aspect="auto")
    
    #imageplot=plt.imshow(tableau8bits, cmap="hot")
    #imageplot=plt.imshow(tableau8bits, cmap="nipy_spectral")
    #plt.colorbar()
    plt.title(nom_echantillon)
    plt.xlabel("Longueur d'onde (nm)")
    plt.ylabel( "Spectres echantillons classés")
    plt.yticks(range(0,tableau8bits.shape[0],5))
    ax.yaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    plt.savefig("figure_plot.png")
    #plt.xlim(limites_spectre[0], limites_spectre[1])
    #plt.ioff()
    plt.show(block=False)
    
def graphique_3D_creation(tableau8bits,nom_echantillon,limites_spectre):
    xx, yy = numpy.mgrid[0:tableau8bits.shape[0], 0:tableau8bits.shape[1]]
    #fig = plt.figure(figsize=(15,15))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(xx, yy, tableau8bits ,rstride=1, cstride=1, cmap="inferno",linewidth=0, antialiased=False)
    ax.view_init(80, 30)
    
    plt.title(nom_echantillon)
    plt.ylabel("Longueur d'onde (nm)")
    plt.xlabel( "Spectres suivant z")
    #ax.set_ylim(limites_spectre[0],limites_spectre[1])
    
    plt.xticks(range(0,tableau8bits.shape[0],5))
    ax.xaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.yaxis.set_tick_params(which='minor', bottom=False)

    plt.show(block=False)

def graphique_sauvegarde(tableau8bits) :
    plt.imsave("figure.png",tableau8bits, cmap="inferno")
    
def graphique_lit_tableau():
    tableau_comparatif=plt.imread("figure.png")
    return tableau_comparatif
    
###############################################################################
# programme principal
###############################################################################
def main(rep_travail, liste_fichiers, type_fichier, tableau_bornes,type_traitement,flag_denominateur, flag_2D, flag_3D):
    os.chdir(rep_travail)
    tableau_comparatif = creer_tableau_avec_x(liste_fichiers,type_fichier, type_traitement)
    DataFrame_comparatif=LIBStick_outils.creer_DataFrame_x_tableau_en_colonnes(tableau_comparatif,liste_fichiers) 
    
    limites_zone1[0]=tableau_bornes[0,0]
    limites_zone1[1]=tableau_bornes[0,1]
    limites_zone2[0]=tableau_bornes[1,0]
    limites_zone2[1]=tableau_bornes[1,1]
    
    DataFrame_resultats=creer_DataFrame_resultats(DataFrame_comparatif,limites_zone1,limites_zone2,flag_denominateur)
    if flag_denominateur == 1 :
        DataFrame_comparatif=pandas.concat([DataFrame_comparatif, DataFrame_resultats["Rapport"]], axis=1)
        DataFrame_comparatif=DataFrame_comparatif.sort_values(by=["Rapport"])
        DataFrame_resultats = DataFrame_resultats.sort_values(by=["Rapport"])
        enregistre_DataFrame_resultats(DataFrame_resultats)
    
    if flag_denominateur == 0 :
        DataFrame_comparatif=pandas.concat([DataFrame_comparatif, DataFrame_resultats["Somme zone 1"]], axis=1)
        DataFrame_comparatif=DataFrame_comparatif.sort_values(by=["Somme zone 1"])
        DataFrame_resultats = DataFrame_resultats.sort_values(by=["Somme zone 1"])
        enregistre_DataFrame_resultats(DataFrame_resultats)    
    
    tableau_comparatif=convertir_Dataframe_resultats_tableau(DataFrame_comparatif)
    tableau8bits=tableau_256gris(tableau_comparatif)
    if flag_2D :
        graphique_creation(tableau8bits, "Echantillons classés", limites_spectre)
    if flag_3D :
        graphique_3D_creation(tableau8bits, "Echantillons classés", limites_spectre)
    graphique_sauvegarde(tableau8bits)
    
    return DataFrame_resultats

