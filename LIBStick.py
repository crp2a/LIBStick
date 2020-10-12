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
import os, configparser
import math, numpy, pandas
import PIL.Image, PIL.ImageTk

import LIBStick_traitements_spectres
import LIBStick_extraction_spectres
import LIBStick_creation_spectre_moyen
import LIBStick_comp_spectres


###############################################################################
# 0- initialisations
###############################################################################
#couleur_interface="lavender"
#couleur_interface="linen"
couleur_interface="light grey"
rep_LIBStick=os.getcwd()
#print(rep_LIBStick)
largeur_lignes=2
taille_case = [3,2]

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
                             "type_extension_L_comp" : "type_extension_L_comp.get()",                             
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
limites_spectre_L_trait=numpy.array([198.0,1013.0])
limites_affichage_spectre_L_trait=numpy.array([198.0,1013.0])
coord_zoom_L_trait=numpy.array([198,0,1013,0])
delta_limites_L_trait=limites_affichage_spectre_L_trait[1]-limites_affichage_spectre_L_trait[0]
flag_premier_lamda_L_trait=True
#flag_premier_fond_L_trait=True
l_L_trait=0.0
spectre_entier_L_trait=numpy.zeros((0,2))
tableau_bornes_L_trait=numpy.array([300.0, 608.0])

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_trait() :
    #global tableau_bornes_L_ext
    tableau_bornes_L_trait[0]=variable_L_trait_1.get()
    tableau_bornes_L_trait[1]=variable_L_trait_2.get()
    return tableau_bornes_L_trait

def choix_fichier_L_trait():
    global nom_fichier_L_trait
    global nom_fichier_seul_L_trait
    global rep_travail_L_trait
    #global nbr_fichier_L_trait
    nom_fichier_L_trait = tkinter.filedialog.askopenfilename(initialdir=rep_travail_L_comp,
                                                                 title='Choisissez un fichier spectre',
                                                                 filetypes=(("fichiers IVEA","*.asc"), 
                                                                            ("fichiers LIBStick","*.tsv"),
                                                                            ("tous","*.*"))   )
    nom_fichier_seul_L_trait=os.path.basename(nom_fichier_L_trait)
    rep_travail_L_trait = os.path.dirname(nom_fichier_L_trait)
    lit_affiche_spectre_L_trait()
    bouton_visualisation_L_trait.configure(state="normal")
    
def visualisation_L_trait():
    global fond_continu_L_trait
    global spectre_corrige_L_trait
    global tableau_bornes_L_trait
    tableau_bornes_L_trait=creation_tab_bornes_L_trait()
    #print(spectre_entier_L_trait)
    spectre_filtre_L_trait = LIBStick_traitements_spectres.creation_spectre_filtre(spectre_entier_L_trait,
                                                                                          tableau_bornes_L_trait,
                                                                                          type_filtre_L_trait.get(),
                                                                                          taille_filtre_L_trait.get(),
                                                                                          ordre_filtre_L_trait.get())
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
    global rep_travail_L_trait
    #global nbr_fichier_L_trait
    #global fond_continu_L_trait
    global spectre_corrige_L_trait    
    global tableau_bornes_L_trait
    tableau_bornes_L_trait=creation_tab_bornes_L_trait()
    flag = flag_tous_fichiers_L_trait.get()
    if flag == False :
        LIBStick_traitements_spectres.execute(rep_travail_L_trait, spectre_corrige_L_trait, nom_fichier_seul_L_trait)
    if flag == True :
        LIBStick_traitements_spectres.execute_en_bloc(rep_travail_L_trait, type_fichier_L_trait.get(), tableau_bornes_L_trait,
                                                      type_filtre_L_trait.get(), taille_filtre_L_trait.get(), ordre_filtre_L_trait.get(),
                                                      type_fond_L_trait.get(), param1_fond_L_trait.get(), param2_fond_L_trait.get(),param3_fond_L_trait.get())
    
###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1_L_trait)
###############################################################################
def change_zoom_inf_L_trait() :
#    global limites_affichage_spectre_L_trait
    if variable_L_trait_zoom_inf.get() >= variable_L_trait_zoom_sup.get() :
        variable_L_trait_zoom_sup.set(variable_L_trait_zoom_inf.get())
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()
    
def change_zoom_sup_L_trait():
#    global limites_affichage_spectre_L_trait
    if variable_L_trait_zoom_sup.get() <= variable_L_trait_zoom_inf.get() :
        variable_L_trait_zoom_inf.set(variable_L_trait_zoom_sup.get())
#    limites_affichage_spectre_L_trait[0]=variable_L_trait_zoom_inf.get()
#    limites_affichage_spectre_L_trait[1]=variable_L_trait_zoom_sup.get()
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
        variable_L_trait_zoom_inf.set(format(debut, "4.1f"))
        variable_L_trait_zoom_sup.set(format(fin, "4.1f"))
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
        variable_L_trait_zoom_inf.set(limites_spectre_L_trait[0])
        variable_L_trait_zoom_sup.set(limites_spectre_L_trait[1])
        limites_affichage_spectre_L_trait[0]=variable_L_trait_zoom_inf.get()
        limites_affichage_spectre_L_trait[1]=variable_L_trait_zoom_sup.get()

def zoom_clic_release_L_trait(event):
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()
         
