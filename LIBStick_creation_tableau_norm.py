#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 11 2020

@author: yannick
"""
###############################################################################
# 1- fonction qui liste des fichiers d'un répertoire
# 2- fonction qui ouvre un fichier, sépare les données en liste de listes
# 3- fonction normalise la seconde colonne : soustraction du minimum puis division par le maximum
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
# 5- fonction qui affiche et sauvegarde des graphes
# 6- lire et regrouper les secondes collonnes (spectres) de ces nouveaux fichier
#    sous la forme d'un tableau tsv et sauver un seul fichier
###############################################################################

import sys,os,numpy
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d as plt3d

sys.path.insert(0,os.path.join(os.path.expanduser("~"),"Desktop"))
sys.path.insert(0,"./dossier_mes_modules/")

###############################################################################
# 1- fonction qui liste des fichiers *.tsv d'un répertoire
###############################################################################
#def repertoire_de_travail_0(rep_script):
#    rep_travail=rep_script+"/test_python_Zone_1/528_543/"
#    #rep_travail=rep_travail+"/test_python_Zone_1/592_608/"
#    return rep_travail

def repertoire_de_travail(rep_script,rep_travail_relatif):
    rep_travail=rep_script+"/"+rep_travail_relatif
    return rep_travail

def creation_liste_fichiers(rep_travail):
    os.chdir(rep_travail)
    liste=[]
    for fichier in os.listdir():
        if (os.path.isfile(fichier) and fichier[-3:] == "tsv") :
            liste.append(fichier)
    liste.sort()
    return liste

###############################################################################
# 2- fonction qui ouvre chaque fichier de la liste, sépare les données en liste de listes,
#    extrait la seconde colonne et l'ajoute à un tableau numpy
###############################################################################
def creer_tableau(liste):
    i=0
    for fichier in liste :
        if i==0 :
            fentree=numpy.loadtxt(fichier, delimiter="\t", usecols=[1])
            tableau=numpy.zeros((fentree.shape[0],0))
            tableau=numpy.column_stack((tableau,fentree))
        else :
            fentree=numpy.loadtxt(fichier, delimiter="\t", usecols=[1])
            tableau=numpy.column_stack((tableau,fentree))
        i=i+1
    return tableau

def creer_tableau_abscisses(liste):
    fichier0=numpy.loadtxt(liste[0], delimiter="\t", usecols=[0])
    tableau_abscisses=numpy.zeros((fichier0.shape[0],0))
    tableau_abscisses=numpy.column_stack((tableau_abscisses,fichier0))
    return tableau_abscisses
    
###############################################################################
# 3- fonction normalise les colonnes du tableau
###############################################################################
def normalise_tableau_aire(tableau):
    for colonne in range(tableau.shape[1]):
        minimum=tableau[:,colonne].min()
        tableau[:,colonne] = (tableau[:,colonne] - minimum)
        aire=tableau[:,colonne].sum()
        tableau[:,colonne] = (tableau[:,colonne] /aire)
    tableau=tableau/tableau.max()
    return tableau
        
###############################################################################
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###############################################################################
def enregistre_fichier(tableau,nom_fichier):
    numpy.savetxt(nom_fichier,tableau,delimiter="\t", newline="\n")
    
def enregistre_fichier_virgule(tableau,nom_fichier):
    tableau=tableau.astype(str)
    tableau=numpy.char.replace(tableau, ".", ",")
    numpy.savetxt(nom_fichier,tableau,delimiter="\t", newline="\n", fmt="%s")
    
def enregistre_tableau_abscisses(tableau_abscisses):
    numpy.savetxt("tableau_abscisses.txt", tableau_abscisses, newline="\n")
    
###############################################################################
# 5- fonctions qui affiche et sauvegarde des graphes
###############################################################################
def tableau_brut_transpose_256gris(tableau_brut):
    tableau8bits_brut=tableau_brut*255
    tableau8bits_brut=tableau8bits_brut.transpose()
    tableau8bits_brut=tableau8bits_brut.astype(int) 
    return tableau8bits_brut

def graphique_brut_sauvegarde(tableau8bits_brut) :
    plt.imsave("figure_brute.png",tableau8bits_brut, cmap="inferno")

def tableau_transpose_256gris(tableau_norm):
    tableau8bits=tableau_norm*255
    tableau8bits=tableau8bits.transpose()
    tableau8bits=tableau8bits.astype(int) 
    return tableau8bits
    
def graphique_creation(tableau8bits,nom_echantillon,bornes):
    #fig=plt.figure()
    fig, ax=plt.subplots()
    #plt.imshow(tableau8bits, cmap="gray", extent=[bornes[0],bornes[1],tableau8bits.shape[0],0], aspect="auto")
    plt.imshow(tableau8bits, cmap="inferno", extent=[bornes[0],bornes[1],tableau8bits.shape[0],0], aspect="auto")
#    print(tableau8bits.shape[0])
#    print(tableau8bits.shape[1])
    #imageplot=plt.imshow(tableau8bits, cmap="hot")
    #imageplot=plt.imshow(tableau8bits, cmap="nipy_spectral")
    #plt.colorbar()
    plt.title(nom_echantillon)
    plt.xlabel("Longueur d'onde (nm)")
    plt.ylabel( "Spectres suivant z")
    plt.yticks(range(0,tableau8bits.shape[0],5))
    ax.yaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.xaxis.set_tick_params(which='minor', bottom=False)
    plt.savefig("figure_plot.png")
    #plt.xlim(bornes[0], bornes[1])
    #plt.ioff()
    plt.show(block=False)
    
def graphique_3D_creation(tableau8bits,nom_echantillon,bornes):
    xx, yy = numpy.mgrid[0:tableau8bits.shape[0], 0:tableau8bits.shape[1]]
    #fig = plt.figure(figsize=(15,15))
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_surface(xx, yy, tableau8bits ,rstride=1, cstride=1, cmap="inferno",linewidth=0, antialiased=False)
    ax.view_init(80, 30)
    
    plt.title(nom_echantillon)
    plt.ylabel("Longueur d'onde (nm)")
    plt.xlabel( "Spectres suivant z")
    #ax.set_ylim(bornes[0],bornes[1])
    
    plt.xticks(range(0,tableau8bits.shape[0],5))
    ax.xaxis.get_ticklocs(minor=True)
    ax.minorticks_on()
    ax.yaxis.set_tick_params(which='minor', bottom=False)

    plt.show(block=False)

def graphique_sauvegarde(tableau8bits) :
    plt.imsave("figure.png",tableau8bits, cmap="inferno")

###############################################################################
# programme principal
###############################################################################
def main (rep_travail,nom_echantillon,bornes, flag_2D, flag_3D) :
    global tableau_norm
    liste_fichiers=creation_liste_fichiers(rep_travail)
    
    tableau_abscisses=creer_tableau_abscisses(liste_fichiers)
    enregistre_tableau_abscisses(tableau_abscisses)
    
    tableau_brut=creer_tableau(liste_fichiers)
    tableau8bits_brut=tableau_brut_transpose_256gris(tableau_brut)
    graphique_brut_sauvegarde(tableau8bits_brut)
    
    tableau_norm=normalise_tableau_aire(tableau_brut)
    enregistre_fichier(tableau_norm,"tableau_normalisé.txt")
    enregistre_fichier_virgule(tableau_norm,"tableau_normalisé_virgules.txt")
    tableau8bits_norm=tableau_transpose_256gris(tableau_norm)
    graphique_sauvegarde(tableau8bits_norm)
    
    if flag_2D == 1 :
        graphique_creation(tableau8bits_norm,nom_echantillon,bornes)
    if flag_3D == 1 :
        graphique_3D_creation(tableau8bits_norm,nom_echantillon,bornes)   


