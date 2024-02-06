#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:56:33 2023

@author: yannick
"""

import pandas as pd
import LIBStick_outils


###################################################################################################
# Recherche de dorrespondance longueur d'onde -> éléments
###################################################################################################
def recherche_elements(long_onde, delta, seuil, repertoire, rep_NIST):
    texte_neutres = recherche_elements_neutres_ions(long_onde, delta,seuil, False, repertoire, rep_NIST)
    texte_ions = recherche_elements_neutres_ions(long_onde, delta,seuil, True, repertoire, rep_NIST)
    # print(texte_neutres)
    # print(texte_ions)
    return texte_neutres, texte_ions


def recherche_elements_neutres_ions(long_onde, delta,seuil, ions, repertoire, rep_NIST):
    borneinf = long_onde-delta
    bornesup = long_onde+delta

    # Chemin vers les fichiers des éléments
    if ions == False :
        elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/elements"
        texte ="--------------------------" + "\n" + "Neutres :" + "\n" + "--------------------------"
        # print("--------------------------")
        # print ("Neutres :")
        # print("--------------------------")
    else :
        elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/ions"
        texte ="--------------------------" + "\n" + "Ions :" + "\n" + "--------------------------"
        # print("--------------------------")
        # print ("Ions :")
        # print("--------------------------")
    # Lister les fichiers
    # Retourne une liste de chemins
    liste_fichiers = LIBStick_outils.creation_liste_fichiers(elements_path,".csv")
    liste_fichiers.sort() #inutile

    # Récupérer les noms des éléments/ions à partir du nom de fichier
    # Retourne un vecteur
    noms_elements = []
    for i in range(len(liste_fichiers)) :
        noms_elements = noms_elements + [liste_fichiers[i][0:-4]]

    # Lire les fichiers
    # Retourne une liste de tableaux (un tableau par fichier lu)
    liste_df_elements=[]
    for fichier in liste_fichiers :
        DataFrame_element = pd.read_table(elements_path+"/"+fichier)
        liste_df_elements = liste_df_elements + [DataFrame_element]

    # for i in range(len(liste_df_elements)): # Pour chaque ième tableau de la liste...
    #     wavelength = liste_df_elements[i]["Longueur d'onde (nm)"].values # ...extraire la longueur d'onde
    #     intensity = liste_df_elements[i]["Intensité normalisée"].values  # ...extraire l'intensité
    #     # print (type(wavelength))
    #     ind = (wavelength > borneinf) & (wavelength < bornesup) & (intensity >= seuil)
    #     # print(ind)
    #     if ind.any():
    #         print(f"{noms_elements[i]} {wavelength[ind].tolist()} {intensity[ind].tolist()}")
    # print("--------------------------")

    # print (liste_df_elements[1])
    resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])
    for i in range(len(liste_df_elements)) : # Pour chaque ième tableau de la liste...
        wavelength = liste_df_elements[i]["Longueur d'onde (nm)"].values # ...extraire la longueur d'onde
        intensity = liste_df_elements[i]["Intensité normalisée"].values  # ...extraire l'intensité
        for j in range(len(wavelength )) :
            if ((wavelength[j] > borneinf) & (wavelength[j] < bornesup) & (intensity[j] >= seuil)) == True :
                # print(str(noms_elements[i]) + " : " + str(wavelength[j]) + "   "  + str(intensity[j]))
                resultat_df.loc[len(resultat_df)] = [noms_elements[i],wavelength[j],intensity[j]]
    texte = texte + "\n" + resultat_df.to_markdown()+ "\n"
    resultat_df.sort_values(by="I relative",ascending=(False), inplace = True)
    texte = texte + "\n" + resultat_df.to_markdown() + "\n"
    return texte



# long_onde = 236.03
# delta = 0.5
# seuil = 5
# rep_LIBStick = "/home/yannick/Bureau/LIBS/LIBStick"
# recherche_elements(long_onde, delta,seuil, rep_LIBStick)
