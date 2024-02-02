#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:41:09 2020
Module outils pour le pré-traitement des spectres
@author: yannick
"""


import os
import math
import numpy as np
import scipy.signal
import LIBStick_outils
try :
    from numba import jit
except :
    pass


###################################################################################################
# fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###################################################################################################
def creation_sous_repertoire(rep_travail):
    """
    Création du sous-répertoire ./traitement pour enregistrer les spectres traités
    """
    repertoire_sauvegarde = rep_travail + "/traitement"
    if os.path.isdir(repertoire_sauvegarde) is False:
        os.mkdir(repertoire_sauvegarde)
    return repertoire_sauvegarde


def creation_sous_repertoire_fond(rep_travail):
    """
    Création du sous-répertoire ./fond_continu pour enregistrer les fonds soustraits
    """
    repertoire_sauvegarde_fond = rep_travail + "/fond_continu"
    if os.path.isdir(repertoire_sauvegarde_fond) is False:
        os.mkdir(repertoire_sauvegarde_fond)
    return repertoire_sauvegarde_fond


def enregistre_fichier(spectre, repertoire, nom_fichier):
    """
    Enregistre les spectres traités dans le sous-répertoire ./traitement
    avec le suffixe _corrige.tsv
    """
    nom_fichier = repertoire + "/" + nom_fichier[0:-4] + "_corrige.tsv"
    np.savetxt(nom_fichier, spectre, delimiter="\t")


def enregistre_fichier_fond(spectre, repertoire, nom_fichier):
    """
    Enregistre les fonds extraits dans le sous-répertoire ./fond_continu
    avec le suffixe _fond_continu.tsv
    """
    nom_fichier = repertoire + "/" + nom_fichier[0:-4] + "_fond_continu.tsv"
    np.savetxt(nom_fichier, spectre, delimiter="\t")


###################################################################################################
# fonction qui limite le traitement aux bornes
###################################################################################################
def creation_spectre_bornes(spectre_entier, tableau_bornes):
    """
    Extrait et retourne un spectre limité aux bornes définies par les Spinbox
    """
    spectre_limite_bornes = np.zeros((0, 2))
    for ligne in spectre_entier:
        if ligne[0] > tableau_bornes[0] and ligne[0] < tableau_bornes[1]:
            spectre_limite_bornes = np.row_stack((spectre_limite_bornes, ligne))
    return spectre_limite_bornes


###################################################################################################
# fonctions de filtres
###################################################################################################
try :
    @jit
    def rolling_ball_fonction(spectre, width_min_max, width_smooth):
        """
        Crée et retourne le fond continu par Rolling-Ball
        https://rdrr.io/cran/baseline/man/baseline.rollingBall.html
        width_min_max 	Width of local window for minimization/maximization
        width_smooth 	Width of local window for smoothing
        """
        # initialisations
        taille_spectre = spectre.shape[0]
        ligne_base = spectre.copy()
        ordonnees = spectre[:, 1]
        minima = np.zeros(taille_spectre)
        maxima = np.zeros(taille_spectre)
        start_window, end_window, somme_ordo_window = 0, 0, 0
        ########## Minimise ##########
        start_window = math.ceil((width_min_max+1)/2)
        minima[0] = np.min(ordonnees[0:start_window])
        for i in range(1, width_min_max):   # -- Start of spectrum --
            end_window = start_window + 1 + (i % 2)
            minima[i] = min(np.min(ordonnees[start_window:end_window]), minima[i-1])  # Check if new is smaller
            start_window = end_window
        for i in range(width_min_max, taille_spectre-width_min_max):   # -- Main part of spectrum --
            if ((ordonnees[start_window] <= minima[i-1])
                    and (ordonnees[start_window-width_min_max] != minima[i-1])):
                minima[i] = ordonnees[start_window]   # Next is smaller
            else:
                minima[i] = np.min(ordonnees[(i-width_min_max):(i+width_min_max)])
            start_window = start_window + 1
        start_window = (taille_spectre - 2*width_min_max - 1)
        for i in range(taille_spectre-width_min_max, taille_spectre):   # -- End of spectrum --
            end_window = start_window + 1 + (i % 2)
            if (np.min(ordonnees[start_window:(end_window)])) > minima[i-1]:
                minima[i] = minima[i-1]   # Removed is larger
            else:
                minima[i] = np.min(ordonnees[end_window:taille_spectre])
            start_window = end_window
        ########## Maximise ##########
        start_window = math.ceil((width_min_max+1)/2)
        maxima[0] = np.max(minima[0:start_window])
        for i in range(1, width_min_max):                # -- Start of spectrum --
            end_window = start_window + 1 + (i % 2)
            #end_window = start_window +1
            maxima[i] = max(np.max(minima[start_window:end_window]), maxima[i-1])  # Check if new is larger
            start_window = end_window
        for i in range(width_min_max, taille_spectre-width_min_max):     # -- Main part of spectrum --
            if ((minima[start_window] >= maxima[i-1]) and (minima[start_window-width_min_max] != maxima[i-1])):
                maxima[i] = minima[start_window]  # Next is larger
            else:
                maxima[i] = np.max(minima[i-width_min_max: i+width_min_max])
            start_window = start_window + 1
        start_window = (taille_spectre - 2*width_min_max - 1)
        for i in range(taille_spectre - width_min_max, taille_spectre):   # -- End of spectrum --
            end_window = start_window + 1 + (i % 2)
            if np.max(minima[start_window:end_window]) < maxima[i-1]:
                maxima[i] = maxima[i-1]   # Removed is smaller
            else:
                maxima[i] = np.max(minima[end_window: taille_spectre])
            start_window = end_window
        ########## Lissage ##########
        start_window = math.ceil((width_min_max+1)/2)
        somme_ordo_window = np.sum(maxima[0:start_window])
        for i in range(0, width_smooth):                 # -- Start of spectrum --
            end_window = start_window + 1 + (i % 2)
            somme_ordo_window = somme_ordo_window + np.sum(maxima[start_window:end_window])
            ligne_base[i, 1] = somme_ordo_window/end_window
            start_window = end_window
        somme_ordo_window = np.sum(maxima[0:2*width_smooth])
        ligne_base[width_smooth, 1] = somme_ordo_window/(2*width_smooth)
        for i in range(width_smooth, taille_spectre-width_smooth):    # -- Main part of spectrum --
            somme_ordo_window = somme_ordo_window - maxima[i-width_smooth] + maxima[i+width_smooth]
            ligne_base[i, 1] = somme_ordo_window/(2*width_smooth)
        start_window = taille_spectre - 2*width_smooth
        somme_ordo_window = somme_ordo_window-maxima[start_window]
        ligne_base[taille_spectre - width_smooth, 1] = somme_ordo_window/(2*width_smooth)
        for i in range(taille_spectre-width_smooth, taille_spectre):    # -- End of spectrum --
            end_window = start_window + 1 + ((i+1) % 2)
            somme_ordo_window = somme_ordo_window-np.sum(maxima[start_window:end_window])
            ligne_base[i, 1] = somme_ordo_window/(taille_spectre - end_window)
            start_window = end_window
        ########## retour ##########
        return ligne_base
except :
    def rolling_ball_fonction(spectre, width_min_max, width_smooth):
        """
        Crée et retourne le fond continu par Rolling-Ball
        https://rdrr.io/cran/baseline/man/baseline.rollingBall.html
        width_min_max 	Width of local window for minimization/maximization
        width_smooth 	Width of local window for smoothing
        """
        # initialisations
        taille_spectre = spectre.shape[0]
        ligne_base = spectre.copy()
        ordonnees = spectre[:, 1]
        minima = np.zeros(taille_spectre)
        maxima = np.zeros(taille_spectre)
        start_window, end_window, somme_ordo_window = 0, 0, 0
        ########## Minimise ##########
        start_window = math.ceil((width_min_max+1)/2)
        minima[0] = np.min(ordonnees[0:start_window])
        for i in range(1, width_min_max):   # -- Start of spectrum --
            end_window = start_window + 1 + (i % 2)
            minima[i] = min(np.min(ordonnees[start_window:end_window]), minima[i-1])  # Check if new is smaller
            start_window = end_window
        for i in range(width_min_max, taille_spectre-width_min_max):   # -- Main part of spectrum --
            if ((ordonnees[start_window] <= minima[i-1])
                    and (ordonnees[start_window-width_min_max] != minima[i-1])):
                minima[i] = ordonnees[start_window]   # Next is smaller
            else:
                minima[i] = np.min(ordonnees[(i-width_min_max):(i+width_min_max)])
            start_window = start_window + 1
        start_window = (taille_spectre - 2*width_min_max - 1)
        for i in range(taille_spectre-width_min_max, taille_spectre):   # -- End of spectrum --
            end_window = start_window + 1 + (i % 2)
            if (np.min(ordonnees[start_window:(end_window)])) > minima[i-1]:
                minima[i] = minima[i-1]   # Removed is larger
            else:
                minima[i] = np.min(ordonnees[end_window:taille_spectre])
            start_window = end_window
        ########## Maximise ##########
        start_window = math.ceil((width_min_max+1)/2)
        maxima[0] = np.max(minima[0:start_window])
        for i in range(1, width_min_max):                # -- Start of spectrum --
            end_window = start_window + 1 + (i % 2)
            #end_window = start_window +1
            maxima[i] = max(np.max(minima[start_window:end_window]), maxima[i-1])  # Check if new is larger
            start_window = end_window
        for i in range(width_min_max, taille_spectre-width_min_max):     # -- Main part of spectrum --
            if ((minima[start_window] >= maxima[i-1]) and (minima[start_window-width_min_max] != maxima[i-1])):
                maxima[i] = minima[start_window]  # Next is larger
            else:
                maxima[i] = np.max(minima[i-width_min_max: i+width_min_max])
            start_window = start_window + 1
        start_window = (taille_spectre - 2*width_min_max - 1)
        for i in range(taille_spectre - width_min_max, taille_spectre):   # -- End of spectrum --
            end_window = start_window + 1 + (i % 2)
            if np.max(minima[start_window:end_window]) < maxima[i-1]:
                maxima[i] = maxima[i-1]   # Removed is smaller
            else:
                maxima[i] = np.max(minima[end_window: taille_spectre])
            start_window = end_window
        ########## Lissage ##########
        start_window = math.ceil((width_min_max+1)/2)
        somme_ordo_window = np.sum(maxima[0:start_window])
        for i in range(0, width_smooth):                 # -- Start of spectrum --
            end_window = start_window + 1 + (i % 2)
            somme_ordo_window = somme_ordo_window + np.sum(maxima[start_window:end_window])
            ligne_base[i, 1] = somme_ordo_window/end_window
            start_window = end_window
        somme_ordo_window = np.sum(maxima[0:2*width_smooth])
        ligne_base[width_smooth, 1] = somme_ordo_window/(2*width_smooth)
        for i in range(width_smooth, taille_spectre-width_smooth):    # -- Main part of spectrum --
            somme_ordo_window = somme_ordo_window - maxima[i-width_smooth] + maxima[i+width_smooth]
            ligne_base[i, 1] = somme_ordo_window/(2*width_smooth)
        start_window = taille_spectre - 2*width_smooth
        somme_ordo_window = somme_ordo_window-maxima[start_window]
        ligne_base[taille_spectre - width_smooth, 1] = somme_ordo_window/(2*width_smooth)
        for i in range(taille_spectre-width_smooth, taille_spectre):    # -- End of spectrum --
            end_window = start_window + 1 + ((i+1) % 2)
            somme_ordo_window = somme_ordo_window-np.sum(maxima[start_window:end_window])
            ligne_base[i, 1] = somme_ordo_window/(taille_spectre - end_window)
            start_window = end_window
        ########## retour ##########
        return ligne_base

try :
    @jit
    def SNIP_fonction(spectre, iterations, LLS_flag):
        """
        Crée et retourne le fond continu par SNIP
        """
        ########## LLS ##########
        if LLS_flag is True:
            spectre[:, 1] = np.log(np.log(np.sqrt(spectre[:, 1] + 1) + 1) + 1)
        ########## SNIP ##########
        dim_spectre = spectre.shape[0]
        fond = spectre.copy()
        for p in range(0, iterations):
            for i in range(p, dim_spectre-p):
                start_window = spectre[i, 1]
                end_window = (spectre[i-p, 1] + spectre[i+p, 1]) / 2
                fond[i, 1] = min(start_window, end_window)
            spectre[:, 1] = fond[:, 1]
        ########## inverse LLS ##########
        if LLS_flag is True:
            fond[:, 1] = (np.exp(np.exp(fond[:, 1]) - 1) - 1)**2 - 1
        ########## retour ##########
        return fond
except :
    def SNIP_fonction(spectre, iterations, LLS_flag):
        """
        Crée et retourne le fond continu par SNIP
        """
        ########## LLS ##########
        if LLS_flag is True:
            spectre[:, 1] = np.log(np.log(np.sqrt(spectre[:, 1] + 1) + 1) + 1)
        ########## SNIP ##########
        dim_spectre = spectre.shape[0]
        fond = spectre.copy()
        for p in range(0, iterations):
            for i in range(p, dim_spectre-p):
                start_window = spectre[i, 1]
                end_window = (spectre[i-p, 1] + spectre[i+p, 1]) / 2
                fond[i, 1] = min(start_window, end_window)
            spectre[:, 1] = fond[:, 1]
        ########## inverse LLS ##########
        if LLS_flag is True:
            fond[:, 1] = (np.exp(np.exp(fond[:, 1]) - 1) - 1)**2 - 1
        ########## retour ##########
        return fond


###################################################################################################
# fonctions de traitement des spectres
###################################################################################################
def creation_spectre_filtre(spectre_entier, tableau_bornes, filtre, taille, ordre, deriv):
    """
    Lisse et retourne le spectre lissé par diverses méthodes
    """
    spectre_filtre = creation_spectre_bornes(spectre_entier, tableau_bornes)
    if filtre == "Aucun":
        pass
    if filtre == "Savitzky-Golay":
        spectre_filtre[:, 1] = scipy.signal.savgol_filter(
            spectre_filtre[:, 1], taille, ordre, deriv, delta=1.0, axis=-1, mode='interp', cval=0.0)
    if filtre == "Median":
        spectre_filtre[:, 1] = scipy.signal.medfilt(spectre_filtre[:, 1], taille)
    if filtre == "Passe-bas":
        print("Pas encore codé")
        # spectre_filtre = spectre_filtre
        # pass
    return spectre_filtre


def creation_fond(spectre_filtre, fond, param1, param2, param3):
    """
    Crée et retourne le fond continu par diverses méthodes
    """
    if fond == "Aucun":
        fond_continu = np.zeros((spectre_filtre.shape[0], 2))
    if fond == "Rolling ball":
        fond_continu = spectre_filtre.copy()
        fond_continu = rolling_ball_fonction(fond_continu, param1, param2)
    if fond == "SNIP":
        fond_continu = spectre_filtre.copy()
        fond_continu = SNIP_fonction(fond_continu, param1, param3)
    if fond == "Top-hat":
        fond_continu = spectre_filtre.copy()
        str_el = np.repeat([1], param1)
        fond_continu[:, 1] = scipy.ndimage.white_tophat(fond_continu[:, 1], None, str_el)
    if fond == "Peak filling":
        print("Pas encore codé")
        fond_continu = spectre_filtre.copy()
        fond_continu[:, 1] = scipy.signal.medfilt(fond_continu[:, 1], param1)
    return fond_continu


try :
    @jit
    def creation_spectre_corrige(spectre_filtre, fond_continu):
        """
        Retourne le spectre lissé et soustrait du fond continu
        """
        spectre_corrige = spectre_filtre.copy()
        spectre_corrige[:, 1] = spectre_filtre[:, 1]-fond_continu[:, 1]
        return spectre_corrige
except :
    def creation_spectre_corrige(spectre_filtre, fond_continu):
        """
        Retourne le spectre lissé et soustrait du fond continu
        """
        spectre_corrige = spectre_filtre.copy()
        spectre_corrige[:, 1] = spectre_filtre[:, 1]-fond_continu[:, 1]
        return spectre_corrige


try :
    @jit
    def execute(rep_travail, spectre_corrige, fond_continu, nom_fichier, flag_sauve_fond):
        """
        Crée les répertoires de sauvegarde et sauvegarde le spectre traité
        actuellement affiché (fond en option)
        """
        repertoire_sauvegarde = creation_sous_repertoire(rep_travail)
        enregistre_fichier(spectre_corrige, repertoire_sauvegarde, nom_fichier)
        if flag_sauve_fond is True:
            repertoire_sauvegarde_fond = creation_sous_repertoire_fond(rep_travail)
            enregistre_fichier_fond(fond_continu, repertoire_sauvegarde_fond, nom_fichier)
except:
    def execute(rep_travail, spectre_corrige, fond_continu, nom_fichier, flag_sauve_fond):
        """
        Crée les répertoires de sauvegarde et sauvegarde le spectre traité
        actuellement affiché (fond en option)
        """
        repertoire_sauvegarde = creation_sous_repertoire(rep_travail)
        enregistre_fichier(spectre_corrige, repertoire_sauvegarde, nom_fichier)
        if flag_sauve_fond is True:
            repertoire_sauvegarde_fond = creation_sous_repertoire_fond(rep_travail)
            enregistre_fichier_fond(fond_continu, repertoire_sauvegarde_fond, nom_fichier)


def execute_en_bloc(rep_travail, type_fichier, tableau_bornes, type_filtre, taille_filtre, ordre,
                    deriv, type_fond, param1, param2, param3, flag_sauve_fond):
    """
    Crée les répertoires de sauvegarde, traite et sauvegarde
    tous les spectres du répertoire en cours (fond en option)
    """
    liste_fichiers = LIBStick_outils.creation_liste_fichiers(rep_travail, type_fichier)
    repertoire_sauvegarde = creation_sous_repertoire(rep_travail)
    if flag_sauve_fond is True:
        repertoire_sauvegarde_fond = creation_sous_repertoire_fond(rep_travail)
    for nom_fichier in liste_fichiers:
        spectre = LIBStick_outils.lit_spectre(nom_fichier, type_fichier)
        spectre = creation_spectre_filtre(
            spectre, tableau_bornes, type_filtre, taille_filtre, ordre, deriv)
        fond_continu = creation_fond(spectre, type_fond, param1, param2, param3)
        spectre = creation_spectre_corrige(spectre, fond_continu)
        enregistre_fichier(spectre, repertoire_sauvegarde, nom_fichier)
        if flag_sauve_fond is True:
            enregistre_fichier_fond(fond_continu, repertoire_sauvegarde_fond, nom_fichier)
