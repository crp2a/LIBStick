#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 12:20:38 2020

@author: yannick
"""
###############################################################################
# 1- fonction qui liste des fichiers d'un répertoire
# 2- fonction qui ouvre un fichier et extrait les lignes de 528 à 543 nm ou de 592 à 608 nm
# 3- fonction qui crée un sous répertoire d'un certain nom passé en argument
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
# 5- faire une boucle sur la liste de fichiers
# 6- lire et regrouper les secondes collonnes (spectres) de ces nouveaux fichier
#    sous la forme d'un tableau tsv et sauver un seul fichier
###############################################################################

import sys,os,numpy
import LIBStick_creation_tableau_norm
import LIBStick_echange_vars
sys.path.insert(0,os.path.join(os.path.expanduser("~"),"Desktop"))
sys.path.insert(0,"./dossier_mes_modules/")

###############################################################################
# 1- fonction qui liste des fichiers *.asc d'un répertoire
###############################################################################
def creation_liste_fichiers(rep_travail):
    os.chdir(rep_travail)
    liste=[]
    for fichier in os.listdir():
        if (os.path.isfile(fichier) and fichier[-3:] == "asc") :
            liste.append(fichier)
    liste.sort()
    return liste

def creation_nom_echantillon(liste_fichiers):
    nom_echantillon=LIBStick_echange_vars.liste_fichiers[0][0:-6]
    return nom_echantillon

###############################################################################
# 2- fonction qui ouvre un fichier et extrait les lignes de 528 à 543 nm ou de 592 à 608 nm
###############################################################################
#def lit_fichier_0(fichier, bas, haut):
#    fentree=open(fichier,"r",encoding="Latin-1")
#    document_tronc=""
#    i=0
#    for ligne in fentree :
#        i=i+1
#        if i>64 :
#            liste_mots=ligne.split()
#            if float(liste_mots[0]) >= bas and float(liste_mots[0]) <= haut :
#                #document2=document2 + "\n" + ligne
#                document_tronc=document_tronc + ligne
#    fentree.close()
#    document_tronc.replace(" ", "\t")
#    return document_tronc

def lit_fichier(fichier, bas, haut):
    document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
    document_tronc=numpy.zeros((0,2))
    for ligne in document :
        if (ligne[0]>=bas and ligne[0]<=haut) :
            document_tronc=numpy.row_stack((document_tronc,ligne))
            #document_tronc=numpy.vstack((document_tronc,ligne)) #idem ci-dessus
    return document_tronc

def lit_spectre(fichier):
    document=numpy.loadtxt(fichier,delimiter="\t",skiprows=64, usecols=[0,1],dtype=float,encoding="Latin-1")
    spectre=numpy.zeros((0,2))
    for ligne in document :
        if (ligne[0]<=608) :
            spectre=numpy.row_stack((spectre,ligne))
    return spectre

###############################################################################
# 3- fonction qui crée un sous répertoire d'un certain nom passé en argument
###############################################################################
#def repertoire_de_travail_0(rep_script):
#    rep_travail=rep_script+"/test_python_Zone_1/"
#    return rep_travail

def repertoire_de_travail(rep_script,rep_travail_relatif):
    rep_travail=rep_script+"/"+rep_travail_relatif
    return rep_travail

def creation_sous_repertoire(rep_travail,tableau_bornes):
    if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1])):
        os.mkdir(rep_travail + "/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1]))
    if not os.path.isdir(rep_travail + "/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1])):
        os.mkdir(rep_travail + "/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1]))

###############################################################################
# 4- fonction qui sauvegarde le résultat dans un fichier tsv dans le sous répertoire
###############################################################################
#def enregistre_fichier_0(document,repertoire,nom_fichier):
#    os.chdir(repertoire)
#    nom_fichier=nom_fichier[0:-4] + "_" + repertoire[-7:] +".tsv"
#    fsortie=open(nom_fichier,"w")
#    fsortie.write(document)
#    fsortie.close()
#    #ecrit_tsv=csv.writer(fsortie, delimiter = '\t')
#    #ecrit_tsv.writerow(document) 

def enregistre_fichier(document,repertoire,nom_fichier):
    os.chdir(repertoire)
    nom_fichier=nom_fichier[0:-4] + "_" + repertoire[-7:] +".tsv"
    numpy.savetxt(nom_fichier,document, delimiter="\t")
     
###############################################################################
# programme principal
###############################################################################
def main_commun(rep_script, rep_travail, tableau_bornes) :
    creation_sous_repertoire(rep_travail,tableau_bornes)
    #LIBStick_echange_vars.liste_fichiers=creation_liste_fichiers(rep_travail)
    LIBStick_echange_vars.nombre_fichiers=len(LIBStick_echange_vars.liste_fichiers)
    nom_echantillon=creation_nom_echantillon(LIBStick_echange_vars.liste_fichiers)
        
#    for i in range(len(liste_fichiers)) :
#        os.chdir(rep_travail)    
#        document_528_543=lit_fichier_0(liste_fichiers[i], 528, 543)
#        document_592_608=lit_fichier_0(liste_fichiers[i], 592, 608)
#        enregistre_fichier_0(document_528_543,rep_travail+"/528_543",liste_fichiers[i])
#        enregistre_fichier_0(document_592_608,rep_travail+"/592_608",liste_fichiers[i])

#    for i in range(len(liste_fichiers)) :
#        os.chdir(rep_travail)
#        document_528_543=lit_fichier(liste_fichiers[i], 528, 543)
#        document_592_608=lit_fichier(liste_fichiers[i], 592, 608)
#        enregistre_fichier(document_528_543,rep_travail+"/528_543",liste_fichiers[i])
#        enregistre_fichier(document_592_608,rep_travail+"/592_608",liste_fichiers[i])
        
    for i in range(len(LIBStick_echange_vars.liste_fichiers)) :
        for bornes in tableau_bornes :
            os.chdir(rep_travail)
            document=lit_fichier(LIBStick_echange_vars.liste_fichiers[i], bornes[0], bornes[1])
            enregistre_fichier(document,rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1]) ,LIBStick_echange_vars.liste_fichiers[i])

#    os.chdir(rep_script)
#    LIBStick_normalisation_creation_tableau.main(rep_travail_relatif+"528_543/")
#    os.chdir(rep_script)
#    LIBStick_normalisation_creation_tableau.main(rep_travail_relatif+"592_608/")

    for bornes in tableau_bornes :
        os.chdir(rep_script)
        LIBStick_creation_tableau_norm.main(rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1])+"/", nom_echantillon,bornes)


def main(rep_travail, tableau_bornes) :
    rep_script=os.getcwd()
    main_commun(rep_script, rep_travail, tableau_bornes)

if __name__=='__main__':
    tableau_bornes=numpy.array([[528, 543],[592, 608]])
    rep_script=os.getcwd()
    #rep_travail=repertoire_de_travail_0(rep_script)
    if (len(sys.argv)) <= 1 :
        rep_travail_relatif="/"
    else :
        rep_travail_relatif=sys.argv[1]
    rep_travail=repertoire_de_travail(rep_script,rep_travail_relatif)
    main_commun(rep_script, rep_travail, tableau_bornes)
    
