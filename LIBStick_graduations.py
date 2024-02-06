#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 14:31:16 2024

@author: yannick
"""

import numpy as np


###################################################
# Initialisations pour test
###################################################
# limites_spectre_x = [400, 512]
# largeur_canevas_spectres = 700
# espacement_en_pixels = 100


###################################################
# Calcul du pas en nm
###################################################
def calcul_pas_nm (taille_canevas_en_pixels, limites_spectre_en_nm, x_pixels, x_du_pas_en_nm) :
    """
    Calcule un pas rond en nm en fonction des limites du spectre et de la résolution en pixels
    du canevas d'affichage du spectre
    """
    nombre_de_marques = taille_canevas_en_pixels // x_pixels # une marque tous les x pixels

    delta_spectre_en_nm = limites_spectre_en_nm[1]-limites_spectre_en_nm[0]
    lim_spectre_arondies=  np.zeros((2))
    lim_spectre_arondies[0] = ((limites_spectre_en_nm[0]//x_du_pas_en_nm) +1)*x_du_pas_en_nm
    lim_spectre_arondies[1] = (limites_spectre_en_nm[1]//x_du_pas_en_nm)*x_du_pas_en_nm
    # print(limites_spectre_en_nm)
    # print(lim_spectre_arondies)
    delta_spectre_arondi =lim_spectre_arondies[1] - lim_spectre_arondies[0]
    pas_en_nm = int(delta_spectre_arondi//nombre_de_marques)
    # print(pas_en_nm)
    pas_en_nm = (np.round((pas_en_nm)/x_du_pas_en_nm))*x_du_pas_en_nm+x_du_pas_en_nm
    # print(pas_en_nm)
    return delta_spectre_en_nm, lim_spectre_arondies, pas_en_nm


###################################################
# Remplissage du tableau de graduations
###################################################
def creation_tableau_graduations_nm(limites_spectre_x, lim_spectre_arondies, pas_en_nm) :
    """
    Création d'une liste des graduations en nm en fonction du pas rond calculé
    et des limites arondies d'affichage du spectre
    """
    # liste_graduations_linspace = np.linspace(int(lim_spectre_arondies[0]),
    #                                          int(lim_spectre_arondies[1]),
    #                                          nombre_de_marques, endpoint= True)
    # liste_graduations_linspace = liste_graduations_linspace.astype(int)
    # print ("liste_graduations_linspace = ")
    # print( liste_graduations_linspace)
    # print("___________________")

    liste_graduations_arange = np.arange(int(lim_spectre_arondies[0]),
                                          int(limites_spectre_x[1]),
                                          int(pas_en_nm))
    # print ("liste_graduations_arange = ")
    # print(liste_graduations_arange)
    # print("___________________")

    # for i in range(int(limites_spectre_arondies[0]),
    #                int(limites_spectre_arondies[1]),
    #                int(pas_en_nm)):
    #     liste_graduations = np.append(liste_graduations, i).astype(int)
    # print ("liste_graduations = ")
    # print(liste_graduations)
    # print("___________________")

    return liste_graduations_arange


###################################################
# Convertion de la liste en nm en liste en pixels
###################################################
def conversion_nm_pixels (limites_spectre_en_nm,
                          delta_spectre_en_nm,
                          taille_canevas_en_pixels,
                          liste_graduations) :
    """
    Crée une liste des garduations en pixels en fonction de la liste des graduations en nm
    et de la taille du canvas en pixels
    """
    conversion_nm_en_pixel = taille_canevas_en_pixels / delta_spectre_en_nm
    liste_graduations_en_pixels = (liste_graduations - limites_spectre_en_nm[0]) * conversion_nm_en_pixel
    liste_graduations_en_pixels = np.round(liste_graduations_en_pixels)

    return liste_graduations_en_pixels


###################################################
# Programme principal de calcul de 2 tableaux de graduation (en nm et en pixels)
###################################################
def calcul_tableaux_graduation(largeur_canevas_spectres, limites_spectre_x, espacement_en_pixels, multiple_du_pas) :
    """
    Fonction principale appelant les autres fonctions et retournant les deux listes
    de gradautions en nm et en pixels
    """
    delta_spectre_en_nm, limites_spectre_arondies, pas = calcul_pas_nm (largeur_canevas_spectres,
                                                                              limites_spectre_x,
                                                                              espacement_en_pixels,
                                                                              multiple_du_pas)
    liste_graduations_en_nm = creation_tableau_graduations_nm (limites_spectre_x,
                                                               limites_spectre_arondies,
                                                               pas)
    liste_graduations_en_pixels = conversion_nm_pixels (limites_spectre_x,
                                                        delta_spectre_en_nm,
                                                        largeur_canevas_spectres,
                                                        liste_graduations_en_nm)
    return liste_graduations_en_nm, liste_graduations_en_pixels



###################################################
# Programme test
###################################################
# liste_graduations_en_nm, liste_graduations_en_pixels = calcul_tableaux_graduation(largeur_canevas_spectres,
#                                                                                   limites_spectre_x,
#                                                                                   espacement_en_pixels)

# print ("liste_graduations_en_nm = ")
# print(liste_graduations_en_nm)
# print("___________________")

# print ("liste_graduations_en_pixels = ")
# print( liste_graduations_en_pixels)
# print("___________________")
