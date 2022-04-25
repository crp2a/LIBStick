#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:31:54 2020
Module outils pour les mesures, la comparaison et la classification des spectres
@author: yannick
"""


import os
import numpy
import pandas
import matplotlib.pyplot as plt
#import mpl_toolkits.mplot3d as plt3d
import LIBStick_outils

limites_zone1 = [534.5, 535.8]
limites_zone2 = [528.0, 543.0]
limites_spectre = [528.0, 543.0]


###################################################################################################
# fonctions création tableaux et dataframe
###################################################################################################
def creer_tableau_avec_x(liste, type_fichier, type_traitement):  # données en colonnes
    """
    Crée tableau de tous les spectres du répertoire en colonne, normalisés ou non,
    avec les lambda en colonne 1
    """
    if type_traitement == 0:   # On ne normalise pas les spectres
        tableau = LIBStick_outils.creer_tableau_avec_x_colonne1(liste, type_fichier)
    if type_traitement == 1:   # On normalise tous les spectres
        tableau = LIBStick_outils.creer_tableau_avec_x_colonne1(liste, type_fichier)
        tableau = LIBStick_outils.normalise_tableau_x_aire(tableau)
        # print(tableau.shape)
    return tableau


def creer_dataframe_resultats(dataframe_comparatif, lim_zone1, lim_zone2, flag_denominateur):
    """
    Crée un dataframe avec les résultats des mesures d'aire sous chaque spectre
    entre chaque bornes des zones 1 et 2 (option) et leur rapport (option)
    """
    if flag_denominateur == 1:
        dataframe_tableau_calculs = pandas.DataFrame()
        sous_dataframe = dataframe_comparatif.loc[:, lim_zone1[0]:lim_zone1[1]]
        dataframe_tableau_calculs["Somme zone 1"] = sous_dataframe.sum(axis=1)
        sous_dataframe = dataframe_comparatif.loc[:, lim_zone2[0]:lim_zone2[1]]
        dataframe_tableau_calculs["Somme zone 2"] = sous_dataframe.sum(axis=1)
        dataframe_tableau_calculs["Rapport"] = dataframe_tableau_calculs["Somme zone 1"] / \
            dataframe_tableau_calculs["Somme zone 2"]
    if flag_denominateur == 0:
        dataframe_tableau_calculs = pandas.DataFrame()
        sous_dataframe = dataframe_comparatif.loc[:, lim_zone1[0]:lim_zone1[1]]
        dataframe_tableau_calculs["Somme zone 1"] = sous_dataframe.sum(axis=1)
    return dataframe_tableau_calculs


def convertir_dataframe_resultats_tableau(dataframe_comparatif):
    """
    Convertit le dataframe_comparatif en tableau et supprime la dernière colonne
    contenant la mesure ayant servi au classement
    """
    tableau = dataframe_comparatif.values
    tableau = numpy.delete(tableau, -1, axis=1)
    # print(tableau.shape)
    return tableau


def enregistre_dataframe_resultats(dataframe_resultats):
    """
    Enregistre les résultats classés des mesures
    aux formats xlsx et tsv (extension .txt)
    """
    #    dataframe_resultats.to_csv("Resultat_fichiers_classes.csv")
    dataframe_resultats.to_excel("Resultat_fichiers_classes.xlsx")
    dataframe_resultats.to_csv("Resultat_fichiers_classes.txt", sep='\t', decimal=",")


###################################################################################################
# fonctions d'affichage graphique du tableau de résultats
###################################################################################################
def tableau_256gris(tableau_norm):
    """
    Convertit les valeurs du tableau des spectres classés entre 0 et 255
    """
    tableau8bits = tableau_norm*255
    tableau8bits = tableau8bits.astype(int)
    return tableau8bits


def graphique_creation(tableau8bits, nom_echantillon, lim_spectre):
    """
    Affiche le tableau de n spectres classés en 256 niveau de gris
    avec la LUT Inferno dans une fenêtre matplotlib.pyplot 2D
    et la sauvegarde sous figure_plot.png
    """
    # fig=plt.figure()
    fig, ax = plt.subplots()
    #plt.imshow(tableau8bits, cmap="gray", extent=[lim_spectre[0],lim_spectre[1],tableau8bits.shape[0],0], aspect="auto")
    plt.imshow(tableau8bits, cmap="inferno", extent=[
               lim_spectre[0], lim_spectre[1], tableau8bits.shape[0], 0], aspect="auto")

    #imageplot=plt.imshow(tableau8bits, cmap="hot")
    #imageplot=plt.imshow(tableau8bits, cmap="nipy_spectral")
    # plt.colorbar()
    plt.title(nom_echantillon)
    plt.xlabel("Longueur d'onde (nm)")
    plt.ylabel("Spectres echantillons classés")
    plt.yticks(range(0, tableau8bits.shape[0], 5))
    ax.yaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    plt.savefig("figure_plot.png")
    #plt.xlim(lim_spectre[0], lim_spectre[1])
    # plt.ioff()
    plt.show(block=False)


# def graphique_3D_creation(tableau8bits,nom_echantillon,lim_spectre):
def graphique_3D_creation(tableau8bits, nom_echantillon):
    """
    Affiche le tableau de n spectres classés en 256 niveau de gris
    avec la LUT Inferno dans une fenêtre matplotlib.pyplot 3D
    """
    xx, yy = numpy.mgrid[0:tableau8bits.shape[0], 0:tableau8bits.shape[1]]
    #fig = plt.figure(figsize=(15,15))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(xx, yy, tableau8bits, rstride=1, cstride=1,
                    cmap="inferno", linewidth=0, antialiased=False)
    ax.view_init(80, 30)

    plt.title(nom_echantillon)
    plt.ylabel("Longueur d'onde (nm)")
    plt.xlabel("Spectres suivant z")
    # ax.set_ylim(lim_spectre[0],lim_spectre[1])

    plt.xticks(range(0, tableau8bits.shape[0], 5))
    ax.xaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.yaxis.set_tick_params(which='minor', bottom=False)

    plt.show(block=False)


def graphique_sauvegarde(tableau8bits):
    """
    Saugegarde le tableau de n spectres classés en 256 niveau de gris
    avec la LUT Inferno sous figure.png
    """
    plt.imsave("figure.png", tableau8bits, cmap="inferno")


# def graphique_lit_tableau():
#     tableau_comparatif = plt.imread("figure.png")
#     return tableau_comparatif


###################################################################################################
# programme principal
###################################################################################################
def main(rep_travail, liste_fichiers, type_fichier, tableau_bornes, type_traitement, flag_denominateur, flag_2D, flag_3D):
    """
    Fonction principale du module
    Crée un tableau_comparatif avec tous les spectres en colonne et les lambda en colonne 0
    Crée un dataframe_comparatif (spectres en ligne) à partir du tableau précédent
    Crée un dataframe_resultats de résultats des mesures
    Ajoute une colonne au dataframe_comparatif avec une des mesures du dataframe_resultats
    Trie par ordre croissant ces deux dataframes à l'aide de cette mesure
    Enregistre dataframe_resultats
    Remplace tableau_comparatif par les valeurs du dataframe_comparatif des spectres
    classés par mesures croissantes et l'affiche sous forme d'image qu'on sauvegarde
    Retourne le dataframe_resultats classé par ordre de mesure croissante
    """
    os.chdir(rep_travail)
    tableau_comparatif = creer_tableau_avec_x(liste_fichiers, type_fichier, type_traitement)
    dataframe_comparatif = LIBStick_outils.creer_dataframe_x_tableau_en_colonnes(tableau_comparatif,
                                                                                 liste_fichiers)

    limites_zone1[0] = tableau_bornes[0, 0]
    limites_zone1[1] = tableau_bornes[0, 1]
    limites_zone2[0] = tableau_bornes[1, 0]
    limites_zone2[1] = tableau_bornes[1, 1]

    dataframe_resultats = creer_dataframe_resultats(
        dataframe_comparatif, limites_zone1, limites_zone2, flag_denominateur)
    if flag_denominateur == 1:
        dataframe_comparatif = pandas.concat(
            [dataframe_comparatif, dataframe_resultats["Rapport"]], axis=1)
        dataframe_comparatif = dataframe_comparatif.sort_values(by=["Rapport"])
        dataframe_resultats = dataframe_resultats.sort_values(by=["Rapport"])
        enregistre_dataframe_resultats(dataframe_resultats)

    if flag_denominateur == 0:
        dataframe_comparatif = pandas.concat(
            [dataframe_comparatif, dataframe_resultats["Somme zone 1"]], axis=1)
        dataframe_comparatif = dataframe_comparatif.sort_values(by=["Somme zone 1"])
        dataframe_resultats = dataframe_resultats.sort_values(by=["Somme zone 1"])
        enregistre_dataframe_resultats(dataframe_resultats)

    tableau_comparatif = convertir_dataframe_resultats_tableau(dataframe_comparatif)
    tableau8bits = tableau_256gris(tableau_comparatif)
    if flag_2D:
        graphique_creation(tableau8bits, "Echantillons classés", limites_spectre)
    if flag_3D:
        # graphique_3D_creation(tableau8bits, "Echantillons classés", limites_spectre)
        graphique_3D_creation(tableau8bits, "Echantillons classés")
    graphique_sauvegarde(tableau8bits)

    return dataframe_resultats
