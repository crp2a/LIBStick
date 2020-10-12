#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 13 14:41:09 2020

@author: yannick
"""

import os, numpy, math
import scipy.signal

###############################################################################
# 1- fonction qui liste des fichiers *.asc ou *.tsv d'un répertoire
###############################################################################
def creation_liste_fichiers(rep_travail, type_fichier):
    os.chdir(rep_travail)
    liste=[]
    if type_fichier == "IVEA" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "asc") :
                liste.append(fichier)
    if type_fichier == "LIBStick" :
        for fichier in os.listdir():
            if (os.path.isfile(fichier) and fichier[-3:] == "tsv") :
                liste.append(fichier)
    liste.sort()
    return liste

#def creation_nom_echantillon(liste_fichiers):
#    nom_echantillon=LIBStick_echange_vars.L_ext_liste_fichiers[0][0:-6]
#    return nom_echantillon


###############################################################################
# 2- fonction qui ouvre un fichier
###############################################################################
def lit_spectre(fichier, type_fichier):
    if type_fichier == "IVEA" :
        document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
        spectre=numpy.zeros((0,2))
        for ligne in document :
            if (ligne[0]<=1013) :
                spectre=numpy.row_stack((spectre,ligne))
    if type_fichier == "LIBStick" :
        spectre=numpy.loadtxt(fichier,delimiter="\t",usecols=[0,1],dtype=float,encoding="Latin-1")
    return spectre

def creation_spectre_bornes(spectre_entier, tableau_bornes):
    spectre_limite_bornes = numpy.zeros((0,2))
    for ligne in spectre_entier :
        if ligne[0] > tableau_bornes[0] and ligne[0] < tableau_bornes[1] :
            spectre_limite_bornes = numpy.row_stack((spectre_limite_bornes,ligne))
    return spectre_limite_bornes


###############################################################################
# 3- fonction qui crée un sous répertoire d'un certain nom passé en argument
###############################################################################
def repertoire_de_travail(rep_script,rep_travail_relatif):
    rep_travail=rep_script+"/"+rep_travail_relatif
    return rep_travail

def creation_sous_repertoire(rep_travail):
    repertoire_sauvegarde = rep_travail + "/traitement"
    if os.path.isdir(repertoire_sauvegarde) == False :
        os.mkdir(repertoire_sauvegarde)
    return repertoire_sauvegarde
  
          
###############################################################################
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###############################################################################
def enregistre_fichier(spectre,repertoire,nom_fichier):
    nom_fichier=repertoire + "/" + nom_fichier[0:-4] + "_corrige.tsv"
    numpy.savetxt(nom_fichier,spectre, delimiter="\t")
  
    
###############################################################################
# 5- fonctions de filtres
###############################################################################
def rolling_ball_fonction(spectre, wm, ws) :
    ########## initialisations
    taille_spectre = spectre.shape[0]
    ligne_base = spectre.copy()
    y = spectre[:,1]
    T1 = numpy.zeros(taille_spectre)
    T2 = numpy.zeros(taille_spectre)
    a, b, v = 0, 0, 0
    ########## Minimise ##########
    a = math.ceil((wm+1)/2)
    T1[0] = numpy.min(y[0:a])
    for i in range(1,wm) :   # -- Start of spectrum --
        b = a +1 +(i%2)
        T1[i] = min(numpy.min(y[a:b]), T1[i-1]) # Check if new is smaller
        a = b   
    for i in range(wm, taille_spectre-wm) :   # -- Main part of spectrum --
        if ( (y[a] <= T1[i-1]) and (y[a-wm] != T1[i-1]) ) :
            T1[i] = y[a]   # Next is smaller
        else :
            T1[i] = numpy.min(y[(i-wm):(i+wm)])
        a = a + 1          
    a = (taille_spectre - 2*wm -1)
    for i in range(taille_spectre-wm, taille_spectre ) :   # -- End of spectrum --
        b =  a +1 + (i%2)
        if (numpy.min(y[a:(b)])) > T1[i-1] :
            T1[i] = T1[i-1]   # Removed is larger
        else :
            T1[i] = numpy.min(y[b:taille_spectre])
        a = b
    ########## Maximise ##########
    a = math.ceil((wm+1)/2)
    T2[0] = numpy.max(T1[0:a])
    for i in range(1,wm) :                # -- Start of spectrum --
        b = a +1 +(i%2)
        #b = a +1
        T2[i] = max(numpy.max(T1[a:b]), T2[i-1]) # Check if new is larger
        a = b    
    for i in range(wm, taille_spectre-wm) :     # -- Main part of spectrum --
        if ( (T1[a] >= T2[i-1]) and (T1[a-wm] != T2[i-1]) ) :
            T2[i] = T1[a] # Next is larger
        else :
            T2[i] = numpy.max(T1[i-wm : i+wm])
        a = a + 1
    a = (taille_spectre - 2*wm -1)
    for i in range(taille_spectre -wm, taille_spectre) :   # -- End of spectrum --
        b = a +1 +(i%2)
        if (numpy.max(T1[a:b]) < T2[i-1]) :
            T2[i] = T2[i-1]   # Removed is smaller
        else :
            T2[i] = numpy.max(T1[b : taille_spectre])
        a = b     
    ########## Lissage ##########
    a =math.ceil((wm+1)/2)
    v = numpy.sum(T2[0:a])
    for i in range(0,ws) :                 # -- Start of spectrum --
        b = a + 1+ (i%2)
        v = v + numpy.sum(T2[a:b])
        ligne_base[i ,1] = v/b
        a = b
    v = numpy.sum(T2[0:2*ws])
    ligne_base[ws, 1] = v/(2*ws)
    for i in range(ws, taille_spectre-ws)  :    # -- Main part of spectrum --
        v = v - T2[i-ws] + T2[i+ws]
        ligne_base[i ,1] = v/(2*ws)
    a = taille_spectre -2*ws
    v = v-T2[a]
    ligne_base[taille_spectre -ws ,1] = v/(2*ws)
    for i in range(taille_spectre-ws, taille_spectre) :    # -- End of spectrum --
        b = a +1 +((i+1)%2)
        v = v-numpy.sum(T2[a:b])
        ligne_base[i ,1] = v/(taille_spectre -b)
        a = b
    ########## retour ##########
    return ligne_base


def SNIP_fonction (spectre, iterations, LLS_flag) :
    ########## LLS ##########
    if LLS_flag == True :
        spectre[:,1] = numpy.log(numpy.log(numpy.sqrt(spectre[:,1] + 1) + 1) + 1)  
    ########## SNIP ##########
    dim_spectre = spectre.shape[0]
    fond = spectre.copy()
    for p in range(0,iterations) :
        for i in range(p, dim_spectre-p) :
            a = spectre[i,1]
            b = (spectre[i-p,1] + spectre[i+p,1]) / 2
            fond[i,1] = min(a,b)
        spectre[:,1] = fond[:,1]            
    ########## inverse LLS ##########
    if LLS_flag == True :
        fond[:,1] = (numpy.exp(numpy.exp(fond[:,1]) - 1) - 1)**2 - 1
    ########## retour ##########
    return fond


###############################################################################
# 6- fonctions de traitement des spectres
###############################################################################
def creation_spectre_filtre(spectre_entier, tableau_bornes, filtre, taille, ordre):
    spectre_filtre = creation_spectre_bornes(spectre_entier, tableau_bornes)
    if filtre == "Aucun" :
        pass
    if filtre == "Savitzky-Golay" :
        #print(spectre_limite_bornes[:,1])
        spectre_filtre[:,1] = scipy.signal.savgol_filter(spectre_filtre[:,1], taille, ordre, deriv=0, delta=1.0, axis=-1, mode='interp', cval=0.0)
    if filtre == "Median" :
        spectre_filtre[:,1] = scipy.signal.medfilt(spectre_filtre[:,1], taille)
    if filtre == "Passe-bas" :
        print ("Pas encore codé")
        spectre_filtre = spectre_filtre
        pass
    return spectre_filtre

def creation_fond(spectre_filtre, fond, param1, param2, param3):
    if fond =="Aucun" :
        fond_continu = numpy.zeros((spectre_filtre.shape[0],2))
    if fond == "Rolling ball" :
        fond_continu = spectre_filtre.copy()
        fond_continu = rolling_ball_fonction(fond_continu, param1, param2)
    if fond =="SNIP" :
        fond_continu = spectre_filtre.copy()
        fond_continu = SNIP_fonction (fond_continu, param1, param3)
    if fond == "Top-hat" :
        fond_continu = spectre_filtre.copy()
        str_el = numpy.repeat([1], param1)
        fond_continu[:,1] = scipy.ndimage.white_tophat(fond_continu[:,1], None, str_el)
    if fond == "Peak filling" :
        print ("Pas encore codé")
        fond_continu = spectre_filtre.copy()
        fond_continu[:,1] = scipy.signal.medfilt(fond_continu[:,1], param1)
    return fond_continu

def creation_spectre_corrige(spectre_filtre, fond_continu):
    spectre_corrige = spectre_filtre.copy()
    spectre_corrige[:,1] = spectre_filtre[:,1]-fond_continu[:,1]
    return spectre_corrige

def execute(rep_travail, spectre_corrige, nom_fichier):
    repertoire_sauvegarde = creation_sous_repertoire(rep_travail)
    enregistre_fichier(spectre_corrige, repertoire_sauvegarde, nom_fichier)

def execute_en_bloc(rep_travail, type_fichier, tableau_bornes, type_filtre, taille_filtre, ordre, type_fond, param1, param2, param3) :
    liste_fichiers = creation_liste_fichiers(rep_travail, type_fichier)
    repertoire_sauvegarde = creation_sous_repertoire(rep_travail)
    for nom_fichier in liste_fichiers :
        spectre = lit_spectre(nom_fichier, type_fichier)
        spectre = creation_spectre_filtre(spectre, tableau_bornes, type_filtre, taille_filtre, ordre)
        fond_continu = creation_fond(spectre, type_fond, param1, param2, param3)
        spectre= creation_spectre_corrige(spectre, fond_continu)
        enregistre_fichier(spectre, repertoire_sauvegarde, nom_fichier)
        