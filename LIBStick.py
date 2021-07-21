#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:32:41 2020

@author: yannick
"""

#import tkinter, tkinter.filedialog, tkinter.ttk
#from LIBStick_IHM_extraction import *

import tkinter, tkinter.filedialog, tkinter.ttk
import tkinter.font, tkinter.messagebox
#import ttkwidgets
import os, configparser, pathlib
import math, numpy, pandas
import PIL.Image, PIL.ImageTk

import LIBStick_outils
import LIBStick_traitements_spectres
import LIBStick_extraction_spectres
import LIBStick_comp_spectres
import LIBStick_ACP


###############################################################################
# 0- initialisations
###############################################################################
#s = tkinter.ttk.Style()
#s.theme_use("alt")

#couleur_interface="lavender"
#couleur_interface="linen"
couleur_interface="light grey"
rep_LIBStick=os.getcwd()
largeur_lignes=2
taille_case = [3,2]
nom_fichier_seul_L_trait=nom_fichier_seul_L_ext=nom_fichier_seul_L_comp=nom_fichier_seul_L_ACP=""

class CaseConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

config=CaseConfigParser()
config.read("LIBStick.ini")
#dico_defaut={"LIBStick_traitement" : "LIBStick_traitement_defaut" ,
#             "LIBStick_extraction" : "LIBStick_extraction_defaut" ,
#             "LIBStick_compare" : "LIBStick_compare_defaut"}

def lit_section_fichier_ini(section) :
    dictionnaire = {}
    options = config.options(section)
    for option in options:
        try:
            dictionnaire[option] = config.get(section, option)
            #if dictionnaire[option] == -1:
            #    DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dictionnaire[option] = None
    return dictionnaire
        
#def reset_section_fichier_ini(section, section_defaut) :
#    options =config.options(section)
#    fichier=open(rep_LIBStick + "/LIBStick.ini", "r+")
#    for option in options :
#        config.set(section,option,config.get(section_defaut,option))
#    config.write(fichier)
#    fichier.close()

def reset_fichier_ini():
    fichier=open(rep_LIBStick + "/LIBStick.ini", "w")
    fichier_reset=open(rep_LIBStick+"/LIBStick_reset.ini", "r")
    lignes= fichier_reset.readlines()
    fichier.writelines(lignes)
    fichier.close()
    fichier_reset.close()
    fenetre_message_ini = tkinter.messagebox.showinfo(title="Attention !", message="Veuillez redémarrer LIBStick pour retrouver les paramètres par défaut.")
    
#def ecrit_section_option_fichier_ini(section, option, valeur) :
#    fichier=open(rep_LIBStick + "/LIBStick.ini", "r+")
#    config.set(section, option, valeur)
#    config.write(fichier)    
#    fichier.close()

def ecrit_fichier_ini() :
    creation_tab_bornes_L_ext()
    creation_tab_bornes_L_comp()
    fichier=open(rep_LIBStick + "/LIBStick.ini", "r+")
    dico_sauvegarde_L_ext = {"flag_zone2_L_ext": "flag_zone2_L_ext.get()",
                             "flag_2D_L_ext" : "flag_2D_L_ext.get()",
                             "flag_3D_L_ext" : "flag_3D_L_ext.get()",
                             "flag_image_brute_L_ext" : "flag_image_brute_L_ext.get()",
                             "borne_zone1_inf_L_ext" : "tableau_bornes_L_ext[0,0]",
                             "borne_zone1_sup_L_ext" : "tableau_bornes_L_ext[0,1]",
                             "borne_zone2_inf_L_ext" : "tableau_bornes_L_ext[1,0]",
                             "borne_zone2_sup_L_ext" : "tableau_bornes_L_ext[1,1]",
                             "rep_travail_L_ext" : "rep_travail_L_ext"
                             }
    dico_sauvegarde_L_comp = {"flag_denominateur_L_comp": "flag_denominateur_L_comp.get()",
                             "flag_2D_L_comp" : "flag_2D_L_comp.get()",
                             "flag_3D_L_comp" : "flag_3D_L_comp.get()",
                             "flag_traitement_L_comp" : "flag_traitement_L_comp.get()",
                             "flag_stat_L_comp" : "flag_stat_L_comp.get()",
                             "borne_zone1_inf_L_comp" : "tableau_bornes_L_comp[0,0]",
                             "borne_zone1_sup_L_comp" : "tableau_bornes_L_comp[0,1]",
                             "borne_zone2_inf_L_comp" : "tableau_bornes_L_comp[1,0]",
                             "borne_zone2_sup_L_comp" : "tableau_bornes_L_comp[1,1]",
                             "rep_travail_L_comp" : "rep_travail_L_comp"
                             }
    for section in config.sections() :
        if section == "LIBStick_extraction" :
            for option,action in  dico_sauvegarde_L_ext.items() :
                config.set(section, str(option), str(eval(action)))
        if section == "LIBStick_compare" :
            for option,action in dico_sauvegarde_L_comp.items() :
                config.set(section, str(option), str(eval(action)))
    config.write(fichier)
    fichier.close() 
  
    
    


###############################################################################
###############################################################################
# Fonctions LIBStick_IHM_traitement : onglet 1
###############################################################################
###############################################################################
def __________L_trait__________():pass
###############################################################################
# 0- initialisations
###############################################################################
def charge_param_L_trait() :
    dictionnaire_ini_L_trait=lit_section_fichier_ini("LIBStick_traitement")
    rep_travail_L_trait = dictionnaire_ini_L_trait["rep_travail_L_trait"]
    return rep_travail_L_trait
    
rep_travail_L_trait=charge_param_L_trait()

limites_spectre_L_trait=numpy.array([198.0,1013.0])             # limites min et max de l'affichage du spectre
limites_affichage_spectre_L_trait=numpy.array([198.0,1013.0])   # limites de l'affichage du spectre à l'écran
coord_zoom_L_trait=numpy.array([198,0,1013,0])
delta_limites_L_trait=limites_affichage_spectre_L_trait[1]-limites_affichage_spectre_L_trait[0]
flag_premier_lamda_L_trait=True
#flag_premier_fond_L_trait=True
l_L_trait=0.0
spectre_entier_L_trait=numpy.zeros((0,2))
spectre_corrige_L_trait=numpy.zeros((0,2))
tableau_bornes_L_trait=numpy.array([300.0, 608.0])

def affiche_nom_spectre_onglet1() :
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_trait)

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_trait() :
    tableau_bornes_L_trait[0]=variable_1_L_trait.get()
    tableau_bornes_L_trait[1]=variable_2_L_trait.get()
    return tableau_bornes_L_trait

def choix_fichier_L_trait():
    global nom_fichier_seul_L_trait
    global type_fichier_L_trait
    global rep_travail_L_trait
    global liste_fichiers_L_trait
    global nombre_fichiers_L_trait
    nom_fichier_L_trait = tkinter.filedialog.askopenfilename(initialdir=rep_travail_L_trait,
                                                                 title='Choisissez un fichier spectre',
                                                                 filetypes=(("fichiers IVEA","*.asc"),
                                                                            ("fichiers SciAps","*.csv"),
                                                                            ("fichiers LIBStick","*.tsv"),
                                                                            ("fichiers LIBStick moyen","*.mean")))
    nom_fichier_seul_L_trait=os.path.basename(nom_fichier_L_trait)    
    type_fichier_L_trait=pathlib.Path(nom_fichier_seul_L_trait).suffix
#    type_fichier_L_trait.set(pathlib.Path(nom_fichier_seul_L_trait).suffix)
    rep_travail_L_trait = os.path.dirname(nom_fichier_L_trait)
    liste_fichiers_L_trait=LIBStick_outils.creation_liste_fichiers(rep_travail_L_trait, type_fichier_L_trait)
    nombre_fichiers_L_trait=len(liste_fichiers_L_trait)
    entree_spectre_L_trait.configure(to=nombre_fichiers_L_trait)
    lit_affiche_spectre_L_trait()
    bouton_visualisation_L_trait.configure(state="normal")
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_trait)
    
def visualisation_L_trait():
    global fond_continu_L_trait
    global spectre_corrige_L_trait
    global tableau_bornes_L_trait
    tableau_bornes_L_trait=creation_tab_bornes_L_trait()
    spectre_filtre_L_trait = LIBStick_traitements_spectres.creation_spectre_filtre(spectre_entier_L_trait,
                                                                                          tableau_bornes_L_trait,
                                                                                          type_filtre_L_trait.get(),
                                                                                          taille_filtre_L_trait.get(),
                                                                                          ordre_filtre_L_trait.get(),
                                                                                          derivee_filtre_L_trait.get())
    fond_continu_L_trait = LIBStick_traitements_spectres.creation_fond(spectre_filtre_L_trait,
                                                                       type_fond_L_trait.get(),
                                                                       param1_fond_L_trait.get(),
                                                                       param2_fond_L_trait.get(),
                                                                       param3_fond_L_trait.get())
    spectre_corrige_L_trait=LIBStick_traitements_spectres.creation_spectre_corrige(spectre_filtre_L_trait, fond_continu_L_trait)
    affiche_spectre_L_trait()
    affiche_fond_L_trait()
    affiche_spectre_corrige_L_trait()
    bouton_execute_L_trait.configure(state="normal")
    
def execute_L_trait():
    flag = flag_tous_fichiers_L_trait.get()
    if flag == False :
        LIBStick_traitements_spectres.execute(rep_travail_L_trait, spectre_corrige_L_trait, nom_fichier_seul_L_trait)
    if flag == True :
        LIBStick_traitements_spectres.execute_en_bloc(rep_travail_L_trait, type_fichier_L_trait, tableau_bornes_L_trait,
                                                      type_filtre_L_trait.get(), taille_filtre_L_trait.get(), ordre_filtre_L_trait.get(), derivee_filtre_L_trait.get(),
                                                      type_fond_L_trait.get(), param1_fond_L_trait.get(), param2_fond_L_trait.get(),param3_fond_L_trait.get())
#        LIBStick_traitements_spectres.execute_en_bloc(rep_travail_L_trait, type_fichier_L_trait.get(), tableau_bornes_L_trait,
#                                                      type_filtre_L_trait.get(), taille_filtre_L_trait.get(), ordre_filtre_L_trait.get(), derivee_filtre_L_trait.get(),
#                                                      type_fond_L_trait.get(), param1_fond_L_trait.get(), param2_fond_L_trait.get(),param3_fond_L_trait.get())
    
###############################################################################
# fonctions graphiques du caneva du spectre (frame1_L_trait)
###############################################################################
def lit_affiche_spectre_L_trait():
    global spectre_entier_L_trait
    global limites_spectre_L_trait
    global fond_continu_L_trait
    os.chdir(rep_travail_L_trait)
    spectre_entier_L_trait=LIBStick_outils.lit_spectre(nom_fichier_seul_L_trait, type_fichier_L_trait)
    limites_spectre_L_trait=lit_limites_abscisses_L_trait(spectre_entier_L_trait)
    affiche_spectre_L_trait()
    fond_continu_L_trait= numpy.zeros((spectre_entier_L_trait.shape[0],2)) #initialisation de 
    
def lit_limites_abscisses_L_trait(spectre):
    tableau_abscisses=spectre[:,0]
    limites_spectre=numpy.zeros((2))
    limites_spectre[0]=tableau_abscisses[0]             # lit le valeurs min et max du spectre
    limites_spectre[1]=tableau_abscisses[-1]
    variable_zoom_inf_L_trait.set(limites_spectre[0])   # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_sup_L_trait.set(limites_spectre[1])
    entree_zoom_inf_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])  #fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_sup_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree_zoom_inf_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree_zoom_sup_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree1_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree2_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    return limites_spectre

def affiche_lambda_L_trait(event):
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    if flag_premier_lamda_L_trait == False :
        canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
        canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
    l= event.x*delta_limites_L_trait/1000+limites_affichage_spectre_L_trait[0]
    lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
    flag_premier_lamda_L_trait=False
    
def affiche_position_souris_L_trait(event):
    global ligne_position_0_L_trait
    global ligne_position_1_L_trait
    canevas0_L_trait.delete(ligne_position_0_L_trait)
    ligne_position_0_L_trait=canevas0_L_trait.create_line(event.x,0,event.x,200, fill="green")
    canevas1_L_trait.delete(ligne_position_1_L_trait)
    ligne_position_1_L_trait=canevas1_L_trait.create_line(event.x,0,event.x,200, fill="green")
    
def affiche_position_souris_motion_L_trait(event):
    global ligne_position_0_L_trait
    global ligne_position_1_L_trait
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    canevas0_L_trait.delete(ligne_position_0_L_trait)
    ligne_position_0_L_trait=canevas0_L_trait.create_line(event.x,0,event.x,200, fill="green")
    canevas1_L_trait.delete(ligne_position_1_L_trait)
    ligne_position_1_L_trait=canevas1_L_trait.create_line(event.x,0,event.x,200, fill="green")
    if flag_premier_lamda_L_trait == False :
        canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
        canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
    l= event.x*delta_limites_L_trait/1000+limites_affichage_spectre_L_trait[0]
    lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
    flag_premier_lamda_L_trait=False
    
def affiche_spectre_L_trait():
    global limites_affichage_spectre_L_trait
    global delta_limites_L_trait
    global minimum_spectre_L_trait
    global maximum_spectre_L_trait
    limites_affichage_spectre_L_trait[0]=variable_zoom_inf_L_trait.get()
    limites_affichage_spectre_L_trait[1]=variable_zoom_sup_L_trait.get()
    delta_limites_L_trait=limites_affichage_spectre_L_trait[1]-limites_affichage_spectre_L_trait[0]
    canevas0_L_trait.delete("all")
    spectre=numpy.zeros((0,2))
    for ligne in spectre_entier_L_trait :
        if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum_spectre_L_trait = minimum = spectre[:,1].min()
    maximum_spectre_L_trait = maximum = spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    #spectre[:,0] = (spectre[:,0] - spectre[0,0])*1000/(spectre[len(spectre),0]-spectre[0,0])
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait
    for i in range(len(spectre) - 1) :
        canevas0_L_trait.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])
    affiche_lignes_spectre_L_trait()
    
def affiche_lignes_spectre_L_trait():
    global ligne0_1
    global ligne0_2
    x_ligne0_1=((variable_1_L_trait.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    x_ligne0_2=((variable_2_L_trait.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    ligne0_1=canevas0_L_trait.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    ligne0_2=canevas0_L_trait.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
        
def deplace_lignes_L_trait():
    deplace_ligne0_1_L_trait()
    deplace_ligne0_2_L_trait()

def deplace_ligne0_1_L_trait():
    global ligne0_1
    canevas0_L_trait.delete(ligne0_1)
    x_ligne0_1=((variable_1_L_trait.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    ligne0_1=canevas0_L_trait.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    if variable_1_L_trait.get() >= variable_2_L_trait.get():
        variable_2_L_trait.set(variable_1_L_trait.get())
        deplace_ligne0_2_L_trait()
        
def deplace_ligne0_2_L_trait():
    global ligne0_2
    canevas0_L_trait.delete(ligne0_2)
    x_ligne0_2=((variable_2_L_trait.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    ligne0_2=canevas0_L_trait.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if variable_2_L_trait.get() <= variable_1_L_trait.get() :
        variable_1_L_trait.set(variable_2_L_trait.get())
        deplace_ligne0_1_L_trait()

def deplace_ligne0_1_return_L_trait(event) :
    deplace_ligne0_1_L_trait()
    
def deplace_ligne0_2_return_L_trait(event) :
    deplace_ligne0_2_L_trait()
    
def change_options_filtre_L_trait(event) :
    filtre = type_filtre_L_trait.get()
    if filtre == "Aucun" :
        entree4_L_trait.configure(state="disable")
        entree5_L_trait.configure(state="disable")
        entree5_2_L_trait.configure(state="disable")
    if filtre == "Savitzky-Golay" :
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="normal")
        entree5_2_L_trait.configure(state="normal")
    if filtre == "Median" :
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="disable")
        entree5_2_L_trait.configure(state="disable")
    if filtre == "Passe-bas" :
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="disable")
        entree5_2_L_trait.configure(state="disable")
        
def change_options_fond_L_trait(event) :
    fond = type_fond_L_trait.get()
    if fond == "Aucun" :
        entree7_L_trait.configure(state="disable")
        entree8_L_trait.configure(state="disable")
        entree8bis_L_trait.configure(state="disable")
    if fond == "Rolling ball" :
        text7_L_trait.configure(text="Taille :")
        entree7_L_trait.configure(state="normal")
        text8_L_trait.configure(text="Lissage :")
        entree8_L_trait.configure(state="normal")
        entree8bis_L_trait.grid_forget()
        entree8_L_trait.grid(row=5, column=6)
    if fond == "SNIP" :
        text7_L_trait.configure(text="Itérations :")
        entree7_L_trait.configure(state="normal")
        text8_L_trait.configure(text="LLS :")
        entree8bis_L_trait.configure(state="normal")
        entree8_L_trait.grid_forget()
        entree8bis_L_trait.grid(row=5, column=6)

def affiche_fond_L_trait():
#    global fond_continu_L_trait
#    global dessin_fond_continu_L_trait
#    global flag_premier_fond_L_trait
#    if flag_premier_fond_L_trait == False :
#        canevas0_L_trait.delete(dessin_fond_continu_L_trait)
    spectre=numpy.zeros((0,2))
    for ligne in fond_continu_L_trait :
        if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum=minimum_spectre_L_trait
    maximum=maximum_spectre_L_trait
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait
    for i in range(len(spectre) - 1) :
        canevas0_L_trait.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1], fill="blue")
#        dessin_fond_continu_L_trait = canevas0_L_trait.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1], fill="blue")
    #flag_premier_fond_L_trait = False
    
###############################################################################
# fonctions graphiques du caneva du spectre corrigé (frame2_L_trait)
###############################################################################  
def lit_affiche_spectre_numero_L_trait():
    global spectre_entier_L_trait
    global nom_fichier_seul_L_trait
    numero=numero_spectre_L_trait.get()-1
    nom_fichier_seul_L_trait=liste_fichiers_L_trait[numero]
    os.chdir(rep_travail_L_trait)
    spectre_entier_L_trait=LIBStick_outils.lit_spectre(nom_fichier_seul_L_trait, type_fichier_L_trait)
    affiche_spectre_L_trait()
    visualisation_L_trait()
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_trait)
    
def lit_affiche_spectre_numero_event_L_trait(event):
    lit_affiche_spectre_numero_L_trait()
    
def affiche_spectre_corrige_L_trait():
    #global limites_affichage_spectre_L_trait
    #global delta_limites_L_trait
    #global spectre_corrige_L_trait
    #limites_affichage_spectre_L_trait[0]=variable_zoom_inf_L_trait.get()
    #limites_affichage_spectre_L_trait[1]=variable_zoom_sup_L_trait.get()
    #delta_limites_L_trait=limites_affichage_spectre_L_trait[1]-limites_affichage_spectre_L_trait[0]
    canevas1_L_trait.delete("all")
    spectre=numpy.zeros((0,2))
    for ligne in spectre_corrige_L_trait :
        if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum=spectre[:,1].min()
    maximum=spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/((maximum - minimum)+0.000000001))
    #spectre[:,0] = (spectre[:,0] - spectre[0,0])*1000/(spectre[len(spectre),0]-spectre[0,0])
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait
    for i in range(len(spectre) - 1) :
        canevas1_L_trait.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])

###############################################################################
# fonctions graphiques de zoom des deux canevas (frame1_L_trait et frame2_L_trait)
###############################################################################
def change_zoom_inf_L_trait() :
    if variable_zoom_inf_L_trait.get() >= variable_zoom_sup_L_trait.get() :
        variable_zoom_sup_L_trait.set(variable_zoom_inf_L_trait.get())
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()
    
def change_zoom_sup_L_trait():
    if variable_zoom_sup_L_trait.get() <= variable_zoom_inf_L_trait.get() :
        variable_zoom_inf_L_trait.set(variable_zoom_sup_L_trait.get())
#    limites_affichage_spectre_L_trait[0]=variable_zoom_inf_L_trait.get()
#    limites_affichage_spectre_L_trait[1]=variable_zoom_sup_L_trait.get()
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()

def change_zoom_inf_return_L_trait(event):
    change_zoom_inf_L_trait()
    
def change_zoom_sup_return_L_trait(event):
    change_zoom_sup_L_trait()

def zoom_clic_L_trait(event):
    global coord_zoom_L_trait
    coord_zoom_L_trait[0]=event.x
    coord_zoom_L_trait[1]=event.y
    
def zoom_drag_and_drop_L_trait(event):
    global ligne_position_0_L_trait
    global ligne_position_1_L_trait
    global coord_zoom_L_trait
    global limites_affichage_spectre_L_trait
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    canevas0_L_trait.delete(ligne_position_0_L_trait)
    ligne_position_0_L_trait=canevas0_L_trait.create_line(event.x,0,event.x,200, fill="green")
    canevas1_L_trait.delete(ligne_position_1_L_trait)
    ligne_position_1_L_trait=canevas1_L_trait.create_line(event.x,0,event.x,200, fill="green")
    coord_zoom_L_trait[2]=event.x
    coord_zoom_L_trait[3]=event.y
    if coord_zoom_L_trait[2] > coord_zoom_L_trait[0] :
        debut= coord_zoom_L_trait[0]*delta_limites_L_trait/1000+limites_affichage_spectre_L_trait[0]
        fin = coord_zoom_L_trait[2]*delta_limites_L_trait/1000+limites_affichage_spectre_L_trait[0]
        variable_zoom_inf_L_trait.set(format(debut, "4.1f"))
        variable_zoom_sup_L_trait.set(format(fin, "4.1f"))
        #affiche la longueur d'onde :
        if flag_premier_lamda_L_trait == False :
            canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
            canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
        l= event.x*delta_limites_L_trait/1000+limites_affichage_spectre_L_trait[0]
        lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
        flag_premier_lamda_L_trait=False
    if coord_zoom_L_trait[2] < coord_zoom_L_trait[0] :
        variable_zoom_inf_L_trait.set(limites_spectre_L_trait[0])
        variable_zoom_sup_L_trait.set(limites_spectre_L_trait[1])
        limites_affichage_spectre_L_trait[0]=variable_zoom_inf_L_trait.get()
        limites_affichage_spectre_L_trait[1]=variable_zoom_sup_L_trait.get()

def zoom_clic_release_L_trait(event):
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()





###############################################################################
###############################################################################
# Fonctions LIBStick_IHM_extraction : onglet 2
###############################################################################
###############################################################################
def __________L_ext__________():pass
###############################################################################
# 0- initialisations
###############################################################################
limites_spectre_L_ext=numpy.array([198.0,1013.0])
limites_affichage_spectre_L_ext=numpy.array([198.0,1013.0])
coord_zoom_L_ext=numpy.array([198,0,1013,0])
delta_limites_L_ext=limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
flag_premier_lamda_L_ext=True
l_L_ext=0.0
spectre_entier_L_ext=numpy.zeros((0,2))
bornes_moyenne_spectres_L_ext=[]
liste_bool_existe_L_ext = False
#tableau_bornes_init_L_ext=numpy.array([[528.0, 543.0],[525.0, 561.5]])
#tableau_bornes_L_ext=numpy.array([[528.0, 543.0],[525.0, 561.5]])
#rep_travail_L_ext="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1"

def charge_param_L_ext() :
    dictionnaire_ini_L_ext=lit_section_fichier_ini("LIBStick_extraction")
    borne_zone1_inf_L_ext = float(dictionnaire_ini_L_ext["borne_zone1_inf_L_ext"])
    borne_zone1_sup_L_ext = float(dictionnaire_ini_L_ext["borne_zone1_sup_L_ext"])
    borne_zone2_inf_L_ext = float(dictionnaire_ini_L_ext["borne_zone2_inf_L_ext"])
    borne_zone2_sup_L_ext = float(dictionnaire_ini_L_ext["borne_zone2_sup_L_ext"])
    tableau_bornes_init_L_ext=numpy.array([[borne_zone1_inf_L_ext,borne_zone1_sup_L_ext],[borne_zone2_inf_L_ext, borne_zone2_sup_L_ext]])
    tableau_bornes_L_ext=numpy.array([[borne_zone1_inf_L_ext,borne_zone1_sup_L_ext],[borne_zone2_inf_L_ext, borne_zone2_sup_L_ext]])
    rep_travail_L_ext = dictionnaire_ini_L_ext["rep_travail_L_ext"]
    flag_zone2_init_L_ext = dictionnaire_ini_L_ext["flag_zone2_L_ext"]
    flag_2D_init_L_ext = dictionnaire_ini_L_ext["flag_2D_L_ext"]
    flag_3D_init_L_ext = dictionnaire_ini_L_ext["flag_3D_L_ext"]
    flag_image_brute_init_L_ext = dictionnaire_ini_L_ext["flag_image_brute_L_ext"]
    return tableau_bornes_init_L_ext,tableau_bornes_L_ext,rep_travail_L_ext,flag_zone2_init_L_ext,flag_2D_init_L_ext,flag_3D_init_L_ext,flag_image_brute_init_L_ext

tableau_bornes_init_L_ext,tableau_bornes_L_ext,rep_travail_L_ext,flag_zone2_init_L_ext,flag_2D_init_L_ext,flag_3D_init_L_ext,flag_image_brute_init_L_ext=charge_param_L_ext()

x1_L_ext=250.0
y_L_ext=100.0
x2_L_ext=250.0

def affiche_nom_spectre_onglet2() :
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ext)

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_ext() :
    #global tableau_bornes_L_ext
    tableau_bornes_L_ext[0,0]=variable_1_L_ext.get()
    tableau_bornes_L_ext[0,1]=variable_2_L_ext.get()
    entree5_L_ext.configure(from_=tableau_bornes_L_ext[0,0], to=tableau_bornes_L_ext[0,1])  
    if flag_zone2_L_ext.get() :
        tableau_bornes_L_ext[1,0]=variable_3_L_ext.get()
        tableau_bornes_L_ext[1,1]=variable_4_L_ext.get()
        entree7_L_ext.configure(from_=tableau_bornes_L_ext[1,0], to=tableau_bornes_L_ext[1,1]) 
    return tableau_bornes_L_ext

def reset_tableau_L_ext() :
    #global tableau_bornes_L_ext
    tableau_bornes_L_ext=tableau_bornes_init_L_ext.copy()
    variable_1_L_ext.set(tableau_bornes_L_ext[0,0])
    variable_2_L_ext.set(tableau_bornes_L_ext[0,1])
    variable_3_L_ext.set(tableau_bornes_L_ext[1,0])
    variable_4_L_ext.set(tableau_bornes_L_ext[1,1])
    deplace_lignes_L_ext()

def choix_fichier_L_ext():
    global nom_fichier_seul_L_ext
    global rep_travail_L_ext
    global nombre_fichiers_L_ext
    global liste_fichiers_L_ext
    global liste_bool_L_ext
    global nombre_fichiers_avant_L_ext
    global liste_bool_existe_L_ext
#    nom_fichier_L_ext = tkinter.filedialog.askopenfilename(initialdir=rep_travail_L_ext,
#                                                                 title='Choisissez un fichier spectre',
#                                                                 filetypes=(("fichiers LIBStick","*.tsv"),
#                                                                            ("fichiers IVEA","*.asc"),
#                                                                            ("fichiers SciAps","*.csv"),
#                                                                            ("fichiers LIBStick moyen","*.mean")))
    nom_fichier_L_ext = tkinter.filedialog.askopenfilename(initialdir=rep_travail_L_ext,
                                                                 title='Choisissez un fichier spectre',
                                                                 filetypes=(("fichiers IVEA","*.asc"),
                                                                            ("fichiers LIBStick","*.tsv"),
                                                                            ("fichiers SciAps","*.csv"),
                                                                            ("fichiers LIBStick moyen","*.mean")))
    nom_fichier_seul_L_ext=os.path.basename(nom_fichier_L_ext)
    type_fichier_L_ext.set(pathlib.Path(nom_fichier_seul_L_ext).suffix)
    rep_travail_L_ext = os.path.dirname(nom_fichier_L_ext)
    liste_fichiers_L_ext=LIBStick_outils.creation_liste_fichiers(rep_travail_L_ext, type_fichier_L_ext.get())
    nombre_fichiers_L_ext=len(liste_fichiers_L_ext)    
    variable_10_L_ext.set(nombre_fichiers_L_ext)
    variable_10_avant_L_ext.set(nombre_fichiers_L_ext)
    if liste_bool_existe_L_ext == False or nombre_fichiers_L_ext != nombre_fichiers_avant_L_ext :
        liste_bool_L_ext=[True]*nombre_fichiers_L_ext
        liste_bool_existe_L_ext = True
        nombre_fichiers_avant_L_ext = nombre_fichiers_L_ext
    lit_affiche_spectre_L_ext(nom_fichier_seul_L_ext)
    bouton_execute_L_ext.configure(state="normal")
    bouton_extraction_L_ext.configure(state="disable")
    entree6_L_ext.configure(to=nombre_fichiers_L_ext)
    entree8_L_ext.configure(to=nombre_fichiers_L_ext)
    entree9_L_ext.configure(to=nombre_fichiers_L_ext)
    entree10_L_ext.configure(to=nombre_fichiers_L_ext)
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ext)
    
def execute_scripts_L_ext():
    global nom_echantillon_L_ext
#    global tableau_brut_L_ext, tableau_norm_L_ext
#    global dataframe_norm_L_ext 
    tableau_bornes_L_ext=creation_tab_bornes_L_ext()
    if flag_zone2_L_ext.get() == 0 :
        canevas2_L_ext.delete("all")
    nom_echantillon_L_ext = LIBStick_extraction_spectres.main(rep_travail_L_ext, tableau_bornes_L_ext,
                                                              type_fichier_L_ext.get(), liste_fichiers_L_ext,
                                                              flag_zone2_L_ext.get(), flag_2D_L_ext.get(), flag_3D_L_ext.get())
    affiche_image_L_ext()
    bouton_extraction_L_ext.configure(state="normal")

def creation_spectre_moyen_L_ext():
    bornes_moyenne_spectres_L_ext.insert(0,variable_9_L_ext.get())
    bornes_moyenne_spectres_L_ext.insert(1,variable_10_L_ext.get())
    tableau_bornes_copy_L_ext=tableau_bornes_L_ext.copy()
    i=3
    if flag_zone2_L_ext.get() == 0:
        tableau_bornes_copy_L_ext=numpy.delete(tableau_bornes_copy_L_ext, (1), axis=0)
        canevas4_L_ext.delete("all")
    for bornes in tableau_bornes_copy_L_ext :
        repertoire=rep_travail_L_ext+"/"+str(bornes[0])+"_"+ str(bornes[1])+"/"
        spectre=LIBStick_extraction_spectres.creation_spectre_moyen_main(repertoire,nom_echantillon_L_ext,bornes,
                                                                         bornes_moyenne_spectres_L_ext, liste_bool_L_ext,
                                                                         flag_spectres_normalises_moyenne_L_ext.get())
        if i==3 :
            canevas3_L_ext.delete("all")
            delta_bornes=bornes[1]-bornes[0]
            spectre[:,0] = (spectre[:,0] - spectre[0,0])*500/delta_bornes
            minimum=spectre[:,1].min()
            maximum=spectre[:,1].max()
            spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
            for j in range(spectre.shape[0] - 1) :
#                dx=500/spectre.shape[0]
#                x=j*dx
#                canevas3_L_ext.create_line(x,spectre[j,1],x+dx,spectre[j+1,1], width=1, fill="red", smooth=1)
                canevas3_L_ext.create_line(spectre[j,0],spectre[j,1],spectre[j+1,0],spectre[j+1,1], width=1, fill="red", smooth=1)
        if i==4 :
            canevas4_L_ext.delete("all")
            delta_bornes=bornes[1]-bornes[0]
            spectre[:,0] = (spectre[:,0] - spectre[0,0])*500/delta_bornes
            minimum=spectre[:,1].min()
            maximum=spectre[:,1].max()
            spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
            for j in range(spectre.shape[0] - 1) :
#                dx=500/spectre.shape[0]
#                x=j*dx
#                canevas4_L_ext.create_line(x,spectre[j,1],x+dx,spectre[j+1,1], width=1, fill="blue", smooth=1)
                canevas4_L_ext.create_line(spectre[j,0],spectre[j,1],spectre[j+1,0],spectre[j+1,1], fill="blue", smooth=1)
        i=i+1
        
###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1_L_ext)
###############################################################################
def lit_affiche_spectre_L_ext(nom_fichier):
    global spectre_entier_L_ext
    global limites_spectre_L_ext
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext=LIBStick_outils.lit_spectre(nom_fichier, type_fichier_L_ext.get())
    limites_spectre_L_ext=lit_limites_abscisses_L_ext(spectre_entier_L_ext)
    affiche_spectre_L_ext()
    
def lit_limites_abscisses_L_ext(spectre):
    tableau_abscisses=spectre[:,0]
    limites_spectre=numpy.zeros((2))
    limites_spectre[0]=tableau_abscisses[0]             # lit le valeurs min et max du spectre
    limites_spectre[1]=tableau_abscisses[-1]
    variable_zoom_inf_L_ext.set(limites_spectre[0])    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_sup_L_ext.set(limites_spectre[1])
    entree_zoom_inf_L_ext.configure(from_=limites_spectre[0], to=limites_spectre[1])   #fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_sup_L_ext.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree1_L_ext.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree2_L_ext.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree3_L_ext.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree4_L_ext.configure(from_=limites_spectre[0], to=limites_spectre[1])
    return limites_spectre

def change_flag_2D_L_ext():
    pass
    
def change_flag_3D_L_ext():
    pass

def change_flag_zone2_L_ext():
    if flag_zone2_L_ext.get() == 0 :
        efface_lignes_3_4_L_ext()
        entree3_L_ext.configure(state="disable")
        entree4_L_ext.configure(state="disable")
        entree7_L_ext.configure(state="disable")
        entree8_L_ext.configure(state="disable")
        canevas2_L_ext.configure(state="disable")
        canevas4_L_ext.configure(state="disable")
    if flag_zone2_L_ext.get() == 1 :
        affiche_lignes_3_4_L_ext()
        entree3_L_ext.configure(state="normal")
        entree4_L_ext.configure(state="normal")
        entree7_L_ext.configure(state="normal")
        entree8_L_ext.configure(state="normal")
        canevas2_L_ext.configure(state="normal")
        canevas4_L_ext.configure(state="normal")

def affiche_lambda_L_ext(event):
    global lambda_texte_spectre_L_ext
    global flag_premier_lamda_L_ext
    if flag_premier_lamda_L_ext == False :
        canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
    l= event.x*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
    lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
    flag_premier_lamda_L_ext=False
    
def affiche_position_souris_L_ext(event):
    global ligne_position_L_ext
    canevas0_L_ext.delete(ligne_position_L_ext)
    ligne_position_L_ext=canevas0_L_ext.create_line(event.x,0,event.x,200, fill="green")
    
def affiche_position_souris_motion_L_ext(event):
    global ligne_position_L_ext
    global lambda_texte_spectre_L_ext
    global flag_premier_lamda_L_ext
    canevas0_L_ext.delete(ligne_position_L_ext)
    ligne_position_L_ext=canevas0_L_ext.create_line(event.x,0,event.x,200, fill="green")
    if flag_premier_lamda_L_ext == False :
        canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
    l= event.x*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
    lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
    flag_premier_lamda_L_ext=False
    
def affiche_spectre_L_ext():
    global limites_affichage_spectre_L_ext
    global delta_limites_L_ext
    global spectre_entier_L_ext
    limites_affichage_spectre_L_ext[0]=variable_zoom_inf_L_ext.get()
    limites_affichage_spectre_L_ext[1]=variable_zoom_sup_L_ext.get()
    delta_limites_L_ext=limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
    canevas0_L_ext.delete("all")
    spectre=numpy.zeros((0,2))   
    for ligne in spectre_entier_L_ext :
        if (ligne[0] >= limites_affichage_spectre_L_ext[0] and ligne[0] <= limites_affichage_spectre_L_ext[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum=spectre[:,1].min()
    maximum=spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext
    for i in range(len(spectre) - 1) :
        canevas0_L_ext.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])
    affiche_lignes_spectre_L_ext()
    
def affiche_lignes_spectre_L_ext():
    global ligne0_1_L_ext
    global ligne0_2_L_ext
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    x_ligne0_1=((variable_1_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    x_ligne0_2=((variable_2_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_1_L_ext=canevas0_L_ext.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    ligne0_2_L_ext=canevas0_L_ext.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if flag_zone2_L_ext.get() :
        x_ligne0_3=((variable_3_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        x_ligne0_4=((variable_4_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_3_L_ext=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
        ligne0_4_L_ext=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        
def deplace_lignes_L_ext():
    deplace_ligne0_1_L_ext()
    deplace_ligne0_2_L_ext()
    if flag_zone2_L_ext.get() :
        deplace_ligne0_3_L_ext()
        deplace_ligne0_4_L_ext()

def deplace_ligne0_1_L_ext():
    global ligne0_1_L_ext
    canevas0_L_ext.delete(ligne0_1_L_ext)
    x_ligne0_1=((variable_1_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_1_L_ext=canevas0_L_ext.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    if variable_1_L_ext.get() >= variable_2_L_ext.get():
        variable_2_L_ext.set(variable_1_L_ext.get())
        deplace_ligne0_2_L_ext()
        
def deplace_ligne0_2_L_ext():
    global ligne0_2_L_ext
    canevas0_L_ext.delete(ligne0_2_L_ext)
    x_ligne0_2=((variable_2_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_2_L_ext=canevas0_L_ext.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if variable_2_L_ext.get() <= variable_1_L_ext.get() :
        variable_1_L_ext.set(variable_2_L_ext.get())
        deplace_ligne0_1_L_ext()

def deplace_ligne0_3_L_ext():
    global ligne0_3_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    if flag_zone2_L_ext.get() :
        x_ligne0_3=((variable_3_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_3_L_ext=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
        if variable_3_L_ext.get() >= variable_4_L_ext.get():
            variable_4_L_ext.set(variable_3_L_ext.get())
            deplace_ligne0_4_L_ext()
        
def deplace_ligne0_4_L_ext():
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_4_L_ext)
    if flag_zone2_L_ext.get() :
        x_ligne0_4=((variable_4_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_4_L_ext=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        if variable_4_L_ext.get() <= variable_3_L_ext.get() :
            variable_3_L_ext.set(variable_4_L_ext.get())
            deplace_ligne0_3_L_ext()

def efface_lignes_3_4_L_ext():
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    canevas0_L_ext.delete(ligne0_4_L_ext)

def affiche_lignes_3_4_L_ext():
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    canevas0_L_ext.delete(ligne0_4_L_ext)
    x_ligne0_3=((variable_3_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    x_ligne0_4=((variable_4_L_ext.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_3_L_ext=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
    ligne0_4_L_ext=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        
def deplace_ligne0_1_return_L_ext(event):
    deplace_ligne0_1_L_ext()
    
def deplace_ligne0_2_return_L_ext(event):
    deplace_ligne0_2_L_ext()
    
def deplace_ligne0_3_return_L_ext(event):
    deplace_ligne0_3_L_ext()
    
def deplace_ligne0_4_return_L_ext(event):
    deplace_ligne0_4_L_ext()
    
###############################################################################
# fonctions graphiques de zoom du caneva 1 (frame1_L_ext)
###############################################################################
def change_zoom_inf_L_ext() :
#    global limites_affichage_spectre_L_ext
    if variable_zoom_inf_L_ext.get() >= variable_zoom_sup_L_ext.get() :
        variable_zoom_sup_L_ext.set(variable_zoom_inf_L_ext.get())
#    limites_affichage_spectre_L_ext[0]=variable_zoom_inf_L_ext.get()
#    limites_affichage_spectre_L_ext[1]=variable_zoom_sup_L_ext.get()
    affiche_spectre_L_ext()
    
def change_zoom_sup_L_ext():
#    global limites_affichage_spectre_L_ext
    if variable_zoom_sup_L_ext.get() <= variable_zoom_inf_L_ext.get() :
        variable_zoom_inf_L_ext.set(variable_zoom_sup_L_ext.get())
#    limites_affichage_spectre_L_ext[0]=variable_zoom_inf_L_ext.get()
#    limites_affichage_spectre_L_ext[1]=variable_zoom_sup_L_ext.get()
    affiche_spectre_L_ext()

def change_zoom_inf_return_L_ext(event):
    change_zoom_inf_L_ext()
    
def change_zoom_sup_return_L_ext(event):
    change_zoom_sup_L_ext()

def zoom_clic_L_ext(event):
    global coord_zoom_L_ext
    coord_zoom_L_ext[0]=event.x
    coord_zoom_L_ext[1]=event.y
    
def zoom_drag_and_drop_L_ext(event):
    global ligne_position_L_ext
    global coord_zoom_L_ext
    global limites_affichage_spectre_L_ext
    global lambda_texte_spectre_L_ext
    global flag_premier_lamda_L_ext
    canevas0_L_ext.delete(ligne_position_L_ext)
    ligne_position_L_ext=canevas0_L_ext.create_line(event.x,0,event.x,200, fill="green")
    coord_zoom_L_ext[2]=event.x
    coord_zoom_L_ext[3]=event.y
    if coord_zoom_L_ext[2] > coord_zoom_L_ext[0] :
        debut= coord_zoom_L_ext[0]*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
        fin = coord_zoom_L_ext[2]*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
        variable_zoom_inf_L_ext.set(format(debut, "4.1f"))
        variable_zoom_sup_L_ext.set(format(fin, "4.1f"))
        #affiche la longueur d'onde :
        if flag_premier_lamda_L_ext == False :
            canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
        l= event.x*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
        lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
        flag_premier_lamda_L_ext=False
    if coord_zoom_L_ext[2] < coord_zoom_L_ext[0] :
        variable_zoom_inf_L_ext.set(limites_spectre_L_ext[0])
        variable_zoom_sup_L_ext.set(limites_spectre_L_ext[1])
        limites_affichage_spectre_L_ext[0]=variable_zoom_inf_L_ext.get()
        limites_affichage_spectre_L_ext[1]=variable_zoom_sup_L_ext.get()

def zoom_clic_release_L_ext(event):
    affiche_spectre_L_ext()

###############################################################################
#  fonctions graphiques des canevas de l'image 1 et 2 (frame2_L_ext)
###############################################################################
def affiche_image_L_ext():
    global photo1, photo2
    if flag_image_brute_L_ext.get() == False :
        fichier1=rep_travail_L_ext+"/"+str(tableau_bornes_L_ext[0,0])+"_"+str(tableau_bornes_L_ext[0,1])+"/figure.png"
    if flag_image_brute_L_ext.get() == True :
        fichier1=rep_travail_L_ext+"/"+str(tableau_bornes_L_ext[0,0])+"_"+str(tableau_bornes_L_ext[0,1])+"/figure_brute.png"
    image1_zoom=PIL.Image.open(fichier1)    
    image1_zoom=image1_zoom.resize((500, 200))
    photo1=PIL.ImageTk.PhotoImage(image1_zoom)
    canevas1_L_ext.create_image(250 ,100 ,image=photo1)
    if flag_zone2_L_ext.get() :
        if flag_image_brute_L_ext.get() == False :
            fichier2=rep_travail_L_ext+"/"+str(tableau_bornes_L_ext[1,0])+"_"+str(tableau_bornes_L_ext[1,1])+"/figure.png"
        if flag_image_brute_L_ext.get() == True :
            fichier2=rep_travail_L_ext+"/"+str(tableau_bornes_L_ext[1,0])+"_"+str(tableau_bornes_L_ext[1,1])+"/figure_brute.png"
        image2_zoom=PIL.Image.open(fichier2)
        image2_zoom=image2_zoom.resize((500,200))
        photo2=PIL.ImageTk.PhotoImage(image2_zoom)
        canevas2_L_ext.create_image(250,100  ,image=photo2)
        
def change_flag_image_brute_L_ext():
    affiche_image_L_ext()
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()

def change_bool_spectre_L_ext() :
    global liste_bool_L_ext
    liste_bool_L_ext[variable_6_L_ext.get()-1]=flag_spectre_inclus_moyenne_L_ext.get()
    print("==================================")
    print (liste_bool_L_ext) 

###############################################################################
# 3- fonctions graphiques du caneva de l'image 1 (frame2_L_ext)
###############################################################################
def coordonnees1_L_ext (event) :
    global x1_L_ext,y_L_ext
    x1_L_ext=event.x
    y_L_ext=event.y
    coord1_to_vars_5_6_L_ext(x1_L_ext,y_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()
   
def deplace_cible1_L_ext():
    global x1_L_ext,y_L_ext
    global ligne1_vert_L_ext, ligne1_hori_L_ext
    canevas1_L_ext.delete(ligne1_vert_L_ext)
    canevas1_L_ext.delete(ligne1_hori_L_ext)
    ligne1_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
    ligne1_hori_L_ext=canevas1_L_ext.create_line(0,y_L_ext,500,y_L_ext, fill="white")   
    
def coord1_to_vars_5_6_L_ext(x,y):
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    variable_5_L_ext.set(format((variable_1_L_ext.get() + (x * (variable_2_L_ext.get()-variable_1_L_ext.get()) / 500)), "4.1f")) # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    variable_6_L_ext.set(math.ceil(y * nombre_fichiers_L_ext / 200))
    nom_fichier_seul_L_ext=liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ext)

def vars_5_6_to_coord1_L_ext():
    global x1_L_ext,y_L_ext
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    x1_L_ext=round( ((variable_5_L_ext.get()-variable_1_L_ext.get())*500) / (variable_2_L_ext.get()-variable_1_L_ext.get())) # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    y_L_ext= round(200*(variable_6_L_ext.get()-0.5)/nombre_fichiers_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()
    nom_fichier_seul_L_ext=liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ext)
    
def vars_5_6_to_coord1_return_L_ext(event):
    vars_5_6_to_coord1_L_ext()

###############################################################################
# 4- fonctions graphiques du caneva de l'image 2 (frame2_L_ext)
###############################################################################      
def coordonnees2_L_ext (event) :
    global x2_L_ext,y_L_ext
    x2_L_ext=event.x
    y_L_ext=event.y
    coord2_to_vars_7_8_L_ext(x2_L_ext,y_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()
    
def deplace_cible2_L_ext():
    global x2_L_ext,y_L_ext
    global ligne2_vert_L_ext, ligne2_hori_L_ext
    canevas2_L_ext.delete(ligne2_vert_L_ext)
    canevas2_L_ext.delete(ligne2_hori_L_ext)
    ligne2_vert_L_ext=canevas2_L_ext.create_line(x2_L_ext,0,x2_L_ext,200, fill="white")
    ligne2_hori_L_ext=canevas2_L_ext.create_line(0,y_L_ext,500,y_L_ext, fill="white")
    
def coord2_to_vars_7_8_L_ext(x,y):
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    variable_7_L_ext.set(format((variable_3_L_ext.get() + (x * (variable_4_L_ext.get()-variable_3_L_ext.get()) / 500)), "4.1f")) # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    variable_6_L_ext.set(math.ceil(y * nombre_fichiers_L_ext / 200))
    nom_fichier_seul_L_ext=liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ext)
    
def vars_7_8_to_coord2_L_ext():
    global x2_L_ext,y_L_ext
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    x2_L_ext= round((variable_7_L_ext.get()-variable_3_L_ext.get())*500/(variable_4_L_ext.get()-variable_3_L_ext.get())) # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    y_L_ext= round(200*(variable_6_L_ext.get()-0.5)/nombre_fichiers_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()
    nom_fichier_seul_L_ext=liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ext)
    
def vars_7_8_to_coord2_return_L_ext(event):
    vars_7_8_to_coord2_L_ext()

###############################################################################
# 5- fonctions graphiques du choix des spectres à moyenner (frame3_L_ext)
###############################################################################
def retro_action_entree10_L_ext():
    global liste_bool_L_ext
    if variable_9_L_ext.get() > variable_10_L_ext.get():
        variable_10_L_ext.set(variable_9_L_ext.get())
        retro_action_entree9_L_ext()
    if variable_9_L_ext.get() > 1 :
        if variable_9_L_ext.get() > variable_9_avant_L_ext.get() :              # si on augmente la valeur de la borne inf
            for i in range(variable_9_avant_L_ext.get()-1, variable_9_L_ext.get()-1) :
                liste_bool_L_ext[i] = False
                if liste_bool_L_ext[i+1] == False :
                    liste_bool_L_ext[i+1] = True
        if variable_9_L_ext.get() < variable_9_avant_L_ext.get() :              # si on diminue la valeur de la borne inf
            for i in range(variable_9_L_ext.get()-1, variable_9_avant_L_ext.get()-1) :
                liste_bool_L_ext[i]=True
    if variable_9_L_ext.get() == 1 :
        for i in range(variable_9_L_ext.get()-1, variable_9_avant_L_ext.get()-1) :
            liste_bool_L_ext[i]=True
    variable_9_avant_L_ext.set(variable_9_L_ext.get())
#    print("==================================")
#    print (liste_bool_L_ext)    

def retro_action_entree9_L_ext():
    global liste_bool_L_ext
    if variable_10_L_ext.get() < variable_9_L_ext.get():
        variable_9_L_ext.set(variable_10_L_ext.get())
        retro_action_entree10_L_ext()
    if variable_10_L_ext.get() < nombre_fichiers_L_ext :
        if variable_10_L_ext.get() < variable_10_avant_L_ext.get() :            # si on diminue la valeur de la borne sup
            for i in range(variable_10_L_ext.get(), variable_10_avant_L_ext.get()) :
                liste_bool_L_ext[i] = False
                if liste_bool_L_ext[i-1] == False :
                    liste_bool_L_ext[i-1] = True 
        if variable_10_L_ext.get() > variable_10_avant_L_ext.get() :            # si on augmente la valeur de la borne sup
            for i in range(variable_10_avant_L_ext.get(), variable_10_L_ext.get()) :
                liste_bool_L_ext[i]=True
    if variable_10_L_ext.get() == nombre_fichiers_L_ext :
        for i in range(variable_10_avant_L_ext.get(), variable_10_L_ext.get()) :
            liste_bool_L_ext[i]=True
    variable_10_avant_L_ext.set(variable_10_L_ext.get())
#    print("==================================")
#    print (liste_bool_L_ext)

def change_entree9_L_ext(event):
    retro_action_entree10_L_ext()
    
def change_entree10_L_ext(event):
    retro_action_entree9_L_ext()
    
    




###############################################################################
###############################################################################
# Fonctions LIBStick_IHM_compare : onglet 3
###############################################################################
###############################################################################
def __________L_comp__________():pass
###############################################################################
# 0- initialisations
###############################################################################
limites_spectre_L_comp=numpy.array([198.0,1013.0])              # limites min et max de l'affichage du spectre
limites_affichage_spectre_L_comp=numpy.array([198.0,1013.0])    # limites de l'affichage du spectre à l'écran
coord_zoom_L_comp=numpy.array([198,0,1013,0])
delta_limites_L_comp=limites_affichage_spectre_L_comp[1]-limites_affichage_spectre_L_comp[0]
flag_premier_lamda_L_comp=True
l_L_comp=0.0
spectre_entier_L_comp=numpy.zeros((0,2))
#tableau_bornes_init_L_comp=numpy.array([ [529.0, 542.0] , [534.7, 535.8] ])
#tableau_bornes_L_comp=numpy.array([ [529.0, 542.0] , [534.7, 535.8] ])
#rep_travail_L_comp="./"
#rep_travail_L_comp="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1"

def charge_param_L_comp() :
    dictionnaire_ini_L_comp=lit_section_fichier_ini("LIBStick_compare")
    borne_zone1_inf_L_comp = float(dictionnaire_ini_L_comp["borne_zone1_inf_L_comp"])
    borne_zone1_sup_L_comp = float(dictionnaire_ini_L_comp["borne_zone1_sup_L_comp"])
    borne_zone2_inf_L_comp = float(dictionnaire_ini_L_comp["borne_zone2_inf_L_comp"])
    borne_zone2_sup_L_comp = float(dictionnaire_ini_L_comp["borne_zone2_sup_L_comp"])
    tableau_bornes_init_L_comp=numpy.array([[borne_zone1_inf_L_comp,borne_zone1_sup_L_comp],[borne_zone2_inf_L_comp, borne_zone2_sup_L_comp]])
    tableau_bornes_L_comp=numpy.array([[borne_zone1_inf_L_comp,borne_zone1_sup_L_comp],[borne_zone2_inf_L_comp, borne_zone2_sup_L_comp]])
    rep_travail_L_comp = dictionnaire_ini_L_comp["rep_travail_L_comp"]
    flag_denominateur_init_L_comp = dictionnaire_ini_L_comp["flag_denominateur_L_comp"]
    flag_2D_init_L_comp = dictionnaire_ini_L_comp["flag_2D_L_comp"]
    flag_3D_init_L_comp = dictionnaire_ini_L_comp["flag_3D_L_comp"]
    flag_traitement_init_L_comp=dictionnaire_ini_L_comp["flag_traitement_L_comp"]
    flag_stat_init_L_comp=dictionnaire_ini_L_comp["flag_stat_L_comp"]
    return tableau_bornes_init_L_comp,tableau_bornes_L_comp,rep_travail_L_comp,flag_denominateur_init_L_comp,flag_2D_init_L_comp,flag_3D_init_L_comp,flag_traitement_init_L_comp,flag_stat_init_L_comp

tableau_bornes_init_L_comp,tableau_bornes_L_comp,rep_travail_L_comp,flag_denominateur_init_L_comp,flag_2D_init_L_comp,flag_3D_init_L_comp,flag_traitement_init_L_comp,flag_stat_init_L_comp= charge_param_L_comp()

x1_L_comp=250.0
y1_L_comp=100.0
#x2_L_comp=250.0
#y2_L_comp=100.0

def affiche_nom_spectre_onglet3() :
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)

###############################################################################
# fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_comp() :
    tableau_bornes_L_comp[0,0]=variable_1_L_comp.get()
    tableau_bornes_L_comp[0,1]=variable_2_L_comp.get()
    #entree5_L_comp.configure(from_=tableau_bornes_L_comp[0,0], to=tableau_bornes_L_comp[0,1])  
    if flag_denominateur_L_comp.get() :
        tableau_bornes_L_comp[1,0]=variable_3_L_comp.get()
        tableau_bornes_L_comp[1,1]=variable_4_L_comp.get()
    return tableau_bornes_L_comp
    
def reset_tableau_L_comp() :
    #global tableau_bornes_L_comp
    tableau_bornes_L_comp=tableau_bornes_init_L_comp.copy()
    variable_1_L_comp.set(tableau_bornes_L_comp[0,0])
    variable_2_L_comp.set(tableau_bornes_L_comp[0,1])
    variable_3_L_comp.set(tableau_bornes_L_comp[1,0])
    variable_4_L_comp.set(tableau_bornes_L_comp[1,1])
    deplace_lignes_L_comp()

def choix_fichier_L_comp():
    global nom_fichier_seul_L_comp
    global rep_travail_L_comp
    global nombre_fichiers_L_comp
    global liste_fichiers_L_comp
    nom_fichier_L_comp = tkinter.filedialog.askopenfilename(title='Choisissez un fichier spectre',
                                                            initialdir=rep_travail_L_comp,
                                                            filetypes=(("fichiers LIBStick moyen","*.mean"),
                                                                       ("fichiers LIBStick","*.tsv"),
                                                                       ("fichiers IVEA","*.asc"),
                                                                       ("fichiers SciAps","*.csv")), multiple=False)
    nom_fichier_seul_L_comp=os.path.basename(nom_fichier_L_comp)
    type_fichier_L_comp.set(pathlib.Path(nom_fichier_seul_L_comp).suffix)
    rep_travail_L_comp = os.path.dirname(nom_fichier_L_comp)
    liste_fichiers_L_comp=LIBStick_outils.creation_liste_fichiers(rep_travail_L_comp, type_fichier_L_comp.get())
    nombre_fichiers_L_comp=len(liste_fichiers_L_comp)    
    lit_affiche_spectre_L_comp()
    bouton_execute_L_comp.configure(state="normal")
    entree6_L_comp.configure(from_=1, to=nombre_fichiers_L_comp)
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)

def lit_affiche_spectre_L_comp():
    global spectre_entier_L_comp 
    global limites_spectre_L_comp
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp, type_fichier_L_comp.get())    
    limites_spectre_L_comp=lit_limites_abscisses_L_comp(spectre_entier_L_comp)
    affiche_spectre_L_comp()

def lit_limites_abscisses_L_comp(spectre):
    tableau_abscisses=spectre[:,0]
    limites_spectre=numpy.zeros((2))
    limites_spectre[0]=tableau_abscisses[0]             # lit le valeurs min et max du spectre
    limites_spectre[1]=tableau_abscisses[-1]
    variable_zoom_inf_L_comp.set(limites_spectre[0])    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_sup_L_comp.set(limites_spectre[1])
    entree_zoom_inf_L_comp.configure(from_=limites_spectre[0], to=limites_spectre[1])   #fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_sup_L_comp.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree1_L_comp.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree2_L_comp.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree3_L_comp.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree4_L_comp.configure(from_=limites_spectre[0], to=limites_spectre[1])
    return limites_spectre
       
def execute_scripts_L_comp():
    global DataFrame_resultats_L_comp
    global photo
    tableau_bornes_L_comp=creation_tab_bornes_L_comp()
    DataFrame_resultats_L_comp = LIBStick_comp_spectres.main(rep_travail_L_comp, liste_fichiers_L_comp, type_fichier_L_comp.get(), tableau_bornes_L_comp, flag_traitement_L_comp.get(),
                                flag_denominateur_L_comp.get(), flag_2D_L_comp.get(), flag_3D_L_comp.get())
    fichier=rep_travail_L_comp+"/figure.png"
    image_zoom=PIL.Image.open(fichier)    
    image_zoom=image_zoom.resize((1000, 200))
    photo=PIL.ImageTk.PhotoImage(image_zoom)
    canevas1_L_comp.create_image(500 ,100 ,image=photo)
    affiche_tableau_resultats_L_comp()
    if flag_stat_L_comp.get() == 0 :
        texte_statistiques_L_comp.grid_forget()
    if flag_stat_L_comp.get() == 1 :
        texte_statistiques_L_comp.grid(row=1, column=3, sticky=tkinter.N)
        calcule_moyenne_ecarttype_L_comp()

###############################################################################
# fonctions graphiques du caneva du spectre (frame1_L_comp)
###############################################################################
def change_flag_denominateur_L_comp():
    if flag_denominateur_L_comp.get() == 0 :
        efface_lignes_3_4_L_comp()
        entree3_L_comp.configure(state="disable")
        entree4_L_comp.configure(state="disable")
    if flag_denominateur_L_comp.get() == 1 :
        affiche_lignes_3_4_L_comp()
        entree3_L_comp.configure(state="normal")
        entree4_L_comp.configure(state="normal")
        
def change_flag_2D_L_comp():
    pass

def change_flag_3D_L_comp():
    pass

def affiche_lambda_L_comp(event):
    global lambda_texte_spectre_L_comp
    global flag_premier_lamda_L_comp
    #affiche_spectre_L_comp()
    if flag_premier_lamda_L_comp == False :
        canevas0_L_comp.delete(lambda_texte_spectre_L_comp)
    l_L_comp= event.x*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
    lambda_texte_spectre_L_comp = canevas0_L_comp.create_text(event.x, event.y, text=str(format(l_L_comp, "4.1f")), fill="blue")
    lambda_texte_L_comp.configure(text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm" ))
    flag_premier_lamda_L_comp=False
    
def affiche_position_souris_L_comp(event):
    global ligne_position_L_comp
    canevas0_L_comp.delete(ligne_position_L_comp)
    ligne_position_L_comp=canevas0_L_comp.create_line(event.x,0,event.x,200, fill="green")
    
def affiche_position_souris_motion_L_comp(event):
    global ligne_position_L_comp
    global lambda_texte_spectre_L_comp
    global flag_premier_lamda_L_comp
    canevas0_L_comp.delete(ligne_position_L_comp)
    ligne_position_L_comp=canevas0_L_comp.create_line(event.x,0,event.x,200, fill="green")
    if flag_premier_lamda_L_comp == False :
        canevas0_L_comp.delete(lambda_texte_spectre_L_comp)
    l_L_comp= event.x*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
    lambda_texte_spectre_L_comp = canevas0_L_comp.create_text(event.x, event.y, text=str(format(l_L_comp, "4.1f")), fill="blue")
    lambda_texte_L_comp.configure(text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm" ))
    flag_premier_lamda_L_comp=False
    
def affiche_spectre_L_comp():
    global limites_affichage_spectre_L_comp
    global delta_limites_L_comp
    global spectre_entier_L_comp
    limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
    limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()
    delta_limites_L_comp=limites_affichage_spectre_L_comp[1]-limites_affichage_spectre_L_comp[0]
    canevas0_L_comp.delete("all")
    spectre=numpy.zeros((0,2))
    for ligne in spectre_entier_L_comp :
        if (ligne[0] >= limites_affichage_spectre_L_comp[0] and ligne[0] <= limites_affichage_spectre_L_comp[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum=spectre[:,1].min()
    maximum=spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    #spectre[:,0] = (spectre[:,0] - spectre[0,0])*1000/(spectre[len(spectre),0]-spectre[0,0])
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp
    for i in range(len(spectre) - 1) :
        canevas0_L_comp.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])
    affiche_lignes_spectre_L_comp()
    
def affiche_lignes_spectre_L_comp():
    global ligne0_1_L_comp
    global ligne0_2_L_comp
    global ligne0_3_L_comp
    global ligne0_4_L_comp
    x_ligne0_1=((variable_1_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    x_ligne0_2=((variable_2_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_1_L_comp=canevas0_L_comp.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    ligne0_2_L_comp=canevas0_L_comp.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if flag_denominateur_L_comp.get() :
        x_ligne0_3=((variable_3_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        x_ligne0_4=((variable_4_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        ligne0_3_L_comp=canevas0_L_comp.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
        ligne0_4_L_comp=canevas0_L_comp.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        
def deplace_lignes_L_comp():
    deplace_ligne0_1_L_comp()
    deplace_ligne0_2_L_comp()
    if flag_denominateur_L_comp.get() :
        deplace_ligne0_3_L_comp()
        deplace_ligne0_4_L_comp()

def deplace_ligne0_1_L_comp():
    global ligne0_1_L_comp
    canevas0_L_comp.delete(ligne0_1_L_comp)
    x_ligne0_1=((variable_1_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_1_L_comp=canevas0_L_comp.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    if variable_1_L_comp.get() >= variable_2_L_comp.get():
        variable_2_L_comp.set(variable_1_L_comp.get())
        deplace_ligne0_2_L_comp()
        
def deplace_ligne0_2_L_comp():
    global ligne0_2_L_comp
    canevas0_L_comp.delete(ligne0_2_L_comp)
    x_ligne0_2=((variable_2_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_2_L_comp=canevas0_L_comp.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if variable_2_L_comp.get() <= variable_1_L_comp.get() :
        variable_1_L_comp.set(variable_2_L_comp.get())
        deplace_ligne0_1_L_comp()

def deplace_ligne0_3_L_comp():
    global ligne0_3_L_comp
    canevas0_L_comp.delete(ligne0_3_L_comp)
    if flag_denominateur_L_comp.get() :
        x_ligne0_3=((variable_3_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        ligne0_3_L_comp=canevas0_L_comp.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
        if variable_3_L_comp.get() >= variable_4_L_comp.get():
            variable_4_L_comp.set(variable_3_L_comp.get())
            deplace_ligne0_4_L_comp()
        
def deplace_ligne0_4_L_comp():
    global ligne0_4_L_comp
    canevas0_L_comp.delete(ligne0_4_L_comp)
    if flag_denominateur_L_comp.get() :
        x_ligne0_4=((variable_4_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        ligne0_4_L_comp=canevas0_L_comp.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        if variable_4_L_comp.get() <= variable_3_L_comp.get() :
            variable_3_L_comp.set(variable_4_L_comp.get())
            deplace_ligne0_3_L_comp()

def efface_lignes_3_4_L_comp():
    global ligne0_3_L_comp
    global ligne0_4_L_comp
    canevas0_L_comp.delete(ligne0_3_L_comp)
    canevas0_L_comp.delete(ligne0_4_L_comp)

def affiche_lignes_3_4_L_comp():
    global ligne0_3_L_comp
    global ligne0_4_L_comp
    canevas0_L_comp.delete(ligne0_3_L_comp)
    canevas0_L_comp.delete(ligne0_4_L_comp)
    x_ligne0_3=((variable_3_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    x_ligne0_4=((variable_4_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_3_L_comp=canevas0_L_comp.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
    ligne0_4_L_comp=canevas0_L_comp.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        
def deplace_ligne0_1_return_L_comp(event):
    deplace_ligne0_1_L_comp()
    
def deplace_ligne0_2_return_L_comp(event):
    deplace_ligne0_2_L_comp()
    
def deplace_ligne0_3_return_L_comp(event):
    deplace_ligne0_3_L_comp()
    
def deplace_ligne0_4_return_L_comp(event):
    deplace_ligne0_4_L_comp()

###############################################################################
# fonctions graphiques de zoom du caneva du spectre (frame1_L_comp)
###############################################################################
def change_zoom_inf_L_comp() :
#    global limites_affichage_spectre_L_comp
    if variable_zoom_inf_L_comp.get() >= variable_zoom_sup_L_comp.get() :
        variable_zoom_sup_L_comp.set(variable_zoom_inf_L_comp.get())
#    limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
#    limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()
    affiche_spectre_L_comp()
    
def change_zoom_sup_L_comp():
#    global limites_affichage_spectre_L_comp
    if variable_zoom_sup_L_comp.get() <= variable_zoom_inf_L_comp.get() :
        variable_zoom_inf_L_comp.set(variable_zoom_sup_L_comp.get())
#    limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
#    limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()
    affiche_spectre_L_comp()

def change_zoom_inf_return_L_comp(event):
    change_zoom_inf_L_comp()
    
def change_zoom_sup_return_L_comp(event):
    change_zoom_sup_L_comp()

def zoom_clic_L_comp(event):
    global coord_zoom_L_comp
    coord_zoom_L_comp[0]=event.x
    coord_zoom_L_comp[1]=event.y
    
def zoom_drag_and_drop_L_comp(event):
    global ligne_position_L_comp
    global coord_zoom_L_comp
    global limites_affichage_spectre_L_comp
    global lambda_texte_spectre_L_comp
    global flag_premier_lamda_L_comp
    canevas0_L_comp.delete(ligne_position_L_comp)
    ligne_position_L_comp=canevas0_L_comp.create_line(event.x,0,event.x,200, fill="green")
    coord_zoom_L_comp[2]=event.x
    coord_zoom_L_comp[3]=event.y
    if coord_zoom_L_comp[2] > coord_zoom_L_comp[0] :
        debut= coord_zoom_L_comp[0]*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
        fin = coord_zoom_L_comp[2]*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
        variable_zoom_inf_L_comp.set(format(debut, "4.1f"))
        variable_zoom_sup_L_comp.set(format(fin, "4.1f"))
        #affiche la longueur d'onde :
        if flag_premier_lamda_L_comp == False :
            canevas0_L_comp.delete(lambda_texte_spectre_L_comp)
        l_L_comp= event.x*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
        lambda_texte_spectre_L_comp = canevas0_L_comp.create_text(event.x, event.y, text=str(format(l_L_comp, "4.1f")), fill="blue")
        lambda_texte_L_comp.configure(text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm" ))
        flag_premier_lamda_L_comp=False
    if coord_zoom_L_comp[2] < coord_zoom_L_comp[0] :
        variable_zoom_inf_L_comp.set(limites_spectre_L_comp[0])
        variable_zoom_sup_L_comp.set(limites_spectre_L_comp[1])
        #limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
        #limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()

def zoom_clic_release_L_comp(event):
    affiche_spectre_L_comp()


###############################################################################
# fonctions graphiques du caneva de l'image 1 (frame2_L_comp)
###############################################################################
def coordonnees1_L_comp (event) :
    global x1_L_comp,y1_L_comp
    x1_L_comp=event.x
    y1_L_comp=event.y
    coord1_to_vars_5_6_L_comp(x1_L_comp,y1_L_comp)
    deplace_cible1_L_comp()
   
def deplace_cible1_L_comp():
    global x1_L_comp,y1_L_comp
    global ligne1_vert_L_comp, ligne1_hori_L_comp
    canevas1_L_comp.delete(ligne1_vert_L_comp)
    canevas1_L_comp.delete(ligne1_hori_L_comp)
    ligne1_vert_L_comp=canevas1_L_comp.create_line(x1_L_comp,0,x1_L_comp,200, fill="white")
    ligne1_hori_L_comp=canevas1_L_comp.create_line(0,y1_L_comp,1000,y1_L_comp, fill="white")    
#    canevas1_L_comp.coords(ligne1_vert_L_comp, x1_L_comp,0,x1_L_comp,200)
#    canevas1_L_comp.coords(ligne1_hori_L_comp, 0,y1_L_comp,400,y1_L_comp)
    
def coord1_to_vars_5_6_L_comp(x,y):
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    variable_5_L_comp.set(format(limites_spectre_L_comp[0] + (x * (limites_spectre_L_comp[1]-limites_spectre_L_comp[0]) / 1000), "4.1f"))
    variable_6_L_comp.set(math.ceil(y * nombre_fichiers_L_comp / 200))
    child_id = tree_resultats_L_comp.get_children()[variable_6_L_comp.get()-1]
    tree_resultats_L_comp.selection_set(child_id)
    selection=tree_resultats_L_comp.item(tree_resultats_L_comp.selection())["values"]
    nom_fichier_seul_L_comp=selection[1]
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()

def vars_5_6_to_coord1_L_comp():
    global x1_L_comp,y1_L_comp
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    x1_L_comp=round( ((variable_5_L_comp.get()-limites_spectre_L_comp[0])*1000) / (limites_spectre_L_comp[1]-limites_spectre_L_comp[0])) 
    y1_L_comp= round(200*(variable_6_L_comp.get()-0.5)/nombre_fichiers_L_comp)
    child_id = tree_resultats_L_comp.get_children()[variable_6_L_comp.get()-1]
    tree_resultats_L_comp.selection_set(child_id)
    selection=tree_resultats_L_comp.item(tree_resultats_L_comp.selection())["values"]
    nom_fichier_seul_L_comp=selection[1]
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    deplace_cible1_L_comp()
    
def vars_5_6_to_coord1_return_L_comp(event):
    vars_5_6_to_coord1_L_comp()

###############################################################################
# fonctions graphiques du tableau de résultats (frame3_L_comp)
###############################################################################
def affiche_tableau_resultats_L_comp(): 
    efface_tableau_resultats_L_comp()
    num_ligne=1
    if flag_denominateur_L_comp.get() == 1 :
        tree_resultats_L_comp.heading(3, text="Rapport zone1/zone2")
        for ligne_tableau in DataFrame_resultats_L_comp.iterrows() :
            ID_L_comp=tree_resultats_L_comp.insert("","end", values=(num_ligne, ligne_tableau[0], DataFrame_resultats_L_comp.iloc[num_ligne-1, 2]))
            num_ligne=num_ligne+1
    if flag_denominateur_L_comp.get() == 0 :
        tree_resultats_L_comp.heading(3, text="Aire zone 1")
        for ligne_tableau in DataFrame_resultats_L_comp.iterrows() :
            ID_L_comp=tree_resultats_L_comp.insert("","end", values=(num_ligne, ligne_tableau[0], DataFrame_resultats_L_comp.iloc[num_ligne-1, 0]))
            num_ligne=num_ligne+1
        
def efface_tableau_resultats_L_comp():
    for i in tree_resultats_L_comp.get_children() :
        tree_resultats_L_comp.delete(i)

def selectionne_spectre_L_comp(event):
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    selection=tree_resultats_L_comp.selection()
    item=tree_resultats_L_comp.item(selection)["values"]
    print(item)
    variable_6_L_comp.set(item[0])
    nom_fichier_seul_L_comp=item[1]
    vars_5_6_to_coord1_L_comp()
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    
def selectionne_spectre_up_L_comp(event):
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    selection=tree_resultats_L_comp.prev(tree_resultats_L_comp.selection())
    item=tree_resultats_L_comp.item(selection)["values"]
    print(item)
    variable_6_L_comp.set(item[0])
    nom_fichier_seul_L_comp=item[1]
    vars_5_6_to_coord1_L_comp()
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    tree_resultats_L_comp.see(selection)

def selectionne_spectre_down_L_comp(event):
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    selection=tree_resultats_L_comp.next(tree_resultats_L_comp.selection())
    item=tree_resultats_L_comp.item(selection)["values"]
    print(item)
    variable_6_L_comp.set(item[0])
    nom_fichier_seul_L_comp=item[1]
    vars_5_6_to_coord1_L_comp()
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()  
    tree_resultats_L_comp.see(selection)

def calcule_moyenne_ecarttype_L_comp() :
    if flag_denominateur_L_comp.get() == 1 :
        median_L_comp=DataFrame_resultats_L_comp["Rapport"].median()
        moyenne_L_comp=DataFrame_resultats_L_comp["Rapport"].mean()
        ecarttype_L_comp=DataFrame_resultats_L_comp["Rapport"].std()
        min_L_comp=DataFrame_resultats_L_comp["Rapport"].min()
        max_L_comp=DataFrame_resultats_L_comp["Rapport"].max()
    if flag_denominateur_L_comp.get() == 0 :
        median_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].median()
        moyenne_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].mean()
        ecarttype_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].std()
        min_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].min()
        max_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].max()
    texte_median="Median :\n" +str(format(median_L_comp, "3.4f"))
    texte_moyenne= "Moyenne :\n" + str(format(moyenne_L_comp, "3.4f"))
    texte_ecarttype= "Ecart type :\n" + str(format(ecarttype_L_comp,"3.4f"))
    texte_min= "Minimum :\n" +  str(format(min_L_comp,"3.4f"))
    texte_max= "Maximum :\n" +  str(format(max_L_comp,"3.4f"))
    texte_statistiques_L_comp.configure(text= texte_median +"\n" +texte_moyenne +"\n"+texte_ecarttype +"\n"+ texte_min +"\n"+ texte_max)





###############################################################################
###############################################################################
# Fonctions LIBStick_IHM_ACP : onglet 4
###############################################################################
###############################################################################
def __________L_ACP__________():pass
###############################################################################
# initialisations
###############################################################################
def charge_param_L_ACP() :
    dictionnaire_ini_L_ACP=lit_section_fichier_ini("LIBStick_ACP")
    borne_zone1_inf_L_ACP = float(dictionnaire_ini_L_ACP["borne_zone1_inf_L_ACP"])
    borne_zone1_sup_L_ACP = float(dictionnaire_ini_L_ACP["borne_zone1_sup_L_ACP"])
    tableau_bornes_init_L_ACP=numpy.array([borne_zone1_inf_L_ACP,borne_zone1_sup_L_ACP])
    tableau_bornes_L_ACP=numpy.array([borne_zone1_inf_L_ACP,borne_zone1_sup_L_ACP])
    rep_travail_L_ACP = dictionnaire_ini_L_ACP["rep_travail_L_ACP"]
    return tableau_bornes_init_L_ACP,tableau_bornes_L_ACP,rep_travail_L_ACP

tableau_bornes_init_L_ACP,tableau_bornes_L_ACP,rep_travail_L_ACP = charge_param_L_ACP()

limites_spectre_L_ACP=numpy.array([198.0,1013.0])             # limites min et max de l'affichage du spectre
limites_affichage_spectre_L_ACP=numpy.array([198.0,1013.0])   # limites de l'affichage du spectre à l'écran
coord_zoom_L_ACP=numpy.array([198,0,1013,0])
delta_limites_L_ACP=limites_affichage_spectre_L_ACP[1]-limites_affichage_spectre_L_ACP[0]
flag_premier_lamda_L_ACP=True
l_L_ACP=0.0
spectre_entier_L_ACP=numpy.zeros((0,2))
spectre_corrige_L_ACP=numpy.zeros((0,2))
#tableau_bornes_L_ACP=numpy.array([300.0, 608.0])

def affiche_nom_spectre_onglet4() :
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ACP)

###############################################################################
# fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_ACP() :
    tableau_bornes_L_ACP[0]=variable_1_L_ACP.get()
    tableau_bornes_L_ACP[1]=variable_2_L_ACP.get() 
    return tableau_bornes_L_ACP

def reset_tableau_L_ACP() :
    tableau_bornes_L_ACP=tableau_bornes_init_L_ACP.copy()
    variable_1_L_ACP.set(tableau_bornes_L_ACP[0])
    variable_2_L_ACP.set(tableau_bornes_L_ACP[1])
    deplace_lignes_L_ACP()

def choix_fichier_L_ACP():
    global nom_fichier_seul_L_ACP
    global rep_travail_L_ACP
    global nombre_fichiers_L_ACP
    global liste_fichiers_L_ACP
    global DataFrame_complet_L_ACP
    nom_fichier_L_ACP = tkinter.filedialog.askopenfilename(title='Choisissez un fichier spectre',
                                                            initialdir=rep_travail_L_ACP,
                                                            filetypes=(("fichiers LIBStick moyen","*.mean"),
                                                                       ("fichiers LIBStick","*.tsv"),
                                                                       ("fichiers IVEA","*.asc"),
                                                                       ("fichiers SciAps","*.csv")), multiple=False)
    nom_fichier_seul_L_ACP=os.path.basename(nom_fichier_L_ACP)
    type_fichier_L_ACP.set(pathlib.Path(nom_fichier_seul_L_ACP).suffix)
    rep_travail_L_ACP = os.path.dirname(nom_fichier_L_ACP)
    liste_fichiers_L_ACP=LIBStick_outils.creation_liste_fichiers(rep_travail_L_ACP, type_fichier_L_ACP.get())
    nombre_fichiers_L_ACP=len(liste_fichiers_L_ACP)    
#    entree6_L_ACP.configure(from_=1, to=nombre_fichiers_L_ACP)
    tableau_spectres_L_ACP=LIBStick_outils.creer_tableau_avec_x_colonne1(liste_fichiers_L_ACP, type_fichier_L_ACP.get())
    DataFrame_complet_L_ACP=LIBStick_outils.creer_DataFrame_x_tableau_en_colonnes(tableau_spectres_L_ACP, liste_fichiers_L_ACP)
    lit_affiche_spectre_L_ACP()    
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ACP)
    bouton_execute_L_ACP.configure(state="normal")

def lit_affiche_spectre_L_ACP():
    global spectre_entier_L_ACP 
    global limites_spectre_L_ACP
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())    
    limites_spectre_L_ACP=lit_limites_abscisses_L_ACP(spectre_entier_L_ACP)
    affiche_spectre_L_ACP()
    affiche_tableau_L_ACP()

def lit_limites_abscisses_L_ACP(spectre):
    tableau_abscisses=spectre[:,0]
    limites_spectre=numpy.zeros((2))
    limites_spectre[0]=tableau_abscisses[0]             # lit le valeurs min et max du spectre
    limites_spectre[1]=tableau_abscisses[-1]
    variable_zoom_inf_L_ACP.set(limites_spectre[0])    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_sup_L_ACP.set(limites_spectre[1])
    entree_zoom_inf_L_ACP.configure(from_=limites_spectre[0], to=limites_spectre[1])   #fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_sup_L_ACP.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree1_L_ACP.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree2_L_ACP.configure(from_=limites_spectre[0], to=limites_spectre[1])
    return limites_spectre

def treeview_dataframe_L_ACP():
    treeview_columns = ["numero", "nom", "calcul ACP","label"] # list of names here
    treeview_df = pandas.DataFrame(columns=treeview_columns)
    for ligne in tree_L_ACP.get_children():
        # each row will come as a list under name "values" 
        values = pandas.DataFrame([tree_L_ACP.item(ligne)["values"]], columns=treeview_columns)
        treeview_df = treeview_df.append(values,ignore_index=True)
    lignes=treeview_df.shape[0]
    treeview_df = treeview_df.set_index([pandas.Index(range(1,lignes+1))])
    return treeview_df

def coupe_dataframe_L_ACP(dataframe,treeview_dataframe,tableau_bornes):
    tableau=dataframe.values
    n=dataframe.shape[0]   #nbre d'observation en lignes
    index_numeros=range(1,n+1)
    dataframe_coupe=pandas.DataFrame(tableau, index=index_numeros, columns=dataframe.columns)
    treeview_dataframe_coupe = treeview_dataframe.copy(deep=True)
    i=1
    for selection in treeview_dataframe["calcul ACP"] :
        if selection == "Non" :
            print("supprime la ligne n° " + str(i))
            dataframe_coupe=dataframe_coupe.drop(index=i)
            treeview_dataframe_coupe=treeview_dataframe_coupe.drop(index=i)
        i=i+1
#    print(dataframe_coupe)
#    print("----------------------------")
    for nom_colonne in dataframe.columns :
        if float(nom_colonne) < tableau_bornes[0] or float(nom_colonne) > tableau_bornes[1] :
            dataframe_coupe = dataframe_coupe.drop(nom_colonne, axis=1)
#    print(dataframe_coupe)
#    print("----------------------------")
    return dataframe_coupe,treeview_dataframe_coupe

def change_flag_3D_L_ACP() :
    if flag_3D_L_ACP.get() == True :
        entree_dim3_L_ACP.configure(state="normal")
    if flag_3D_L_ACP.get() == False :
        entree_dim3_L_ACP.configure(state="disable")

def execute_ACP_L_ACP() :
    global donnees_ACP_L_ACP
    global dataframe_facteurs_ACP_L_ACP
    tableau_bornes_L_ACP=creation_tab_bornes_L_ACP()
    dataframe=DataFrame_complet_L_ACP.copy(deep=True) # copie indispensable car la suite modifierait DataFrame_complet_L_ACP !
    treeview_dataframe = treeview_dataframe_L_ACP()
    dataframe,treeview_dataframe=coupe_dataframe_L_ACP(dataframe,treeview_dataframe,tableau_bornes_L_ACP) # suprime les lignes non incluses dans le calcul de l'ACP
    if flag_normalise_L_ACP.get()==True :
        dataframe=LIBStick_outils.normalise_DataFrame_aire(dataframe)
    if flag_3D_L_ACP.get() :
        dim_L_ACP = [dim_1_L_ACP.get(), dim_2_L_ACP.get(), dim_3_L_ACP.get()]
    else :
        dim_L_ACP = [dim_1_L_ACP.get(), dim_2_L_ACP.get()]
    donnees_ACP_L_ACP=LIBStick_ACP.calcul_ACP_sklearn(dataframe,treeview_dataframe, dim_L_ACP,
                                              flag_centre_reduit_L_ACP.get(), flag_3D_L_ACP.get(),
                                              flag_echelle_L_ACP.get(), flag_eboulis_L_ACP.get())
    nbr_spectres = dataframe.shape[0]
    nbr_variables = dataframe.shape[1]
    nbr_composantes = nbr_spectres
    if nbr_spectres >= 20 :
        nbr_composantes = 20
    valeurs_propres_corrigees = donnees_ACP_L_ACP.explained_variance_ * (nbr_spectres-1)/nbr_spectres
#    print(valeurs_propres_corrigees)
    sqrt_valeurs_propres_corrigees = numpy.sqrt(valeurs_propres_corrigees)
    facteurs_ACP_corrigees = numpy.zeros((nbr_composantes,nbr_variables))
    for i in range(nbr_composantes) :
        facteurs_ACP_corrigees[i,:] = donnees_ACP_L_ACP.components_[i,:] * sqrt_valeurs_propres_corrigees[i]
    dataframe_facteurs_ACP_L_ACP=pandas.DataFrame(facteurs_ACP_corrigees, columns=dataframe.columns)
    affiche_spectres_var_ACP_L_ACP()
    bouton_enregistre_L_ACP.configure(state="normal")
    
def enregistre_var_explic_L_ACP() :
    suffixe_L_ACP="_"
    if flag_normalise_L_ACP.get() == True :
        suffixe_L_ACP = suffixe_L_ACP + "norm_"
    if flag_centre_reduit_L_ACP.get() == True :
        suffixe_L_ACP = suffixe_L_ACP + "reduit_"
    nom_fichier_sauvegarde_L_ACP = tkinter.filedialog.asksaveasfilename(title='Sauvegarde de variables explicites',
                                                            initialdir=rep_travail_L_ACP)
    nom_fichier_sauvegarde_L_ACP = nom_fichier_sauvegarde_L_ACP + suffixe_L_ACP
#    pandas.DataFrame(spectre_dim1_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP+"dim1.csv")
    pandas.DataFrame(spectre_dim1_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP + str(dim_1_L_ACP.get()) + ".txt",
                     sep='\t', decimal=",", header=None, index=None)
    pandas.DataFrame(spectre_dim1_L_ACP).to_excel(nom_fichier_sauvegarde_L_ACP + str(dim_1_L_ACP.get()) + ".xls",
                                                  header=None, index=None)
#    pandas.DataFrame(spectre_dim2_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP+"dim2.csv")
    pandas.DataFrame(spectre_dim2_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP + str(dim_2_L_ACP.get()) + ".txt",
                     sep='\t', decimal=",", header=None, index=None)
    pandas.DataFrame(spectre_dim2_L_ACP).to_excel(nom_fichier_sauvegarde_L_ACP + str(dim_2_L_ACP.get()) + ".xls",
                     header=None, index=None)
    if flag_3D_L_ACP.get() == True :
        pandas.DataFrame(spectre_dim3_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP + str(dim_3_L_ACP.get()) + ".txt",
                         sep='\t', decimal=",", header=None, index=None)
        pandas.DataFrame(spectre_dim3_L_ACP).to_excel(nom_fichier_sauvegarde_L_ACP + str(dim_3_L_ACP.get()) + ".xls",
                         header=None, index=None)

###############################################################################
# fonctions graphiques du caneva du spectre (frame1_L_ACP)
###############################################################################
def affiche_lambda_L_ACP(event):
    global lambda_texte_spectre_0_L_ACP
    global lambda_texte_spectre_1_L_ACP
    global flag_premier_lamda_L_ACP
    #affiche_spectre_L_ACP()
    if flag_premier_lamda_L_ACP == False :
        canevas0_L_ACP.delete(lambda_texte_spectre_0_L_ACP)
        canevas1_L_ACP.delete(lambda_texte_spectre_1_L_ACP)
    l_L_ACP= event.x*delta_limites_L_ACP/1000+limites_affichage_spectre_L_ACP[0]
    lambda_texte_spectre_0_L_ACP = canevas0_L_ACP.create_text(event.x, event.y, text=str(format(l_L_ACP, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_ACP = canevas1_L_ACP.create_text(event.x, event.y, text=str(format(l_L_ACP, "4.1f")), fill="blue")
    lambda_texte_L_ACP.configure(text="Lambda = " + str(format(l_L_ACP, "4.1f") + " nm" ))
    flag_premier_lamda_L_ACP=False
    
def affiche_position_souris_L_ACP(event):
    global ligne_position_0_L_ACP
    global ligne_position_1_L_ACP
    canevas0_L_ACP.delete(ligne_position_0_L_ACP)
    ligne_position_0_L_ACP=canevas0_L_ACP.create_line(event.x,0,event.x,200, fill="green")
    canevas1_L_ACP.delete(ligne_position_1_L_ACP)
    ligne_position_1_L_ACP=canevas1_L_ACP.create_line(event.x,0,event.x,200, fill="green")
    
def affiche_position_souris_motion_L_ACP(event):
    global ligne_position_0_L_ACP
    global ligne_position_1_L_ACP
    global lambda_texte_spectre_0_L_ACP
    global lambda_texte_spectre_1_L_ACP
    global flag_premier_lamda_L_ACP
    canevas0_L_ACP.delete(ligne_position_0_L_ACP)
    canevas1_L_ACP.delete(ligne_position_1_L_ACP)
    ligne_position_0_L_ACP=canevas0_L_ACP.create_line(event.x,0,event.x,200, fill="green")
    ligne_position_1_L_ACP=canevas1_L_ACP.create_line(event.x,0,event.x,200, fill="green")
    if flag_premier_lamda_L_ACP == False :
        canevas0_L_ACP.delete(lambda_texte_spectre_0_L_ACP)
        canevas1_L_ACP.delete(lambda_texte_spectre_1_L_ACP)
    l_L_ACP= event.x*delta_limites_L_ACP/1000+limites_affichage_spectre_L_ACP[0]
    lambda_texte_spectre_0_L_ACP = canevas0_L_ACP.create_text(event.x, event.y, text=str(format(l_L_ACP, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_ACP = canevas1_L_ACP.create_text(event.x, event.y, text=str(format(l_L_ACP, "4.1f")), fill="blue")
    lambda_texte_L_ACP.configure(text="Lambda = " + str(format(l_L_ACP, "4.1f") + " nm" ))
    flag_premier_lamda_L_ACP=False
    
def affiche_spectre_L_ACP():
    global limites_affichage_spectre_L_ACP
    global delta_limites_L_ACP
    global spectre_entier_L_ACP
    limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
    limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()
    delta_limites_L_ACP=limites_affichage_spectre_L_ACP[1]-limites_affichage_spectre_L_ACP[0]
    canevas0_L_ACP.delete("all")
    spectre=numpy.zeros((0,2))
    for ligne in spectre_entier_L_ACP :
        if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum=spectre[:,1].min()
    maximum=spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    #spectre[:,0] = (spectre[:,0] - spectre[0,0])*1000/(spectre[len(spectre),0]-spectre[0,0])
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP
    for i in range(len(spectre) - 1) :
        canevas0_L_ACP.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])
    affiche_lignes_spectre_L_ACP()
    
def affiche_lignes_spectre_L_ACP():
    global ligne0_1_L_ACP
    global ligne0_2_L_ACP
    global ligne0_3_L_ACP
    global ligne0_4_L_ACP
    x_ligne0_1=((variable_1_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP)
    x_ligne0_2=((variable_2_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP)
    ligne0_1_L_ACP=canevas0_L_ACP.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    ligne0_2_L_ACP=canevas0_L_ACP.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    
def deplace_lignes_L_ACP():
    deplace_ligne0_1_L_ACP()
    deplace_ligne0_2_L_ACP()
#    if flag_denominateur_L_ACP.get() :
#        deplace_ligne0_3_L_ACP()
#        deplace_ligne0_4_L_ACP()

def deplace_ligne0_1_L_ACP():
    global ligne0_1_L_ACP
    canevas0_L_ACP.delete(ligne0_1_L_ACP)
    x_ligne0_1=((variable_1_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP)
    ligne0_1_L_ACP=canevas0_L_ACP.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    if variable_1_L_ACP.get() >= variable_2_L_ACP.get():
        variable_2_L_ACP.set(variable_1_L_ACP.get())
        deplace_ligne0_2_L_ACP()
        
def deplace_ligne0_2_L_ACP():
    global ligne0_2_L_ACP
    canevas0_L_ACP.delete(ligne0_2_L_ACP)
    x_ligne0_2=((variable_2_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP)
    ligne0_2_L_ACP=canevas0_L_ACP.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if variable_2_L_ACP.get() <= variable_1_L_ACP.get() :
        variable_1_L_ACP.set(variable_2_L_ACP.get())
        deplace_ligne0_1_L_ACP()
        
def deplace_ligne0_1_return_L_ACP(event):
    deplace_ligne0_1_L_ACP()
    
def deplace_ligne0_2_return_L_ACP(event):
    deplace_ligne0_2_L_ACP()

###############################################################################
# fonctions graphiques du caneva des "spectres de variable de l'ACP" (frame3_L_ACP)
###############################################################################  
def affiche_spectres_var_ACP_L_ACP():
    global spectre_dim1_L_ACP
    global spectre_dim2_L_ACP
    global spectre_dim3_L_ACP
    
    spectres=dataframe_facteurs_ACP_L_ACP.values
    canevas1_L_ACP.delete("all")
    
    dim1=dim_1_L_ACP.get()-1
    dim2=dim_2_L_ACP.get()-1
    spectre_dim1_L_ACP=dataframe_facteurs_ACP_L_ACP.columns
    spectre_dim2_L_ACP=dataframe_facteurs_ACP_L_ACP.columns
    spectre_dim1_L_ACP=numpy.column_stack((spectre_dim1_L_ACP,spectres[dim1,:]))
    spectre_dim2_L_ACP=numpy.column_stack((spectre_dim2_L_ACP,spectres[dim2,:]))

    spectre1=numpy.zeros((0,2))
    spectre2=numpy.zeros((0,2))
    for ligne in spectre_dim1_L_ACP :
        if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]) :
            spectre1=numpy.row_stack((spectre1,ligne))
    for ligne in spectre_dim2_L_ACP :
        if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]) :
            spectre2=numpy.row_stack((spectre2,ligne))
    
    minimum1=spectre1[:,1].min()
    maximum1=spectre1[:,1].max()
    minimum2=spectre2[:,1].min()
    maximum2=spectre2[:,1].max()
    minimum=min(minimum1,minimum2)
    maximum=max(maximum1,maximum2)
    
    if flag_3D_L_ACP.get() == True :
        dim3=dim_3_L_ACP.get()-1
        spectre_dim3_L_ACP=dataframe_facteurs_ACP_L_ACP.columns
        spectre_dim3_L_ACP=numpy.column_stack((spectre_dim3_L_ACP,spectres[dim3,:]))
        spectre3=numpy.zeros((0,2))
        for ligne in spectre_dim3_L_ACP :
            if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]) :
                spectre3=numpy.row_stack((spectre3,ligne))
        minimum3=spectre3[:,1].min()
        maximum3=spectre3[:,1].max()       
        minimum=min(minimum,minimum3)
        maximum=max(maximum,maximum3)
    
    spectre1[:,1] = (200-(spectre1[:,1] - minimum)*200/((maximum - minimum)+0.000000001))
    spectre1[:,0] = (spectre1[:,0] - limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP
    for i in range(len(spectre1) - 1) :
        canevas1_L_ACP.create_line(spectre1[i,0],spectre1[i,1],spectre1[i+1,0],spectre1[i+1,1], fill="red")
        
    spectre2[:,1] = (200-(spectre2[:,1] - minimum)*200/((maximum - minimum)+0.000000001))
    spectre2[:,0] = (spectre2[:,0] - limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP
    for i in range(len(spectre2) - 1) :
        canevas1_L_ACP.create_line(spectre2[i,0],spectre2[i,1],spectre2[i+1,0],spectre2[i+1,1], fill="blue")
    
    if flag_3D_L_ACP.get() == True :
        spectre3[:,1] = (200-(spectre3[:,1] - minimum)*200/((maximum - minimum)+0.000000001))
        spectre3[:,0] = (spectre3[:,0] - limites_affichage_spectre_L_ACP[0])*1000/delta_limites_L_ACP
        for i in range(len(spectre3) - 1) :
            canevas1_L_ACP.create_line(spectre3[i,0],spectre3[i,1],spectre3[i+1,0],spectre3[i+1,1], fill="green")

    y=(200-(0 - minimum)*200/((maximum - minimum)+0.000000001))
    canevas1_L_ACP.create_line(0,y,1000,y, fill="grey")

###############################################################################
# fonctions graphiques de zoom du caneva du spectre (frame1_L_ACP)
###############################################################################
def change_zoom_inf_L_ACP() :
#    global limites_affichage_spectre_L_ACP
    if variable_zoom_inf_L_ACP.get() >= variable_zoom_sup_L_ACP.get() :
        variable_zoom_sup_L_ACP.set(variable_zoom_inf_L_ACP.get())
#    limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
#    limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()
    affiche_spectre_L_ACP()
    affiche_spectres_var_ACP_L_ACP()
    
def change_zoom_sup_L_ACP():
#    global limites_affichage_spectre_L_ACP
    if variable_zoom_sup_L_ACP.get() <= variable_zoom_inf_L_ACP.get() :
        variable_zoom_inf_L_ACP.set(variable_zoom_sup_L_ACP.get())
#    limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
#    limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()
    affiche_spectre_L_ACP()
    affiche_spectres_var_ACP_L_ACP()

def change_zoom_inf_return_L_ACP(event):
    change_zoom_inf_L_ACP()
    
def change_zoom_sup_return_L_ACP(event):
    change_zoom_sup_L_ACP()

def zoom_clic_L_ACP(event):
    global coord_zoom_L_ACP
    coord_zoom_L_ACP[0]=event.x
    coord_zoom_L_ACP[1]=event.y
    
def zoom_drag_and_drop_L_ACP(event):
    global ligne_position_0_L_ACP
    global ligne_position_1_L_ACP
    global coord_zoom_L_ACP
    global limites_affichage_spectre_L_ACP
    global lambda_texte_spectre_0_L_ACP
    global lambda_texte_spectre_1_L_ACP
    global flag_premier_lamda_L_ACP
    canevas0_L_ACP.delete(ligne_position_0_L_ACP)
    canevas1_L_ACP.delete(ligne_position_1_L_ACP)
    ligne_position_0_L_ACP=canevas0_L_ACP.create_line(event.x,0,event.x,200, fill="green")
    ligne_position_1_L_ACP=canevas1_L_ACP.create_line(event.x,0,event.x,200, fill="green")
    coord_zoom_L_ACP[2]=event.x
    coord_zoom_L_ACP[3]=event.y
    if coord_zoom_L_ACP[2] > coord_zoom_L_ACP[0] :
        debut= coord_zoom_L_ACP[0]*delta_limites_L_ACP/1000+limites_affichage_spectre_L_ACP[0]
        fin = coord_zoom_L_ACP[2]*delta_limites_L_ACP/1000+limites_affichage_spectre_L_ACP[0]
        variable_zoom_inf_L_ACP.set(format(debut, "4.1f"))
        variable_zoom_sup_L_ACP.set(format(fin, "4.1f"))
        #affiche la longueur d'onde :
        if flag_premier_lamda_L_ACP == False :
            canevas0_L_ACP.delete(lambda_texte_spectre_0_L_ACP)
            canevas1_L_ACP.delete(lambda_texte_spectre_1_L_ACP)
        l_L_ACP= event.x*delta_limites_L_ACP/1000+limites_affichage_spectre_L_ACP[0]
        lambda_texte_spectre_0_L_ACP = canevas0_L_ACP.create_text(event.x, event.y, text=str(format(l_L_ACP, "4.1f")), fill="blue")
        lambda_texte_spectre_1_L_ACP = canevas1_L_ACP.create_text(event.x, event.y, text=str(format(l_L_ACP, "4.1f")), fill="blue")
        lambda_texte_L_ACP.configure(text="Lambda = " + str(format(l_L_ACP, "4.1f") + " nm" ))
        flag_premier_lamda_L_ACP=False
    if coord_zoom_L_ACP[2] < coord_zoom_L_ACP[0] :
        variable_zoom_inf_L_ACP.set(limites_spectre_L_ACP[0])
        variable_zoom_sup_L_ACP.set(limites_spectre_L_ACP[1])
        #limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
        #limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()

def zoom_clic_release_L_ACP(event):
    affiche_spectre_L_ACP()
    affiche_spectres_var_ACP_L_ACP()

###############################################################################
# fonctions graphiques du tableau de résultats (frame2_L_ACP)
###############################################################################
def affiche_tableau_L_ACP():
    efface_tableau_L_ACP()
    num_ligne=1
    for ligne_tableau in DataFrame_complet_L_ACP.iterrows() :
        ID_L_ACP=tree_L_ACP.insert("","end", values=(num_ligne, ligne_tableau[0], "Oui", 0))
        num_ligne=num_ligne+1
        
def efface_tableau_L_ACP():
    for i in tree_L_ACP.get_children() :
        tree_L_ACP.delete(i)

def selectionne_spectre_L_ACP(event):
    global spectre_entier_L_ACP
    global nom_fichier_seul_L_ACP
    selection=tree_L_ACP.selection()
    item=tree_L_ACP.item(selection)["values"]
#    print(tree_L_ACP.focus())
#    print(tree_L_ACP.item(tree_L_ACP.focus()))
    nom_fichier_seul_L_ACP=item[1]
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ACP)
    affiche_spectre_L_ACP()
    
def selectionne_spectre_up_L_ACP(event):
    global spectre_entier_L_ACP
    global nom_fichier_seul_L_ACP    
    selection=tree_L_ACP.prev(tree_L_ACP.selection())
    item=tree_L_ACP.item(selection)["values"]
    nom_fichier_seul_L_ACP=item[1]
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ACP)
    affiche_spectre_L_ACP()
    tree_L_ACP.see(selection)

def selectionne_spectre_down_L_ACP(event):
    global spectre_entier_L_ACP
    global nom_fichier_seul_L_ACP
    selection=tree_L_ACP.next(tree_L_ACP.selection())
    item=tree_L_ACP.item(selection)["values"]
    nom_fichier_seul_L_ACP=item[1]
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP=LIBStick_outils.lit_spectre(nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())
    fenetre_principale.title("LIBStick v1.5"+"\t spectre : "+nom_fichier_seul_L_ACP)
    affiche_spectre_L_ACP()
    tree_L_ACP.see(selection)

def change_tree_selection_L_ACP(event):
    selection=tree_L_ACP.selection()
    item=tree_L_ACP.item(selection)["values"]
    if item[2] == "Non" :
#        tree_L_ACP.item(selection, values=(item[0],item[1], "Oui"))
        tree_L_ACP.item(selection, values=(item[0],item[1], "Oui",item[3]), tags="select")
    if item[2] == "Oui" :
#        tree_L_ACP.item(selection, values=(item[0],item[1],"Non"))
        tree_L_ACP.item(selection, values=(item[0],item[1],"Non",item[3]), tags="deselect")
        
def ouvre_fenetre_change_tree_label_L_ACP(event):
    global fenetre_label_L_ACP
    global tableau_label_ouvert_flag_L_ACP
    selection=tree_L_ACP.selection()
    item=tree_L_ACP.item(selection)["values"]
    if tableau_label_ouvert_flag_L_ACP == False :
        tableau_label_ouvert_flag_L_ACP=True
        fenetre_label_L_ACP=tkinter.Toplevel(fenetre_principale)
        fenetre_label_L_ACP.geometry("200x150")
        fenetre_label_L_ACP.resizable(False,False)
        frame_label_L_ACP=tkinter.Frame(fenetre_label_L_ACP, bg="light grey")
        frame_label_L_ACP.pack()
        label_L_ACP.set(value=item[3])
        entree_label_L_ACP=tkinter.Spinbox(frame_label_L_ACP, from_=0, to=20, increment=1, width=200, textvariable=label_L_ACP)
        entree_label_L_ACP.pack(ipadx=0, ipady=0)
        buttonFont = tkinter.font.Font(family='Helvetica', size=30)
        bouton_label_L_ACP=tkinter.Button(frame_label_L_ACP, text="Valider", font=buttonFont, width=200,height=100,
                                          command = validation_label_L_ACP, bg=couleur_interface)
        bouton_label_L_ACP.pack(ipadx=0, ipady=0)
        fenetre_label_L_ACP.protocol("WM_DELETE_WINDOW", ferme_fenetre_change_tree_label_L_ACP)
    else :
        validation_label_L_ACP()
#        fenetre_label_L_ACP.focus_force()
#        fenetre_label_L_ACP.focus_set()
        fenetre_label_L_ACP.protocol("WM_DELETE_WINDOW", ferme_fenetre_change_tree_label_L_ACP)
        
def ferme_fenetre_change_tree_label_L_ACP():
    global tableau_label_ouvert_flag_L_ACP
    tableau_label_ouvert_flag_L_ACP=False
    fenetre_label_L_ACP.destroy()
            
def validation_label_L_ACP() :
    selection=tree_L_ACP.selection()
    item=tree_L_ACP.item(selection)["values"]
    tree_L_ACP.item(selection, values=(item[0],item[1], item[2],label_L_ACP.get()))



###############################################################################
###############################################################################
# Fonctions LIBStick_elements : fenetre Toplevel
###############################################################################
###############################################################################
def __________L_ele__________():pass
###############################################################################
# 0- initialisations
###############################################################################
tableau_periodique_ouvert_L_ele= False

###############################################################################
# 1- fonctions d'affichage du tableau périodique et des positions sur le spectre
###############################################################################
def lit_tableau_periodique_L_ele() :    
    DataFrame_tableau_periodique_L_ele= pandas.read_table(rep_LIBStick+"/LIBStick_datas/LIBStick_classification.tsv")
    return DataFrame_tableau_periodique_L_ele

def lit_element_L_ele(symbole):
    try :
        if flag_neutres_ions_L_ele.get() == 1 :
            DataFrame_element_L_ele=pandas.read_table(rep_LIBStick+"/LIBStick_datas/elements/"+symbole+".csv")
            return DataFrame_element_L_ele
        if flag_neutres_ions_L_ele.get() == 2 :
            DataFrame_element_L_ele=pandas.read_table(rep_LIBStick+"/LIBStick_datas/ions/"+symbole+".csv")
            return DataFrame_element_L_ele            
    except :
        fenetre_exception_L_ele=tkinter.messagebox.showinfo(title="Attention !", message="Pas d'informations pour cet élément.")
        print("Pas de fichier de données pour cet éléments")
        
def affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre, ID_onglet):
    if ID_onglet == 0 :
        affiche_spectre_L_trait()
        affiche_fond_L_trait()
        affiche_spectre_corrige_L_trait()
    if ID_onglet == 1 :
        affiche_spectre_L_ext()
    if ID_onglet == 2 :
        affiche_spectre_L_comp()
    if ID_onglet == 3 :
        affiche_spectre_L_ACP()
        affiche_spectres_var_ACP_L_ACP()
    if flag_neutres_ions_L_ele.get() == 1 :
        couleur_lignes="magenta2"
    if flag_neutres_ions_L_ele.get() == 2 :
        couleur_lignes="cyan3"
    for ligne_tableau in DataFrame_element_L_ele.itertuples() :
        if float(ligne_tableau[2]) > limites_affichage_spectre[0] and float(ligne_tableau[2]) < limites_affichage_spectre[1] :
            delta_limites= limites_affichage_spectre[1]-limites_affichage_spectre[0]
            long_onde=ligne_tableau[2]
            intensite_relative=ligne_tableau[5]
            if intensite_relative >= 10 and flag_sup10_L_ele.get() == 1 :
                #affiche_ligne_element(long_onde, canevas0_L_ext)
                x_ligne=((long_onde-limites_affichage_spectre[0])*1000/delta_limites)
                if ID_onglet==0 :
                    ligne0=canevas0_L_trait.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                    ligne1=canevas1_L_trait.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                if ID_onglet==1 :
                    ligne=canevas0_L_ext.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                if ID_onglet==2 :
                    ligne=canevas0_L_comp.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                if ID_onglet==3 :
                    ligne0=canevas0_L_ACP.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                    ligne1=canevas1_L_ACP.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
            if intensite_relative < 10 and intensite_relative >= 1 and flag_sup1_L_ele.get() == 1 :
                x_ligne=((long_onde-limites_affichage_spectre[0])*1000/delta_limites)
                if ID_onglet==0 :
                    ligne0=canevas0_L_trait.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                    ligne1=canevas1_L_trait.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                if ID_onglet==1 :
                    ligne=canevas0_L_ext.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                if ID_onglet==2 :
                    ligne=canevas0_L_comp.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                if ID_onglet==3 :
                    ligne0=canevas0_L_ACP.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                    ligne1=canevas1_L_ACP.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
            if intensite_relative < 1 and flag_inf1_L_ele.get() == 1 :
                x_ligne=((long_onde-limites_affichage_spectre[0])*1000/delta_limites)
                if ID_onglet==0 :
                    ligne0=canevas0_L_trait.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))
                    ligne1=canevas1_L_trait.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))
                if ID_onglet==1 :
                    ligne=canevas0_L_ext.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))
                if ID_onglet==2 :
                    ligne=canevas0_L_comp.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))  
                if ID_onglet==3 :
                    ligne0=canevas0_L_ACP.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))
                    ligne1=canevas1_L_ACP.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))

def affiches_lignes_element_bis_L_ele() :
    ID_onglet = onglets.index("current")
    if ID_onglet == 0 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_trait, 0)
    if ID_onglet == 1 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_ext, 1)
    if ID_onglet == 2 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_comp, 2)
    if ID_onglet == 3 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_ACP, 3)
        
def affiches_lignes_neutres_ions_L_ele() :
    global DataFrame_element_L_ele
    DataFrame_element_L_ele =lit_element_L_ele(symbole_L_ele)
    affiches_lignes_element_bis_L_ele()
    
    
def affiche_tableau_periodique_L_ele(DataFrame_tableau_periodique_L_ele, frame1, bouton_affichage_L_ele): 
    for ligne_tableau in DataFrame_tableau_periodique_L_ele.itertuples() :
        Z=ligne_tableau[1]
        symbole=ligne_tableau[2]
        nom=ligne_tableau[3]
        ligne=ligne_tableau[5]
        colonne=ligne_tableau[6]
        couleur=ligne_tableau[8]
        boutton_L_ele = case_classification(frame1, nom, symbole,  Z, ligne, colonne, couleur,bouton_affichage_L_ele)

def ouvre_fenetre_classification_L_ele():
    global fenetre_classification_L_ele
    global tableau_periodique_ouvert_L_ele
    if tableau_periodique_ouvert_L_ele == False :
        fenetre_classification_L_ele=tkinter.Toplevel(fenetre_principale)
        fenetre_classification_L_ele.resizable(False,False)
        frame1_L_ele=tkinter.Frame(fenetre_classification_L_ele, bg="light grey")
        frame1_L_ele.pack()
            
        bouton_affichage_L_ele=tkinter.Button(frame1_L_ele, width=taille_case[0]*2, height=taille_case[1]*2)
        bouton_affichage_L_ele.configure(command=affiches_lignes_element_bis_L_ele)
        bouton_affichage_L_ele.grid(row=1, column=7, rowspan=3, columnspan=2)
        
        coche_El_I_L_ele=tkinter.Radiobutton(frame1_L_ele, text="Neutres", variable=flag_neutres_ions_L_ele, value=1, bg=couleur_interface, command=affiches_lignes_neutres_ions_L_ele)
        coche_El_I_L_ele.grid(row=1, column=5, columnspan=3, sticky=tkinter.W)
        coche_El_II_L_ele=tkinter.Radiobutton(frame1_L_ele, text="Ions +", variable=flag_neutres_ions_L_ele, value=2, bg=couleur_interface, command=affiches_lignes_neutres_ions_L_ele)
        coche_El_II_L_ele.grid(row=2, column=5, columnspan=3, sticky=tkinter.W)

        coche_sup10_L_ele=tkinter.Checkbutton(frame1_L_ele, text="I relative >= 10%", variable=flag_sup10_L_ele, bg=couleur_interface, command=affiches_lignes_element_bis_L_ele)
        coche_sup10_L_ele.grid(row=1, column=9, columnspan=4, sticky=tkinter.W)
        coche_sup1_L_ele=tkinter.Checkbutton(frame1_L_ele, text="1% <= I relative < 10%", variable=flag_sup1_L_ele, bg=couleur_interface, command=affiches_lignes_element_bis_L_ele)
        coche_sup1_L_ele.grid(row=2, column=9, columnspan=4, sticky=tkinter.W)
        coche_inf1_L_ele=tkinter.Checkbutton(frame1_L_ele, text="I relative < 1%", variable=flag_inf1_L_ele, bg=couleur_interface, command=affiches_lignes_element_bis_L_ele)
        coche_inf1_L_ele.grid(row=3, column=9, columnspan=4, sticky=tkinter.W)
    
        DataFrame_tableau_periodique_L_ele=lit_tableau_periodique_L_ele()
        affiche_tableau_periodique_L_ele(DataFrame_tableau_periodique_L_ele, frame1_L_ele, bouton_affichage_L_ele)
        tableau_periodique_ouvert_L_ele = True
        fenetre_classification_L_ele.protocol("WM_DELETE_WINDOW", ferme_fenetre_classification_L_ele)
    else :
        #fenetre_classification_L_ele.lift()
        fenetre_classification_L_ele.focus_force()
        fenetre_classification_L_ele.focus_set()

def ferme_fenetre_classification_L_ele():
    global tableau_periodique_ouvert_L_ele
    tableau_periodique_ouvert_L_ele=False
    fenetre_classification_L_ele.destroy()










###############################################################################
###############################################################################
# LIBStick : interface principale
###############################################################################
###############################################################################
def __________IHM_LIBStick__________():pass
###############################################################################
#  Interface graphique : nouvelles classes
###############################################################################
class AutoScrollbar(tkinter.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    # cf. : http://effbot.org/zone/tkinter-autoscrollbar.htm
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tkinter.Scrollbar.set(self, lo, hi)
        
class case_classification(tkinter.Button) :
    taille_case = [3,2]
    def __init__(self, boss, nom, symbole,  Z, ligne, colonne, couleur, bouton_affichage):
        texte="    "+str(Z)+"\n"+symbole
        tkinter.Button.__init__(self, boss, text=texte, bg=couleur, command=lambda : self.affiche_pics(nom, symbole,Z,couleur,bouton_affichage))
        self.configure(width=taille_case[0], height=taille_case[1])
        #self.config(font=tkinter.font.Font(size=8,weight="bold"))
        self.grid(row=ligne, column=colonne)
        
    def affiche_pics(self,nom, symbole,Z,couleur, bouton_affichage):
        global symbole_L_ele
        global DataFrame_element_L_ele
        symbole_L_ele = symbole
        texte="     "+str(Z)+"\n"+symbole
        bouton_affichage.configure(text=texte, bg=couleur)
        bouton_affichage.config(font=tkinter.font.Font(size=10 , weight="bold"))
        DataFrame_element_L_ele = lit_element_L_ele(symbole)
        ID_onglet = onglets.index("current")
        if ID_onglet == 0 :
            affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_trait, ID_onglet)
        if ID_onglet == 1 :
            affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_ext, ID_onglet)
        if ID_onglet == 2 :
            affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_comp, ID_onglet)
        if ID_onglet == 3 :
            affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_ACP, ID_onglet)

###############################################################################
# 7- Interface graphique : création fenêtre principale avec scrolls et onglets
###############################################################################
fenetre_principale=tkinter.Tk()
fenetre_principale.title("LIBStick v1.5")
fenetre_principale.geometry("1160x750+100+50")
#fenetre_principale.maxsize(width=1160, height=850)
fenetre_principale.maxsize(width=1160, height=750)

vscrollbar = AutoScrollbar(fenetre_principale,orient=tkinter.VERTICAL)
vscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
hscrollbar = AutoScrollbar(fenetre_principale,orient=tkinter.HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

canevas_scroll=tkinter.Canvas(fenetre_principale,yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
canevas_scroll.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

vscrollbar.config(command=canevas_scroll.yview)
hscrollbar.config(command=canevas_scroll.xview)
# make the canvas expandable
fenetre_principale.grid_rowconfigure(0, weight=1)
fenetre_principale.grid_columnconfigure(0, weight=1)

frame_scroll=tkinter.Frame(canevas_scroll, bg=couleur_interface)
frame_scroll.rowconfigure(1, weight=1)
frame_scroll.columnconfigure(1, weight=1)

onglets=tkinter.ttk.Notebook(frame_scroll)
onglets.pack()
onglet1=tkinter.Frame(onglets, bg=couleur_interface)
onglet2=tkinter.Frame(onglets, bg=couleur_interface)
onglet3=tkinter.Frame(onglets, bg=couleur_interface)
onglet4=tkinter.Frame(onglets, bg=couleur_interface)
#onglet3=tkinter.ttk.Frame(onglets)
onglet1.pack()
onglet2.pack()
onglet3.pack()
onglet4.pack()

onglets.add(onglet1, text="LIBStick pré-traitements")
onglets.add(onglet2, text="LIBStick extraction")
onglets.add(onglet3, text="LIBStick comparaison")
onglets.add(onglet4, text="LIBStick ACP")

barre_menus = tkinter.Menu(fenetre_principale)
menu_fichier = tkinter.Menu(barre_menus)
menu_traitement=tkinter.Menu(barre_menus)
menu_extraction=tkinter.Menu(barre_menus)
menu_comparaison=tkinter.Menu(barre_menus)

barre_menus.add_cascade(label="Fichier", menu=menu_fichier)
menu_fichier.add_command(label="Sauvegarde des paramètres actuels", command=ecrit_fichier_ini)
menu_fichier.add_command(label="Restaure les paramètres par défaut au prochain démarrage", command=reset_fichier_ini)
menu_fichier.add_command(label="Quitter", command=fenetre_principale.quit)

barre_menus.add_cascade(label="Traitement", menu=menu_traitement)
#type_fichier_L_trait=tkinter.StringVar(value="IVEA")
#menu_traitement.add_radiobutton(label="LIBS IVEA (*.asc)", value="IVEA", variable=type_fichier_L_trait, state="disable")
#menu_traitement.add_radiobutton(label="LIBStick (*.tsv)", value="LIBStick", variable=type_fichier_L_trait, state="disable")

barre_menus.add_cascade(label="Extraction", menu=menu_extraction)
#type_fichier_L_ext=tkinter.StringVar(value="IVEA")
#menu_extraction.add_radiobutton(label="LIBS IVEA (*.asc)", value="IVEA", variable=type_fichier_L_ext)
#menu_extraction.add_radiobutton(label="LIBStick (*.tsv)", value="LIBStick", variable=type_fichier_L_ext)

barre_menus.add_cascade(label="Comparaison", menu=menu_comparaison)
#type_fichier_L_comp=tkinter.StringVar(value="LIBStick")
#menu_comparaison.add_radiobutton(label="LIBS IVEA (*.asc)", value="IVEA", variable=type_fichier_L_comp, state="disable")
#menu_comparaison.add_radiobutton(label="LIBStick (*.tsv)", value="LIBStick", variable=type_fichier_L_comp, state="disable")

fenetre_principale.config(menu=barre_menus)

#fenetre_classification_L_ele=tkinter.Toplevel(fenetre_principale)

###############################################################################
# Interface graphique : gestion de évènements
###############################################################################
def click_onglets(event):
#   onglet_click = onglets.tk.call(onglets._w, "identify", "tab", event.x, event.y)
    onglet_actif = onglets.index(onglets.select())
    if onglet_actif == 0 :
        affiche_nom_spectre_onglet1()
    if onglet_actif == 1 :
        affiche_nom_spectre_onglet2()
    if onglet_actif == 2 :
        affiche_nom_spectre_onglet3()
    if onglet_actif == 3 :
        affiche_nom_spectre_onglet4()

onglets.bind("<ButtonRelease-1>",click_onglets)





###############################################################################
###############################################################################
# Interface graphique LIBStick_IHM_traitement : onglet 1
###############################################################################
###############################################################################
def __________IHM_traitement__________():pass
###############################################################################
# 8- Interface graphique : création des différentes zones/étapes (frames 1-2)
###############################################################################
frame1_L_trait=tkinter.Frame(onglet1,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame2_L_trait=tkinter.Frame(onglet1,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)

frame1_L_trait.grid(row=10, column=10, sticky = "nsew")
frame2_L_trait.grid(row=20, column=10, sticky = "nsew")
#frame1_L_trait.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame2_L_trait.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame1_L_trait.grid_propagate(False)
#frame2_L_trait.grid_propagate(False)

###############################################################################
# 9- Interface graphique frame1_L_trait : 
###############################################################################
canevas0_L_trait=tkinter.Canvas(frame1_L_trait, width=1000, height=200, bg="white")
canevas0_L_trait.grid(row=1, column=1, columnspan=6)

ligne_position_0_L_trait=canevas0_L_trait.create_line(0,0,0,200, fill="white")

lambda_texte_L_trait = tkinter.Label(frame1_L_trait, text="Lambda = " + str(format(l_L_trait, "4.1f") + " nm"), bg=couleur_interface)
lambda_texte_L_trait.grid(row=2, column=5,columnspan=2, sticky=tkinter.E)

text1_L_trait=tkinter.Label(frame1_L_trait, text="Première borne inf. en nm", bg=couleur_interface)
text2_L_trait=tkinter.Label(frame1_L_trait, text="Première borne sup. en nm", bg=couleur_interface)
text1_L_trait.grid(row=2, column=1, sticky=tkinter.W)
text2_L_trait.grid(row=2, column=3, sticky=tkinter.W)
variable_1_L_trait=tkinter.DoubleVar(value=tableau_bornes_L_trait[0])
variable_2_L_trait=tkinter.DoubleVar(value=tableau_bornes_L_trait[1])
entree1_L_trait=tkinter.Spinbox(frame1_L_trait, from_=198, to=1013, textvariable=variable_1_L_trait,
                                command=deplace_ligne0_1_L_trait, foreground="red")
entree2_L_trait=tkinter.Spinbox(frame1_L_trait, from_=198, to=1013, textvariable=variable_2_L_trait,
                                command=deplace_ligne0_2_L_trait, foreground="red")
entree1_L_trait.grid(row=2, column=2)
entree2_L_trait.grid(row=2, column=4)

text3_L_trait=tkinter.Label(frame1_L_trait, text="Filtre :", bg=couleur_interface)
text4_L_trait=tkinter.Label(frame1_L_trait, text="Taille :", bg=couleur_interface)
text5_L_trait = tkinter.Label(frame1_L_trait, text="Ordre :", bg=couleur_interface)
text5_2_L_trait = tkinter.Label(frame1_L_trait, text="Dérivée :", bg=couleur_interface)
text3_L_trait.grid(row=3, column=1, sticky=tkinter.W)
text4_L_trait.grid(row=3, column=3, sticky=tkinter.W)
text5_L_trait.grid(row=4, column=3, sticky=tkinter.W)
text5_2_L_trait.grid(row=4, column=5, sticky=tkinter.W)
type_filtre_L_trait=tkinter.StringVar(value="Savitzky-Golay")
taille_filtre_L_trait=tkinter.IntVar(value=5)
ordre_filtre_L_trait=tkinter.IntVar(value=2)
derivee_filtre_L_trait=tkinter.IntVar(value=0)
#entree3_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_filtre_L_trait,
#                                     values=["Aucun", "Savitzky-Golay", "Median", "Passe-bas"])
entree3_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_filtre_L_trait,
                                     values=["Aucun", "Savitzky-Golay", "Median"])
entree4_L_trait=tkinter.Spinbox(frame1_L_trait, from_=3, to=199, increment=2, textvariable = taille_filtre_L_trait)
entree5_L_trait=tkinter.Spinbox(frame1_L_trait, from_=2, to=9, textvariable = ordre_filtre_L_trait)
entree5_2_L_trait=tkinter.Spinbox(frame1_L_trait, from_=0, to=2, textvariable = derivee_filtre_L_trait)
entree3_L_trait.grid(row=3, column=2, columnspan=1)
entree4_L_trait.grid(row=3, column=4)
entree5_L_trait.grid(row=4, column=4)
entree5_2_L_trait.grid(row=4, column=6)

text6_L_trait=tkinter.Label(frame1_L_trait, text="Fond :", bg=couleur_interface)
text7_L_trait=tkinter.Label(frame1_L_trait, text="Itérations :", bg=couleur_interface)
text8_L_trait=tkinter.Label(frame1_L_trait, text="LLS :", bg=couleur_interface)
text6_L_trait.grid(row=5, column=1, sticky=tkinter.W)
text7_L_trait.grid(row=5, column=3, sticky=tkinter.W)
text8_L_trait.grid(row=5, column=5, sticky=tkinter.W)
type_fond_L_trait=tkinter.StringVar(value="SNIP")
param1_fond_L_trait=tkinter.IntVar(value=20)
param2_fond_L_trait=tkinter.IntVar(value=10)
param3_fond_L_trait=tkinter.BooleanVar(value=False)
#entree6_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_fond_L_trait,
#                                     values=["Aucun", "Rolling ball", "SNIP", "Top-hat", "Peak filling"])
entree6_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_fond_L_trait,
                                     values=["Aucun", "Rolling ball", "SNIP"])
entree7_L_trait=tkinter.Spinbox(frame1_L_trait, from_=3, to=100, textvariable=param1_fond_L_trait)
entree8_L_trait=tkinter.Spinbox(frame1_L_trait, from_=1, to=100, textvariable=param2_fond_L_trait)
entree8bis_L_trait=tkinter.Checkbutton(frame1_L_trait, text="LLS", variable=param3_fond_L_trait, bg=couleur_interface)
entree6_L_trait.grid(row=5, column=2, columnspan=1)
entree7_L_trait.grid(row=5, column=4)
entree8_L_trait.grid(row=5, column=6)
entree8_L_trait.grid_remove()
entree8bis_L_trait.grid(row=5, column=6)

frame1_1_L_trait=tkinter.Frame(frame1_L_trait, bg=couleur_interface)
frame1_1_L_trait.grid(row=1, column=7, rowspan=4, sticky=tkinter.N+tkinter.S)

text_zoom_L_trait=tkinter.Label(frame1_1_L_trait, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_trait.grid(row=1, column=1, sticky=tkinter.N)
variable_zoom_inf_L_trait=tkinter.DoubleVar(value=198)
variable_zoom_sup_L_trait=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_trait=tkinter.Spinbox(frame1_1_L_trait, from_=198, to=1013, increment=5,
                                        textvariable=variable_zoom_inf_L_trait,
                                        command=change_zoom_inf_L_trait, width=9)
entree_zoom_sup_L_trait=tkinter.Spinbox(frame1_1_L_trait, from_=198, to=1013, increment=5,
                                        textvariable=variable_zoom_sup_L_trait,
                                        command=change_zoom_sup_L_trait, width=9)
entree_zoom_inf_L_trait.grid(row=2, column=1, sticky=tkinter.N)
entree_zoom_sup_L_trait.grid(row=3, column=1, sticky=tkinter.N)

#type_fichier_L_trait=tkinter.StringVar(value=".asc")
bouton_rep_L_trait=tkinter.Button(frame1_1_L_trait, text="Fichier",
                                  command=choix_fichier_L_trait, width=9, bg=couleur_interface)
bouton_visualisation_L_trait=tkinter.Button(frame1_1_L_trait, text="Visualisation",
                                            command = visualisation_L_trait, state="disable", width=9, bg=couleur_interface)
bouton_rep_L_trait.grid(row=4, column=1, sticky=tkinter.N)
bouton_visualisation_L_trait.grid(row=5, column=1, sticky=tkinter.N)

image_classification=tkinter.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")
#bouton_classification_L_trait=tkinter.Button(frame1_1_L_trait, text="classification",
#                                             command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_trait=tkinter.Button(frame1_1_L_trait, image=image_classification,
                                             command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_trait.grid(row=8, column=1, sticky=tkinter.S)

###############################################################################
# 10- Interface graphique frame2_L_trait
###############################################################################
canevas1_L_trait=tkinter.Canvas(frame2_L_trait, width=1000, height=200, bg="white")
canevas1_L_trait.grid(row=1, column=1, columnspan=2)

ligne_position_1_L_trait=canevas1_L_trait.create_line(0,0,0,200, fill="white")

frame2_1_L_trait=tkinter.Frame(frame2_L_trait)
frame2_1_L_trait.grid(row=1, column=5, rowspan=3, sticky=tkinter.N)

flag_tous_fichiers_init_L_trait=False
flag_tous_fichiers_L_trait=tkinter.BooleanVar(value=flag_tous_fichiers_init_L_trait)
coche_tous_fichiers_L_trait=tkinter.Checkbutton(frame2_1_L_trait, text="Appliquer sur\ntous les fichiers\ndu répertoire",
                                            variable=flag_tous_fichiers_L_trait, bg=couleur_interface)
coche_tous_fichiers_L_trait.grid(row=1, column=1)

bouton_execute_L_trait=tkinter.Button(frame2_1_L_trait, text="Executer", state="disable",
                                      command = execute_L_trait , width=9, bg=couleur_interface)
bouton_execute_L_trait.grid(row=2, column=1)

text_spectre_L_trait=tkinter.Label(frame2_1_L_trait, text="Spectre : ", bg=couleur_interface)
text_spectre_L_trait.grid(row=3, column=1, sticky=tkinter.N)
numero_spectre_L_trait=tkinter.IntVar(value=1)
entree_spectre_L_trait=tkinter.Spinbox(frame2_1_L_trait, from_=1, to=50, textvariable=numero_spectre_L_trait,
                                       command=lit_affiche_spectre_numero_L_trait, width=9)
entree_spectre_L_trait.grid(row=4, column=1, sticky=tkinter.N)

###############################################################################
# 12- Interface graphique : gestion de évènements
###############################################################################
entree_zoom_inf_L_trait.bind("<Return>", change_zoom_inf_return_L_trait)
entree_zoom_sup_L_trait.bind("<Return>", change_zoom_sup_return_L_trait)
entree_zoom_inf_L_trait.bind("<KP_Enter>", change_zoom_inf_return_L_trait)
entree_zoom_sup_L_trait.bind("<KP_Enter>", change_zoom_sup_return_L_trait)
entree_zoom_inf_L_trait.bind("<Tab>", change_zoom_inf_return_L_trait)
entree_zoom_sup_L_trait.bind("<Tab>", change_zoom_sup_return_L_trait)
#entree_zoom_inf_L_trait.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_trait)
#entree_zoom_sup_L_trait.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_trait)

canevas0_L_trait.bind("<ButtonRelease-1>", affiche_lambda_L_trait)
canevas0_L_trait.bind("<Motion>", affiche_position_souris_L_trait)
canevas0_L_trait.bind("<B1-Motion>", affiche_position_souris_motion_L_trait)
canevas0_L_trait.bind("<Button-3>", zoom_clic_L_trait)
canevas0_L_trait.bind("<B3-Motion>", zoom_drag_and_drop_L_trait)
canevas0_L_trait.bind("<ButtonRelease-3>", zoom_clic_release_L_trait)

canevas1_L_trait.bind("<ButtonRelease-1>", affiche_lambda_L_trait)
canevas1_L_trait.bind("<Motion>", affiche_position_souris_L_trait)
canevas1_L_trait.bind("<B1-Motion>", affiche_position_souris_motion_L_trait)
canevas1_L_trait.bind("<Button-3>", zoom_clic_L_trait)
canevas1_L_trait.bind("<B3-Motion>", zoom_drag_and_drop_L_trait)
canevas1_L_trait.bind("<ButtonRelease-3>", zoom_clic_release_L_trait)

entree1_L_trait.bind("<Return>", deplace_ligne0_1_return_L_trait)
entree2_L_trait.bind("<Return>", deplace_ligne0_2_return_L_trait)
entree1_L_trait.bind("<KP_Enter>", deplace_ligne0_1_return_L_trait)
entree2_L_trait.bind("<KP_Enter>", deplace_ligne0_2_return_L_trait)
entree1_L_trait.bind("<Tab>", deplace_ligne0_1_return_L_trait)
entree2_L_trait.bind("<Tab>", deplace_ligne0_2_return_L_trait)
#entree1_L_trait.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_1_return_L_trait)
#entree2_L_trait.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_2_return_L_trait)

entree3_L_trait.bind("<<ComboboxSelected>>", change_options_filtre_L_trait)
entree3_L_trait.bind("<Return>", change_options_filtre_L_trait)
entree3_L_trait.bind("<KP_Enter>", change_options_filtre_L_trait)
entree3_L_trait.bind("<Tab>", change_options_filtre_L_trait)

entree6_L_trait.bind("<<ComboboxSelected>>", change_options_fond_L_trait)
entree6_L_trait.bind("<Return>", change_options_fond_L_trait)
entree6_L_trait.bind("<KP_Enter>", change_options_fond_L_trait)
entree6_L_trait.bind("<Tab>", change_options_fond_L_trait)

entree_spectre_L_trait.bind("<Return>", lit_affiche_spectre_numero_event_L_trait)
entree_spectre_L_trait.bind("<Tab>", lit_affiche_spectre_numero_event_L_trait)
entree_spectre_L_trait.bind("<KP_Enter>", lit_affiche_spectre_numero_event_L_trait)





###############################################################################
###############################################################################
# Interface graphique LIBStick_IHM_extraction : onglet 2
###############################################################################
###############################################################################
def __________IHM_extraction__________():pass
###############################################################################
# 8- Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###############################################################################
frame1_L_ext=tkinter.Frame(onglet2,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame2_L_ext=tkinter.Frame(onglet2,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame3_L_ext=tkinter.Frame(onglet2,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)

frame1_L_ext.grid(row=10, column=10, sticky = "nsew")
frame2_L_ext.grid(row=20, column=10, sticky = "nsew")
frame3_L_ext.grid(row=30, column=10, sticky = "nsew")
#frame1_L_ext.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame2_L_ext.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame3_L_ext.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# 9- Interface graphique frame1_L_ext : création selection répertoire, affiche spectre et bouton executer
###############################################################################
canevas0_L_ext=tkinter.Canvas(frame1_L_ext, width=1000, height=200, bg="white")
canevas0_L_ext.grid(row=1, column=1, columnspan=6)

ligne_position_L_ext=canevas0_L_ext.create_line(0,0,0,200, fill="white")

lambda_texte_L_ext = tkinter.Label(frame1_L_ext, text="Lambda = " + str(format(l_L_ext, "4.1f") + " nm"), bg=couleur_interface)
lambda_texte_L_ext.grid(row=2, column=5)

text1_L_ext=tkinter.Label(frame1_L_ext, text="Première borne inf. en nm", bg=couleur_interface)
text2_L_ext=tkinter.Label(frame1_L_ext, text="Première borne sup. en nm", bg=couleur_interface)
text3_L_ext=tkinter.Label(frame1_L_ext, text="Seconde borne inf. en nm", bg=couleur_interface)
text4_L_ext=tkinter.Label(frame1_L_ext, text="Seconde borne sup. en nm", bg=couleur_interface)
text1_L_ext.grid(row=2, column=1)
text2_L_ext.grid(row=2, column=3)
text3_L_ext.grid(row=3, column=1)
text4_L_ext.grid(row=3, column=3)

variable_1_L_ext=tkinter.DoubleVar(value=tableau_bornes_L_ext[0,0])
variable_2_L_ext=tkinter.DoubleVar(value=tableau_bornes_L_ext[0,1])
variable_3_L_ext=tkinter.DoubleVar( value=tableau_bornes_L_ext[1,0])
variable_4_L_ext=tkinter.DoubleVar(value=tableau_bornes_L_ext[1,1])
entree1_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_1_L_ext, command=deplace_ligne0_1_L_ext, foreground="red")
entree2_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_2_L_ext, command=deplace_ligne0_2_L_ext, foreground="red")
entree3_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_3_L_ext, command=deplace_ligne0_3_L_ext, foreground="blue")
entree4_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_4_L_ext, command=deplace_ligne0_4_L_ext, foreground="blue")
entree1_L_ext.grid(row=2, column=2)
entree2_L_ext.grid(row=2, column=4)
entree3_L_ext.grid(row=3, column=2)
entree4_L_ext.grid(row=3, column=4)

flag_zone2_L_ext=tkinter.IntVar(value=flag_zone2_init_L_ext)
coche_zone2_L_ext=tkinter.Checkbutton(frame1_L_ext, text="Seconde extraction ?", variable=flag_zone2_L_ext, command=change_flag_zone2_L_ext, bg=couleur_interface)
coche_zone2_L_ext.grid(row=3, column=5)

bouton_reset_L_ext=tkinter.Button(frame1_L_ext, text="Reset", command=reset_tableau_L_ext, width=9, bg=couleur_interface)
bouton_reset_L_ext.grid(row=2, column=6, rowspan=2)

frame1_1_L_ext=tkinter.Frame(frame1_L_ext, bg=couleur_interface)
frame1_1_L_ext.grid(row=1, column=7, rowspan=3, sticky=tkinter.N)

text_zoom_L_ext=tkinter.Label(frame1_1_L_ext, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_ext.grid(row=1, column=1)
variable_zoom_inf_L_ext=tkinter.DoubleVar(value=198)
variable_zoom_sup_L_ext=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_ext=tkinter.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_zoom_inf_L_ext,
                                      command=change_zoom_inf_L_ext, width=9)
entree_zoom_sup_L_ext=tkinter.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_zoom_sup_L_ext,
                                      command=change_zoom_sup_L_ext, width=9)
entree_zoom_inf_L_ext.grid(row=2, column=1)
entree_zoom_sup_L_ext.grid(row=3, column=1)

type_fichier_L_ext=tkinter.StringVar(value=".asc")
#bouton_rep_L_ext=tkinter.Button(frame1_1_L_ext, text="Repertoire\nde travail" ,command=choix_rep_L_ext, width=9, bg=couleur_interface)
bouton_rep_L_ext=tkinter.Button(frame1_1_L_ext, text="Fichier" ,command=choix_fichier_L_ext, width=9, bg=couleur_interface)
bouton_execute_L_ext=tkinter.Button(frame1_1_L_ext, text="Exécute", command=execute_scripts_L_ext, state="disable", width=9, bg=couleur_interface)
bouton_rep_L_ext.grid(row=4, column=1)
bouton_execute_L_ext.grid(row=5, column=1)

flag_2D_L_ext=tkinter.IntVar(value=flag_2D_init_L_ext)
#coche_2D_L_ext=tkinter.Checkbutton(frame1_1_L_ext, text="Sortie 2D", variable=flag_2D_L_ext, command=change_flag_2D_L_ext, bg=couleur_interface)
coche_2D_L_ext=tkinter.Checkbutton(frame1_1_L_ext, text="Sortie 2D", variable=flag_2D_L_ext, bg=couleur_interface)
coche_2D_L_ext.grid(row=6, column=1)

flag_3D_L_ext=tkinter.IntVar(value=flag_3D_init_L_ext)
#coche_3D_L_ext=tkinter.Checkbutton(frame1_1_L_ext, text="Sortie 3D", variable=flag_3D_L_ext, command=change_flag_3D_L_ext, bg=couleur_interface)
coche_3D_L_ext=tkinter.Checkbutton(frame1_1_L_ext, text="Sortie 3D", variable=flag_3D_L_ext, bg=couleur_interface)
coche_3D_L_ext.grid(row=7, column=1)

#image_classification=tkinter.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")
bouton_classification_L_ext=tkinter.Button(frame1_1_L_ext, image= image_classification, command=ouvre_fenetre_classification_L_ele)
#bouton_classification_L_ext=tkinter.Button(frame1_1_L_ext, text="classification", command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_ext.grid(row=8, column=1, sticky=tkinter.S)

###############################################################################
# Interface graphique frame2_L_ext : création visues des résultats et aide à la sélection
###############################################################################
canevas1_L_ext=tkinter.Canvas(frame2_L_ext, width=500, height=200, bg="white")
canevas2_L_ext=tkinter.Canvas(frame2_L_ext, width=500, height=200, bg="white")
canevas1_L_ext.grid(row=1, column=1, columnspan=4)
canevas2_L_ext.grid(row=1, column=5, columnspan=4)

text5_L_ext = tkinter.Label(frame2_L_ext, text="Position x (nm) : ", bg=couleur_interface)
text6_L_ext = tkinter.Label(frame2_L_ext, text="Position y (n° de spectre) : ", bg=couleur_interface)
text7_L_ext = tkinter.Label(frame2_L_ext, text="Position x (nm) : ", bg=couleur_interface)
text8_L_ext = tkinter.Label(frame2_L_ext, text="Position y (n° de spectre) : ", bg=couleur_interface)
text5_L_ext.grid(row=2, column=1, sticky=tkinter.E)
text6_L_ext.grid(row=2, column=3, sticky=tkinter.E)
text7_L_ext.grid(row=2, column=5, sticky=tkinter.E)
text8_L_ext.grid(row=2, column=7, sticky=tkinter.E)

variable_5_L_ext=tkinter.DoubleVar(value=0)
variable_6_L_ext=tkinter.IntVar(value=0)
variable_7_L_ext=tkinter.DoubleVar(value=0)
entree5_L_ext=tkinter.Spinbox(frame2_L_ext, from_=198, to=1013, textvariable=variable_5_L_ext, command=vars_5_6_to_coord1_L_ext, increment=0.5, width=9, foreground="red")
entree6_L_ext=tkinter.Spinbox(frame2_L_ext, from_=1, to=200, textvariable=variable_6_L_ext, command=vars_5_6_to_coord1_L_ext, width=9, foreground="red")
entree7_L_ext=tkinter.Spinbox(frame2_L_ext, from_=198, to=1013, textvariable=variable_7_L_ext, command=vars_7_8_to_coord2_L_ext, increment=0.5, width=9, foreground="blue")
entree8_L_ext=tkinter.Spinbox(frame2_L_ext, from_=1, to=200, textvariable=variable_6_L_ext, command=vars_7_8_to_coord2_L_ext, width=9, foreground="blue")
entree5_L_ext.grid(row=2, column=2, sticky=tkinter.W)
entree6_L_ext.grid(row=2, column=4, sticky=tkinter.W)
entree7_L_ext.grid(row=2, column=6, sticky=tkinter.W)
entree8_L_ext.grid(row=2, column=8, sticky=tkinter.W)

frame2_1_L_ext=tkinter.Frame(frame2_L_ext)
frame2_1_L_ext.grid(row=1, column=9, rowspan=3, sticky=tkinter.N)

flag_image_brute_L_ext=tkinter.BooleanVar(value=flag_image_brute_init_L_ext)
coche_image_brute_L_ext=tkinter.Checkbutton(frame2_1_L_ext, text="Image brute\nspectres non\nnormalisés",
                                            variable=flag_image_brute_L_ext, command=change_flag_image_brute_L_ext, bg=couleur_interface)
coche_image_brute_L_ext.grid(row=1, column=1)

flag_spectre_inclus_moyenne_L_ext=tkinter.BooleanVar(value=True)
coche_spectre_inclus_moyenne_L_ext=tkinter.Checkbutton(frame2_1_L_ext, text="Spectre inclus\ndans spectre\nmoyen",
                                                       variable=flag_spectre_inclus_moyenne_L_ext, command=change_bool_spectre_L_ext, bg=couleur_interface)
coche_spectre_inclus_moyenne_L_ext.grid(row=2, column=1)

ligne1_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
ligne1_hori_L_ext=canevas1_L_ext.create_line(0,y_L_ext,500,y_L_ext, fill="white")
ligne2_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
ligne2_hori_L_ext=canevas1_L_ext.create_line(0,y_L_ext,500,y_L_ext, fill="white")

affiche_lignes_spectre_L_ext()

###############################################################################
# 11- Interface graphique frame3_L_ext : création selection des spectres à moyenner
###############################################################################
canevas3_L_ext=tkinter.Canvas(frame3_L_ext, width=500, height=200, bg="white")
canevas4_L_ext=tkinter.Canvas(frame3_L_ext, width=500, height=200, bg="white")
canevas3_L_ext.grid(row=3, column=1, columnspan=2)
canevas4_L_ext.grid(row=3, column=3, columnspan=2)

frame3_1_L_ext=tkinter.Frame(frame3_L_ext, bg=couleur_interface)
frame3_1_L_ext.grid(row=1, column=5, rowspan=4, sticky=tkinter.N)

text9_L_ext=tkinter.Label(frame3_1_L_ext, text="Du spectre n° :", bg=couleur_interface)
text10_L_ext=tkinter.Label(frame3_1_L_ext, text="Au spectre n° :", bg=couleur_interface)
text9_L_ext.grid(row=1, column=1)
text10_L_ext.grid(row=3, column=1)

variable_9_L_ext=tkinter.IntVar(value=0)
variable_9_avant_L_ext=tkinter.IntVar(value=1)
variable_10_L_ext=tkinter.IntVar(value=0)
variable_10_avant_L_ext=tkinter.IntVar(value=0)
entree9_L_ext=tkinter.Spinbox(frame3_1_L_ext,from_=1, to=200, textvariable=variable_9_L_ext, command=retro_action_entree10_L_ext, width=9)
entree10_L_ext=tkinter.Spinbox(frame3_1_L_ext,from_=1, to=200, textvariable=variable_10_L_ext, command=retro_action_entree9_L_ext, width=9)
entree9_L_ext.grid(row=2, column=1)
entree10_L_ext.grid(row=4, column=1)

bouton_extraction_L_ext=tkinter.Button(frame3_1_L_ext, text="Extraction", state="disable", command=creation_spectre_moyen_L_ext, width=9, bg=couleur_interface)
bouton_extraction_L_ext.grid(row=5, column=1)

flag_spectres_normalises_moyenne_L_ext=tkinter.BooleanVar(value=True)
coche_spectres_normalises_moyenne_L_ext=tkinter.Checkbutton(frame3_1_L_ext, text="Moyenne des\nspectres \nnormalisés",
                                                       variable=flag_spectres_normalises_moyenne_L_ext, bg=couleur_interface)
coche_spectres_normalises_moyenne_L_ext.grid(row=6, column=1)

###############################################################################
# 12- Interface graphique : gestion de évènements
###############################################################################
canevas0_L_ext.bind("<ButtonRelease-1>", affiche_lambda_L_ext)
canevas0_L_ext.bind("<Motion>", affiche_position_souris_L_ext)
canevas0_L_ext.bind("<B1-Motion>", affiche_position_souris_motion_L_ext)
canevas0_L_ext.bind("<Button-3>", zoom_clic_L_ext)
canevas0_L_ext.bind("<B3-Motion>", zoom_drag_and_drop_L_ext)
canevas0_L_ext.bind("<ButtonRelease-3>", zoom_clic_release_L_ext)

entree_zoom_inf_L_ext.bind("<Return>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<Return>", change_zoom_sup_return_L_ext)
entree_zoom_inf_L_ext.bind("<KP_Enter>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<KP_Enter>", change_zoom_sup_return_L_ext)
entree_zoom_inf_L_ext.bind("<Tab>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<Tab>", change_zoom_sup_return_L_ext)
#entree_zoom_inf_L_ext.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_ext)
#entree_zoom_sup_L_ext.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_ext)

canevas1_L_ext.bind("<ButtonRelease-1>", coordonnees1_L_ext)
canevas2_L_ext.bind("<ButtonRelease-1>", coordonnees2_L_ext)

entree1_L_ext.bind("<Return>", deplace_ligne0_1_return_L_ext)
entree2_L_ext.bind("<Return>", deplace_ligne0_2_return_L_ext)
entree3_L_ext.bind("<Return>", deplace_ligne0_3_return_L_ext)
entree4_L_ext.bind("<Return>", deplace_ligne0_4_return_L_ext)
entree1_L_ext.bind("<KP_Enter>", deplace_ligne0_1_return_L_ext)
entree2_L_ext.bind("<KP_Enter>", deplace_ligne0_2_return_L_ext)
entree3_L_ext.bind("<KP_Enter>", deplace_ligne0_3_return_L_ext)
entree4_L_ext.bind("<KP_Enter>", deplace_ligne0_4_return_L_ext)
entree1_L_ext.bind("<Tab>", deplace_ligne0_1_return_L_ext)
entree2_L_ext.bind("<Tab>", deplace_ligne0_2_return_L_ext)
entree3_L_ext.bind("<Tab>", deplace_ligne0_3_return_L_ext)
entree4_L_ext.bind("<Tab>", deplace_ligne0_4_return_L_ext)
#entree1_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_1_return_L_ext)
#entree2_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_2_return_L_ext)
#entree3_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_3_return_L_ext)
#entree4_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_4_return_L_ext)


entree5_L_ext.bind("<Return>", vars_5_6_to_coord1_return_L_ext)
entree6_L_ext.bind("<Return>", vars_5_6_to_coord1_return_L_ext)
entree7_L_ext.bind("<Return>", vars_7_8_to_coord2_return_L_ext)
entree8_L_ext.bind("<Return>", vars_7_8_to_coord2_return_L_ext)
entree5_L_ext.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_ext)
entree6_L_ext.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_ext)
entree7_L_ext.bind("<KP_Enter>", vars_7_8_to_coord2_return_L_ext)
entree8_L_ext.bind("<KP_Enter>", vars_7_8_to_coord2_return_L_ext)
entree5_L_ext.bind("<Tab>", vars_5_6_to_coord1_return_L_ext)
entree6_L_ext.bind("<Tab>", vars_5_6_to_coord1_return_L_ext)
entree7_L_ext.bind("<Tab>", vars_7_8_to_coord2_return_L_ext)
entree8_L_ext.bind("<Tab>", vars_7_8_to_coord2_return_L_ext)

entree9_L_ext.bind("<Return>", change_entree9_L_ext)
entree10_L_ext.bind("<Return>", change_entree10_L_ext)
entree9_L_ext.bind("<KP_Enter>", change_entree9_L_ext)
entree10_L_ext.bind("<KP_Enter>", change_entree10_L_ext)
entree9_L_ext.bind("<Tab>", change_entree9_L_ext)
entree10_L_ext.bind("<Tab>", change_entree10_L_ext)
#entree9_L_ext.bind("<Shift-ISO_Left_Tab>", change_entree9_L_ext)
#entree10_L_ext.bind("<Shift-ISO_Left_Tab>", change_entree10_L_ext)





###############################################################################
###############################################################################
# Interface graphique LIBStick_IHM_compare : onglet 3
###############################################################################
###############################################################################
def __________IHM_compare__________():pass
###############################################################################
# Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###############################################################################
frame1_L_comp=tkinter.Frame(onglet3,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame2_L_comp=tkinter.Frame(onglet3,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame3_L_comp=tkinter.Frame(onglet3,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)

frame1_L_comp.grid(row=10, column=10, sticky = "nsew")
frame2_L_comp.grid(row=20, column=10, sticky = "nsew")
frame3_L_comp.grid(row=30, column=10, sticky = "nsew")
#frame1_L_comp.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame2_L_comp.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame3_L_comp.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# Interface graphique frame1_L_comp : création selection répertoire, affiche spectre et bouton executer
###############################################################################
canevas0_L_comp=tkinter.Canvas(frame1_L_comp, width=1000, height=200, bg="white")
canevas0_L_comp.grid(row=1, column=1, columnspan=6)

ligne_position_L_comp=canevas0_L_comp.create_line(0,0,0,200, fill="white")

lambda_texte_L_comp = tkinter.Label(frame1_L_comp, text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm"), bg=couleur_interface)
lambda_texte_L_comp.grid(row=2, column=5)

text1_L_comp=tkinter.Label(frame1_L_comp, text="Numérateur borne inf. en nm", bg=couleur_interface)
text2_L_comp=tkinter.Label(frame1_L_comp, text="Numérateur borne sup. en nm", bg=couleur_interface)
text3_L_comp=tkinter.Label(frame1_L_comp, text="Dénominateur borne inf. en nm", bg=couleur_interface)
text4_L_comp=tkinter.Label(frame1_L_comp, text="Dénominateur borne sup. en nm", bg=couleur_interface)
text1_L_comp.grid(row=2, column=1)
text2_L_comp.grid(row=2, column=3)
text3_L_comp.grid(row=3, column=1)
text4_L_comp.grid(row=3, column=3)

variable_1_L_comp=tkinter.DoubleVar(value=tableau_bornes_L_comp[0,0])
variable_2_L_comp=tkinter.DoubleVar(value=tableau_bornes_L_comp[0,1])
variable_3_L_comp=tkinter.DoubleVar( value=tableau_bornes_L_comp[1,0])
variable_4_L_comp=tkinter.DoubleVar(value=tableau_bornes_L_comp[1,1])
entree1_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_1_L_comp, command=deplace_ligne0_1_L_comp, foreground="red")
entree2_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_2_L_comp, command=deplace_ligne0_2_L_comp, foreground="red")
entree3_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5,textvariable=variable_3_L_comp, command=deplace_ligne0_3_L_comp, foreground="blue")
entree4_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5,textvariable=variable_4_L_comp, command=deplace_ligne0_4_L_comp, foreground="blue")
entree1_L_comp.grid(row=2, column=2)
entree2_L_comp.grid(row=2, column=4)
entree3_L_comp.grid(row=3, column=2)
entree4_L_comp.grid(row=3, column=4)

flag_denominateur_L_comp=tkinter.IntVar(value=flag_denominateur_init_L_comp)
coche_denominateur_L_comp=tkinter.Checkbutton(frame1_L_comp, text="Dénominateur ?", variable=flag_denominateur_L_comp,
                                              command=change_flag_denominateur_L_comp, bg=couleur_interface)
coche_denominateur_L_comp.grid(row=3, column=5)

bouton_reset_L_comp=tkinter.Button(frame1_L_comp, text="Reset", command=reset_tableau_L_comp, width=9, bg=couleur_interface)
bouton_reset_L_comp.grid(row=2, column=6, rowspan=2)

frame1_1_L_comp=tkinter.Frame(frame1_L_comp, bg=couleur_interface)
frame1_1_L_comp.grid(row=1, column=7, rowspan=3, sticky=tkinter.N)

text_zoom_L_comp=tkinter.Label(frame1_1_L_comp, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_comp.grid(row=1, column=1)
variable_zoom_inf_L_comp=tkinter.DoubleVar(value=198)
variable_zoom_sup_L_comp=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_comp=tkinter.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_inf_L_comp,
                                       command=change_zoom_inf_L_comp, width=9)
entree_zoom_sup_L_comp=tkinter.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_sup_L_comp,
                                       command=change_zoom_sup_L_comp, width=9)
entree_zoom_inf_L_comp.grid(row=2, column=1)
entree_zoom_sup_L_comp.grid(row=3, column=1)

type_fichier_L_comp=tkinter.StringVar(value=".mean")
#bouton_rep_L_comp=tkinter.Button(frame1_1_L_comp, text="Repertoire\nde travail" ,command=choix_rep_L_comp, width=9, bg=couleur_interface)
bouton_rep_L_comp=tkinter.Button(frame1_1_L_comp, text="Fichier" ,command=choix_fichier_L_comp, width=9, bg=couleur_interface)
bouton_execute_L_comp=tkinter.Button(frame1_1_L_comp, text="Exécute", command=execute_scripts_L_comp, state="disable", width=9, bg=couleur_interface)
bouton_rep_L_comp.grid(row=4, column=1)
bouton_execute_L_comp.grid(row=5, column=1)

flag_2D_L_comp=tkinter.IntVar(value=flag_2D_init_L_comp)
coche_2D_L_comp=tkinter.Checkbutton(frame1_1_L_comp, text="Sortie 2D", variable=flag_2D_L_comp, bg=couleur_interface)
#coche_2D_L_comp=tkinter.Checkbutton(frame1_1_L_comp, text="Sortie 2D", variable=flag_2D_L_comp, command=change_flag_2D_L_comp, bg=couleur_interface)
coche_2D_L_comp.grid(row=6, column=1)

flag_3D_L_comp=tkinter.IntVar(value=flag_3D_init_L_comp)
coche_3D_L_comp=tkinter.Checkbutton(frame1_1_L_comp, text="Sortie 3D", variable=flag_3D_L_comp, bg=couleur_interface)
#coche_3D_L_comp=tkinter.Checkbutton(frame1_1_L_comp, text="Sortie 3D", variable=flag_3D_L_comp, command=change_flag_3D_L_comp, bg=couleur_interface)
coche_3D_L_comp.grid(row=7, column=1)

#image_classification=tkinter.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")
#bouton_classification_L_comp=tkinter.Button(frame1_1_L_comp, text="classification", command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_comp=tkinter.Button(frame1_1_L_comp, image= image_classification, command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_comp.grid(row=8, column=1, sticky=tkinter.S)

###############################################################################
# Interface graphique frame2_L_comp : affichage des spectres classés
###############################################################################
canevas1_L_comp=tkinter.Canvas(frame2_L_comp, width=1000, height=200, bg="white")
canevas1_L_comp.grid(row=1, column=1, columnspan=4)

#text5_L_comp = tkinter.Label(frame2_L_comp, text="Position x (nm) : ", bg=couleur_interface)
#text6_L_comp = tkinter.Label(frame2_L_comp, text="Position y (n° de spectre) : ", bg=couleur_interface)
#text5_L_comp.grid(row=2, column=1, sticky=tkinter.E)
#text6_L_comp.grid(row=2, column=3, sticky=tkinter.E)

#variable_5_L_comp=tkinter.DoubleVar(value=0)
#variable_6_L_comp=tkinter.IntVar(value=0)
#entree5_L_comp=tkinter.Spinbox(frame2_L_comp, from_=198, to=1013, textvariable=variable_5_L_comp, command=vars_5_6_to_coord1_L_comp, increment=0.5, width=9)
#entree6_L_comp=tkinter.Spinbox(frame2_L_comp, from_=1, to=100, textvariable=variable_6_L_comp, command=vars_5_6_to_coord1_L_comp, width=9)
#entree5_L_comp.grid(row=2, column=2, sticky=tkinter.W)
#entree6_L_comp.grid(row=2, column=4, sticky=tkinter.W)

frame2_1_L_comp=tkinter.Frame(frame2_L_comp)
frame2_1_L_comp.grid(row=1, column=5, rowspan=3, sticky=tkinter.N)

#text7_L_comp=tkinter.Label(frame2_1_L_comp, text="Type de\nfichiers à\ncomparer :")
#text7_L_comp.grid(row=1, column=1)

flag_traitement_L_comp=tkinter.IntVar(value=flag_traitement_init_L_comp)
coche_traitement_L_comp=tkinter.Checkbutton(frame2_1_L_comp, text="Normalisation\ndes spectres", variable=flag_traitement_L_comp, bg=couleur_interface)
coche_traitement_L_comp.grid(row=1, column=1)

#type_traitement_L_comp=tkinter.StringVar(value="Echantillons différents")
#type_traitement_combobox_L_comp=tkinter.ttk.Combobox(frame2_1_L_comp, textvariable=type_traitement_L_comp, width=10, values=["Echantillons différents", "Même échantillon"])
#type_traitement_combobox_L_comp.grid(row=2, column=1)

#text8_L_comp=tkinter.Label(frame2_1_L_comp, text="\nEchantillons différents :\nspectres moyens\nd'échantillons\ndifférents\n\nMême échantillon :\nspectres du même\néchantillon")
#text8_L_comp.grid(row=3, column=1)

flag_stat_L_comp=tkinter.IntVar(value=flag_stat_init_L_comp)
coche_stat_L_comp=tkinter.Checkbutton(frame2_1_L_comp, text="Statistiques", variable=flag_stat_L_comp, bg=couleur_interface)
coche_stat_L_comp.grid(row=2, column=1)

ligne1_vert_L_comp=canevas1_L_comp.create_line(x1_L_comp,0,x1_L_comp,200, fill="white")
ligne1_hori_L_comp=canevas1_L_comp.create_line(0,y1_L_comp,500,y1_L_comp, fill="white")

text5_L_comp = tkinter.Label(frame2_1_L_comp, text="\nPosition x (nm) : ", bg=couleur_interface)
text6_L_comp = tkinter.Label(frame2_1_L_comp, text="Position y \n(n° de spectre) : ", bg=couleur_interface)
text5_L_comp.grid(row=4, column=1)
text6_L_comp.grid(row=6, column=1)

variable_5_L_comp=tkinter.DoubleVar(value=0)
variable_6_L_comp=tkinter.IntVar(value=0)
entree5_L_comp=tkinter.Spinbox(frame2_1_L_comp, from_=198, to=1013, textvariable=variable_5_L_comp, command=vars_5_6_to_coord1_L_comp, increment=0.5, width=9)
entree6_L_comp=tkinter.Spinbox(frame2_1_L_comp, from_=1, to=100, textvariable=variable_6_L_comp, command=vars_5_6_to_coord1_L_comp, width=9)
entree5_L_comp.grid(row=5, column=1)
entree6_L_comp.grid(row=7, column=1)

affiche_lignes_spectre_L_comp()

###############################################################################
# 11- Interface graphique frame3_L_comp : affichage des résultats sous forme de TreeView
###############################################################################
tree_resultats_L_comp=tkinter.ttk.Treeview(frame3_L_comp, columns=(1,2,3), height = 10 ,show = "headings")
tree_resultats_L_comp.column(1, width=200)
tree_resultats_L_comp.column(2, width=600)
tree_resultats_L_comp.column(3, width=200)
tree_resultats_L_comp.heading(1, text="n°")
tree_resultats_L_comp.heading(2, text="Nom du spectre")
tree_resultats_L_comp.heading(3, text="Rapport zone1/zone2")
tree_resultats_L_comp.grid(row=1, column=1, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
scroll_tree_resultat_L_comp=tkinter.ttk.Scrollbar(frame3_L_comp, orient=tkinter.VERTICAL, command=tree_resultats_L_comp.yview)
scroll_tree_resultat_L_comp.grid(row=1, column=2, sticky=tkinter.N+tkinter.S)
tree_resultats_L_comp.configure(yscrollcommand=scroll_tree_resultat_L_comp.set)

texte_statistiques_L_comp=tkinter.Message(frame3_L_comp, bg=couleur_interface)
#texte_statistiques_L_comp.grid(row=1, column=3, sticky=tkinter.N)

###############################################################################
# Interface graphique : gestion de évènements
###############################################################################
canevas0_L_comp.bind("<ButtonRelease-1>", affiche_lambda_L_comp)
canevas0_L_comp.bind("<Motion>", affiche_position_souris_L_comp)
canevas0_L_comp.bind("<B1-Motion>", affiche_position_souris_motion_L_comp)
canevas0_L_comp.bind("<Button-3>", zoom_clic_L_comp)
canevas0_L_comp.bind("<B3-Motion>", zoom_drag_and_drop_L_comp)
canevas0_L_comp.bind("<ButtonRelease-3>", zoom_clic_release_L_comp)

entree_zoom_inf_L_comp.bind("<Return>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<Return>", change_zoom_sup_return_L_comp)
entree_zoom_inf_L_comp.bind("<KP_Enter>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<KP_Enter>", change_zoom_sup_return_L_comp)
entree_zoom_inf_L_comp.bind("<Tab>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<Tab>", change_zoom_sup_return_L_comp)
#entree_zoom_inf_L_comp.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_comp)
#entree_zoom_sup_L_comp.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_comp)

canevas1_L_comp.bind("<ButtonRelease-1>", coordonnees1_L_comp)

entree1_L_comp.bind("<Return>", deplace_ligne0_1_return_L_comp)
entree2_L_comp.bind("<Return>", deplace_ligne0_2_return_L_comp)
entree3_L_comp.bind("<Return>", deplace_ligne0_3_return_L_comp)
entree4_L_comp.bind("<Return>", deplace_ligne0_4_return_L_comp)
entree1_L_comp.bind("<KP_Enter>", deplace_ligne0_1_return_L_comp)
entree2_L_comp.bind("<KP_Enter>", deplace_ligne0_2_return_L_comp)
entree3_L_comp.bind("<KP_Enter>", deplace_ligne0_3_return_L_comp)
entree4_L_comp.bind("<KP_Enter>", deplace_ligne0_4_return_L_comp)
entree1_L_comp.bind("<Tab>", deplace_ligne0_1_return_L_comp)
entree2_L_comp.bind("<Tab>", deplace_ligne0_2_return_L_comp)
entree3_L_comp.bind("<Tab>", deplace_ligne0_3_return_L_comp)
entree4_L_comp.bind("<Tab>", deplace_ligne0_4_return_L_comp)
#entree1_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_1_return_L_comp)
#entree2_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_2_return_L_comp)
#entree3_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_3_return_L_comp)
#entree4_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_4_return_L_comp)

entree5_L_comp.bind("<Return>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<Return>", vars_5_6_to_coord1_return_L_comp)
entree5_L_comp.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_comp)
entree5_L_comp.bind("<Tab>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<Tab>", vars_5_6_to_coord1_return_L_comp)

tree_resultats_L_comp.bind("<ButtonRelease-1>", selectionne_spectre_L_comp)
tree_resultats_L_comp.bind("<Up>", selectionne_spectre_up_L_comp)
tree_resultats_L_comp.bind("<Down>", selectionne_spectre_down_L_comp)





###############################################################################
###############################################################################
# Interface graphique LIBStick_IHM_ACP : onglet 4
###############################################################################
###############################################################################
def __________IHM_ACP__________():pass
###############################################################################
# Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###############################################################################
frame1_L_ACP=tkinter.Frame(onglet4,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame2_L_ACP=tkinter.Frame(onglet4,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame3_L_ACP=tkinter.Frame(onglet4,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)

frame1_L_ACP.grid(row=10, column=10, sticky = "nsew")
frame2_L_ACP.grid(row=20, column=10, sticky = "nsew")
frame3_L_ACP.grid(row=30, column=10, sticky = "nsew")
#frame1_L_ACP.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame2_L_ACP.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
#frame3_L_ACP.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# Interface graphique frame1_L_ACP : création selection répertoire, affiche spectre et bouton executer
###############################################################################
canevas0_L_ACP=tkinter.Canvas(frame1_L_ACP, width=1000, height=200, bg="white")
canevas0_L_ACP.grid(row=1, column=1, columnspan=6)

ligne_position_0_L_ACP=canevas0_L_ACP.create_line(0,0,0,200, fill="white")

lambda_texte_L_ACP = tkinter.Label(frame1_L_ACP, text="Lambda = " + str(format(l_L_ACP, "4.1f") + " nm"), bg=couleur_interface)
lambda_texte_L_ACP.grid(row=2, column=5)

text1_L_ACP=tkinter.Label(frame1_L_ACP, text="Numérateur borne inf. en nm", bg=couleur_interface)
text2_L_ACP=tkinter.Label(frame1_L_ACP, text="Numérateur borne sup. en nm", bg=couleur_interface)
text1_L_ACP.grid(row=2, column=1)
text2_L_ACP.grid(row=2, column=3)

variable_1_L_ACP=tkinter.DoubleVar(value=tableau_bornes_L_ACP[0])
variable_2_L_ACP=tkinter.DoubleVar(value=tableau_bornes_L_ACP[1])
entree1_L_ACP=tkinter.Spinbox(frame1_L_ACP, from_=198, to=1013, increment=0.5, textvariable=variable_1_L_ACP, command=deplace_ligne0_1_L_ACP)
entree2_L_ACP=tkinter.Spinbox(frame1_L_ACP, from_=198, to=1013, increment=0.5, textvariable=variable_2_L_ACP, command=deplace_ligne0_2_L_ACP)
entree1_L_ACP.grid(row=2, column=2)
entree2_L_ACP.grid(row=2, column=4)

#bouton_reset_L_ACP=tkinter.Button(frame1_L_ACP, text="Reset", command=reset_tableau_L_ACP, width=9, bg=couleur_interface)
#bouton_reset_L_ACP.grid(row=2, column=6, rowspan=2)

frame1_1_L_ACP=tkinter.Frame(frame1_L_ACP, bg=couleur_interface)
frame1_1_L_ACP.grid(row=1, column=7, rowspan=3, sticky=tkinter.N)

text_zoom_L_ACP=tkinter.Label(frame1_1_L_ACP, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_ACP.grid(row=1, column=1, sticky=tkinter.N)
variable_zoom_inf_L_ACP=tkinter.DoubleVar(value=198)
variable_zoom_sup_L_ACP=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_ACP=tkinter.Spinbox(frame1_1_L_ACP, from_=198, to=1013, increment=1, textvariable=variable_zoom_inf_L_ACP, command=change_zoom_inf_L_ACP, width=9)
entree_zoom_sup_L_ACP=tkinter.Spinbox(frame1_1_L_ACP, from_=198, to=1013, increment=1, textvariable=variable_zoom_sup_L_ACP, command=change_zoom_sup_L_ACP, width=9)
entree_zoom_inf_L_ACP.grid(row=2, column=1, sticky=tkinter.N)
entree_zoom_sup_L_ACP.grid(row=3, column=1, sticky=tkinter.N)

type_fichier_L_ACP=tkinter.StringVar(value=".mean")
bouton_rep_L_ACP=tkinter.Button(frame1_1_L_ACP, text="Fichier" ,command=choix_fichier_L_ACP, width=9, bg=couleur_interface)
bouton_rep_L_ACP.grid(row=4, column=1, sticky=tkinter.N)

bouton_classification_L_ACP=tkinter.Button(frame1_1_L_ACP, image= image_classification, command=ouvre_fenetre_classification_L_ele)
#bouton_classification_L_ACP=tkinter.Button(frame1_1_L_ACP, text="classification", command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_ACP.grid(row=8, column=1, sticky=tkinter.S)

###############################################################################
# Interface graphique frame2_L_ACP : affichage des résultats sous forme de TreeView
###############################################################################
tableau_label_ouvert_flag_L_ACP = False
label_L_ACP=tkinter.IntVar(0)

tree_L_ACP=tkinter.ttk.Treeview(frame2_L_ACP, columns=(1,2,3,4), height = 10 ,show = "headings")
tree_L_ACP.tag_configure("deselect", foreground="red")
tree_L_ACP.tag_configure("select", foreground="black")
tree_L_ACP.column(1, width=50)
tree_L_ACP.column(2, width=600)
tree_L_ACP.column(3, width=200)
tree_L_ACP.column(4, width=100)
tree_L_ACP.heading(1, text="n°")
tree_L_ACP.heading(2, text="Nom du spectre")
tree_L_ACP.heading(3, text="Utlisé pour l'ACP :")
tree_L_ACP.heading(4, text="Label :")
tree_L_ACP.grid(row=1, column=1, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)
scroll_tree_L_ACP=tkinter.ttk.Scrollbar(frame2_L_ACP, orient=tkinter.VERTICAL, command=tree_L_ACP.yview)
scroll_tree_L_ACP.grid(row=1, column=2, sticky=tkinter.N+tkinter.S)
tree_L_ACP.configure(yscrollcommand=scroll_tree_L_ACP.set)

frame2_1_L_ACP=tkinter.Frame(frame2_L_ACP, bg=couleur_interface)
frame2_1_L_ACP.grid(row=1, column=7, rowspan=3, sticky=tkinter.N)

flag_normalise_L_ACP=tkinter.BooleanVar(value=True)
coche_normalise_L_ACP=tkinter.Checkbutton(frame2_1_L_ACP, text="Spectres normalisés", variable=flag_normalise_L_ACP, bg=couleur_interface)
coche_normalise_L_ACP.grid(row=1, column=1)

flag_centre_reduit_L_ACP=tkinter.BooleanVar(value=False)
coche_centre_reduit_L_ACP=tkinter.Checkbutton(frame2_1_L_ACP, text="Centré reduit", variable=flag_centre_reduit_L_ACP, bg=couleur_interface)
coche_centre_reduit_L_ACP.grid(row=2, column=1)

bouton_execute_L_ACP=tkinter.Button(frame2_1_L_ACP, text="ACP", command=execute_ACP_L_ACP, state="disable", width=9, bg=couleur_interface)
bouton_execute_L_ACP.grid(row=3, column=1)

text_dim_L_ACP=tkinter.Label(frame2_1_L_ACP, text="Dimensions : ", bg=couleur_interface)
text_dim_L_ACP.grid(row=4, column=1)
dim_1_L_ACP=tkinter.IntVar(value=1)
entree_dim1_L_ACP=tkinter.Spinbox(frame2_1_L_ACP, from_=1, to=20, increment=1, textvariable=dim_1_L_ACP,
                                  width=9, foreground="red")
dim_2_L_ACP=tkinter.IntVar(value=2)
entree_dim2_L_ACP=tkinter.Spinbox(frame2_1_L_ACP, from_=1, to=20, increment=1, textvariable=dim_2_L_ACP,
                                  width=9, foreground="blue")
dim_3_L_ACP=tkinter.IntVar(value=3)
entree_dim3_L_ACP=tkinter.Spinbox(frame2_1_L_ACP, from_=1, to=20, increment=1, textvariable=dim_3_L_ACP, state="disable",
                                  width=9, foreground="green")
entree_dim1_L_ACP.grid(row=5, column=1)
entree_dim2_L_ACP.grid(row=6, column=1)
entree_dim3_L_ACP.grid(row=7, column=1)

flag_3D_L_ACP=tkinter.BooleanVar(value=False)
coche_3D_L_ACP=tkinter.Checkbutton(frame2_1_L_ACP, text="3 dimensions", variable=flag_3D_L_ACP, command=change_flag_3D_L_ACP, bg=couleur_interface)
coche_3D_L_ACP.grid(row=8, column=1)

flag_echelle_L_ACP=tkinter.BooleanVar(value=True)
coche_echelle_L_ACP=tkinter.Checkbutton(frame2_1_L_ACP, text="Même echelle x et y", variable=flag_echelle_L_ACP, bg=couleur_interface)
coche_echelle_L_ACP.grid(row=9, column=1)

flag_eboulis_L_ACP=tkinter.BooleanVar(value=True)
coche_eboulis_L_ACP=tkinter.Checkbutton(frame2_1_L_ACP, text="Diag. éboulis", variable=flag_eboulis_L_ACP, bg=couleur_interface)
coche_eboulis_L_ACP.grid(row=10, column=1)

#flag_calcul_L_ACP=tkinter.BooleanVar(value=False)
#coche_calcul_L_ACP=tkinter.Checkbutton(frame2_1_L_ACP, text="fanalysis ?", variable=flag_calcul_L_ACP, bg=couleur_interface)
#coche_calcul_L_ACP.grid(row=8, column=1)

###############################################################################
# Interface graphique frame3_L_ACP : affichage des "spectres" des variables de l'ACP
###############################################################################
canevas1_L_ACP=tkinter.Canvas(frame3_L_ACP, width=1000, height=200, bg="white")
canevas1_L_ACP.grid(row=1, column=1, columnspan=6)

frame3_1_L_ACP = tkinter.Frame(frame3_L_ACP, bg=couleur_interface)
frame3_1_L_ACP.grid(row=1, column=7, rowspan=3, sticky=tkinter.N)

bouton_enregistre_L_ACP=tkinter.Button(frame3_1_L_ACP, text="Enregistrer \nfacteurs \nde l'ACP", command=enregistre_var_explic_L_ACP,
                                       state="disable", width=9, bg=couleur_interface)
bouton_enregistre_L_ACP.grid(row=1, column=1)

ligne_position_1_L_ACP=canevas0_L_ACP.create_line(0,0,0,200, fill="white")

###############################################################################
# Interface graphique : gestion de évènements
###############################################################################
canevas0_L_ACP.bind("<ButtonRelease-1>", affiche_lambda_L_ACP)
canevas0_L_ACP.bind("<Motion>", affiche_position_souris_L_ACP)
canevas0_L_ACP.bind("<B1-Motion>", affiche_position_souris_motion_L_ACP)
canevas0_L_ACP.bind("<Button-3>", zoom_clic_L_ACP)
canevas0_L_ACP.bind("<B3-Motion>", zoom_drag_and_drop_L_ACP)
canevas0_L_ACP.bind("<ButtonRelease-3>", zoom_clic_release_L_ACP)

entree_zoom_inf_L_ACP.bind("<Return>", change_zoom_inf_return_L_ACP)
entree_zoom_sup_L_ACP.bind("<Return>", change_zoom_sup_return_L_ACP)
entree_zoom_inf_L_ACP.bind("<KP_Enter>", change_zoom_inf_return_L_ACP)
entree_zoom_sup_L_ACP.bind("<KP_Enter>", change_zoom_sup_return_L_ACP)
entree_zoom_inf_L_ACP.bind("<Tab>", change_zoom_inf_return_L_ACP)
entree_zoom_sup_L_ACP.bind("<Tab>", change_zoom_sup_return_L_ACP)
#entree_zoom_inf_L_ACP.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_ACP)
#entree_zoom_sup_L_ACP.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_ACP)

#canevas1_L_ACP.bind("<ButtonRelease-1>", coordonnees1_L_ACP)

entree1_L_ACP.bind("<Return>", deplace_ligne0_1_return_L_ACP)
entree2_L_ACP.bind("<Return>", deplace_ligne0_2_return_L_ACP)
entree1_L_ACP.bind("<KP_Enter>", deplace_ligne0_1_return_L_ACP)
entree2_L_ACP.bind("<KP_Enter>", deplace_ligne0_2_return_L_ACP)
entree1_L_ACP.bind("<Tab>", deplace_ligne0_1_return_L_ACP)
entree2_L_ACP.bind("<Tab>", deplace_ligne0_2_return_L_ACP)

tree_L_ACP.bind("<ButtonRelease-1>", selectionne_spectre_L_ACP)
#tree_L_ACP.bind("<Button-1>", selectionne_spectre_L_ACP)
tree_L_ACP.bind("<Up>", selectionne_spectre_up_L_ACP)
tree_L_ACP.bind("<Down>", selectionne_spectre_down_L_ACP)
tree_L_ACP.bind("<Double-Button-1>", change_tree_selection_L_ACP)
tree_L_ACP.bind("<space>", change_tree_selection_L_ACP)
tree_L_ACP.bind("l", ouvre_fenetre_change_tree_label_L_ACP)

canevas1_L_ACP.bind("<ButtonRelease-1>", affiche_lambda_L_ACP)
canevas1_L_ACP.bind("<Motion>", affiche_position_souris_L_ACP)
canevas1_L_ACP.bind("<B1-Motion>", affiche_position_souris_motion_L_ACP)
canevas1_L_ACP.bind("<Button-3>", zoom_clic_L_ACP)
canevas1_L_ACP.bind("<B3-Motion>", zoom_drag_and_drop_L_ACP)
canevas1_L_ACP.bind("<ButtonRelease-3>", zoom_clic_release_L_ACP)





###############################################################################
###############################################################################
# Interface graphique LIBStick : classification périodique
###############################################################################
###############################################################################
def __________IHM_tableau_periodique__________():pass
###############################################################################
flag_neutres_ions_L_ele=tkinter.IntVar(value=1)

flag_sup10_L_ele=tkinter.IntVar(value=1)
flag_sup1_L_ele=tkinter.IntVar(value=1)
flag_inf1_L_ele=tkinter.IntVar(value=0)





###############################################################################
###############################################################################
# LIBStick : interface principale
###############################################################################
###############################################################################
def __________IHM_divers__________():pass
###############################################################################
#  Interface graphique : gestion du redimentionnement de la fenêtre principale
###############################################################################
canevas_scroll.create_window(0, 0, anchor='nw', window=frame_scroll)
frame_scroll.update_idletasks()
canevas_scroll.config(scrollregion=canevas_scroll.bbox("all"))

fenetre_principale.mainloop()
