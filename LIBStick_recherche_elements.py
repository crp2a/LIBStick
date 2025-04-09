#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:56:33 2023

@author: yannick
"""

import pandas as pd
import LIBStick_outils


###################################################################################################
# Passe en mémoire vive le contenu de tous les fichiers dans deux dataframes
###################################################################################################
def creation_df_elements(ions, repertoire, rep_NIST):
    """
    Passe en mémoire vive le contenu de tous les fichiers dans deux dataframes

    Parameters
    ----------
    ions : TYPE
        DESCRIPTION.
    repertoire : TYPE
        DESCRIPTION.
    rep_NIST : TYPE
        DESCRIPTION.

    Returns
    -------
    resultat_df : Un dataframe de tous les éléments avec toutes les longueurs d'onde et les intensités relatives

    """
    # Chemin vers les fichiers des éléments
    if ions == False :
        elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/elements"
    else :
        elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/ions"
    # Lister les fichiers
    # Retourne une liste de chemins
    liste_fichiers = LIBStick_outils.creation_liste_fichiers(elements_path,".csv")
    
    # Récupérer les noms des éléments/ions à partir du nom de fichier
    # Retourne un vecteur
    # Lire les fichiers
    # Retourne une liste de tableaux (un tableau par fichier lu)  
    noms_elements = []
    resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])
    for i, fichier in zip(range(len(liste_fichiers)), liste_fichiers) :
        noms_elements = noms_elements + [liste_fichiers[i][0:-4]]
        DataFrame_element = pd.read_table(elements_path+"/"+fichier)
        liste_nom = [liste_fichiers[i][0:-4]] * DataFrame_element.shape[0]
        df = pd.DataFrame({"Element": liste_nom,
                           "Longueur d'onde" : DataFrame_element["Longueur d'onde (nm)"],
                           "I relative" : DataFrame_element["Intensité normalisée"]})
        resultat_df = pd.concat([resultat_df, df], axis=0, ignore_index=True)
    
    # noms_elements = []
    # liste_df_elements=[]
    # resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])
    # for i, fichier in zip(range(len(liste_fichiers)), liste_fichiers) :
    #     noms_elements = noms_elements + [liste_fichiers[i][0:-4]]
    #     DataFrame_element = pd.read_table(elements_path+"/"+fichier)
    #     liste_df_elements = liste_df_elements + [DataFrame_element]
    
    # for i in range(len(liste_df_elements)) : # Pour chaque ième tableau de la liste...
    #     wavelength = liste_df_elements[i]["Longueur d'onde (nm)"].values # ...extraire la longueur d'onde
    #     intensity = liste_df_elements[i]["Intensité normalisée"].values  # ...extraire l'intensité
    #     for j in range(len(wavelength )) :
    #         resultat_df.loc[len(resultat_df)] = [noms_elements[i],wavelength[j],intensity[j]]
            
    return resultat_df
    
    
###################################################################################################
# Recherche de correspondance longueur d'onde -> éléments en automatique
###################################################################################################
def recherche_elements_neutres_ions_auto(long_onde, delta, seuil, ions, df_elements):
    """
    Recherche auto de tous les pics
    
    Parameters
    ----------
    long_onde : TYPE
        DESCRIPTION.
    delta : TYPE
        DESCRIPTION.
    seuil : TYPE
        DESCRIPTION.
    ions : TYPE
        DESCRIPTION.
    df_elements : TYPE
        DESCRIPTION.

    Returns
    -------
    texte : TYPE
        DESCRIPTION.
    resultat_df : TYPE
        DESCRIPTION.

    """
    borneinf = long_onde-delta
    bornesup = long_onde+delta
    if ions == False :
        texte =  "**Neutres** :" + "\n\n" + "---------------------------"
    else :
        texte =  "**Ions** :" + "\n\n" + "---------------------------"
    resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])

    resultat_df = df_elements[(df_elements["Longueur d'onde"] > borneinf) & 
                              (df_elements["Longueur d'onde"] < bornesup) & 
                              (df_elements["I relative"] >= seuil)]
    
    # liste_inf_wavelength = [borneinf] * df_elements.shape[0]
    # liste_sup_wavelength = [bornesup] * df_elements.shape[0]
    # liste_int_min = [seuil] * df_elements.shape[0]
    # for i in range(len(df_elements)) : # Pour chaque ième ligne du tableau...
    #     noms_elements = df_elements["Element"].iloc[i]
    #     wavelength = df_elements["Longueur d'onde"].iloc[i]
    #     intensity = df_elements["I relative"].iloc[i]
    #     if ((wavelength > borneinf) & (wavelength < bornesup) & (intensity >= seuil)) == True :
    #         resultat_df.loc[len(resultat_df)] = [noms_elements,wavelength,intensity]
            
    resultat_df.sort_values(by="I relative",ascending=(False), inplace = True)
    texte = texte + "\n" + resultat_df.to_markdown() + "\n"
    return texte, resultat_df


###################################################################################################
# Recherche de correspondance longueur d'onde -> éléments
###################################################################################################
def recherche_elements(long_onde, delta, seuil, df_neutres, df_ions):
    texte_neutres, resultat_df_neutres = recherche_elements_neutres_ions(long_onde, delta,seuil, False, df_neutres)
    texte_ions, resultat_df_ions = recherche_elements_neutres_ions(long_onde, delta,seuil, True, df_ions)
    return texte_neutres, texte_ions, resultat_df_neutres, resultat_df_ions


def recherche_elements_neutres_ions(long_onde, delta,seuil, ions, df_elements):
    borneinf = long_onde-delta
    bornesup = long_onde+delta
    if ions == False :
        texte ="--------------------------" + "\n" + "Neutres :" + "\n" + "--------------------------"
    else :
        texte ="--------------------------" + "\n" + "Ions :" + "\n" + "--------------------------"

    resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])
    resultat_df = df_elements[(df_elements["Longueur d'onde"] > borneinf) & 
                              (df_elements["Longueur d'onde"] < bornesup) & 
                              (df_elements["I relative"] >= seuil)]
    
    # for i in range(len(df_elements)) : # Pour chaque ième tableau de la liste...
    #     noms_elements = df_elements["Element"].iloc[i]
    #     wavelength = df_elements["Longueur d'onde"].iloc[i]
    #     intensity = df_elements["I relative"].iloc[i]
    #     if ((wavelength > borneinf) & (wavelength < bornesup) & (intensity >= seuil)) == True :
    #         resultat_df.loc[len(resultat_df)] = [noms_elements,wavelength,intensity]
    
    texte = texte + "\n" + resultat_df.to_markdown()+ "\n"
    resultat_df.sort_values(by="I relative",ascending=(False), inplace = True)
    texte = texte + "\n" + resultat_df.to_markdown() + "\n"
    return texte, resultat_df


# ###################################################################################################
# # Recherche de correspondance longueur d'onde -> éléments
# ###################################################################################################
# def recherche_elements(long_onde, delta, seuil, repertoire, rep_NIST):
#     texte_neutres, resultat_df_neutres = recherche_elements_neutres_ions(long_onde, delta,seuil, False, repertoire, rep_NIST)
#     texte_ions, resultat_df_ions = recherche_elements_neutres_ions(long_onde, delta,seuil, True, repertoire, rep_NIST)
#     # print(texte_neutres)
#     # print(texte_ions)
#     return texte_neutres, texte_ions, resultat_df_neutres, resultat_df_ions


# def recherche_elements_neutres_ions(long_onde, delta,seuil, ions, repertoire, rep_NIST):
#     borneinf = long_onde-delta
#     bornesup = long_onde+delta

#     # Chemin vers les fichiers des éléments
#     if ions == False :
#         elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/elements"
#         texte ="--------------------------" + "\n" + "Neutres :" + "\n" + "--------------------------"
#         # print("--------------------------")
#         # print ("Neutres :")
#         # print("--------------------------")
#     else :
#         elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/ions"
#         texte ="--------------------------" + "\n" + "Ions :" + "\n" + "--------------------------"
#         # print("--------------------------")
#         # print ("Ions :")
#         # print("--------------------------")
#     # Lister les fichiers
#     # Retourne une liste de chemins
#     liste_fichiers = LIBStick_outils.creation_liste_fichiers(elements_path,".csv")
#     liste_fichiers.sort() #inutile

#     # Récupérer les noms des éléments/ions à partir du nom de fichier
#     # Retourne un vecteur
#     noms_elements = []
#     for i in range(len(liste_fichiers)) :
#         noms_elements = noms_elements + [liste_fichiers[i][0:-4]]

#     # Lire les fichiers
#     # Retourne une liste de tableaux (un tableau par fichier lu)
#     liste_df_elements=[]
#     for fichier in liste_fichiers :
#         DataFrame_element = pd.read_table(elements_path+"/"+fichier)
#         liste_df_elements = liste_df_elements + [DataFrame_element]

#     # for i in range(len(liste_df_elements)): # Pour chaque ième tableau de la liste...
#     #     wavelength = liste_df_elements[i]["Longueur d'onde (nm)"].values # ...extraire la longueur d'onde
#     #     intensity = liste_df_elements[i]["Intensité normalisée"].values  # ...extraire l'intensité
#     #     # print (type(wavelength))
#     #     ind = (wavelength > borneinf) & (wavelength < bornesup) & (intensity >= seuil)
#     #     # print(ind)
#     #     if ind.any():
#     #         print(f"{noms_elements[i]} {wavelength[ind].tolist()} {intensity[ind].tolist()}")
#     # print("--------------------------")

#     # print (liste_df_elements[1])
#     resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])
#     for i in range(len(liste_df_elements)) : # Pour chaque ième tableau de la liste...
#         wavelength = liste_df_elements[i]["Longueur d'onde (nm)"].values # ...extraire la longueur d'onde
#         intensity = liste_df_elements[i]["Intensité normalisée"].values  # ...extraire l'intensité
#         for j in range(len(wavelength )) :
#             if ((wavelength[j] > borneinf) & (wavelength[j] < bornesup) & (intensity[j] >= seuil)) == True :
#                 # print(str(noms_elements[i]) + " : " + str(wavelength[j]) + "   "  + str(intensity[j]))
#                 resultat_df.loc[len(resultat_df)] = [noms_elements[i],wavelength[j],intensity[j]]
#     texte = texte + "\n" + resultat_df.to_markdown()+ "\n"
#     resultat_df.sort_values(by="I relative",ascending=(False), inplace = True)
#     texte = texte + "\n" + resultat_df.to_markdown() + "\n"
#     return texte, resultat_df


###################################################################################################
# Recherche de correspondance longueur d'onde -> éléments en automatique
###################################################################################################
# def recherche_elements_neutres_ions_auto(long_onde, delta,seuil, ions, repertoire, rep_NIST):
#     borneinf = long_onde-delta
#     bornesup = long_onde+delta
#     # texte = "Lambda : " + str(long_onde)

#     # Chemin vers les fichiers des éléments
#     if ions == False :
#         elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/elements"
#         texte =  "**Neutres** :" + "\n\n" + "---------------------------"
#     else :
#         elements_path = repertoire + "/LIBStick_datas/" + rep_NIST + "/ions"
#         texte =  "**Ions** :" + "\n\n" + "---------------------------"
#     # Lister les fichiers
#     # Retourne une liste de chemins
#     liste_fichiers = LIBStick_outils.creation_liste_fichiers(elements_path,".csv")
#     liste_fichiers.sort() #inutile

#     # Récupérer les noms des éléments/ions à partir du nom de fichier
#     # Retourne un vecteur
#     noms_elements = []
#     for i in range(len(liste_fichiers)) :
#         noms_elements = noms_elements + [liste_fichiers[i][0:-4]]

#     # Lire les fichiers
#     # Retourne une liste de tableaux (un tableau par fichier lu)
#     liste_df_elements=[]
#     for fichier in liste_fichiers :
#         DataFrame_element = pd.read_table(elements_path+"/"+fichier)
#         liste_df_elements = liste_df_elements + [DataFrame_element]
#     # print (liste_df_elements)

#     resultat_df = pd.DataFrame(columns=["Element","Longueur d'onde","I relative"])
#     for i in range(len(liste_df_elements)) : # Pour chaque ième tableau de la liste...
#         wavelength = liste_df_elements[i]["Longueur d'onde (nm)"].values # ...extraire la longueur d'onde
#         intensity = liste_df_elements[i]["Intensité normalisée"].values  # ...extraire l'intensité
#         for j in range(len(wavelength )) :
#             if ((wavelength[j] > borneinf) & (wavelength[j] < bornesup) & (intensity[j] >= seuil)) == True :
#                 resultat_df.loc[len(resultat_df)] = [noms_elements[i],wavelength[j],intensity[j]]
#     # texte = texte + "\n" + resultat_df.to_markdown()+ "\n"
#     resultat_df.sort_values(by="I relative",ascending=(False), inplace = True)
#     texte = texte + "\n" + resultat_df.to_markdown() + "\n"
#     return texte, resultat_df

