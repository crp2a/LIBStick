#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 10:12:06 2020
Module outils généraux de manipulation des fichiers spectres
de transformations de tableaux et dataframes
@author: yannick
"""


###################################################################################################
###################################################################################################
# fonctions générales de gestion des repertoires, fichiers et création de DataFrames
###################################################################################################
###################################################################################################
import os
import numpy as np
import pandas as pd
try :
    from numba import jit
except :
    pass


###################################################################################################
# fonctions générales de gestion des repertoires et fichiers
###################################################################################################
def repertoire_de_travail(rep_script, rep_travail_relatif):
    """
    Renvoie le répertoire de travail absolu à partir du
    répertoire de travail relatif
    """
    rep_travail = rep_script+"/"+rep_travail_relatif
    return rep_travail


def creation_liste_fichiers(rep_travail, type_fichier):
    """
    Renvoie la liste des fichiers d'un même extension d'un répertoire
    """
    os.chdir(rep_travail)
    liste = []
    if type_fichier == ".mean":
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-4:] == "mean"):
                liste.append(fichier)
    if type_fichier == ".tsv":
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "tsv"):
                liste.append(fichier)
    if type_fichier == ".asc":
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "asc"):
                liste.append(fichier)
    if type_fichier == ".csv":
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "csv"):
                liste.append(fichier)
    liste.sort()
    return liste


def lit_spectre(fichier, type_fichier):
    """
    Lit un fichier spectre suivant le type de fichier et
    renvoie ce spectre sous forme d'un tableau
    """
    if type_fichier == ".mean":
        spectre = np.loadtxt(fichier, delimiter="\t", dtype=float, encoding="Latin-1")
    if type_fichier == ".tsv":
        spectre = np.loadtxt(fichier, delimiter="\t", dtype=float, encoding="Latin-1")
    if type_fichier == ".csv":
        spectre = np.loadtxt(fichier, delimiter=",", skiprows=1, dtype=float, encoding="Latin-1")
        nb_colonnes = spectre.shape[1]
        if nb_colonnes == 3:
            spectre = np.delete(spectre, 0, axis=1)
    if type_fichier == ".asc":
        spectre = np.loadtxt(fichier, delimiter="\t", skiprows=64, usecols=[0, 1],
                             dtype=float, encoding="Latin-1")
        # document=np.loadtxt(fichier,delimiter="\t",skiprows=64,
        #                        usecols=[0,1],dtype=float,encoding="Latin-1")
        # spectre=np.zeros((0,2))
        # for ligne in document :
        #     if (ligne[0]<=1013) :
        #         spectre=np.row_stack((spectre,ligne))
    return spectre


###################################################################################################
# fonctions générales de création de DataFrame
###################################################################################################
# creation tableau avec lambda (1ere ligne) et spectres dans les lignes suivantes
# INUTILISE !!!! UNIQUEMENT POUR DES FICHIERS tsv !!!!
def creer_tableau_avec_x_ligne1(liste):
    """
    Creation tableau avec lambda (1ere ligne) et
    les ordonnées de tous les spectres de la liste de fichiers
    dans les lignes suivantes
    INUTILISE !!!! UNIQUEMENT POUR DES FICHIERS tsv !!!!
    """
    i = 0
    for fichier in liste:
        if i == 0:
            tableau = np.loadtxt(fichier, delimiter="\t")
        else:
            fichier_entree = np.loadtxt(fichier, delimiter="\t", usecols=[1])
            tableau = np.column_stack((tableau, fichier_entree))
        i = i+1
    tableau = np.transpose(tableau)
    return tableau


# creation tableau avec lambda (1ere colonne) et spectres dans le colonnes suivantes
def creer_tableau_avec_x_colonne1(liste, type_fichier):
    """
    Creation tableau avec lambda (1ere colonne) et
    les ordonnées de tous les spectres de la liste de fichiers du même type
    dans les colonnes suivantes
    """
    i = 0
    if type_fichier == ".tsv":
        for fichier in liste:
            if i == 0:
                tableau = np.loadtxt(fichier, delimiter="\t")
            else:
                fichier_entree = np.loadtxt(fichier, delimiter="\t", usecols=[1])
                tableau = np.column_stack((tableau, fichier_entree))
            i = i+1
    if type_fichier == ".mean":
        for fichier in liste:
            if i == 0:
                tableau = np.loadtxt(fichier, delimiter="\t")
            else:
                fichier_entree = np.loadtxt(fichier, delimiter="\t", usecols=[1])
                tableau = np.column_stack((tableau, fichier_entree))
            i = i+1
    if type_fichier == ".csv":
        for fichier in liste:
            if i == 0:
                tableau = np.loadtxt(fichier, delimiter=",", skiprows=1)
                nb_colonnes = tableau.shape[1]
                if nb_colonnes == 3:
                    tableau = np.delete(tableau, 0, axis=1)
            else:
                if nb_colonnes == 2:
                    fichier_entree = np.loadtxt(fichier, delimiter=",", skiprows=1, usecols=[1])
                if nb_colonnes == 3:
                    fichier_entree = np.loadtxt(fichier, delimiter=",", skiprows=1, usecols=[2])
                tableau = np.column_stack((tableau, fichier_entree))
            i = i+1
    if type_fichier == ".asc":
        for fichier in liste:
            if i == 0:
                tableau = np.loadtxt(fichier, delimiter="\t", skiprows=64, usecols=[
                                        0, 1], dtype=float, encoding="Latin-1")
            else:
                fichier_entree = np.loadtxt(fichier, delimiter="\t", skiprows=64, usecols=[
                                               1], dtype=float, encoding="Latin-1")
                tableau = np.column_stack((tableau, fichier_entree))
            i = i+1
    return tableau


# creation d'un DataFrame avec lambda en nom des colonnes et le nom des fichiers en index des lignes
# INUTILISE !!!! et sûrement FAUX !!!!
def creer_dataframe_x_tableau_en_lignes(tableau_en_lignes, liste):
    """
    Creation d'un DataFrame avec lambda en nom des colonnes et
    le nom des fichiers en index des lignes
    à partir d'un tableau de spectres en lignes
    # INUTILISE !!!! et sûrement FAUX (cf. transpose à vérifier) !!!!
    """
    #    liste[0:0] = ["Lambda (nm)"]
    dataframe = pd.DataFrame(np.transpose(tableau_en_lignes[1:, :]),
                             index=liste,
                             columns=tableau_en_lignes[0, :])  # sûrement FAUX !!!!
    return dataframe


# creation d'un DFataFrame avec lambda en nom des colonnes et le nom des fichiers
# en index des lignes
def creer_dataframe_x_tableau_en_colonnes(tableau_en_colonnes, liste):
    """
    Creation d'un DataFrame avec lambda en nom des colonnes et
    le nom des fichiers en index des lignes
    à partir d'un tableau de spectres en colonnes
    """
    #    liste[0:0] = ["Lambda (nm)"]
    dataframe = pd.DataFrame(np.transpose(tableau_en_colonnes[:, 1:]),
                             index=liste,
                             columns=tableau_en_colonnes[:, 0])
    return dataframe


# creation d'un DataFrame avec lambda en nom des colonnes et le nom des fichiers en index
# des lignes entre bornes inf et sup
def creer_dataframe_x_tableau_en_colonnes_bornes(tableau_en_colonnes, liste, bornes):
    """
    Creation d'un DataFrame avec lambda en nom des colonnes et
    le nom des fichiers en index des lignes
    à partir d'un tableau de spectres en colonnes
    entre bornes inf et sup
    """
    dataframe = pd.DataFrame(np.transpose(tableau_en_colonnes[:, 1:]),
                             index=liste,
                             columns=tableau_en_colonnes[:, 0])
    dataframe_bornes = dataframe.loc[:, bornes[0]:bornes[1]]
    return dataframe_bornes


def creer_dataframe_bornes(dataframe, bornes):
    """
    Creation d'un DataFrame avec lambda en nom des colonnes et
    le nom des fichiers en index des lignes
    à partir d'un DataFrame
    entre bornes inf et sup
    """
    dataframe_bornes = dataframe.loc[:, bornes[0]:bornes[1]]
    return dataframe_bornes


###################################################################################################
# normalisation des spectres d'un tableau, données en colonnes, abscisses dans la première colonne
###################################################################################################
try :
    @jit
    def normalise_tableau_x_aire(tableau):  # données en colonnes, abscisses dans la première colonne
        """
        Normalise un tableau de spectres en colonnes
        Minimum à 0 et divise par l'aire sous la courbe (ainsi aire du spectre = 1)
        """
        for colonne in range(tableau.shape[1]-1):
            minimum = tableau[:, colonne+1].min()
            tableau[:, colonne+1] = (tableau[:, colonne+1] - minimum)
            aire = tableau[:, colonne+1].sum()
            tableau[:, colonne+1] = (tableau[:, colonne+1] / aire)
        return tableau
except :
    def normalise_tableau_x_aire(tableau):  # données en colonnes, abscisses dans la première colonne
        """
        Normalise un tableau de spectres en colonnes
        Minimum à 0 et divise par l'aire sous la courbe (ainsi aire du spectre = 1)
        """
        for colonne in range(tableau.shape[1]-1):
            minimum = tableau[:, colonne+1].min()
            tableau[:, colonne+1] = (tableau[:, colonne+1] - minimum)
            aire = tableau[:, colonne+1].sum()
            tableau[:, colonne+1] = (tableau[:, colonne+1] / aire)
        return tableau

try :
    @jit
    def normalise_tableau_x_maximum(tableau):  # données en colonnes, abscisses dans la première colonne
        """
        Normalise un tableau de spectres en colonnes
        Minimum à 0 et divise par le maximum du spectre
        """
        for colonne in range(tableau.shape[1]-1):
            minimum = tableau[:, colonne+1].min()
            tableau[:, colonne+1] = (tableau[:, colonne+1] - minimum)
    #        aire=tableau[:,colonne+1].sum()
    #        tableau[:,colonne+1] = (tableau[:,colonne+1] /aire)
        tableau = tableau/tableau.max()  # A ne pas faire car dépend de la liste à un instant t !!!
        return tableau
except :
    def normalise_tableau_x_maximum(tableau):  # données en colonnes, abscisses dans la première colonne
        """
        Normalise un tableau de spectres en colonnes
        Minimum à 0 et divise par le maximum du spectre
        """
        for colonne in range(tableau.shape[1]-1):
            minimum = tableau[:, colonne+1].min()
            tableau[:, colonne+1] = (tableau[:, colonne+1] - minimum)
    #        aire=tableau[:,colonne+1].sum()
    #        tableau[:,colonne+1] = (tableau[:,colonne+1] /aire)
        tableau = tableau/tableau.max()  # A ne pas faire car dépend de la liste à un instant t !!!
        return tableau


###################################################################################################
# normalisation des spectres d'un DataFrame, données en lignes
###################################################################################################
def normalise_dataframe_aire(dataframe):  # données lignes
    """
    Normalise un DataFrame de spectres (données en lignes)
    Minimum à 0 et divise par l'aire sous la courbe (ainsi aire du spectre = 1)
    """
    tableau = dataframe.values
    for ligne in range(tableau.shape[0]):
        minimum = tableau[ligne, :].min()
        tableau[ligne, :] = (tableau[ligne, :] - minimum)
        aire = tableau[ligne, :].sum()
        tableau[ligne, :] = (tableau[ligne, :] / aire)
    dataframe = pd.DataFrame(tableau, index=dataframe.index, columns=dataframe.columns)
    return dataframe


###################################################################################################
# Binning des spectres d'un tableau, données en colonnes, abscisses dans la première colonne
###################################################################################################
def binning_spectre (spectre, taille_bin=2):
    """
    Effectue un binning par moyenne sur un spectre.
    Args:
        spectre: Le spectre d'entrée sous forme de tableau NumPy.
        taille_bin: La taille de chaque bin.
    Returns:
        Le spectre binné.
    """
    # Vérification de la taille du spectre par rapport à la taille du bin
    # et supprime les derniers pixels du spectres
    if len(spectre) % taille_bin != 0:
        supprime = (len(spectre) % taille_bin)
        spectre = spectre[: -supprime]
    # Reshape le spectre en une matrice où chaque ligne correspond à un bin
    spectre_reshape = spectre.reshape(-1, taille_bin)
    # Calcul de la moyenne de chaque ligne (chaque bin)
    spectre_binne = np.mean(spectre_reshape, axis=1)
    # print("-----------------------")
    # print(spectre.shape)    
    # print(spectre_reshape)
    # print(spectre_reshape.shape)
    # print(spectre_binne.shape)
    return spectre_binne


def binning_dataframe(dataframe, taille_bin=2):
    """
    Effectue un binning par moyenne sur tous les spectres d'un Dataframe (un spectre par ligne)
    Parameters
    ----------
    dataframe : TYPE
        DESCRIPTION.
    taille_bin : TYPE, optional
        DESCRIPTION. The default is 2.
    Returns
    -------
    None.
    """
    tableau = dataframe.values    
    tableau_binne = np.zeros((tableau.shape[0], tableau.shape[1]//taille_bin))
    for ligne in range(tableau.shape[0]):
        spectre = tableau[ligne, :]
        spectre_binne = binning_spectre(spectre, taille_bin)
        tableau_binne[ligne, :] = spectre_binne
              
    colonnes = dataframe.columns.values
    colonnes_binne = binning_spectre(colonnes, taille_bin)
    dataframe_binne = pd.DataFrame(tableau_binne, index=dataframe.index)
    dataframe_binne.columns = colonnes_binne
    # print(dataframe)
    # print("------------------------")
    # print(dataframe_binne)
    return dataframe_binne

