#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:20:38 2020
Module outils pour l'extration de parties des spectres et création de spectres moyens
@author: yannick
"""


import sys
import os
import numpy as np
import matplotlib.pyplot as plt
#import mpl_toolkits.mplot3d as plt3d
import LIBStick_outils

sys.path.insert(0, os.path.join(os.path.expanduser("~"), "Desktop"))
sys.path.insert(0, "./dossier_mes_modules/")


###################################################################################################
# fonction qui liste des fichiers *.asc d'un répertoire
###################################################################################################
def creation_nom_echantillon(liste_fichiers):
    """
    Retourne le nom de l'échantillon en utilisant le nom du premier spectre du répertoire
    et en suppriment les 6 dernier carractères (extension et numéro à deux chiffres)
    """
    nom_echantillon = liste_fichiers[0][0:-6]
    return nom_echantillon


###################################################################################################
# fonction qui lit un fichier spectre
###################################################################################################
def lit_fichier_entre_bornes(fichier, bas, haut, type_fichier):
    """
    Lit un fichier spectre grâce à LIBStick_outils.lit_spectre et renvoie un spectre
    tronqué, uniquement entre les bornes basses et hautes données par les spinbox
    """
    document = LIBStick_outils.lit_spectre(fichier, type_fichier)
    document_tronc = np.zeros((0, 2))
    document_tronc = document[(document[:,0] >= bas) &
                              (document[:,0] <= haut)]
    # for ligne in document:
    #     if (ligne[0] >= bas and ligne[0] <= haut):
    #         document_tronc = np.row_stack((document_tronc, ligne))
    #         # document_tronc=np.vstack((document_tronc,ligne)) #idem ci-dessus
    return document_tronc


###################################################################################################
# fonction qui crée un sous répertoire d'un certain nom passé en argument
###################################################################################################
def creation_sous_repertoire(rep_travail, tableau_bornes, flag_zone2):
    """
    Création de sous répertoire dont les noms correspondent aux bornes des zones à extraire
    """
    if flag_zone2:
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0, 0])+"_"
                             + str(tableau_bornes[0, 1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[0, 0])+"_"+str(tableau_bornes[0, 1]))
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[1, 0])+"_"
                             + str(tableau_bornes[1, 1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[1, 0])+"_"+str(tableau_bornes[1, 1]))
    if flag_zone2 == 0:
        if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0, 0])+"_"
                             + str(tableau_bornes[0, 1])):
            os.mkdir(rep_travail + "/"+str(tableau_bornes[0, 0])+"_"+str(tableau_bornes[0, 1]))


###################################################################################################
# fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###################################################################################################
def enregistre_spectre(document, repertoire, nom_fichier):
    """
    Enregistrement d'un spectre tronqué dans le sous répertoire correspondant aux bornes
    """
    os.chdir(repertoire)
    nom_fichier = nom_fichier[0:-4] + "_" + repertoire[-11:] + ".tsv"
    np.savetxt(nom_fichier, document, delimiter="\t")


###################################################################################################
# fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###################################################################################################
def enregistre_fichier_point(tableau, nom_fichier):
    """
    Enregistre le tableau des n spectres tronqués en fichier texte tabulé
    et le point comme séparateur de décimales
    """
    np.savetxt(nom_fichier, tableau, delimiter="\t", newline="\n")


def enregistre_fichier_virgule(tableau, nom_fichier):
    """
    Enregistre le tableau des n spectres tronqués en fichier texte tabulé
    et la virgule comme séparateur de décimales
    """
    tableau = tableau.astype(str)
    tableau = np.char.replace(tableau, ".", ",")
    np.savetxt(nom_fichier, tableau, delimiter="\t", newline="\n", fmt="%s")


def enregistre_dataframe_point(dataframe, nom_fichier):
    """
    Enregistre le dataframe des n spectres tronqués en fichier texte
    et le point comme séparateur de décimales
    """
    #    dataframe.to_excel(nom_fichier+".xlsx")
    dataframe.to_csv(nom_fichier+".txt", decimal=".", sep="\t")


###################################################################################################
# fonction normalise les colonnes du tableau
###################################################################################################
# def normalise_tableau_aire(tableau):
#    for colonne in range(1,tableau.shape[1]):
#        minimum=tableau[:,colonne].min()
#        tableau[:,colonne] = (tableau[:,colonne] - minimum)
#        aire=tableau[:,colonne].sum()
#        tableau[:,colonne] = (tableau[:,colonne] /aire)
#    tableau[:,1:]=tableau[:,1:]/tableau[:,1:].max()
#    return tableau


###################################################################################################
# fonctions qui affichent et sauvegardent des graphes
###################################################################################################
def tableau_brut_transpose_256gris(tableau_brut):
    """
    Crée tableau des n spectres bruts en supprimant lambda,
    multiplie les valeurs par 255
    et le transpose de façon à avoir chaque spectre en ligne
    """
    tableau8bits_brut = tableau_brut[:, 1:]
    tableau8bits_brut = tableau8bits_brut*255
    tableau8bits_brut = tableau8bits_brut.transpose()
    tableau8bits_brut = tableau8bits_brut.astype(int)
    return tableau8bits_brut


def graphique_brut_sauvegarde(tableau8bits_brut):
    """
    Sauvegarde le tableau brut de n spectres au format image png
    en fausses couleurs Inferno au lieu de niveau de gris
    """
    plt.imsave("figure_brute.png", tableau8bits_brut, cmap="inferno")


def tableau_transpose_256gris(tableau_norm):
    """
    Crée tableau des n spectres normalisés en supprimant lambda,
    converti les valeurs entre 0 et 255 au lieu de 0 et 1
    et le transpose de façon à avoir chaque spectre en ligne
    """
    tableau8bits = tableau_norm[:, 1:]
    tableau8bits = tableau8bits*255
    tableau8bits = tableau8bits.transpose()
    tableau8bits = tableau8bits.astype(int)
    return tableau8bits


def graphique_creation(tableau8bits, nom_echantillon, bornes):
    """
    Affiche le tableau de n spectres normalisés en 256 niveau de gris
    avec la LUT Inferno dans une fenêtre matplotlib.pyplot 2D
    et la sauvegarde sous figure_plot.png
    """
    # fig=plt.figure()
    fig, ax = plt.subplots()
    # plt.imshow(tableau8bits, cmap="gray", extent=[
    #     bornes[0],bornes[1],tableau8bits.shape[0],0], aspect="auto")
    plt.imshow(tableau8bits, cmap="inferno", extent=[
               bornes[0], bornes[1], tableau8bits.shape[0], 0], aspect="auto")
#    print(tableau8bits.shape[0])
#    print(tableau8bits.shape[1])
    #imageplot=plt.imshow(tableau8bits, cmap="hot")
    #imageplot=plt.imshow(tableau8bits, cmap="nipy_spectral")
    # plt.colorbar()
    plt.title(nom_echantillon)
    plt.xlabel("Longueur d'onde (nm)")
    plt.ylabel("Spectres suivant z")
    plt.yticks(range(0, tableau8bits.shape[0], 5))
    ax.yaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    plt.savefig("figure_plot.png")
    #plt.xlim(bornes[0], bornes[1])
    # plt.ioff()
    plt.show(block=False)


# def graphique_3D_creation(tableau8bits,nom_echantillon,bornes):
def graphique_3D_creation(tableau8bits, nom_echantillon):
    """
    Affiche le tableau de n spectres normalisés en 256 niveau de gris
    avec la LUT Inferno dans une fenêtre matplotlib.pyplot 3D
    """
    xx, yy = np.mgrid[0:tableau8bits.shape[0], 0:tableau8bits.shape[1]]
    #fig = plt.figure(figsize=(15,15))
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.plot_surface(xx, yy, tableau8bits, rstride=1, cstride=1,
                    cmap="inferno", linewidth=0, antialiased=False)
    ax.view_init(80, 30)

    plt.title(nom_echantillon)
    plt.ylabel("Longueur d'onde (nm)")
    plt.xlabel("Spectres suivant z")
    # ax.set_ylim(bornes[0],bornes[1])

    plt.xticks(range(0, tableau8bits.shape[0], 5))
    ax.xaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.yaxis.set_tick_params(which='minor', bottom=False)

    plt.show(block=False)


def graphique_sauvegarde(tableau8bits):
    """
    Saugegarde le tableau de n spectres normalisés en 256 niveau de gris
    avec la LUT Inferno sous figure.png
    """
    plt.imsave("figure.png", tableau8bits, cmap="inferno")


###################################################################################################
# ex-LIBStick_creation_tableau_norm525.0
###################################################################################################
def creation_tableau_norm(rep_travail, nom_echantillon, bornes, flag_2D, flag_3D):
    """
    Crée un tableau avec tous les spectres d'un répertoire dont
    tous ces spectres avaient déjà été extraits entre les bornes des spinbox.
    Sauvegarde le tableau des spectres bruts et le tableau des spectres normalisés
    sous forme de fichier texte et d'image png
    Sauvegarde le même tableau mais en dataframe en ajoutant les lambda
    """
    liste_fichiers = LIBStick_outils.creation_liste_fichiers(rep_travail, ".tsv")
    tableau_brut = LIBStick_outils.creer_tableau_avec_x_colonne1(liste_fichiers, ".tsv")
    tableau8bits_brut = tableau_brut_transpose_256gris(tableau_brut)
    graphique_brut_sauvegarde(tableau8bits_brut)
    enregistre_fichier_point(tableau_brut, "tableau_brut_points.txt")

    tableau_norm = LIBStick_outils.normalise_tableau_x_aire(tableau_brut)
    enregistre_fichier_point(tableau_norm, "tableau_normalisé_points.txt")
    enregistre_fichier_virgule(tableau_norm, "tableau_normalisé_virgules.txt")
    tableau8bits_norm = tableau_transpose_256gris(tableau_norm)
    graphique_sauvegarde(tableau8bits_norm)

#    dataframe_norm=creer_dataframe(tableau_norm, liste_fichiers)
    dataframe_norm = LIBStick_outils.creer_dataframe_x_tableau_en_colonnes(
        tableau_norm, liste_fichiers)
#    print("DataFrame " + str(dataframe_norm.info()))
    enregistre_dataframe_point(dataframe_norm, "dataframe_normalisé_points")

    if flag_2D == 1:
        graphique_creation(tableau8bits_norm, nom_echantillon, bornes)
    if flag_3D == 1:
        graphique_3D_creation(tableau8bits_norm, nom_echantillon)
        # graphique_3D_creation(tableau8bits_norm,nom_echantillon,bornes)


###################################################################################################
# Création spectre moyen
###################################################################################################
# x sur la première colonne
# def creation_spectre_moyen_avec_x(tableau_norm, bornes_moyenne_spectres):
#    tableau_abscisses=tableau_norm[:,0]
#    tableau_extrait=tableau_norm[:,1:]
#    indice_premier=(bornes_moyenne_spectres[0]-1)
#    indice_dernier=(bornes_moyenne_spectres[1])
#    tableau_extrait=tableau_extrait[:,indice_premier:indice_dernier]
#    spectre_moyen=tableau_extrait.sum(axis=1)
#    spectre_moyen=spectre_moyen/tableau_extrait.shape[1]
#    spectre_moyen=np.column_stack((tableau_abscisses,spectre_moyen))
#    return spectre_moyen


# x sur la première colonne
def creation_spectre_moyen_avec_x_tableau_bool(tableau_norm, liste_bool):
    """
    Crée un spectre moyen à l'aide des spectres sélectionnés
    """
    tableau_abscisses = tableau_norm[:, 0]
    tableau_extrait = tableau_norm[:, 1:]
    for i in range(len(liste_bool), 0, -1):
        if liste_bool[i-1] is False:
            # print("supprime : " + str(i))
            tableau_extrait = np.delete(tableau_extrait, i-1, axis=1)
    spectre_moyen = tableau_extrait.sum(axis=1)
    spectre_moyen = spectre_moyen/tableau_extrait.shape[1]
    spectre_moyen = np.column_stack((tableau_abscisses, spectre_moyen))
    return spectre_moyen


def enregistre_spectre_moyen(spectre_moyen, nom_echantillon, bornes,
                             flag_spectres_normalises_moyenne):
    """
    enregistre le spectre moyen au format tsv  avec l'extension .mean
    et le suffixe _spectre_moyen_norm_ ou _spectre_moyen_
    ainsi que les bornes inf et sup
    """
    if flag_spectres_normalises_moyenne is True:
        nom_fichier = nom_echantillon+"_spectre_moyen_norm_" + \
            str(bornes[0])+"_"+str(bornes[1])+".mean"
    else:
        nom_fichier = nom_echantillon+"_spectre_moyen_" + str(bornes[0])+"_"+str(bornes[1])+".mean"
    nom_fichier = str(np.char.replace(nom_fichier, " ", "_"))
    np.savetxt(nom_fichier, spectre_moyen, delimiter="\t", newline="\n")


def creation_spectre_moyen_main(rep_travail, nom_echantillon, bornes, liste_bool,
                                flag_spectres_normalises_moyenne):
    """
    Normalise ou non les spectres
    puis crée le spectre moyen à l'aide des spectres sélectionnés
    puis enregistre le spectre moyen
    et retourne le spectre moyen
    """
    os.chdir(rep_travail)
    tableau = np.loadtxt("tableau_brut_points.txt", delimiter="\t",
                            dtype=float, encoding="Latin-1")
    if flag_spectres_normalises_moyenne is True:
        # print("moyenne des spectres normalisés")
        tableau = LIBStick_outils.normalise_tableau_x_aire(tableau)
    # else:
    #     print("moyenne des spectres bruts")
#    print(tableau)
#    spectre_moyen=creation_spectre_moyen_avec_x(tableau_norm, bornes_moyenne_spectres)
    spectre_moyen = creation_spectre_moyen_avec_x_tableau_bool(tableau, liste_bool)
    enregistre_spectre_moyen(spectre_moyen, nom_echantillon, bornes,
                             flag_spectres_normalises_moyenne)
    return spectre_moyen


###################################################################################################
# programme principal
###################################################################################################
def main(rep_travail, tableau_bornes, type_fichier, liste_fichiers, flag_zone2, flag_2D, flag_3D):
    """
    Fonction principale du module
    Crée un ou deux sous-répertoire de sauvegarde
    Extrait les spectres entre les bornes choisies par les spinbox et les enregistre
    """
    rep_script = os.getcwd()
    if flag_zone2 == 0:
        tableau_bornes = np.delete(tableau_bornes, (1), axis=0)
    creation_sous_repertoire(rep_travail, tableau_bornes, flag_zone2)
    nom_echantillon = creation_nom_echantillon(liste_fichiers)
    for i in range(len(liste_fichiers)):
        for bornes in tableau_bornes:
            os.chdir(rep_travail)
            document = lit_fichier_entre_bornes(liste_fichiers[i], 
                                                bornes[0], bornes[1], 
                                                type_fichier)
            enregistre_spectre(document, rep_travail+"/" +
                               str(bornes[0])+"_" + str(bornes[1]), 
                               liste_fichiers[i])
    for bornes in tableau_bornes:
        os.chdir(rep_script)
        creation_tableau_norm(rep_travail+"/"+str(bornes[0])+"_" + str(bornes[1])+"/",
                              nom_echantillon, bornes, flag_2D, flag_3D)
    return nom_echantillon
#    return nom_echantillon, dataframe_norm