def lit_affiche_spectre_L_trait():
    global spectre_entier_L_trait 
    os.chdir(rep_travail_L_trait)
    spectre_entier_L_trait=LIBStick_traitements_spectres.lit_spectre(nom_fichier_L_trait, type_fichier_L_trait.get())
    affiche_spectre_L_trait()

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
    global spectre_entier_L_trait
    global minimum_spectre_L_trait
    global maximum_spectre_L_trait
    limites_affichage_spectre_L_trait[0]=variable_L_trait_zoom_inf.get()
    limites_affichage_spectre_L_trait[1]=variable_L_trait_zoom_sup.get()
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
    x_ligne0_1=((variable_L_trait_1.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    x_ligne0_2=((variable_L_trait_2.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    ligne0_1=canevas0_L_trait.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    ligne0_2=canevas0_L_trait.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
        
def deplace_lignes_L_trait():
    deplace_ligne0_1_L_trait()
    deplace_ligne0_2_L_trait()

def deplace_ligne0_1_L_trait():
    global ligne0_1
    canevas0_L_trait.delete(ligne0_1)
    x_ligne0_1=((variable_L_trait_1.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    ligne0_1=canevas0_L_trait.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    if variable_L_trait_1.get() >= variable_L_trait_2.get():
        variable_L_trait_2.set(variable_L_trait_1.get())
        deplace_ligne0_2_L_trait()
        
def deplace_ligne0_2_L_trait():
    global ligne0_2
    canevas0_L_trait.delete(ligne0_2)
    x_ligne0_2=((variable_L_trait_2.get()-limites_affichage_spectre_L_trait[0])*1000/delta_limites_L_trait)
    ligne0_2=canevas0_L_trait.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if variable_L_trait_2.get() <= variable_L_trait_1.get() :
        variable_L_trait_1.set(variable_L_trait_2.get())
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
    if filtre == "Savitzky-Golay" :
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="normal")
    if filtre == "Median" :
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="disable")
    if filtre == "Passe-bas" :
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="disable")
        
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
        entree8_L_trait.grid(row=4, column=6)
    if fond == "SNIP" :
        text7_L_trait.configure(text="Itérations :")
        entree7_L_trait.configure(state="normal")
        text8_L_trait.configure(text="LLS :")
        entree8bis_L_trait.configure(state="normal")
        entree8_L_trait.grid_forget()
        entree8bis_L_trait.grid(row=4, column=6)

def affiche_fond_L_trait():
    global fond_continu_L_trait
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
        dessin_fond_continu_L_trait = canevas0_L_trait.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1], fill="blue")
    #flag_premier_fond_L_trait = False
    
###############################################################################
# 3- fonctions graphiques du caneva du spectre corrigé (frame2_L_trait)
###############################################################################  
  
def affiche_spectre_corrige_L_trait():
    #global limites_affichage_spectre_L_trait
    #global delta_limites_L_trait
    global spectre_corrige_L_trait
    #limites_affichage_spectre_L_trait[0]=variable_L_trait_zoom_inf.get()
    #limites_affichage_spectre_L_trait[1]=variable_L_trait_zoom_sup.get()
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
y1_L_ext=100.0
x2_L_ext=250.0
y2_L_ext=100.0

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_ext() :
    #global tableau_bornes_L_ext
    tableau_bornes_L_ext[0,0]=variable_L_ext_1.get()
    tableau_bornes_L_ext[0,1]=variable_L_ext_2.get()
    entree5_L_ext.configure(from_=tableau_bornes_L_ext[0,0], to=tableau_bornes_L_ext[0,1])  
    if flag_zone2_L_ext.get() :
        tableau_bornes_L_ext[1,0]=variable_L_ext_3.get()
        tableau_bornes_L_ext[1,1]=variable_L_ext_4.get()
        entree7_L_ext.configure(from_=tableau_bornes_L_ext[1,0], to=tableau_bornes_L_ext[1,1]) 
    return tableau_bornes_L_ext

def reset_tableau_L_ext() :
    #global tableau_bornes_L_ext
    tableau_bornes_L_ext=tableau_bornes_init_L_ext.copy()
    variable_L_ext_1.set(tableau_bornes_L_ext[0,0])
    variable_L_ext_2.set(tableau_bornes_L_ext[0,1])
    variable_L_ext_3.set(tableau_bornes_L_ext[1,0])
    variable_L_ext_4.set(tableau_bornes_L_ext[1,1])
    deplace_lignes_L_ext()

def choix_rep_L_ext():
    global rep_travail_L_ext
    global nombre_fichiers_L_ext
    global liste_fichiers_L_ext
    rep_travail_L_ext = tkinter.filedialog.askdirectory(initialdir=rep_travail_L_ext,title='Choisissez un repertoire')   
    liste_fichiers_L_ext=LIBStick_extraction_spectres.creation_liste_fichiers(rep_travail_L_ext, type_fichier_L_ext.get())
    nombre_fichiers_L_ext=len(liste_fichiers_L_ext)    
    lit_affiche_spectre_L_ext()
    bouton_execute_L_ext.configure(state="normal")
    bouton_extraction_L_ext.configure(state="disable")
    entree6_L_ext.configure(to=nombre_fichiers_L_ext)
    entree8_L_ext.configure(to=nombre_fichiers_L_ext)
    entree9_L_ext.configure(to=nombre_fichiers_L_ext)
    entree10_L_ext.configure(to=nombre_fichiers_L_ext)
    
def execute_scripts_L_ext():
    global liste_fichiers_L_ext
    global nom_echantillon_L_ext
    tableau_bornes_L_ext=creation_tab_bornes_L_ext()
    if flag_zone2_L_ext.get() == 0 :
        canevas2_L_ext.delete("all")
    nom_echantillon_L_ext = LIBStick_extraction_spectres.main(rep_travail_L_ext, tableau_bornes_L_ext,
                                                              type_fichier_L_ext.get(), liste_fichiers_L_ext,
                                                              flag_zone2_L_ext.get(), flag_2D_L_ext.get(), flag_3D_L_ext.get())

    affiche_image_L_ext()
    bouton_extraction_L_ext.configure(state="normal")
    #plt.show(block=False)

def creation_spectre_moyen_L_ext():
    bornes_moyenne_spectres_L_ext.insert(0,variable_L_ext_9.get())
    bornes_moyenne_spectres_L_ext.insert(1,variable_L_ext_10.get())
    tableau_bornes_copy_L_ext=tableau_bornes_L_ext.copy()
    i=3
    if flag_zone2_L_ext.get() == 0:
        tableau_bornes_copy_L_ext=numpy.delete(tableau_bornes_copy_L_ext, (1), axis=0)
        canevas4_L_ext.delete("all")
    for bornes in tableau_bornes_copy_L_ext :
        repertoire=rep_travail_L_ext+"/"+str(bornes[0])+"_"+ str(bornes[1])+"/"
        spectre=LIBStick_creation_spectre_moyen.main(repertoire,nom_echantillon_L_ext,bornes, bornes_moyenne_spectres_L_ext)
        if i==3 :
            canevas3_L_ext.delete("all")
            minimum=spectre[:,1].min()
            maximum=spectre[:,1].max()
            spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
            for j in range(spectre.shape[0] - 1) :
                dx=500/spectre.shape[0]
                x=j*dx
                canevas3_L_ext.create_line(x,spectre[j,1],x+dx,spectre[j+1,1], width=1, fill="red", smooth=1)
        if i==4 :
            canevas4_L_ext.delete("all")
            minimum=spectre[:,1].min()
            maximum=spectre[:,1].max()
            spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
            for j in range(spectre.shape[0] - 1) :
                dx=500/spectre.shape[0]
                x=j*dx
                canevas4_L_ext.create_line(x,spectre[j,1],x+dx,spectre[j+1,1], width=1, fill="blue", smooth=1)
        i=i+1
        
###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1_L_ext)
###############################################################################
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
        
def change_zoom_inf_L_ext() :
#    global limites_affichage_spectre_L_ext
    if variable_L_ext_zoom_inf.get() >= variable_L_ext_zoom_sup.get() :
        variable_L_ext_zoom_sup.set(variable_L_ext_zoom_inf.get())
#    limites_affichage_spectre_L_ext[0]=variable_L_ext_zoom_inf.get()
#    limites_affichage_spectre_L_ext[1]=variable_L_ext_zoom_sup.get()
    affiche_spectre_L_ext()
    
def change_zoom_sup_L_ext():
#    global limites_affichage_spectre_L_ext
    if variable_L_ext_zoom_sup.get() <= variable_L_ext_zoom_inf.get() :
        variable_L_ext_zoom_inf.set(variable_L_ext_zoom_sup.get())
#    limites_affichage_spectre_L_ext[0]=variable_L_ext_zoom_inf.get()
#    limites_affichage_spectre_L_ext[1]=variable_L_ext_zoom_sup.get()
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
        variable_L_ext_zoom_inf.set(format(debut, "4.1f"))
        variable_L_ext_zoom_sup.set(format(fin, "4.1f"))
        #affiche la longueur d'onde :
        if flag_premier_lamda_L_ext == False :
            canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
        l= event.x*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
        lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
        flag_premier_lamda_L_ext=False
    if coord_zoom_L_ext[2] < coord_zoom_L_ext[0] :
        variable_L_ext_zoom_inf.set(limites_spectre_L_ext[0])
        variable_L_ext_zoom_sup.set(limites_spectre_L_ext[1])
        limites_affichage_spectre_L_ext[0]=variable_L_ext_zoom_inf.get()
        limites_affichage_spectre_L_ext[1]=variable_L_ext_zoom_sup.get()

def zoom_clic_release_L_ext(event):
    affiche_spectre_L_ext()
         
def lit_affiche_spectre_L_ext():
    global spectre_entier 
    os.chdir(rep_travail_L_ext)
    spectre_entier=LIBStick_extraction_spectres.lit_spectre(liste_fichiers_L_ext[0], type_fichier_L_ext.get())
    affiche_spectre_L_ext()

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
    global spectre_entier
    limites_affichage_spectre_L_ext[0]=variable_L_ext_zoom_inf.get()
    limites_affichage_spectre_L_ext[1]=variable_L_ext_zoom_sup.get()
    delta_limites_L_ext=limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
    canevas0_L_ext.delete("all")
    spectre=numpy.zeros((0,2))
    for ligne in spectre_entier :
        if (ligne[0] >= limites_affichage_spectre_L_ext[0] and ligne[0] <= limites_affichage_spectre_L_ext[1]) :
            spectre=numpy.row_stack((spectre,ligne))
    minimum=spectre[:,1].min()
    maximum=spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    #spectre[:,0] = (spectre[:,0] - spectre[0,0])*1000/(spectre[len(spectre),0]-spectre[0,0])
    spectre[:,0] = (spectre[:,0] - limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext
    for i in range(len(spectre) - 1) :
        canevas0_L_ext.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])
    affiche_lignes_spectre_L_ext()
    
def affiche_lignes_spectre_L_ext():
    global ligne0_1_L_ext
    global ligne0_2_L_ext
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    x_ligne0_1=((variable_L_ext_1.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    x_ligne0_2=((variable_L_ext_2.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_1_L_ext=canevas0_L_ext.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    ligne0_2_L_ext=canevas0_L_ext.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if flag_zone2_L_ext.get() :
        x_ligne0_3=((variable_L_ext_3.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        x_ligne0_4=((variable_L_ext_4.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
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
    x_ligne0_1=((variable_L_ext_1.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_1_L_ext=canevas0_L_ext.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red", width=largeur_lignes)
    if variable_L_ext_1.get() >= variable_L_ext_2.get():
        variable_L_ext_2.set(variable_L_ext_1.get())
        deplace_ligne0_2_L_ext()
        
def deplace_ligne0_2_L_ext():
    global ligne0_2_L_ext
    canevas0_L_ext.delete(ligne0_2_L_ext)
    x_ligne0_2=((variable_L_ext_2.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_2_L_ext=canevas0_L_ext.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red", width=largeur_lignes)
    if variable_L_ext_2.get() <= variable_L_ext_1.get() :
        variable_L_ext_1.set(variable_L_ext_2.get())
        deplace_ligne0_1_L_ext()

def deplace_ligne0_3_L_ext():
    global ligne0_3_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    if flag_zone2_L_ext.get() :
        x_ligne0_3=((variable_L_ext_3.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_3_L_ext=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue", width=largeur_lignes)
        if variable_L_ext_3.get() >= variable_L_ext_4.get():
            variable_L_ext_4.set(variable_L_ext_3.get())
            deplace_ligne0_4_L_ext()
        
def deplace_ligne0_4_L_ext():
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_4_L_ext)
    if flag_zone2_L_ext.get() :
        x_ligne0_4=((variable_L_ext_4.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_4_L_ext=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue", width=largeur_lignes)
        if variable_L_ext_4.get() <= variable_L_ext_3.get() :
            variable_L_ext_3.set(variable_L_ext_4.get())
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
    x_ligne0_3=((variable_L_ext_3.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    x_ligne0_4=((variable_L_ext_4.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
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

###############################################################################
# 3- fonctions graphiques du caneva de l'image 1 (frame2_L_ext)
###############################################################################
def coordonnees1_L_ext (event) :
    global x1_L_ext,y1_L_ext
    x1_L_ext=event.x
    y1_L_ext=event.y
    coord1_to_vars_5_6_L_ext(x1_L_ext,y1_L_ext)
    deplace_cible1_L_ext()
   
def deplace_cible1_L_ext():
    global x1_L_ext,y1_L_ext
    global ligne1_vert_L_ext, ligne1_hori_L_ext
    canevas1_L_ext.delete(ligne1_vert_L_ext)
    canevas1_L_ext.delete(ligne1_hori_L_ext)
    ligne1_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
    ligne1_hori_L_ext=canevas1_L_ext.create_line(0,y1_L_ext,500,y1_L_ext, fill="white")    
#    canevas1_L_ext.coords(ligne1_vert_L_ext, x1_L_ext,0,x1_L_ext,200)
#    canevas1_L_ext.coords(ligne1_hori_L_ext, 0,y1_L_ext,400,y1_L_ext)
    
def coord1_to_vars_5_6_L_ext(x,y):
    variable_L_ext_5.set(format((variable_L_ext_1.get() + (x * (variable_L_ext_2.get()-variable_L_ext_1.get()) / 500)), "4.1f"))
    variable_L_ext_6.set(math.ceil(y * nombre_fichiers_L_ext / 200))

def vars_5_6_to_coord1_L_ext():
    global x1_L_ext,y1_L_ext
    x1_L_ext=round( ((variable_L_ext_5.get()-variable_L_ext_1.get())*500) / (variable_L_ext_2.get()-variable_L_ext_1.get())) 
    y1_L_ext= round(200*(variable_L_ext_6.get()-0.5)/nombre_fichiers_L_ext)
    deplace_cible1_L_ext()
    
def vars_5_6_to_coord1_return_L_ext(event):
    vars_5_6_to_coord1_L_ext()

###############################################################################
# 4- fonctions graphiques du caneva de l'image 2 (frame2_L_ext)
###############################################################################      
def coordonnees2_L_ext (event) :
    global x2_L_ext,y2_L_ext
    x2_L_ext=event.x
    y2_L_ext=event.y
    coord2_to_vars_7_8_L_ext(x2_L_ext,y2_L_ext)
    deplace_cible2_L_ext()
    
def deplace_cible2_L_ext():
    global x2_L_ext,y2_L_ext
    global ligne2_vert_L_ext, ligne2_hori_L_ext
    canevas2_L_ext.delete(ligne2_vert_L_ext)
    canevas2_L_ext.delete(ligne2_hori_L_ext)
    ligne2_vert_L_ext=canevas2_L_ext.create_line(x2_L_ext,0,x2_L_ext,200, fill="white")
    ligne2_hori_L_ext=canevas2_L_ext.create_line(0,y2_L_ext,500,y2_L_ext, fill="white")
    
def coord2_to_vars_7_8_L_ext(x,y):
    variable_L_ext_7.set(format((variable_L_ext_3.get() + (x * (variable_L_ext_4.get()-variable_L_ext_3.get()) / 500)), "4.1f"))
    variable_L_ext_8.set(math.ceil(y * nombre_fichiers_L_ext / 200))

def vars_7_8_to_coord2_L_ext():
    global x2_L_ext,y2_L_ext
    x2_L_ext= round((variable_L_ext_7.get()-variable_L_ext_3.get())*500/(variable_L_ext_4.get()-variable_L_ext_3.get()))
    y2_L_ext= round(200*(variable_L_ext_8.get()-0.5)/nombre_fichiers_L_ext)
    deplace_cible2_L_ext()
    
def vars_7_8_to_coord2_return_L_ext(event):
    vars_7_8_to_coord2_L_ext()

###############################################################################
# 5- fonctions graphiques du choix des spectres à moyenner (frame3_L_ext)
###############################################################################
def retro_action_entree10_L_ext():
    if variable_L_ext_9.get() > variable_L_ext_10.get():
        variable_L_ext_10.set(variable_L_ext_9.get())

def retro_action_entree9_L_ext():
    if variable_L_ext_10.get() < variable_L_ext_9.get():
        variable_L_ext_9.set(variable_L_ext_10.get())

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
limites_spectre_L_comp=numpy.array([198.0,1013.0])
limites_affichage_spectre_L_comp=numpy.array([198.0,1013.0])
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
    return tableau_bornes_init_L_comp,tableau_bornes_L_comp,rep_travail_L_comp,flag_denominateur_init_L_comp,flag_2D_init_L_comp,flag_3D_init_L_comp

tableau_bornes_init_L_comp,tableau_bornes_L_comp,rep_travail_L_comp,flag_denominateur_init_L_comp,flag_2D_init_L_comp,flag_3D_init_L_comp= charge_param_L_comp()

x1_L_comp=250.0
y1_L_comp=100.0
#x2_L_comp=250.0
#y2_L_comp=100.0

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_comp() :
    #global tableau_bornes_L_comp
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

def choix_rep_L_comp():
    global rep_travail_L_comp
    global liste_fichiers_L_comp
    global nombre_fichier_L_comp
    rep_travail_L_comp = tkinter.filedialog.askdirectory(initialdir=rep_travail_L_comp,title='Choisissez un repertoire')
    liste_fichiers_L_comp=LIBStick_comp_spectres.creation_liste_fichiers(rep_travail_L_comp, type_extension_L_comp.get())
    nombre_fichier_L_comp=len(liste_fichiers_L_comp)
    lit_affiche_spectre_L_comp()
    bouton_execute_L_comp.configure(state="normal")
    entree6_L_comp.configure(to=nombre_fichier_L_comp)

def lit_affiche_spectre_L_comp():
    global spectre_entier_L_comp 
    global limites_spectre_L_comp
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp=LIBStick_comp_spectres.lit_spectre(liste_fichiers_L_comp[0], type_extension_L_comp.get())
    limites_spectre_L_comp=lit_limites_abscisses_L_comp(spectre_entier_L_comp)
    #print (spectre_entier_L_comp)
    affiche_spectre_L_comp()

def lit_limites_abscisses_L_comp(spectre):
    tableau_abscisses=spectre[:,0]
    limites_spectre=numpy.zeros((2))
    limites_spectre[0]=limites_affichage_spectre_L_comp[0]=tableau_abscisses[0]
    limites_spectre[1]=limites_affichage_spectre_L_comp[1]=tableau_abscisses[-1]
    variable_zoom_inf_L_comp.set(limites_affichage_spectre_L_comp[0])
    variable_zoom_sup_L_comp.set(limites_affichage_spectre_L_comp[1])
    entree_zoom_inf_L_comp.configure(from_=limites_spectre_L_comp[0], to=limites_spectre_L_comp[1])
    entree_zoom_sup_L_comp.configure(from_=limites_spectre_L_comp[0], to=limites_spectre_L_comp[1])
    entree1_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    entree2_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    entree3_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    entree4_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    return limites_spectre
       
def execute_scripts_L_comp():
    global DataFrame_resultats_L_comp
    tableau_bornes_L_comp=creation_tab_bornes_L_comp()
    DataFrame_resultats_L_comp = LIBStick_comp_spectres.main(rep_travail_L_comp, liste_fichiers_L_comp, tableau_bornes_L_comp, type_extension_L_comp.get(),
                                flag_denominateur_L_comp.get(), flag_2D_L_comp.get(), flag_3D_L_comp.get())
    global photo
    fichier=rep_travail_L_comp+"/figure.png"
    image_zoom=PIL.Image.open(fichier)    
    image_zoom=image_zoom.resize((1000, 200))
    photo=PIL.ImageTk.PhotoImage(image_zoom)
    canevas1_L_comp.create_image(500 ,100 ,image=photo)
    affiche_tableau_resultats_L_comp()
    if type_extension_L_comp.get() == "*.tsv" :
        texte_statistiques_L_comp.grid(row=1, column=3, sticky=tkinter.N)
        calcule_moyenne_ecarttype_L_comp()
    if type_extension_L_comp.get() == "*.mean" :
        texte_statistiques_L_comp.grid_forget()

###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1_L_comp)
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
    global lambda_texte_spectre
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
            canevas0_L_comp.delete(lambda_texte_spectre)
        l_L_comp= event.x*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
        lambda_texte_spectre = canevas0_L_comp.create_text(event.x, event.y, text=str(format(l_L_comp, "4.1f")), fill="blue")
        lambda_texte_L_comp.configure(text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm" ))
        flag_premier_lamda_L_comp=False
    if coord_zoom_L_comp[2] < coord_zoom_L_comp[0] :
        variable_zoom_inf_L_comp.set(limites_spectre_L_comp[0])
        variable_zoom_sup_L_comp.set(limites_spectre_L_comp[1])
        #limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
        #limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()

def zoom_clic_release_L_comp(event):
    affiche_spectre_L_comp()

def affiche_lambda_L_comp(event):
    global lambda_texte_spectre
    global flag_premier_lamda_L_comp
    #affiche_spectre_L_comp()
    if flag_premier_lamda_L_comp == False :
        canevas0_L_comp.delete(lambda_texte_spectre)
    l_L_comp= event.x*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
    lambda_texte_spectre = canevas0_L_comp.create_text(event.x, event.y, text=str(format(l_L_comp, "4.1f")), fill="blue")
    lambda_texte_L_comp.configure(text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm" ))
    flag_premier_lamda_L_comp=False
    
def affiche_position_souris_L_comp(event):
    global ligne_position_L_comp
    canevas0_L_comp.delete(ligne_position_L_comp)
    ligne_position_L_comp=canevas0_L_comp.create_line(event.x,0,event.x,200, fill="green")
    
def affiche_position_souris_motion_L_comp(event):
    global ligne_position_L_comp
    global lambda_texte_spectre
    global flag_premier_lamda_L_comp
    canevas0_L_comp.delete(ligne_position_L_comp)
    ligne_position_L_comp=canevas0_L_comp.create_line(event.x,0,event.x,200, fill="green")
    if flag_premier_lamda_L_comp == False :
        canevas0_L_comp.delete(lambda_texte_spectre)
    l_L_comp= event.x*delta_limites_L_comp/1000+limites_affichage_spectre_L_comp[0]
    lambda_texte_spectre = canevas0_L_comp.create_text(event.x, event.y, text=str(format(l_L_comp, "4.1f")), fill="blue")
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
# 3- fonctions graphiques du caneva de l'image 1 (frame2_L_comp)
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
    variable_5_L_comp.set(format(limites_spectre_L_comp[0] + (x * (limites_spectre_L_comp[1]-limites_spectre_L_comp[0]) / 1000), "4.1f"))
    variable_6_L_comp.set(math.ceil(y * nombre_fichier_L_comp / 200))

def vars_5_6_to_coord1_L_comp():
    global x1_L_comp,y1_L_comp
    x1_L_comp=round( ((variable_5_L_comp.get()-limites_spectre_L_comp[0])*1000) / (limites_spectre_L_comp[1]-limites_spectre_L_comp[0])) 
    y1_L_comp= round(200*(variable_6_L_comp.get()-0.5)/nombre_fichier_L_comp)
    deplace_cible1_L_comp()
    
def vars_5_6_to_coord1_return_L_comp(event):
    vars_5_6_to_coord1_L_comp()

###############################################################################
# 4- fonctions graphiques du caneva de l'image 2 (frame2_L_comp)
###############################################################################      


###############################################################################
# 5- fonctions graphiques du tableau de résultats (frame3_L_comp)
###############################################################################
def affiche_tableau_resultats_L_comp(): 
    efface_tableau_resultats_L_comp()
    num_ligne=1
    if flag_denominateur_L_comp.get() == 1 :
        tree_resultats_L_comp.heading(3, text="Rapport zone1/zone2")
        for ligne_tableau in DataFrame_resultats_L_comp.iterrows() :
            ID_L_comp=tree_resultats_L_comp.insert("","end", values=(num_ligne, ligne_tableau[0], DataFrame_resultats_L_comp.iloc[num_ligne-1, 2]))
            #print(ID)
            num_ligne=num_ligne+1
    if flag_denominateur_L_comp.get() == 0 :
        tree_resultats_L_comp.heading(3, text="Aire zone 1")
        for ligne_tableau in DataFrame_resultats_L_comp.iterrows() :
            ID_L_comp=tree_resultats_L_comp.insert("","end", values=(num_ligne, ligne_tableau[0], DataFrame_resultats_L_comp.iloc[num_ligne-1, 0]))
            #print(ID)
            num_ligne=num_ligne+1
        
def efface_tableau_resultats_L_comp():
    for i in tree_resultats_L_comp.get_children() :
        tree_resultats_L_comp.delete(i)

def selectionne_spectre_L_comp(event):
    selection=tree_resultats_L_comp.item(tree_resultats_L_comp.selection())["values"]
    variable_6_L_comp.set(selection[0])
    vars_5_6_to_coord1_L_comp()

def calcule_moyenne_ecarttype_L_comp() :
    if flag_denominateur_L_comp.get() == 1 :
        moyenne_L_comp=DataFrame_resultats_L_comp["Rapport"].mean()
        ecarttype_L_comp=DataFrame_resultats_L_comp["Rapport"].std()
        min_L_comp=DataFrame_resultats_L_comp["Rapport"].min()
        max_L_comp=DataFrame_resultats_L_comp["Rapport"].max()
    if flag_denominateur_L_comp.get() == 0 :
        moyenne_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].mean()
        ecarttype_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].std()
        min_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].min()
        max_L_comp=DataFrame_resultats_L_comp["Somme zone 1"].max()
    texte_moyenne= "Moyenne :\n" + str(format(moyenne_L_comp, "3.4f"))
    texte_ecarttype= "Ecart type :\n" + str(format(ecarttype_L_comp,"3.4f"))
    texte_min= "Minimum :\n" +  str(format(min_L_comp,"3.4f"))
    texte_max= "Maximum :\n" +  str(format(max_L_comp,"3.4f"))
    texte_statistiques_L_comp.configure(text= texte_moyenne +"\n\n"+texte_ecarttype +"\n\n"+ texte_min +"\n\n"+ texte_max)





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
    if ID_onglet == 1 :
        affiche_spectre_L_ext()
    if ID_onglet == 2 :
        affiche_spectre_L_comp()
    if flag_neutres_ions_L_ele.get() == 1 :
        couleur_lignes="magenta2"
    if flag_neutres_ions_L_ele.get() == 2 :
        couleur_lignes="cyan3"
    for ligne_tableau in DataFrame_element_L_ele.itertuples() :
        if float(ligne_tableau[2]) > limites_affichage_spectre[0] and float(ligne_tableau[2]) < limites_affichage_spectre[1] :
            delta_limites= limites_affichage_spectre[1]-limites_affichage_spectre[0]
            long_onde=ligne_tableau[2]
            intensite_relative=ligne_tableau[5]
            #print (intensite_relative)
            if intensite_relative >= 10 and flag_sup10_L_ele.get() == 1 :
                #affiche_ligne_element(long_onde, canevas0_L_ext)
                x_ligne=((long_onde-limites_affichage_spectre[0])*1000/delta_limites)
                if ID_onglet==0 :
                    ligne=canevas0_L_trait.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                if ID_onglet==1 :
                    ligne=canevas0_L_ext.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
                if ID_onglet==2 :
                    ligne=canevas0_L_comp.create_line(x_ligne,0,x_ligne,200, fill=couleur_lignes, dash=(4,1))
            if intensite_relative < 10 and intensite_relative >= 1 and flag_sup1_L_ele.get() == 1 :
                x_ligne=((long_onde-limites_affichage_spectre[0])*1000/delta_limites)
                if ID_onglet==0 :
                    ligne=canevas0_L_trait.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                if ID_onglet==1 :
                    ligne=canevas0_L_ext.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
                if ID_onglet==2 :
                    ligne=canevas0_L_comp.create_line(x_ligne,100,x_ligne,200, fill=couleur_lignes, dash=(4,2))
            if intensite_relative < 1 and flag_inf1_L_ele.get() == 1 :
                x_ligne=((long_onde-limites_affichage_spectre[0])*1000/delta_limites)
                if ID_onglet==0 :
                    ligne=canevas0_L_trait.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))
                if ID_onglet==1 :
                    ligne=canevas0_L_ext.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))
                if ID_onglet==2 :
                    ligne=canevas0_L_comp.create_line(x_ligne,165,x_ligne,200, fill=couleur_lignes, dash=(4,3))                    

def affiches_lignes_element_bis_L_ele() :
    ID_onglet = onglets.index("current")
    if ID_onglet == 0 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_trait, 0)
    if ID_onglet == 1 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_ext, 1)
    if ID_onglet == 2 :
        affiches_lignes_element_L_ele(DataFrame_element_L_ele, limites_affichage_spectre_L_comp, 2)
        
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

###############################################################################
# 7- Interface graphique : création fenêtre principale avec scrolls et onglets
###############################################################################
fenetre_principale=tkinter.Tk()
fenetre_principale.title("LIBStick v1.0")
fenetre_principale.geometry("1150x850+100+50")
fenetre_principale.maxsize(width=1160, height=850)

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
#onglet3=tkinter.ttk.Frame(onglets)
onglet1.pack()
onglet2.pack()
onglet3.pack()

onglets.add(onglet1, text="LIBStick pré-traitements")
onglets.add(onglet2, text="LIBStick extraction")
onglets.add(onglet3, text="LIBStick comparaison")

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
type_fichier_L_trait=tkinter.StringVar(value="IVEA")
menu_traitement.add_radiobutton(label="LIBS IVEA (*.asc)", value="IVEA", variable=type_fichier_L_trait)
menu_traitement.add_radiobutton(label="LIBStick (*.tsv)", value="LIBStick", variable=type_fichier_L_trait)

barre_menus.add_cascade(label="Extraction", menu=menu_extraction)
type_fichier_L_ext=tkinter.StringVar(value="IVEA")
menu_extraction.add_radiobutton(label="LIBS IVEA (*.asc)", value="IVEA", variable=type_fichier_L_ext)
menu_extraction.add_radiobutton(label="LIBStick (*.tsv)", value="LIBStick", variable=type_fichier_L_ext)

barre_menus.add_cascade(label="Comparaison", menu=menu_comparaison)
type_fichier_L_comp=tkinter.StringVar(value="LIBStick")
menu_comparaison.add_radiobutton(label="LIBS IVEA (*.asc)", value="IVEA", variable=type_fichier_L_comp)
menu_comparaison.add_radiobutton(label="LIBStick (*.tsv)", value="LIBStick", variable=type_fichier_L_comp)

fenetre_principale.config(menu=barre_menus)

#fenetre_classification_L_ele=tkinter.Toplevel(fenetre_principale)





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

frame1_L_trait.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
frame2_L_trait.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)

###############################################################################
# 9- Interface graphique frame1_L_trait : 
###############################################################################
canevas0_L_trait=tkinter.Canvas(frame1_L_trait, width=1000, height=200, bg="white")
canevas0_L_trait.grid(row=1, column=1, columnspan=6)

ligne_position_0_L_trait=canevas0_L_trait.create_line(0,0,0,200, fill="white")

lambda_texte_L_trait = tkinter.Label(frame1_L_trait, text="Lambda = " + str(format(l_L_ext, "4.1f") + " nm"), bg=couleur_interface)
lambda_texte_L_trait.grid(row=2, column=5,columnspan=2, sticky=tkinter.E)

text1_L_trait=tkinter.Label(frame1_L_trait, text="Première borne inf. en nm", bg=couleur_interface)
text2_L_trait=tkinter.Label(frame1_L_trait, text="Première borne sup. en nm", bg=couleur_interface)
text1_L_trait.grid(row=2, column=1, sticky=tkinter.W)
text2_L_trait.grid(row=2, column=3, sticky=tkinter.W)
variable_L_trait_1=tkinter.DoubleVar(value=tableau_bornes_L_trait[0])
variable_L_trait_2=tkinter.DoubleVar(value=tableau_bornes_L_trait[1])
entree1_L_trait=tkinter.Spinbox(frame1_L_trait, from_=198, to=1013,
                                textvariable=variable_L_trait_1,
                                command=deplace_ligne0_1_L_trait)
entree2_L_trait=tkinter.Spinbox(frame1_L_trait, from_=198, to=1013,
                                textvariable=variable_L_trait_2,
                                command=deplace_ligne0_2_L_trait)
entree1_L_trait.grid(row=2, column=2)
entree2_L_trait.grid(row=2, column=4)

text3_L_trait=tkinter.Label(frame1_L_trait, text="Filtre :", bg=couleur_interface)
text4_L_trait=tkinter.Label(frame1_L_trait, text="Taille :", bg=couleur_interface)
text5_L_trait = tkinter.Label(frame1_L_trait, text="Ordre :", bg=couleur_interface)
text3_L_trait.grid(row=3, column=1, sticky=tkinter.W)
text4_L_trait.grid(row=3, column=3, sticky=tkinter.W)
text5_L_trait.grid(row=3, column=5, sticky=tkinter.W)
type_filtre_L_trait=tkinter.StringVar(value="Savitzky-Golay")
taille_filtre_L_trait=tkinter.IntVar(value=5)
ordre_filtre_L_trait=tkinter.IntVar(value=2)
#entree3_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_filtre_L_trait,
#                                     values=["Aucun", "Savitzky-Golay", "Median", "Passe-bas"])
entree3_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_filtre_L_trait,
                                     values=["Aucun", "Savitzky-Golay", "Median"])
entree4_L_trait=tkinter.Spinbox(frame1_L_trait, from_=3, to=199, increment=2, textvariable = taille_filtre_L_trait)
entree5_L_trait=tkinter.Spinbox(frame1_L_trait, from_=2, to=3, textvariable = ordre_filtre_L_trait)
entree3_L_trait.grid(row=3, column=2, columnspan=1)
entree4_L_trait.grid(row=3, column=4)
entree5_L_trait.grid(row=3, column=6)

text6_L_trait=tkinter.Label(frame1_L_trait, text="Fond :", bg=couleur_interface)
text7_L_trait=tkinter.Label(frame1_L_trait, text="Itérations :", bg=couleur_interface)
text8_L_trait=tkinter.Label(frame1_L_trait, text="LLS :", bg=couleur_interface)
text6_L_trait.grid(row=4, column=1, sticky=tkinter.W)
text7_L_trait.grid(row=4, column=3, sticky=tkinter.W)
text8_L_trait.grid(row=4, column=5, sticky=tkinter.W)
type_fond_L_trait=tkinter.StringVar(value="SNIP")
param1_fond_L_trait=tkinter.IntVar(value=20)
param2_fond_L_trait=tkinter.IntVar(value=10)
param3_fond_L_trait=tkinter.BooleanVar(value=True)
#entree6_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_fond_L_trait,
#                                     values=["Aucun", "Rolling ball", "SNIP", "Top-hat", "Peak filling"])
entree6_L_trait=tkinter.ttk.Combobox(frame1_L_trait, textvariable=type_fond_L_trait,
                                     values=["Aucun", "Rolling ball", "SNIP"])
entree7_L_trait=tkinter.Spinbox(frame1_L_trait, from_=3, to=100, textvariable=param1_fond_L_trait)
entree8_L_trait=tkinter.Spinbox(frame1_L_trait, from_=1, to=100, textvariable=param2_fond_L_trait)
entree8bis_L_trait=tkinter.Checkbutton(frame1_L_trait, text="LLS", variable=param3_fond_L_trait, bg=couleur_interface)
entree6_L_trait.grid(row=4, column=2, columnspan=1)
entree7_L_trait.grid(row=4, column=4)
entree8_L_trait.grid(row=4, column=6)
entree8_L_trait.grid_remove()
entree8bis_L_trait.grid(row=4, column=6)

frame1_1_L_trait=tkinter.Frame(frame1_L_trait, bg=couleur_interface)
frame1_1_L_trait.grid(row=1, column=7, rowspan=4, sticky=tkinter.N+tkinter.S)

text_zoom_L_trait=tkinter.Label(frame1_1_L_trait, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_trait.grid(row=1, column=1, sticky=tkinter.N)
variable_L_trait_zoom_inf=tkinter.DoubleVar(value=198)
variable_L_trait_zoom_sup=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_trait=tkinter.Spinbox(frame1_1_L_trait, from_=198, to=1013, increment=5,
                                        textvariable=variable_L_trait_zoom_inf,
                                        command=change_zoom_inf_L_trait, width=9)
entree_zoom_sup_L_trait=tkinter.Spinbox(frame1_1_L_trait, from_=198, to=1013, increment=5,
                                        textvariable=variable_L_trait_zoom_sup,
                                        command=change_zoom_sup_L_trait, width=9)
entree_zoom_inf_L_trait.grid(row=2, column=1, sticky=tkinter.N)
entree_zoom_sup_L_trait.grid(row=3, column=1, sticky=tkinter.N)

bouton_rep_L_trait=tkinter.Button(frame1_1_L_trait, text="Fichier",
                                  command=choix_fichier_L_trait, width=9, bg=couleur_interface)
bouton_visualisation_L_trait=tkinter.Button(frame1_1_L_trait, text="Visualisation",
                                            command = visualisation_L_trait, state="disable", width=9, bg=couleur_interface)
bouton_rep_L_trait.grid(row=4, column=1, sticky=tkinter.N)
bouton_visualisation_L_trait.grid(row=5, column=1, sticky=tkinter.N)

image_classification=tkinter.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")
bouton_classification_L_trait=tkinter.Button(frame1_1_L_trait, image=image_classification,
                                             command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_trait.grid(row=6, column=1, sticky=tkinter.S)

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
coche_image_brute_L_ext=tkinter.Checkbutton(frame2_1_L_trait, text="Appliquer sur\ntous les fichiers\ndu répertoire",
                                            variable=flag_tous_fichiers_L_trait, bg=couleur_interface)
coche_image_brute_L_ext.grid(row=1, column=1)

bouton_execute_L_trait=tkinter.Button(frame2_1_L_trait, text="Executer", state="disable",
                                      command = execute_L_trait , width=9, bg=couleur_interface)
bouton_execute_L_trait.grid(row=2, column=1)

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

frame1_L_ext.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
frame2_L_ext.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
frame3_L_ext.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

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

variable_L_ext_1=tkinter.DoubleVar(value=tableau_bornes_L_ext[0,0])
variable_L_ext_2=tkinter.DoubleVar(value=tableau_bornes_L_ext[0,1])
variable_L_ext_3=tkinter.DoubleVar( value=tableau_bornes_L_ext[1,0])
variable_L_ext_4=tkinter.DoubleVar(value=tableau_bornes_L_ext[1,1])
entree1_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_1, command=deplace_ligne0_1_L_ext)
entree2_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_2, command=deplace_ligne0_2_L_ext)
entree3_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_3, command=deplace_ligne0_3_L_ext)
entree4_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_4, command=deplace_ligne0_4_L_ext)
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
frame1_1_L_ext.grid(row=1, column=7, rowspan=3)

text_zoom_L_ext=tkinter.Label(frame1_1_L_ext, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_ext.grid(row=1, column=1)
variable_L_ext_zoom_inf=tkinter.DoubleVar(value=198)
variable_L_ext_zoom_sup=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_ext=tkinter.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_L_ext_zoom_inf, command=change_zoom_inf_L_ext, width=9)
entree_zoom_sup_L_ext=tkinter.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_L_ext_zoom_sup, command=change_zoom_sup_L_ext, width=9)
entree_zoom_inf_L_ext.grid(row=2, column=1)
entree_zoom_sup_L_ext.grid(row=3, column=1)

bouton_rep_L_ext=tkinter.Button(frame1_1_L_ext, text="Repertoire\nde travail" ,command=choix_rep_L_ext, width=9, bg=couleur_interface)
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
bouton_classification_L_ext.grid(row=8, column=1, sticky=tkinter.N)

###############################################################################
# 10- Interface graphique frame2_L_ext : création visues des résultats et aide à la sélection
###############################################################################
canevas1_L_ext=tkinter.Canvas(frame2_L_ext, width=500, height=200, bg="white")
canevas2_L_ext=tkinter.Canvas(frame2_L_ext, width=500, height=200, bg="white")
canevas1_L_ext.grid(row=1, column=1, columnspan=2)
canevas2_L_ext.grid(row=1, column=3, columnspan=2)

variable_L_ext_5=tkinter.DoubleVar(value=0)
variable_L_ext_6=tkinter.IntVar(value=0)
variable_L_ext_7=tkinter.DoubleVar(value=0)
variable_L_ext_8=tkinter.IntVar(value=0)
entree5_L_ext=tkinter.Spinbox(frame2_L_ext, from_=198, to=1013, textvariable=variable_L_ext_5, command=vars_5_6_to_coord1_L_ext, increment=0.5)
entree6_L_ext=tkinter.Spinbox(frame2_L_ext, from_=1, to=200, textvariable=variable_L_ext_6, command=vars_5_6_to_coord1_L_ext)
entree7_L_ext=tkinter.Spinbox(frame2_L_ext, from_=198, to=1013, textvariable=variable_L_ext_7, command=vars_7_8_to_coord2_L_ext, increment=0.5)
entree8_L_ext=tkinter.Spinbox(frame2_L_ext, from_=1, to=200, textvariable=variable_L_ext_8, command=vars_7_8_to_coord2_L_ext)
entree5_L_ext.grid(row=2, column=1)
entree6_L_ext.grid(row=2, column=2)
entree7_L_ext.grid(row=2, column=3)
entree8_L_ext.grid(row=2, column=4)

text5_L_ext = tkinter.Label(frame2_L_ext, text="Position x (nm)", bg=couleur_interface)
text6_L_ext = tkinter.Label(frame2_L_ext, text="Position y (n° de spectre)", bg=couleur_interface)
text7_L_ext = tkinter.Label(frame2_L_ext, text="Position x (nm)", bg=couleur_interface)
text8_L_ext = tkinter.Label(frame2_L_ext, text="Position y (n° de spectre)", bg=couleur_interface)
text5_L_ext.grid(row=3, column=1)
text6_L_ext.grid(row=3, column=2)
text7_L_ext.grid(row=3, column=3)
text8_L_ext.grid(row=3, column=4)

frame2_2_L_ext=tkinter.Frame(frame2_L_ext)
frame2_2_L_ext.grid(row=1, column=5, rowspan=3, sticky=tkinter.N)

flag_image_brute_L_ext=tkinter.BooleanVar(value=flag_image_brute_init_L_ext)
coche_image_brute_L_ext=tkinter.Checkbutton(frame2_2_L_ext, text="Image brute\nspectres non\nnormalisés", variable=flag_image_brute_L_ext, command=change_flag_image_brute_L_ext, bg=couleur_interface)
coche_image_brute_L_ext.grid(row=3, column=1)

ligne1_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
ligne1_hori_L_ext=canevas1_L_ext.create_line(0,y1_L_ext,500,y1_L_ext, fill="white")
ligne2_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
ligne2_hori_L_ext=canevas1_L_ext.create_line(0,y1_L_ext,500,y1_L_ext, fill="white")

affiche_lignes_spectre_L_ext()

###############################################################################
# 11- Interface graphique frame3_L_ext : création selection des spectres à moyenner
###############################################################################
text9_L_ext=tkinter.Label(frame3_L_ext, text="Du spectre n° :", bg=couleur_interface)
text10_L_ext=tkinter.Label(frame3_L_ext, text="Au spectre n° :", bg=couleur_interface)
text9_L_ext.grid(row=1, column=1)
text10_L_ext.grid(row=1, column=3)

variable_L_ext_9=tkinter.IntVar(value=0)
variable_L_ext_10=tkinter.IntVar(value=0)
entree9_L_ext=tkinter.Spinbox(frame3_L_ext,from_=1, to=200, textvariable=variable_L_ext_9, command=retro_action_entree10_L_ext)
entree10_L_ext=tkinter.Spinbox(frame3_L_ext,from_=1, to=200, textvariable=variable_L_ext_10, command=retro_action_entree9_L_ext)
entree9_L_ext.grid(row=1, column=2)
entree10_L_ext.grid(row=1, column=4)

frame3_1_L_ext=tkinter.Frame(frame3_L_ext, bg=couleur_interface)
frame3_1_L_ext.grid(row=1, column=5)
bouton_extraction_L_ext=tkinter.Button(frame3_1_L_ext, text="Extraction", state="disable", command=creation_spectre_moyen_L_ext, width=9, bg=couleur_interface)
bouton_extraction_L_ext.grid(row=1, column=1)

canevas3_L_ext=tkinter.Canvas(frame3_L_ext, width=500, height=200, bg="white")
canevas4_L_ext=tkinter.Canvas(frame3_L_ext, width=500, height=200, bg="white")
canevas3_L_ext.grid(row=3, column=1, columnspan=2)
canevas4_L_ext.grid(row=3, column=3, columnspan=2)

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
# 8- Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###############################################################################
frame1_L_comp=tkinter.Frame(onglet3,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame2_L_comp=tkinter.Frame(onglet3,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)
frame3_L_comp=tkinter.Frame(onglet3,borderwidth=2,relief=tkinter.RAISED, bg=couleur_interface)

frame1_L_comp.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
frame2_L_comp.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
frame3_L_comp.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# 9- Interface graphique frame1_L_comp : création selection répertoire, affiche spectre et bouton executer
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
entree1_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_1_L_comp, command=deplace_ligne0_1_L_comp)
entree2_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_2_L_comp, command=deplace_ligne0_2_L_comp)
entree3_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5,textvariable=variable_3_L_comp, command=deplace_ligne0_3_L_comp)
entree4_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5,textvariable=variable_4_L_comp, command=deplace_ligne0_4_L_comp)
entree1_L_comp.grid(row=2, column=2)
entree2_L_comp.grid(row=2, column=4)
entree3_L_comp.grid(row=3, column=2)
entree4_L_comp.grid(row=3, column=4)

flag_denominateur_L_comp=tkinter.IntVar(value=flag_denominateur_init_L_comp)
coche_denominateur_L_comp=tkinter.Checkbutton(frame1_L_comp, text="Dénominateur ?", variable=flag_denominateur_L_comp, command=change_flag_denominateur_L_comp, bg=couleur_interface)
coche_denominateur_L_comp.grid(row=3, column=5)

bouton_reset_L_comp=tkinter.Button(frame1_L_comp, text="Reset", command=reset_tableau_L_comp, width=9, bg=couleur_interface)
bouton_reset_L_comp.grid(row=2, column=6, rowspan=2)

frame1_1_L_comp=tkinter.Frame(frame1_L_comp, bg=couleur_interface)
frame1_1_L_comp.grid(row=1, column=7, rowspan=3)

text_zoom_L_comp=tkinter.Label(frame1_1_L_comp, text="Zoom : ", width=9, bg=couleur_interface)
text_zoom_L_comp.grid(row=1, column=1)
variable_zoom_inf_L_comp=tkinter.DoubleVar(value=198)
variable_zoom_sup_L_comp=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_comp=tkinter.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_inf_L_comp, command=change_zoom_inf_L_comp, width=9)
entree_zoom_sup_L_comp=tkinter.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_sup_L_comp, command=change_zoom_sup_L_comp, width=9)
entree_zoom_inf_L_comp.grid(row=2, column=1)
entree_zoom_sup_L_comp.grid(row=3, column=1)

bouton_rep_L_comp=tkinter.Button(frame1_1_L_comp, text="Repertoire\nde travail" ,command=choix_rep_L_comp, width=9, bg=couleur_interface)
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
bouton_classification_L_comp=tkinter.Button(frame1_1_L_comp, image= image_classification, command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_comp.grid(row=8, column=1, sticky=tkinter.N)

###############################################################################
# 10- Interface graphique frame2_L_comp : affichage des spectres classés
###############################################################################
canevas1_L_comp=tkinter.Canvas(frame2_L_comp, width=1000, height=200, bg="white")
canevas1_L_comp.grid(row=1, column=1, columnspan=2)

variable_5_L_comp=tkinter.DoubleVar(value=0)
variable_6_L_comp=tkinter.IntVar(value=0)
entree5_L_comp=tkinter.Spinbox(frame2_L_comp, from_=198, to=1013, textvariable=variable_5_L_comp, command=vars_5_6_to_coord1_L_comp, increment=0.5)
entree6_L_comp=tkinter.Spinbox(frame2_L_comp, from_=1, to=100, textvariable=variable_6_L_comp, command=vars_5_6_to_coord1_L_comp)
entree5_L_comp.grid(row=2, column=1)
entree6_L_comp.grid(row=2, column=2)

text5_L_comp = tkinter.Label(frame2_L_comp, text="Position x (nm)", bg=couleur_interface)
text6_L_comp = tkinter.Label(frame2_L_comp, text="Position y (n° de spectre)", bg=couleur_interface)
text5_L_comp.grid(row=3, column=1)
text6_L_comp.grid(row=3, column=2)

frame2_2_L_comp=tkinter.Frame(frame2_L_comp)
frame2_2_L_comp.grid(row=1, column=5, rowspan=3, sticky=tkinter.N)

text7_L_comp=tkinter.Label(frame2_2_L_comp, text="Type de\nfichiers à\ncomparer :")
text7_L_comp.grid(row=1, column=1)

type_extension_L_comp=tkinter.StringVar(value="*.tsv")
type_extension_combobox_L_comp=tkinter.ttk.Combobox(frame2_2_L_comp, textvariable=type_extension_L_comp, width=10, values=["*.mean", "*.tsv"])
type_extension_combobox_L_comp.grid(row=2, column=1)

text8_L_comp=tkinter.Label(frame2_2_L_comp, text="\n*.mean :\nspectres moyens\nd'échantillons\ndifférents\n\n*.tsv :\nspectres du même\néchantillon")
text8_L_comp.grid(row=3, column=1)

ligne1_vert_L_comp=canevas1_L_comp.create_line(x1_L_comp,0,x1_L_comp,200, fill="white")
ligne1_hori_L_comp=canevas1_L_comp.create_line(0,y1_L_comp,500,y1_L_comp, fill="white")

affiche_lignes_spectre_L_comp()

###############################################################################
# 11- Interface graphique frame3_L_comp : affichage des résultats sous forme de TreeView
###############################################################################
tree_resultats_L_comp=tkinter.ttk.Treeview(frame3_L_comp, columns=(1,2,3), height = 10 ,show = "headings")
tree_resultats_L_comp.column(1, width=10)
tree_resultats_L_comp.column(2, width=600)
tree_resultats_L_comp.column(1, width=200)
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
# 12- Interface graphique : gestion de évènements
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





###############################################################################
###############################################################################
# Interface graphique LIBStick : classification périodique
###############################################################################
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

###############################################################################
#  Interface graphique : gestion du redimentionnement de la fenêtre principale
###############################################################################
canevas_scroll.create_window(0, 0, anchor='nw', window=frame_scroll)
frame_scroll.update_idletasks()
canevas_scroll.config(scrollregion=canevas_scroll.bbox("all"))

fenetre_principale.mainloop()
