#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 12:32:41 2020
Programme principal et interface graphique de LIBStick
@author: yannick
"""
# pylint: disable=invalid-name, line-too-long, global-statement, unused-argument

# import tkinter, tkinter.filedialog, tkinter.ttk
# from LIBStick_IHM_extraction import *

import os, sys
import time
import configparser
import pathlib
import gettext
import math
import numpy as np
import pandas as pd
import PIL.Image
import PIL.ImageTk

import tkinter as tk
import tkinter.filedialog as fd
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
import tkinter.font as font
import tkinter.messagebox as messagebox
# import ttkwidgets

import LIBStick_outils
import LIBStick_traitements_spectres
import LIBStick_extraction_spectres
import LIBStick_comp_spectres
import LIBStick_ACP


###################################################################################################
# initialisations générales et définitions des variables globales
###################################################################################################
NOM_OS = os.name
rep_LIBStick = os.getcwd()

# interface graphique
flag_change_fenetre = False
largeur_fenetre_principale = 1155
hauteur_fenetre_principale = 750
largeur_canevas_spectres = 1000
hauteur_canevas_spectres = 200

COULEUR_INTERFACE = "papaya whip"
# COULEUR_INTERFACE="linen"
# COULEUR_INTERFACE="light grey"
LARGEUR_LIGNES = 2
# taille_font= 10
if NOM_OS == "posix" :
    TAILLE_CASE = [2,2]
if NOM_OS == "nt" :
    TAILLE_CASE = [4, 2]
TAILLE_FONT_CLASSIFICATION = 8

# textes d'affichage de la longueur d'onde
lambda_texte_spectre_0_L_trait = lambda_texte_spectre_1_L_trait = 0
lambda_texte_spectre_L_ext = 0
lambda_texte_spectre_L_comp = 0
lambda_texte_spectre_0_L_ACP = lambda_texte_spectre_1_L_ACP = 0

# noms des fichiers et répertoires, listes des fichiers, nombre de fichiers
nom_echantillon_L_ext = ""
nom_fichier_seul_L_trait = nom_fichier_seul_L_ext = nom_fichier_seul_L_comp = nom_fichier_seul_L_ACP = ""
rep_travail_L_trait = rep_travail_L_ext = rep_travail_L_comp = rep_travail_L_ACP = ""
liste_fichiers_L_trait = liste_fichiers_L_ext = liste_fichiers_L_comp = liste_fichiers_L_ACP = []
liste_bool_L_ext = []
nombre_fichiers_L_trait = nombre_fichiers_L_ext = nombre_fichiers_L_comp = nombre_fichiers_L_ACP = 1
nombre_fichiers_avant_L_ext = 1

# gestion des zooms
minimum_spectre_L_trait = maximum_spectre_L_trait = minimum_spectre_lineaire_L_trait = 0
maximum_spectre_corrige_L_trait = 0
# maximum_spectre_ancien_L_ext = 0
# maximum_spectre_ancien_L_comp = 0
# maximum_spectre_ancien_L_ACP = 0

# identifiants des lignes
ligne0_1_L_trait = ligne0_2_L_trait = 0
ligne0_1_L_ext = ligne0_2_L_ext = ligne0_3_L_ext = ligne0_4_L_ext = 0
ligne0_1_L_comp = ligne0_2_L_comp = ligne0_3_L_comp = ligne0_4_L_comp = 0
ligne0_1_L_ACP = ligne0_2_L_ACP = 0

# position des traits verticaux sur les spectres
ligne_position_0_x_L_trait = ligne_position_1_x_L_trait = 0
ligne_position_0_y_L_trait = ligne_position_1_y_L_trait = 0
ligne_position_x_L_ext = ligne_position_y_L_ext = 0
ligne1_vert_L_ext = ligne1_hori_L_ext = 0
ligne2_vert_L_ext = ligne2_hori_L_ext = 0
ligne_position_x_L_comp = ligne_position_y_L_comp = 0
ligne1_vert_L_comp = ligne1_hori_L_comp = 0
ligne_position_x_L_ACP = ligne_position_y_L_ACP = ligne_position_1_L_ACP = 0

# identifiants des photos
image1_zoom_L_ext = image2_zoom_L_ext = image_zoom_L_comp = 0
# photo1_L_ext = photo2_L_ext = photo_L_comp = 0

# Dataframes
DataFrame_resultats_L_comp = DataFrame_complet_L_ACP = dataframe_facteurs_ACP_L_ACP = pd.DataFrame()
spectre_dim1_L_ACP = spectre_dim2_L_ACP = spectre_dim3_L_ACP = pd.DataFrame()
DataFrame_element_L_ele = pd.DataFrame()

# identifiants des fenêtres
fenetre_label_L_ACP = 0
fenetre_classification_L_ele = 0

# divers
symbole_L_ele = ""
old_time = time.time()


class CaseConfigParser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr


config = CaseConfigParser()
config.read("LIBStick.ini")


def lit_section_fichier_ini(section):
    """
    Lit un section du fichier LIBStick.ini
    """
    dictionnaire = {}
    options = config.options(section)
    for option in options:
        try:
            dictionnaire[option] = config.get(section, option)
            # if dictionnaire[option] == -1:
            #    DebugPrint("skip: %s" % option)
        except UserWarning:
            print("exception on %s!" % option)
            dictionnaire[option] = None
    return dictionnaire


def reset_fichier_ini():
    """
    Ré-initialise les valeurs par défaut du fichier LIBStick.ini
    à l'aide du fichier LIBStick_reset.ini
    """
    fichier = open(rep_LIBStick + "/LIBStick.ini", "w", encoding="utf-8")
    fichier_reset = open(rep_LIBStick+"/LIBStick_reset.ini", "r", encoding="utf-8")
    lignes = fichier_reset.readlines()
    fichier.writelines(lignes)
    fichier.close()
    fichier_reset.close()
    messagebox.showinfo(title=_("Attention !"),
                                message=_("Veuillez redémarrer LIBStick pour retrouver les paramètres par défaut."))


def charge_param_langue():
    """
    Lit la langue au démarage du logiciel de la section LIBStick_langue
    du fichier LIBStick.ini par la fonction lit_section_fichier_ini(section)
    """
    dictionnaire_ini_langue = lit_section_fichier_ini("LIBStick_langue")
    langue = dictionnaire_ini_langue["langue"]
    return langue

langue_LIBStick = charge_param_langue()
try:
    # gettext.find(langue_LIBStick)
    traduction = gettext.translation(
        langue_LIBStick, localedir="locale", languages=[langue_LIBStick])
    traduction.install()
    _ = traduction.gettext
except UnicodeTranslateError:
    gettext.install("fr")
    _ = gettext.gettext


def charge_param_interface():
    """
    Lit le style au démarage du logiciel de la section LIBStick_interface
    du fichier LIBStick.ini par la fonction lit_section_fichier_ini(section)
    """
    dictionnaire_ini_interface = lit_section_fichier_ini("LIBStick_interface")
    style_interface = dictionnaire_ini_interface["style"]
    flag_style = dictionnaire_ini_interface["flag_couleur_LIBStick"]
    return style_interface, flag_style

style_interface_LIBStick, flag_style_LIBStick_ini = charge_param_interface()
# print (style_interface_LIBStick)
# print (flag_style_LIBStick_ini)


def ecrit_fichier_ini():
    """
    Sauvegarde tous les paramètres actuels du logiciel dans le fichier
    LIBStick.ini sauf la langue
    """
    creation_tab_bornes_L_ext()
    creation_tab_bornes_L_comp()
    fichier = open(rep_LIBStick + "/LIBStick.ini", "w", encoding="utf-8")
    dico_sauvegarde_L_ext = {"flag_zone2_L_ext": "flag_zone2_L_ext.get()",
                             "flag_2D_L_ext": "flag_2D_L_ext.get()",
                             "flag_3D_L_ext": "flag_3D_L_ext.get()",
                             "flag_image_brute_L_ext": "flag_image_brute_L_ext.get()",
                             "borne_zone1_inf_L_ext": "tableau_bornes_L_ext[0,0]",
                             "borne_zone1_sup_L_ext": "tableau_bornes_L_ext[0,1]",
                             "borne_zone2_inf_L_ext": "tableau_bornes_L_ext[1,0]",
                             "borne_zone2_sup_L_ext": "tableau_bornes_L_ext[1,1]",
                             "rep_travail_L_ext": "rep_travail_L_ext"
                             }
    dico_sauvegarde_L_comp = {"flag_denominateur_L_comp": "flag_denominateur_L_comp.get()",
                              "flag_2D_L_comp": "flag_2D_L_comp.get()",
                              "flag_3D_L_comp": "flag_3D_L_comp.get()",
                              "flag_traitement_L_comp": "flag_traitement_L_comp.get()",
                              "flag_stat_L_comp": "flag_stat_L_comp.get()",
                              "borne_zone1_inf_L_comp": "tableau_bornes_L_comp[0,0]",
                              "borne_zone1_sup_L_comp": "tableau_bornes_L_comp[0,1]",
                              "borne_zone2_inf_L_comp": "tableau_bornes_L_comp[1,0]",
                              "borne_zone2_sup_L_comp": "tableau_bornes_L_comp[1,1]",
                              "rep_travail_L_comp": "rep_travail_L_comp"
                              }
    for section in config.sections():
        if section == "LIBStick_extraction":
            for option, action in dico_sauvegarde_L_ext.items():
                config.set(section, str(option), str(eval(action)))
        if section == "LIBStick_compare":
            for option, action in dico_sauvegarde_L_comp.items():
                config.set(section, str(option), str(eval(action)))
    config.write(fichier)
    fichier.close()


def ecrit_param_langue():
    """
    Sauvegarde dans le fichier LIBStick.ini la langue
    """
    fichier = open(rep_LIBStick + "/LIBStick.ini", "w", encoding="utf-8")
    config.set("LIBStick_langue", "langue", langue_menu.get())
    config.write(fichier)
    fichier.close()


def ecrit_param_interface():
    """
    Sauvegarde dans le fichier LIBStick.ini le style de l'interface
    """
    fichier = open(rep_LIBStick + "/LIBStick.ini", "w", encoding="utf-8")
    config.set("LIBStick_interface", "flag_couleur_LIBStick", str(flag_style_LIBStick_couleur.get()))
    config.set("LIBStick_interface", "style", str(style_menu.get()))
    config.write(fichier)
    fichier.close()


def fenetre_pricipale_en_avant():
    """
    Met au premier plan la fenetre principale mais ne la bloque pas au premier plan
    """
    fenetre_principale.attributes("-topmost", True)
    fenetre_principale.attributes("-topmost", False)


def change_taille_fenetre(event):
    """
    Applique des changements d'affichage lors du changement de la taille de la fenêtre
    """
    global largeur_canevas_spectres
    global hauteur_canevas_spectres
    # global old_time
    if fenetre_principale.winfo_width() < 1150 :
        largeur_canevas_spectres = 1000
    else :
        largeur_canevas_spectres = 1000 + fenetre_principale.winfo_width() - 1150
    if fenetre_principale.winfo_height() < 750 :
        hauteur_canevas_spectres = 200
    else :
        hauteur_canevas_spectres = 200 + (fenetre_principale.winfo_height() - 750)/2
    # cur_time = time.time()
    # if (cur_time - old_time) > 0.001 :
    #     applique_change_taille_fenetre()
    #     old_time = time.time()
    applique_change_taille_fenetre()


def applique_change_taille_fenetre():
    global old_time
    canevas0_L_trait.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres+170)
    canevas1_L_trait.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres)
    canevas0_L_ext.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres)
    canevas1_L_ext.config(width=largeur_canevas_spectres/2, height=hauteur_canevas_spectres)
    canevas2_L_ext.config(width=largeur_canevas_spectres/2, height=hauteur_canevas_spectres)
    canevas3_L_ext.config(width=largeur_canevas_spectres/2, height=200)
    canevas4_L_ext.config(width=largeur_canevas_spectres/2, height=200)
    canevas0_L_comp.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres)
    canevas1_L_comp.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres)
    canevas0_L_ACP.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres)
    canevas1_L_ACP.config(width=largeur_canevas_spectres, height=hauteur_canevas_spectres)

    cur_time = time.time()
    if (cur_time - old_time) > 0.1 :
        remplit_fenetres()
        old_time = time.time()


def remplit_fenetres():
    global flag_change_fenetre
    ID_onglet = onglets.index("current")
    if ID_onglet == 0:
        try :
            flag_change_fenetre = True
            affiche_spectre_L_trait()
            flag_change_fenetre = False
        except :
            pass
        try :
            flag_change_fenetre = True
            affiche_spectre_corrige_L_trait()
            flag_change_fenetre = False
        except :
            pass
        try :
            flag_change_fenetre = True
            affiche_fond_L_trait()
            flag_change_fenetre = False
        except :
            pass
    if ID_onglet == 1:
        try :
            flag_change_fenetre = True
            affiche_spectre_L_ext()
            flag_change_fenetre = False
        except :
            pass
        try :
            affiche_image_L_ext()
        except :
            pass
        try :
            if flag_zone2_L_ext.get() == 0 :
                affiche_spectre_moyen1_L_ext()
            else :
                affiche_spectre_moyen1_L_ext()
                affiche_spectre_moyen2_L_ext()
        except :
            pass
    if ID_onglet == 2:
        try :
            flag_change_fenetre = True
            affiche_spectre_L_comp()
            flag_change_fenetre = False
        except :
            pass
        try :
            affiche_image_L_comp()
        except :
            pass
    if ID_onglet == 3:
        try :
            flag_change_fenetre = True
            affiche_spectre_L_ACP()
            flag_change_fenetre = False
        except :
            pass
        try :
            flag_change_fenetre = True
            affiche_spectres_var_ACP_L_ACP()
            flag_change_fenetre = False
        except :
            pass


def redemarre_programme():
    """Restarts the current program.
    Note: this function does not return. Any cleanup action (like
    saving data) must be done before calling this function."""
    python = sys.executable
    os.execl(python, python, * sys.argv)


###################################################################################################
###################################################################################################
# Fonctions LIBStick_IHM_traitement : onglet 1
###################################################################################################
###################################################################################################
def __________L_trait__________():
    """Fonctions LIBStick_IHM_traitement : onglet 1"""
###################################################################################################
###################################################################################################


###################################################################################################
# initialisations
###################################################################################################
def charge_param_L_trait():
    """
    Initialisation des paramètres de traitement
    """
    dictionnaire_ini_L_trait = lit_section_fichier_ini("LIBStick_traitement")
    rep_travail = dictionnaire_ini_L_trait["rep_travail_L_trait"]
    return rep_travail


rep_travail_L_trait = charge_param_L_trait()

# limites min et max de l'affichage du spectre
limites_spectre_x_L_trait = np.array([198.0, 1013.0])
# limites de l'affichage du spectre à l'écran
limites_affichage_spectre_L_trait = np.array([198.0, 1013.0])
coord_zoom_L_trait = np.array([198, 0, 1013, 0])
delta_limites_L_trait = limites_affichage_spectre_L_trait[1]-limites_affichage_spectre_L_trait[0]

flag_premier_lamda_L_trait = True
flag_dezoom_L_trait = False
flag_bouton_zoom_L_trait = False
flag_dezoom_L_ext = False
flag_bouton_zoom_L_ext = False
flag_dezoom_L_comp = False
flag_bouton_zoom_L_comp = False
flag_dezoom_L_ACP = False
flag_bouton_zoom_L_ACP = False
# flag_premier_fond_L_trait=True

spectre_entier_L_trait = np.zeros((0, 2))
fond_continu_L_trait = np.zeros((0, 2))
spectre_corrige_L_trait = np.zeros((0, 2))
tableau_bornes_L_trait = np.array([300.0, 608.0])


def affiche_nom_spectre_onglet1():
    """
    Affichage de la version de LIBStick et du nom du spectre à l'écran pour l'onglet Traitement
    """
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_trait)


###################################################################################################
# fonctions traitement des données
###################################################################################################
def creation_tab_bornes_L_trait():
    """
    Lecture des Spinbox et création du tableau des bornes du traitement du spectre
    """
    tableau_bornes_L_trait[0] = variable_1_L_trait.get()
    tableau_bornes_L_trait[1] = variable_2_L_trait.get()
    return tableau_bornes_L_trait


def choix_fichier_L_trait():
    """
    Ouverture/affichage d'un fichier spectre et récupération du chemin du répertoire. Bouton Fichier
    """
    global nom_fichier_seul_L_trait
    global rep_travail_L_trait
    global liste_fichiers_L_trait
    global nombre_fichiers_L_trait
    nom_fichier_L_trait = fd.askopenfilename(initialdir=rep_travail_L_trait,
                                                             title=_('Choisissez un fichier spectre'),
                                                             filetypes=(("fichiers IVEA", "*.asc"),
                                                                        ("fichiers SciAps", "*.csv"),
                                                                        ("fichiers LIBStick", "*.tsv"),
                                                                        ("fichiers LIBStick moyen", "*.mean")))
    nom_fichier_seul_L_trait = os.path.basename(nom_fichier_L_trait)
    type_fichier_L_trait.set(pathlib.Path(nom_fichier_seul_L_trait).suffix)
    rep_travail_L_trait = os.path.dirname(nom_fichier_L_trait)
    liste_fichiers_L_trait = LIBStick_outils.creation_liste_fichiers(rep_travail_L_trait,
                                                                     type_fichier_L_trait.get())
    nombre_fichiers_L_trait = len(liste_fichiers_L_trait)
    entree_spectre_L_trait.configure(to=nombre_fichiers_L_trait)
    lit_affiche_spectre_L_trait()
    bouton_visualisation_L_trait.configure(state="normal")
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_trait)


def visualisation_L_trait():
    """
    Calcul et affichage du spectre traité. Bouton Visualisation
    """
    global fond_continu_L_trait
    global spectre_corrige_L_trait
    global tableau_bornes_L_trait
    tableau_bornes_L_trait = creation_tab_bornes_L_trait()
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
    spectre_corrige_L_trait = LIBStick_traitements_spectres.creation_spectre_corrige(spectre_filtre_L_trait,
                                                                                     fond_continu_L_trait)
    affiche_spectre_L_trait()
    affiche_fond_L_trait()
    affiche_spectre_corrige_L_trait()
    bouton_execute_L_trait.configure(state="normal")


def execute_L_trait():
    """
    Traitement et sauvegarde du/des spectre(s). Bouton Executer
    """
    flag_tous_fichiers = flag_tous_fichiers_L_trait.get()
    flag_sauve_fond = flag_sauve_fond_L_trait.get()
    if flag_tous_fichiers is False:
        LIBStick_traitements_spectres.execute(rep_travail_L_trait, spectre_corrige_L_trait,
                                              fond_continu_L_trait, nom_fichier_seul_L_trait,
                                              flag_sauve_fond)
    if flag_tous_fichiers is True:
        LIBStick_traitements_spectres.execute_en_bloc(rep_travail_L_trait, type_fichier_L_trait.get(),
                                                      tableau_bornes_L_trait, type_filtre_L_trait.get(),
                                                      taille_filtre_L_trait.get(), ordre_filtre_L_trait.get(),
                                                      derivee_filtre_L_trait.get(), type_fond_L_trait.get(),
                                                      param1_fond_L_trait.get(), param2_fond_L_trait.get(),
                                                      param3_fond_L_trait.get(), flag_sauve_fond)


###################################################################################################
# fonctions graphiques du caneva du spectre (frame1_L_trait)
###################################################################################################
def lit_affiche_spectre_L_trait():
    """
    Lecture d'un fichier spectre et affichage du spectre brut.
    """
    global spectre_entier_L_trait
    global limites_spectre_x_L_trait, limites_spectre_y_L_trait
    global maximum_spectre_L_trait, maximum_spectre_corrige_L_trait
    global fond_continu_L_trait
    os.chdir(rep_travail_L_trait)
    spectre_entier_L_trait = LIBStick_outils.lit_spectre(nom_fichier_seul_L_trait,
                                                         type_fichier_L_trait.get())
    limites_spectre_x_L_trait, limites_spectre_y_L_trait = lit_limites_L_trait(spectre_entier_L_trait)
    maximum_spectre_L_trait = maximum_spectre_corrige_L_trait = limites_spectre_y_L_trait[1]
    affiche_spectre_L_trait()
    fond_continu_L_trait = np.zeros((spectre_entier_L_trait.shape[0], 2))


def lit_limites_L_trait(spectre):
    """
    Lit les limites hautes et basses d'un spectre
    et fixe les valeurs du zoom à ces valeurs min et max
    """
    # tableau_abscisses = spectre[:, 0]
    # tableau_ordonnees = spectre[:, 1].max()
    limites_spectre_x = np.zeros((2))
    limites_spectre_x[0] = spectre[0, 0]             # lit les abscisses min et max du spectre
    limites_spectre_x[1] = spectre[-1, 0]
    limites_spectre_y = np.zeros((2))
    limites_spectre_y[0] = spectre[:, 1].min()             # lit les valeurs min et max du spectre
    limites_spectre_y[1] = spectre[:, 1].max()
    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_inf_L_trait.set(limites_spectre_x[0])
    variable_zoom_sup_L_trait.set(limites_spectre_x[1])
    # fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_inf_L_trait.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree_zoom_sup_L_trait.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    # entree_zoom_inf_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    # entree_zoom_sup_L_trait.configure(from_=limites_spectre[0], to=limites_spectre[1])
    entree1_L_trait.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree2_L_trait.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    return limites_spectre_x,limites_spectre_y


def affiche_lambda_L_trait(event):
    """
    Affiche la valeur de la longueur d'onde sur les spectres
    des canevas 0 et 1 et dans la zone de texte dédiée
    """
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    if flag_premier_lamda_L_trait is False:
        canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
        canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
    l = event.x*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
    lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_trait = False


def affiche_position_souris_0_L_trait(event):
    """
    Affiche la position du curseur sur les canevas 0 et 1 lors du déplacement
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_0_x_L_trait
    global ligne_position_1_x_L_trait
    global ligne_position_0_y_L_trait
    global ligne_position_1_y_L_trait
    canevas0_L_trait.delete(ligne_position_0_x_L_trait)
    canevas0_L_trait.delete(ligne_position_0_y_L_trait)
    ligne_position_0_x_L_trait = canevas0_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres+170, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    canevas1_L_trait.delete(ligne_position_1_x_L_trait)
    canevas1_L_trait.delete(ligne_position_1_y_L_trait)
    ligne_position_1_x_L_trait = canevas1_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ratio_y0 = event.y/(hauteur_canevas_spectres+170)
        ligne_position_1_y_L_trait = canevas1_L_trait.create_line(0, ratio_y0*hauteur_canevas_spectres,
                                                                  largeur_canevas_spectres, ratio_y0*hauteur_canevas_spectres,
                                                                  fill="green")


def affiche_position_souris_motion_0_L_trait(event):
    """
    Affiche la position du curseur et la valeur de lambda
    sur les canevas 0 et 1 lors du déplacement avec clic droit maintenu
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_0_x_L_trait
    global ligne_position_1_x_L_trait
    global ligne_position_0_y_L_trait
    global ligne_position_1_y_L_trait
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    canevas0_L_trait.delete(ligne_position_0_x_L_trait)
    canevas0_L_trait.delete(ligne_position_0_y_L_trait)
    ligne_position_0_x_L_trait = canevas0_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres+170, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    canevas1_L_trait.delete(ligne_position_1_x_L_trait)
    canevas1_L_trait.delete(ligne_position_1_y_L_trait)
    ligne_position_1_x_L_trait = canevas1_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ratio_y0 = event.y/(hauteur_canevas_spectres+170)
        ligne_position_1_y_L_trait = canevas1_L_trait.create_line(0, ratio_y0*hauteur_canevas_spectres,
                                                                  largeur_canevas_spectres, ratio_y0*hauteur_canevas_spectres,
                                                                  fill="green")
    if flag_premier_lamda_L_trait is False:
        canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
        canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
    l = event.x*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
    lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_trait = False


def affiche_spectre_L_trait():
    """
    Affichage du spectre dans le canevas 0 avec gestion du zoom y auto ou non
    """
    global limites_affichage_spectre_L_trait
    global delta_limites_L_trait
    global minimum_spectre_lineaire_L_trait
    global minimum_spectre_L_trait
    global maximum_spectre_L_trait
    global flag_echelle_log_L_trait
    limites_affichage_spectre_L_trait[0] = variable_zoom_inf_L_trait.get()
    limites_affichage_spectre_L_trait[1] = variable_zoom_sup_L_trait.get()
    # gestion du zoom avec y personnalisé
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_trait is False and flag_bouton_zoom_L_trait is False :
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        minimum_spectre_L_trait = spectre[:, 1].min()
        coord_y_min = min(coord_zoom_L_trait[1],coord_zoom_L_trait[3])
        coord_y_min = (coord_y_min*(hauteur_canevas_spectres+170)/hauteur_canevas_spectres)
        # print("coord_y0_min = " + str(coord_y_min))
        ratio_y_0_max = (hauteur_canevas_spectres+170-coord_y_min)/(hauteur_canevas_spectres+170)
        if  flag_change_fenetre is False :
            maximum = maximum_spectre_L_trait * ratio_y_0_max
            # maximum = (maximum_spectre_L_trait-minimum_spectre_L_trait) * ratio_y_0_max
            maximum_spectre_L_trait = maximum
        else :
            maximum = maximum_spectre_L_trait

        delta_limites_L_trait = limites_affichage_spectre_L_trait[1] - limites_affichage_spectre_L_trait[0]
        canevas0_L_trait.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_trait.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_trait = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum_spectre_L_trait = minimum = spectre[:, 1].min()

    # gestion du zoom avec y personnalisé par les boutons de zoom
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_trait is False and flag_bouton_zoom_L_trait is True:
        maximum = maximum_spectre_L_trait
        delta_limites_L_trait = limites_affichage_spectre_L_trait[1] -  limites_affichage_spectre_L_trait[0]
        canevas0_L_trait.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_trait.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_trait = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum_spectre_L_trait = minimum = spectre[:, 1].min()

    # gestion du zoom avec y automatique
    if flag_zoom_auto_y.get() is True or flag_dezoom_L_trait is True:
        delta_limites_L_trait = limites_affichage_spectre_L_trait[1] - limites_affichage_spectre_L_trait[0]
        canevas0_L_trait.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_trait.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_trait = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum_spectre_L_trait = minimum = spectre[:, 1].min()
        maximum_spectre_L_trait = maximum = spectre[:, 1].max()

    # dessin du spectre
    spectre[:, 1] = (hauteur_canevas_spectres+170-(spectre[:, 1] - minimum)*(hauteur_canevas_spectres+170)/(maximum - minimum))
    spectre[:, 0] = (spectre[:, 0] - limites_affichage_spectre_L_trait[0]) * \
        largeur_canevas_spectres/delta_limites_L_trait
    for i in range(len(spectre) - 1):
        canevas0_L_trait.create_line(spectre[i, 0], spectre[i, 1], spectre[i+1, 0], spectre[i+1, 1])
    affiche_lignes_spectre_L_trait()


def affiche_fond_L_trait():
    """
    Affichage du fond continu du spectre dans le canevas 0
    """
    limites_affichage_spectre_L_trait[0] = variable_zoom_inf_L_trait.get()
    limites_affichage_spectre_L_trait[1] = variable_zoom_sup_L_trait.get()
    spectre = np.zeros((0, 2))
    for ligne in fond_continu_L_trait:
        if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
            spectre = np.row_stack((spectre, ligne))
    minimum = minimum_spectre_L_trait
    maximum = maximum_spectre_L_trait
    if flag_echelle_log_L_trait.get() == True :
        spectre[:,1] = np.log(spectre[:,1]-minimum_spectre_lineaire_L_trait)
    spectre[:, 1] = (hauteur_canevas_spectres+170-(spectre[:, 1] - minimum)*(hauteur_canevas_spectres+170)/(maximum - minimum))
    spectre[:, 0] = (spectre[:, 0] - limites_affichage_spectre_L_trait[0]) * \
        largeur_canevas_spectres/delta_limites_L_trait
    for i in range(len(spectre) - 1):
        canevas0_L_trait.create_line(spectre[i, 0], spectre[i, 1],
                                     spectre[i+1, 0], spectre[i+1, 1], fill="blue")
    # flag_premier_fond_L_trait = False


def mise_a_jour_affichage_L_trait() :
    affiche_spectre_L_trait()
    affiche_fond_L_trait()


def affiche_lignes_spectre_L_trait():
    """
    Affichages des limites du traitement sur le spectre sous forme de deux lignes
    rouges verticales. Les valeurs sont fixées par les spinbox borne inf. et borne sup.
    """
    global ligne0_1_L_trait
    global ligne0_2_L_trait
    x_ligne0_1 = ((variable_1_L_trait.get() -
                   limites_affichage_spectre_L_trait[0])*largeur_canevas_spectres/delta_limites_L_trait)
    x_ligne0_2 = ((variable_2_L_trait.get() -
                   limites_affichage_spectre_L_trait[0])*largeur_canevas_spectres/delta_limites_L_trait)
    ligne0_1_L_trait = canevas0_L_trait.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres+170, fill="red", width=LARGEUR_LIGNES)
    ligne0_2_L_trait = canevas0_L_trait.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres+170, fill="red", width=LARGEUR_LIGNES)


def deplace_lignes_L_trait():
    """
    Déplace les lignes rouges des limites inf et sup sur le canevas 0
    """
    deplace_ligne0_1_L_trait()
    deplace_ligne0_2_L_trait()


def deplace_ligne0_1_L_trait():
    """
    Déplace la ligne rouge de la limite inf. sur le canevas 0
    """
    global ligne0_1_L_trait
    canevas0_L_trait.delete(ligne0_1_L_trait)
    x_ligne0_1 = ((variable_1_L_trait.get() -
                   limites_affichage_spectre_L_trait[0])*largeur_canevas_spectres/delta_limites_L_trait)
    ligne0_1_L_trait = canevas0_L_trait.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres+170, fill="red", width=LARGEUR_LIGNES)
    if variable_1_L_trait.get() >= variable_2_L_trait.get():
        variable_2_L_trait.set(variable_1_L_trait.get())
        deplace_ligne0_2_L_trait()


def deplace_ligne0_2_L_trait():
    """
    Déplace la ligne rouge de la limite sup. sur le canevas 0
    """
    global ligne0_2_L_trait
    canevas0_L_trait.delete(ligne0_2_L_trait)
    x_ligne0_2 = ((variable_2_L_trait.get() -
                   limites_affichage_spectre_L_trait[0])*largeur_canevas_spectres/delta_limites_L_trait)
    ligne0_2_L_trait = canevas0_L_trait.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres+170, fill="red", width=LARGEUR_LIGNES)
    if variable_2_L_trait.get() <= variable_1_L_trait.get():
        variable_1_L_trait.set(variable_2_L_trait.get())
        deplace_ligne0_1_L_trait()


def deplace_ligne0_1_return_L_trait(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite inf. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne inf.
    """
    deplace_ligne0_1_L_trait()


def deplace_ligne0_2_return_L_trait(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite sup. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne sup.
    """
    deplace_ligne0_2_L_trait()


def change_options_filtre_L_trait(event):
    """
    Change l'état des entrées (grisé ou non) en fonction du type de filtre sélectionné
    """
    filtre = type_filtre_L_trait.get()
    if filtre == "Aucun":
        entree4_L_trait.configure(state="disable")
        entree5_L_trait.configure(state="disable")
        entree5_2_L_trait.configure(state="disable")
    if filtre == "Savitzky-Golay":
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="normal")
        entree5_2_L_trait.configure(state="normal")
    if filtre == "Median":
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="disable")
        entree5_2_L_trait.configure(state="disable")
    if filtre == "Passe-bas":
        entree4_L_trait.configure(state="normal")
        entree5_L_trait.configure(state="disable")
        entree5_2_L_trait.configure(state="disable")


def change_options_fond_L_trait(event):
    """
    Change l'état des entrées (grisé ou non) en fonction du type de fond sélectionné
    """
    fond = type_fond_L_trait.get()
    if fond == "Aucun":
        entree7_L_trait.configure(state="disable")
        entree8_L_trait.configure(state="disable")
        entree8bis_L_trait.configure(state="disable")
    if fond == "Rolling ball":
        text7_L_trait.configure(text="Taille :")
        entree7_L_trait.configure(state="normal")
        text8_L_trait.configure(text="Lissage :")
        entree8_L_trait.configure(state="normal")
        entree8bis_L_trait.grid_forget()
        entree8_L_trait.grid(row=5, column=6)
    if fond == "SNIP":
        text7_L_trait.configure(text="Itérations :")
        entree7_L_trait.configure(state="normal")
        text8_L_trait.configure(text="LLS :")
        entree8bis_L_trait.configure(state="normal")
        entree8_L_trait.grid_forget()
        entree8bis_L_trait.grid(row=5, column=6)


###################################################################################################
# fonctions graphiques du caneva du spectre corrigé (frame2_L_trait)
###################################################################################################
def lit_affiche_spectre_numero_L_trait():
    """
    Mets à jour le spectre à afficher et le fond continu dans le canevas 0,
    le spectre corrigé dans le canevas 1 ainsi que
    le nom du spectre affiché dans la barre de titre
    lorsqu'on change de spectre à l'aide la spinbox Spectre
    """
    global spectre_entier_L_trait
    global nom_fichier_seul_L_trait
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    numero = numero_spectre_L_trait.get()-1
    nom_fichier_seul_L_trait = liste_fichiers_L_trait[numero]
    os.chdir(rep_travail_L_trait)
    spectre_entier_L_trait = LIBStick_outils.lit_spectre(nom_fichier_seul_L_trait,
                                                         type_fichier_L_trait.get())
    #affiche_spectre_L_trait()
    visualisation_L_trait()
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_trait)
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


def lit_affiche_spectre_numero_event_L_trait(event):
    """
    Déclenche la mise à jour des affichages (spectre, fond, spectre corrigé et nom)
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Spectre
    """
    lit_affiche_spectre_numero_L_trait()


def affiche_spectre_corrige_L_trait():
    """
    Affichage du spectre corrigé dans le canevas 1 avec gestion du zoom y auto ou non
    """
    global maximum_spectre_corrige_L_trait

    # gestion du zoom avec y personnalisé
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_trait is False and flag_bouton_zoom_L_trait is False:
        spectre = np.zeros((0, 2))
        for ligne in spectre_corrige_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        # minimum_spectre_corrige_avant_zoom_L_trait = spectre[:, 1].min()
        coord_y_min = min(coord_zoom_L_trait[1],coord_zoom_L_trait[3])
        # print("coord_y1_min = " + str(coord_y_min))
        ratio_y_1_max = (hauteur_canevas_spectres-coord_y_min)/hauteur_canevas_spectres
        if  flag_change_fenetre is False :
            maximum = maximum_spectre_corrige_L_trait * ratio_y_1_max
            # maximum = (maximum_spectre_corrige_L_trait -minimum_spectre_corrige_avant_zoom_L_trait) * ratio_y_1_max
        else :
            maximum = maximum_spectre_corrige_L_trait

        canevas1_L_trait.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_corrige_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y personnalisé par les boutons de zoom
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_trait is False and flag_bouton_zoom_L_trait is True:
        maximum = maximum_spectre_corrige_L_trait
        canevas1_L_trait.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_corrige_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y automatique
    if flag_zoom_auto_y.get() is True or flag_dezoom_L_trait is True:
        canevas1_L_trait.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_corrige_L_trait:
            if (ligne[0] >= limites_affichage_spectre_L_trait[0] and ligne[0] <= limites_affichage_spectre_L_trait[1]):
                spectre = np.row_stack((spectre, ligne))
        minimum = spectre[:, 1].min()
        maximum_spectre_corrige_L_trait = maximum = spectre[:, 1].max()

    # dessin du spectre
    spectre[:, 1] = (hauteur_canevas_spectres-(spectre[:, 1] - minimum)*hauteur_canevas_spectres/((maximum - minimum)+0.000000001))
    spectre[:, 0] = (spectre[:, 0] - limites_affichage_spectre_L_trait[0]) * \
        largeur_canevas_spectres/delta_limites_L_trait
    for i in range(len(spectre) - 1):
        canevas1_L_trait.create_line(spectre[i, 0], spectre[i, 1], spectre[i+1, 0], spectre[i+1, 1])


def affiche_position_souris_1_L_trait(event):
    """
    Affiche la position du curseur sur les canevas 0 et 1 lors du déplacement
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_0_x_L_trait
    global ligne_position_1_x_L_trait
    global ligne_position_0_y_L_trait
    global ligne_position_1_y_L_trait
    canevas0_L_trait.delete(ligne_position_0_x_L_trait)
    canevas0_L_trait.delete(ligne_position_0_y_L_trait)
    ligne_position_0_x_L_trait = canevas0_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres+170, fill="green")
    if flag_zoom_auto_y.get() is False:
        ratio_y1 = event.y/(hauteur_canevas_spectres)
        ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, ratio_y1*(hauteur_canevas_spectres+170),
                                                                  largeur_canevas_spectres, ratio_y1*(hauteur_canevas_spectres+170),
                                                                  fill="green")
    canevas1_L_trait.delete(ligne_position_1_x_L_trait)
    canevas1_L_trait.delete(ligne_position_1_y_L_trait)
    ligne_position_1_x_L_trait = canevas1_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_1_y_L_trait = canevas1_L_trait.create_line(0, event.y,
                                                                  largeur_canevas_spectres, event.y,
                                                                  fill="green")


def affiche_position_souris_motion_1_L_trait(event):
    """
    Affiche la position du curseur et la valeur de lambda
    sur les canevas 0 et 1 lors du déplacement avec clic droit maintenu
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_0_x_L_trait
    global ligne_position_1_x_L_trait
    global ligne_position_0_y_L_trait
    global ligne_position_1_y_L_trait
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    canevas0_L_trait.delete(ligne_position_0_x_L_trait)
    canevas0_L_trait.delete(ligne_position_0_y_L_trait)
    ligne_position_0_x_L_trait = canevas0_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres+170, fill="green")
    if flag_zoom_auto_y.get() is False:
        ratio_y1 = event.y/(hauteur_canevas_spectres)
        ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, ratio_y1*(hauteur_canevas_spectres+170),
                                                                  largeur_canevas_spectres, ratio_y1*(hauteur_canevas_spectres+170),
                                                                  fill="green")
    canevas1_L_trait.delete(ligne_position_1_x_L_trait)
    canevas1_L_trait.delete(ligne_position_1_y_L_trait)
    ligne_position_1_x_L_trait = canevas1_L_trait.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_1_y_L_trait = canevas1_L_trait.create_line(0, event.y,
                                                                  largeur_canevas_spectres, event.y,
                                                                  fill="green")
    if flag_premier_lamda_L_trait is False:
        canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
        canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
    l = event.x*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
    lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_trait = False

###################################################################################################
# fonctions graphiques de zoom des deux canevas (frame1_L_trait et frame2_L_trait)
###################################################################################################
def change_zoom_inf_L_trait():
    """
    Déclenche la mise à jour des différents affichages (spectre et fond du canevas 0
    spectre corrigé du canevas 1) lors d'un changement des valeurs
    de la bornes inf de la spinbox de zoom inf
    """
    global flag_bouton_zoom_L_trait
    if variable_zoom_inf_L_trait.get() >= variable_zoom_sup_L_trait.get():
        variable_zoom_sup_L_trait.set(variable_zoom_inf_L_trait.get())
    flag_bouton_zoom_L_trait = True
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()
    flag_bouton_zoom_L_trait = False


def change_zoom_sup_L_trait():
    """
    Déclenche la mise à jour des différents affichages (spectre et fond du canevas 0
    spectre corrigé du canevas 1) lors d'un changement des valeurs
    de la bornes sup de la spinbox de zoom sup
    """
    global flag_bouton_zoom_L_trait
    if variable_zoom_sup_L_trait.get() <= variable_zoom_inf_L_trait.get():
        variable_zoom_inf_L_trait.set(variable_zoom_sup_L_trait.get())
#    limites_affichage_spectre_L_trait[0]=variable_zoom_inf_L_trait.get()
#    limites_affichage_spectre_L_trait[1]=variable_zoom_sup_L_trait.get()
    flag_bouton_zoom_L_trait = True
    affiche_spectre_L_trait()
    affiche_spectre_corrige_L_trait()
    affiche_fond_L_trait()
    flag_bouton_zoom_L_trait = False


def change_zoom_inf_return_L_trait(event):
    """
    Déclenche la mise à jour des affichages (spectre, fond, spectre corrigé et nom)
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom inf.
    """
    change_zoom_inf_L_trait()


def change_zoom_sup_return_L_trait(event):
    """
    Déclenche la mise à jour des affichages (spectre, fond, spectre corrigé et nom)
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom sup.
    """
    change_zoom_sup_L_trait()


def zoom_clic_0_L_trait(event):
    """
    Récupère les coordonnées du curseur lors d'un clic gauche
    sur le canevas 0 (position x et y  en pixels sur le canevas)
    et affiche la valeur de lambda
    """
    global coord_zoom_L_trait
    affiche_lambda_L_trait(event)
    coord_zoom_L_trait[0] = event.x
    coord_zoom_L_trait[1] = event.y*hauteur_canevas_spectres/(hauteur_canevas_spectres+170)


def zoom_drag_and_drop_0_L_trait(event):
    """
    Gestion du zoom ou dé-zoom à l'aide d'un cliqué-glissé avec le
    bouton gauche de la souris
    """
    global ligne_position_0_x_L_trait
    global ligne_position_1_x_L_trait
    global ligne_position_0_y_L_trait
    global ligne_position_1_y_L_trait
    global coord_zoom_L_trait
    global limites_affichage_spectre_L_trait
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    global flag_dezoom_L_trait
    canevas0_L_trait.delete(ligne_position_0_x_L_trait)
    canevas0_L_trait.delete(ligne_position_0_y_L_trait)
    ligne_position_0_x_L_trait = canevas0_L_trait.create_line(event.x, 0, event.x,
                                                              hauteur_canevas_spectres+170,
                                                              fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, event.y,
                                                                  largeur_canevas_spectres, event.y,
                                                                  fill="green")
    canevas1_L_trait.delete(ligne_position_1_x_L_trait)
    canevas1_L_trait.delete(ligne_position_1_y_L_trait)
    ligne_position_1_x_L_trait = canevas1_L_trait.create_line(event.x, 0, event.x,
                                                              hauteur_canevas_spectres,
                                                              fill="green")
    if flag_zoom_auto_y.get() is False:
        ratio_y0 = event.y/(hauteur_canevas_spectres+170)
        ligne_position_1_y_L_trait = canevas1_L_trait.create_line(0, ratio_y0*hauteur_canevas_spectres,
                                                                  largeur_canevas_spectres,
                                                                  ratio_y0*hauteur_canevas_spectres,
                                                                  fill="green")
    coord_zoom_L_trait[2] = event.x
    coord_zoom_L_trait[3] = event.y*hauteur_canevas_spectres/(hauteur_canevas_spectres+170)
    if coord_zoom_L_trait[3] < 0 :
        coord_zoom_L_trait[3] = 0
    if coord_zoom_L_trait[3] >  hauteur_canevas_spectres :
        coord_zoom_L_trait[3] = hauteur_canevas_spectres

    # drag and drop bouton droit de gauche à droite : zoom
    if coord_zoom_L_trait[2] > coord_zoom_L_trait[0]:
        flag_dezoom_L_trait = False
        debut = coord_zoom_L_trait[0]*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
        fin = coord_zoom_L_trait[2]*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
        variable_zoom_inf_L_trait.set(format(debut, "4.1f"))
        variable_zoom_sup_L_trait.set(format(fin, "4.1f"))
        # affiche la longueur d'onde :
        if flag_premier_lamda_L_trait is False:
            canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
            canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
        l = event.x*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
        lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
        flag_premier_lamda_L_trait = False

    # drag and drop bouton droit de droite à gauche : dézoom, retour visu de tout le spectre
    if coord_zoom_L_trait[2] < coord_zoom_L_trait[0]:
        flag_dezoom_L_trait = True
        variable_zoom_inf_L_trait.set(limites_spectre_x_L_trait[0])
        variable_zoom_sup_L_trait.set(limites_spectre_x_L_trait[1])
        limites_affichage_spectre_L_trait[0] = variable_zoom_inf_L_trait.get()
        limites_affichage_spectre_L_trait[1] = variable_zoom_sup_L_trait.get()


def zoom_clic_1_L_trait(event):
    """
    Récupère les coordonnées du curseur lors d'un clic gauche
    sur le canevas 1 (position x et y  en pixels sur le canevas)
    et affiche la valeur de lambda
    """
    global coord_zoom_L_trait
    affiche_lambda_L_trait(event)
    coord_zoom_L_trait[0] = event.x
    coord_zoom_L_trait[1] = event.y


def zoom_drag_and_drop_1_L_trait(event):
    """
    Gestion du zoom ou dé-zoom à l'aide d'un cliqué-glissé avec le
    bouton gauche de la souris
    """
    global ligne_position_0_x_L_trait
    global ligne_position_1_x_L_trait
    global ligne_position_0_y_L_trait
    global ligne_position_1_y_L_trait
    global coord_zoom_L_trait
    global limites_affichage_spectre_L_trait
    global lambda_texte_spectre_0_L_trait
    global lambda_texte_spectre_1_L_trait
    global flag_premier_lamda_L_trait
    global flag_dezoom_L_trait
    canevas0_L_trait.delete(ligne_position_0_x_L_trait)
    canevas0_L_trait.delete(ligne_position_0_y_L_trait)
    ligne_position_0_x_L_trait = canevas0_L_trait.create_line(event.x, 0, event.x,
                                                              hauteur_canevas_spectres+170,
                                                              fill="green")
    if flag_zoom_auto_y.get() is False:
        ratio_y1 = event.y/(hauteur_canevas_spectres)
        ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, ratio_y1*(hauteur_canevas_spectres+170),
                                                                  largeur_canevas_spectres,
                                                                  ratio_y1*(hauteur_canevas_spectres+170),
                                                                  fill="green")
    canevas1_L_trait.delete(ligne_position_1_x_L_trait)
    canevas1_L_trait.delete(ligne_position_1_y_L_trait)
    ligne_position_1_x_L_trait = canevas1_L_trait.create_line(event.x, 0, event.x,
                                                              hauteur_canevas_spectres,
                                                              fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_1_y_L_trait = canevas1_L_trait.create_line(0, event.y,
                                                                  largeur_canevas_spectres, event.y,
                                                                  fill="green")
    coord_zoom_L_trait[2] = event.x
    coord_zoom_L_trait[3] = event.y
    if coord_zoom_L_trait[3] < 0 :
        coord_zoom_L_trait[3] = 0
    if coord_zoom_L_trait[3] >  hauteur_canevas_spectres :
        coord_zoom_L_trait[3] = hauteur_canevas_spectres

    # drag and drop bouton droit de gauche à droite : zoom
    if coord_zoom_L_trait[2] > coord_zoom_L_trait[0]:
        flag_dezoom_L_trait = False
        debut = coord_zoom_L_trait[0]*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
        fin = coord_zoom_L_trait[2]*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
        variable_zoom_inf_L_trait.set(format(debut, "4.1f"))
        variable_zoom_sup_L_trait.set(format(fin, "4.1f"))
        # affiche la longueur d'onde :
        if flag_premier_lamda_L_trait is False:
            canevas0_L_trait.delete(lambda_texte_spectre_0_L_trait)
            canevas1_L_trait.delete(lambda_texte_spectre_1_L_trait)
        l = event.x*delta_limites_L_trait/largeur_canevas_spectres+limites_affichage_spectre_L_trait[0]
        lambda_texte_spectre_0_L_trait = canevas0_L_trait.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_spectre_1_L_trait = canevas1_L_trait.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_trait.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
        flag_premier_lamda_L_trait = False

    # drag and drop bouton droit de droite à gauche : dézoom, retour visu de tout le spectre
    if coord_zoom_L_trait[2] < coord_zoom_L_trait[0]:
        flag_dezoom_L_trait = True
        variable_zoom_inf_L_trait.set(limites_spectre_x_L_trait[0])
        variable_zoom_sup_L_trait.set(limites_spectre_x_L_trait[1])
        limites_affichage_spectre_L_trait[0] = variable_zoom_inf_L_trait.get()
        limites_affichage_spectre_L_trait[1] = variable_zoom_sup_L_trait.get()


def zoom_clic_release_L_trait(event):
    """
    Mise à jour des affichages des canevas 0 et 1 au moment du relachement
    du clic gauche à la fin du cliqué-glissé pour zoomer
    """
    affiche_spectre_L_trait()
    affiche_fond_L_trait()
    affiche_spectre_corrige_L_trait()


###################################################################################################
###################################################################################################
# Fonctions LIBStick_IHM_extraction : onglet 2
###################################################################################################
###################################################################################################
def __________L_ext__________():
    """Fonctions LIBStick_IHM_extraction : onglet 2"""
###################################################################################################
###################################################################################################


###################################################################################################
# initialisations
###################################################################################################
limites_spectre_x_L_ext = np.array([198.0, 1013.0])
limites_affichage_spectre_L_ext = np.array([198.0, 1013.0])
coord_zoom_L_ext = np.array([198, 0, 1013, 0])
delta_limites_L_ext = limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
flag_premier_lamda_L_ext = True
spectre_entier_L_ext = np.zeros((0, 2))
# bornes_moyenne_spectres_L_ext=[]
liste_bool_existe_L_ext = False


def charge_param_L_ext():
    """
    Initialisation des paramètres de extraction
    """
    dictionnaire_ini = lit_section_fichier_ini("LIBStick_extraction")
    borne_zone1_inf = float(dictionnaire_ini["borne_zone1_inf_L_ext"])
    borne_zone1_sup = float(dictionnaire_ini["borne_zone1_sup_L_ext"])
    borne_zone2_inf = float(dictionnaire_ini["borne_zone2_inf_L_ext"])
    borne_zone2_sup = float(dictionnaire_ini["borne_zone2_sup_L_ext"])
    tableau_bornes_init = np.array([[borne_zone1_inf, borne_zone1_sup], [
        borne_zone2_inf, borne_zone2_sup]])
    tableau_bornes = np.array([[borne_zone1_inf, borne_zone1_sup], [
        borne_zone2_inf, borne_zone2_sup]])
    rep_travail = dictionnaire_ini["rep_travail_L_ext"]
    flag_zone2_init = dictionnaire_ini["flag_zone2_L_ext"]
    flag_2D_init = dictionnaire_ini["flag_2D_L_ext"]
    flag_3D_init = dictionnaire_ini["flag_3D_L_ext"]
    flag_image_brute_init = dictionnaire_ini["flag_image_brute_L_ext"]
    return tableau_bornes_init, tableau_bornes, rep_travail, flag_zone2_init, flag_2D_init, flag_3D_init, flag_image_brute_init


tableau_bornes_init_L_ext, tableau_bornes_L_ext, rep_travail_L_ext, flag_zone2_init_L_ext, flag_2D_init_L_ext, flag_3D_init_L_ext, flag_image_brute_init_L_ext = charge_param_L_ext()

x1_L_ext = 250.0
y_L_ext = 100.0
x2_L_ext = 250.0


def affiche_nom_spectre_onglet2():
    """
    Affichage de la version de LIBStick et du nom du spectre à l'écran pour l'onglet Extaction
    """
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ext)


###################################################################################################
# fonctions traitement des données
###################################################################################################
def creation_tab_bornes_L_ext():
    """
    Lecture des Spinbox et création du tableau des bornes de l'extraction de
    zones du spectre
    """
    # global tableau_bornes_L_ext
    tableau_bornes_L_ext[0, 0] = variable_1_L_ext.get()
    tableau_bornes_L_ext[0, 1] = variable_2_L_ext.get()
    entree5_L_ext.configure(from_=tableau_bornes_L_ext[0, 0], to=tableau_bornes_L_ext[0, 1])
    if flag_zone2_L_ext.get():
        tableau_bornes_L_ext[1, 0] = variable_3_L_ext.get()
        tableau_bornes_L_ext[1, 1] = variable_4_L_ext.get()
        entree7_L_ext.configure(from_=tableau_bornes_L_ext[1, 0], to=tableau_bornes_L_ext[1, 1])
    return tableau_bornes_L_ext


def reset_tableau_L_ext():
    """
    Réinitialisation des valeurs par défaut enregistrées dans le fichier LIBStick.ini
    """
    global tableau_bornes_L_ext
    tableau_bornes_L_ext = tableau_bornes_init_L_ext.copy()
    variable_1_L_ext.set(tableau_bornes_L_ext[0, 0])
    variable_2_L_ext.set(tableau_bornes_L_ext[0, 1])
    variable_3_L_ext.set(tableau_bornes_L_ext[1, 0])
    variable_4_L_ext.set(tableau_bornes_L_ext[1, 1])
    deplace_lignes_L_ext()


def choix_fichier_L_ext():
    """
    Ouverture/affichage d'un fichier spectre et récupération du chemin du répertoire. Bouton Fichier
    """
    global nom_fichier_seul_L_ext
    global rep_travail_L_ext
    global nombre_fichiers_L_ext
    global liste_fichiers_L_ext
    global liste_bool_L_ext
    global nombre_fichiers_avant_L_ext
    global liste_bool_existe_L_ext
    nom_fichier_L_ext = fd.askopenfilename(initialdir=rep_travail_L_ext,
                                                           title='Choisissez un fichier spectre',
                                                                 filetypes=(("fichiers IVEA", "*.asc"),
                                                                            ("fichiers LIBStick",
                                                                             "*.tsv"),
                                                                            ("fichiers SciAps", "*.csv"),
                                                                            ("fichiers LIBStick moyen", "*.mean")))
    nom_fichier_seul_L_ext = os.path.basename(nom_fichier_L_ext)
    type_fichier_L_ext.set(pathlib.Path(nom_fichier_seul_L_ext).suffix)
    rep_travail_L_ext = os.path.dirname(nom_fichier_L_ext)
    liste_fichiers_L_ext = LIBStick_outils.creation_liste_fichiers(rep_travail_L_ext,
                                                                   type_fichier_L_ext.get())
    nombre_fichiers_L_ext = len(liste_fichiers_L_ext)
    variable_10_L_ext.set(nombre_fichiers_L_ext)
    variable_10_avant_L_ext.set(nombre_fichiers_L_ext)
    if liste_bool_existe_L_ext is False or nombre_fichiers_L_ext != nombre_fichiers_avant_L_ext:
        liste_bool_L_ext = [True]*nombre_fichiers_L_ext
        liste_bool_existe_L_ext = True
        nombre_fichiers_avant_L_ext = nombre_fichiers_L_ext
    lit_affiche_spectre_L_ext(nom_fichier_seul_L_ext)
    bouton_execute_L_ext.configure(state="normal")
    bouton_extraction_L_ext.configure(state="disable")
    entree6_L_ext.configure(to=nombre_fichiers_L_ext)
    entree8_L_ext.configure(to=nombre_fichiers_L_ext)
    entree9_L_ext.configure(to=nombre_fichiers_L_ext)
    entree10_L_ext.configure(to=nombre_fichiers_L_ext)
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ext)


def execute_scripts_L_ext():
    """
    Lance l'extraction de la (des) zone(s) sur tous les spectres
    ayant la même extension du répertoire sélectionné.
    Affiche l(es) image(s) des spectres extraits classés par n° de spectre
    dans les canevas 1 (et 2)
    """
    global nom_echantillon_L_ext
    tableau_bornes = creation_tab_bornes_L_ext()
    if flag_zone2_L_ext.get() == 0:
        canevas2_L_ext.delete("all")
    nom_echantillon_L_ext = LIBStick_extraction_spectres.main(rep_travail_L_ext, tableau_bornes,
                                                              type_fichier_L_ext.get(), liste_fichiers_L_ext,
                                                              flag_zone2_L_ext.get(), flag_2D_L_ext.get(), flag_3D_L_ext.get())
    ouvre_image_L_ext()
    affiche_image_L_ext()
    bouton_extraction_L_ext.configure(state="normal")


def creation_spectre_moyen_L_ext():
    """
    Crée et sauvegarde le(s) spectre(s) moyen(s)
    et les affiches dans les canevas 3 (et 4)
    ATTENTION : A REVOIR DANS LE CAS OU UNE SEULE ZONE EXTRAITE !!!!
    """
    global spectre_moyen_1, spectre_moyen_2
    global bornes_spectre_moyen_1, bornes_spectre_moyen_2
    tableau_bornes_copy_L_ext = tableau_bornes_L_ext.copy()
    i = 1
    if flag_zone2_L_ext.get() == 0 :
        tableau_bornes_copy_L_ext = np.delete(tableau_bornes_copy_L_ext, (1), axis=0)
        canevas4_L_ext.delete("all")
    for bornes in tableau_bornes_copy_L_ext:
        repertoire = rep_travail_L_ext+"/"+str(bornes[0])+"_" + str(bornes[1])+"/"
        if i == 1:
            bornes_spectre_moyen_1 = bornes
            spectre_moyen_1 = LIBStick_extraction_spectres.creation_spectre_moyen_main(repertoire, nom_echantillon_L_ext, bornes,
                                                                   liste_bool_L_ext, flag_spectres_normalises_moyenne_L_ext.get())
            affiche_spectre_moyen1_L_ext()
        if i == 2:
            bornes_spectre_moyen_2 = bornes
            spectre_moyen_2 = LIBStick_extraction_spectres.creation_spectre_moyen_main(repertoire, nom_echantillon_L_ext, bornes,
                                                                   liste_bool_L_ext, flag_spectres_normalises_moyenne_L_ext.get())
            affiche_spectre_moyen2_L_ext()
        i = i+1


def affiche_spectre_moyen1_L_ext():
    """
    Affiche le spectre moyen 1 dans les canevas 3
    """
    spectre = spectre_moyen_1.copy()
    canevas3_L_ext.delete("all")
    delta_bornes = bornes_spectre_moyen_1[1]-bornes_spectre_moyen_1[0]
    spectre[:, 0] = (spectre[:, 0] - spectre[0, 0])*largeur_canevas_spectres/(2*delta_bornes)
    minimum = spectre[:, 1].min()
    maximum = spectre[:, 1].max()
    spectre[:, 1] = (200-(spectre[:, 1] - minimum)*200/(maximum - minimum))
    for j in range(spectre.shape[0] - 1):
        canevas3_L_ext.create_line(spectre[j, 0], spectre[j, 1], spectre[j+1, 0], spectre[j+1, 1], width=1, fill="red", smooth=1)


def affiche_spectre_moyen2_L_ext():
    """
    Affiche le spectre moyen 2 dans les canevas 4
    """
    spectre = spectre_moyen_2.copy()
    canevas4_L_ext.delete("all")
    delta_bornes = bornes_spectre_moyen_2[1]-bornes_spectre_moyen_2[0]
    spectre[:, 0] = (spectre[:, 0] - spectre[0, 0])*largeur_canevas_spectres/(2*delta_bornes)
    minimum = spectre[:, 1].min()
    maximum = spectre[:, 1].max()
    spectre[:, 1] = (200-(spectre[:, 1] - minimum)*200/(maximum - minimum))
    for j in range(spectre.shape[0] - 1):
        canevas4_L_ext.create_line(spectre[j, 0], spectre[j, 1], spectre[j+1, 0], spectre[j+1, 1], width=1, fill="blue", smooth=1)


###################################################################################################
# fonctions graphiques du caneva du spectre (frame1_L_ext)
###################################################################################################
def lit_affiche_spectre_L_ext(nom_fichier):
    """
    Lecture d'un fichier spectre et affichage du spectre
    """
    global spectre_entier_L_ext
    global limites_spectre_x_L_ext, limites_spectre_y_L_ext
    global maximum_spectre_L_ext
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext = LIBStick_outils.lit_spectre(nom_fichier, type_fichier_L_ext.get())
    limites_spectre_x_L_ext, limites_spectre_y_L_ext = lit_limites_L_ext(spectre_entier_L_ext)
    maximum_spectre_L_ext = limites_spectre_y_L_ext[1]
    affiche_spectre_L_ext()


def lit_limites_L_ext(spectre):
    """
    Lit les limites hautes et basses d'un spectre
    et fixe les valeurs du zoom à ces valeurs min et max
    """
    limites_spectre_x = np.zeros((2))
    limites_spectre_x[0] = spectre[0, 0]             # lit les abscisses min et max du spectre
    limites_spectre_x[1] = spectre[-1, 0]
    limites_spectre_y = np.zeros((2))
    limites_spectre_y[0] = spectre[:, 1].min()             # lit les valeurs min et max du spectre
    limites_spectre_y[1] = spectre[:, 1].max()
    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_inf_L_ext.set(limites_spectre_x[0])
    variable_zoom_sup_L_ext.set(limites_spectre_x[1])
    # fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_inf_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree_zoom_sup_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree1_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree2_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree3_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree4_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    return limites_spectre_x,limites_spectre_y


# def change_flag_2D_L_ext():
#     pass


# def change_flag_3D_L_ext():
#     pass


def change_flag_zone2_L_ext():
    """
    Change l'état des entrées (grisé ou non) en fonction du nombre de zones d'extraction (1 ou 2)
    et efface ou affiche les lignes bleues des limites inf et sup de la seconde zone
    """
    if flag_zone2_L_ext.get() == 0:
        efface_lignes_3_4_L_ext()
        entree3_L_ext.configure(state="disable")
        entree4_L_ext.configure(state="disable")
        entree7_L_ext.configure(state="disable")
        entree8_L_ext.configure(state="disable")
        canevas2_L_ext.configure(state="disable")
        canevas4_L_ext.configure(state="disable")
    if flag_zone2_L_ext.get() == 1:
        affiche_lignes_3_4_L_ext()
        entree3_L_ext.configure(state="normal")
        entree4_L_ext.configure(state="normal")
        entree7_L_ext.configure(state="normal")
        entree8_L_ext.configure(state="normal")
        canevas2_L_ext.configure(state="normal")
        canevas4_L_ext.configure(state="normal")


def affiche_lambda_L_ext(event):
    """
    Affiche la valeur de la longueur d'onde sur le spectre du canevas 0
    et dans la zone de texte dédiée
    """
    global lambda_texte_spectre_L_ext
    global flag_premier_lamda_L_ext
    if flag_premier_lamda_L_ext is False:
        canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
    l = event.x*delta_limites_L_ext/largeur_canevas_spectres+limites_affichage_spectre_L_ext[0]
    lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_ext = False


def affiche_position_souris_L_ext(event):
    """
    Affiche la position du curseur sur le caneva 0 lors du déplacement
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_x_L_ext
    global ligne_position_y_L_ext
    canevas0_L_ext.delete(ligne_position_x_L_ext)
    canevas0_L_ext.delete(ligne_position_y_L_ext)
    ligne_position_x_L_ext = canevas0_L_ext.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_ext = canevas0_L_ext.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")


def affiche_position_souris_motion_L_ext(event):
    """
    Affiche la position du curseur et la valeur de lambda
    sur le canevas 0 lors du déplacement avec clic droit maintenu
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_x_L_ext
    global ligne_position_y_L_ext
    global lambda_texte_spectre_L_ext
    global flag_premier_lamda_L_ext
    canevas0_L_ext.delete(ligne_position_x_L_ext)
    canevas0_L_ext.delete(ligne_position_y_L_ext)
    ligne_position_x_L_ext = canevas0_L_ext.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_ext = canevas0_L_ext.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    if flag_premier_lamda_L_ext is False:
        canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
    l = event.x*delta_limites_L_ext/largeur_canevas_spectres+limites_affichage_spectre_L_ext[0]
    lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_ext = False


def affiche_spectre_L_ext():
    """
    Affichage du spectre dans le canevas 0 avec gestion du zoom y auto ou non
    """
    global limites_affichage_spectre_L_ext
    global delta_limites_L_ext
    global minimum_spectre_lineaire_L_ext
    global maximum_spectre_L_ext
    global flag_echelle_log_L_ext
    # global minimum_spectre_L_ext
    limites_affichage_spectre_L_ext[0] = variable_zoom_inf_L_ext.get()
    limites_affichage_spectre_L_ext[1] = variable_zoom_sup_L_ext.get()
    # gestion du zoom avec y personnalisé
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_ext is False and flag_bouton_zoom_L_ext is False:
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ext:
            if (ligne[0] >= limites_affichage_spectre_L_ext[0] and ligne[0] <= limites_affichage_spectre_L_ext[1]):
                spectre = np.row_stack((spectre, ligne))
        # minimum_spectre_L_ext = spectre[:, 1].min()
        coord_y_min = min(coord_zoom_L_ext[1],coord_zoom_L_ext[3])
        # print("coord_y1_min = " + str(coord_y_min))
        ratio_y_max = (hauteur_canevas_spectres-coord_y_min)/hauteur_canevas_spectres
        if  flag_change_fenetre is False :
            maximum = maximum_spectre_L_ext * ratio_y_max
            # maximum = (maximum_spectre_L_ext-minimum_spectre_L_ext) * ratio_y_max
            maximum_spectre_L_ext = maximum
        else :
            maximum = maximum_spectre_L_ext

        delta_limites_L_ext = limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
        canevas0_L_ext.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ext:
            if (ligne[0] >= limites_affichage_spectre_L_ext[0] and ligne[0] <= limites_affichage_spectre_L_ext[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_ext.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_ext = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y personnalisé par les boutons de zoom
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_ext is False and flag_bouton_zoom_L_ext is True:
        maximum = maximum_spectre_L_ext
        delta_limites_L_ext = limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
        canevas0_L_ext.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ext:
            if (ligne[0] >= limites_affichage_spectre_L_ext[0] and ligne[0] <= limites_affichage_spectre_L_ext[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_ext.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_ext = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y automatique
    if flag_zoom_auto_y.get() is True or flag_dezoom_L_ext is True:
        delta_limites_L_ext = limites_affichage_spectre_L_ext[1]-limites_affichage_spectre_L_ext[0]
        canevas0_L_ext.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ext:
            if (ligne[0] >= limites_affichage_spectre_L_ext[0] and ligne[0] <= limites_affichage_spectre_L_ext[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_ext.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_ext = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum = spectre[:, 1].min()
        maximum_spectre_L_ext = maximum = spectre[:, 1].max()

    # dessin du spectre
    spectre[:, 1] = (hauteur_canevas_spectres-(spectre[:, 1] - minimum)*hauteur_canevas_spectres/(maximum - minimum))
    spectre[:, 0] = (spectre[:, 0] - limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext
    for i in range(len(spectre) - 1):
        canevas0_L_ext.create_line(spectre[i, 0], spectre[i, 1], spectre[i+1, 0], spectre[i+1, 1])
    affiche_lignes_spectre_L_ext()


def mise_a_jour_affichage_L_ext() :
    affiche_spectre_L_ext()


def affiche_lignes_spectre_L_ext():
    """
    Affichages des limites de(s) extraction(s) sur le spectre sous forme de deux lignes
    rouges verticales (et deux lignes bleues verticales).
    Les valeurs sont fixées par les 2 (4) spinbox borne inf. et borne sup.
    """
    global ligne0_1_L_ext
    global ligne0_2_L_ext
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    x_ligne0_1 = (
        (variable_1_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
    x_ligne0_2 = (
        (variable_2_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
    ligne0_1_L_ext = canevas0_L_ext.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    ligne0_2_L_ext = canevas0_L_ext.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if flag_zone2_L_ext.get():
        x_ligne0_3 = (
            (variable_3_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
        x_ligne0_4 = (
            (variable_4_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
        ligne0_3_L_ext = canevas0_L_ext.create_line(
            x_ligne0_3, 0, x_ligne0_3, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
        ligne0_4_L_ext = canevas0_L_ext.create_line(
            x_ligne0_4, 0, x_ligne0_4, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)


def deplace_lignes_L_ext():
    """
    Déplace les lignes rouges (et bleues) des limites inf et sup
    de(s) zone(s) d'extraction sur le canevas 0
    """
    deplace_ligne0_1_L_ext()
    deplace_ligne0_2_L_ext()
    if flag_zone2_L_ext.get():
        deplace_ligne0_3_L_ext()
        deplace_ligne0_4_L_ext()


def deplace_ligne0_1_L_ext():
    """
    Déplace la ligne rouge de la limite inf. de la zone d'extraction 1 sur le canevas 0
    """
    global ligne0_1_L_ext
    canevas0_L_ext.delete(ligne0_1_L_ext)
    x_ligne0_1 = (
        (variable_1_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
    ligne0_1_L_ext = canevas0_L_ext.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if variable_1_L_ext.get() >= variable_2_L_ext.get():
        variable_2_L_ext.set(variable_1_L_ext.get())
        deplace_ligne0_2_L_ext()


def deplace_ligne0_2_L_ext():
    """
    Déplace la ligne rouge de la limite sup. de la zone d'extraction 1 sur le canevas 0
    """
    global ligne0_2_L_ext
    canevas0_L_ext.delete(ligne0_2_L_ext)
    x_ligne0_2 = (
        (variable_2_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
    ligne0_2_L_ext = canevas0_L_ext.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if variable_2_L_ext.get() <= variable_1_L_ext.get():
        variable_1_L_ext.set(variable_2_L_ext.get())
        deplace_ligne0_1_L_ext()


def deplace_ligne0_3_L_ext():
    """
    Déplace la ligne bleue de la limite inf. de la zone d'extraction 2 sur le canevas 0
    """
    global ligne0_3_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    if flag_zone2_L_ext.get():
        x_ligne0_3 = (
            (variable_3_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
        ligne0_3_L_ext = canevas0_L_ext.create_line(
            x_ligne0_3, 0, x_ligne0_3, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
        if variable_3_L_ext.get() >= variable_4_L_ext.get():
            variable_4_L_ext.set(variable_3_L_ext.get())
            deplace_ligne0_4_L_ext()


def deplace_ligne0_4_L_ext():
    """
    Déplace la ligne bleue de la limite sup. de la zone d'extraction 2 sur le canevas 0
    """
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_4_L_ext)
    if flag_zone2_L_ext.get():
        x_ligne0_4 = (
            (variable_4_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
        ligne0_4_L_ext = canevas0_L_ext.create_line(
            x_ligne0_4, 0, x_ligne0_4, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
        if variable_4_L_ext.get() <= variable_3_L_ext.get():
            variable_3_L_ext.set(variable_4_L_ext.get())
            deplace_ligne0_3_L_ext()


def efface_lignes_3_4_L_ext():
    """
    Efface les lignes bleues de la zone d'extraction 2 sur le canevas 0
    si pas de seconde extraction choisie par la case à cocher
    """
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    canevas0_L_ext.delete(ligne0_4_L_ext)


def affiche_lignes_3_4_L_ext():
    """
    Affiche les lignes bleues de la zone d'extraction 2 sur le canevas 0
    si seconde extraction choisie par la case à cocher
    """
    global ligne0_3_L_ext
    global ligne0_4_L_ext
    canevas0_L_ext.delete(ligne0_3_L_ext)
    canevas0_L_ext.delete(ligne0_4_L_ext)
    x_ligne0_3 = (
        (variable_3_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
    x_ligne0_4 = (
        (variable_4_L_ext.get()-limites_affichage_spectre_L_ext[0])*largeur_canevas_spectres/delta_limites_L_ext)
    ligne0_3_L_ext = canevas0_L_ext.create_line(
        x_ligne0_3, 0, x_ligne0_3, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
    ligne0_4_L_ext = canevas0_L_ext.create_line(
        x_ligne0_4, 0, x_ligne0_4, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)


def deplace_ligne0_1_return_L_ext(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite inf. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne inf. de la zone d'extraction 1
    """
    deplace_ligne0_1_L_ext()


def deplace_ligne0_2_return_L_ext(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite sup. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne sup. de la zone d'extraction 1
    """
    deplace_ligne0_2_L_ext()


def deplace_ligne0_3_return_L_ext(event):
    """
    Déclenche le déplacement de la ligne bleue de la limite inf. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne inf. de la zone d'extraction 2
    """
    deplace_ligne0_3_L_ext()


def deplace_ligne0_4_return_L_ext(event):
    """
    Déclenche le déplacement de la ligne bleue de la limite sup. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne sup. de la zone d'extraction 2
    """
    deplace_ligne0_4_L_ext()


###################################################################################################
# fonctions graphiques de zoom du caneva 1 (frame1_L_ext)
###################################################################################################
def change_zoom_inf_L_ext():
    """
    Déclenche la mise à jour des différents affichages lors d'un changement
    des valeurs de la bornes inf de la spinbox de zoom inf
    """
    global flag_bouton_zoom_L_ext
#    global limites_affichage_spectre_L_ext
    if variable_zoom_inf_L_ext.get() >= variable_zoom_sup_L_ext.get():
        variable_zoom_sup_L_ext.set(variable_zoom_inf_L_ext.get())
    flag_bouton_zoom_L_ext = True
#    limites_affichage_spectre_L_ext[0]=variable_zoom_inf_L_ext.get()
#    limites_affichage_spectre_L_ext[1]=variable_zoom_sup_L_ext.get()
    affiche_spectre_L_ext()
    flag_bouton_zoom_L_ext = False


def change_zoom_sup_L_ext():
    """
    Déclenche la mise à jour des différents affichages lors d'un changement
    des valeurs de la bornes sup de la spinbox de zoom sup
    """
    global flag_bouton_zoom_L_ext
#    global limites_affichage_spectre_L_ext
    if variable_zoom_sup_L_ext.get() <= variable_zoom_inf_L_ext.get():
        variable_zoom_inf_L_ext.set(variable_zoom_sup_L_ext.get())
    flag_bouton_zoom_L_ext = True
#    limites_affichage_spectre_L_ext[0]=variable_zoom_inf_L_ext.get()
#    limites_affichage_spectre_L_ext[1]=variable_zoom_sup_L_ext.get()
    affiche_spectre_L_ext()
    flag_bouton_zoom_L_ext = False


def change_zoom_inf_return_L_ext(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom inf.
    """
    change_zoom_inf_L_ext()


def change_zoom_sup_return_L_ext(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom sup.
    """
    change_zoom_sup_L_ext()


def zoom_clic_L_ext(event):
    """
    Récupère les coordonnées du curseur lors d'un clic gauche
    sur le canevas 0 (position x et y  en pixels sur le canevas)
    et affiche la valeur de lambda
    """
    global coord_zoom_L_ext
    affiche_lambda_L_ext(event)
    coord_zoom_L_ext[0] = event.x
    coord_zoom_L_ext[1] = event.y


def zoom_drag_and_drop_L_ext(event):
    """
    Gestion du zoom ou dé-zoom à l'aide d'un cliqué-glissé avec le
    bouton gauche de la souris
    """
    global ligne_position_x_L_ext
    global ligne_position_y_L_ext
    global coord_zoom_L_ext
    global limites_affichage_spectre_L_ext
    global lambda_texte_spectre_L_ext
    global flag_premier_lamda_L_ext
    global flag_dezoom_L_ext
    canevas0_L_ext.delete(ligne_position_x_L_ext)
    canevas0_L_ext.delete(ligne_position_y_L_ext)
    ligne_position_x_L_ext = canevas0_L_ext.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_ext = canevas0_L_ext.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    coord_zoom_L_ext[2] = event.x
    coord_zoom_L_ext[3] = event.y
    if coord_zoom_L_ext[3] < 0 :
        coord_zoom_L_ext[3] = 0
    if coord_zoom_L_ext[3] >  hauteur_canevas_spectres :
        coord_zoom_L_ext[3] = hauteur_canevas_spectres

    # drag and drop bouton droit de gauche à droite : zoom
    if coord_zoom_L_ext[2] > coord_zoom_L_ext[0]:
        flag_dezoom_L_ext = False
        debut = coord_zoom_L_ext[0]*delta_limites_L_ext/largeur_canevas_spectres+limites_affichage_spectre_L_ext[0]
        fin = coord_zoom_L_ext[2]*delta_limites_L_ext/largeur_canevas_spectres+limites_affichage_spectre_L_ext[0]
        variable_zoom_inf_L_ext.set(format(debut, "4.1f"))
        variable_zoom_sup_L_ext.set(format(fin, "4.1f"))
        # affiche la longueur d'onde :
        if flag_premier_lamda_L_ext is False:
            canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
        l = event.x*delta_limites_L_ext/largeur_canevas_spectres+limites_affichage_spectre_L_ext[0]
        lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
        flag_premier_lamda_L_ext = False

    # drag and drop bouton droit de droite à gauche : dézoom, retour visu de tout le spectre
    if coord_zoom_L_ext[2] < coord_zoom_L_ext[0]:
        flag_dezoom_L_ext = True
        variable_zoom_inf_L_ext.set(limites_spectre_x_L_ext[0])
        variable_zoom_sup_L_ext.set(limites_spectre_x_L_ext[1])
        limites_affichage_spectre_L_ext[0] = variable_zoom_inf_L_ext.get()
        limites_affichage_spectre_L_ext[1] = variable_zoom_sup_L_ext.get()


def zoom_clic_release_L_ext(event):
    """
    Mise à jour des affichages du canevas 0 au moment du relachement
    du clic gauche à la fin du cliqué-glissé pour zoomer
    """
    affiche_spectre_L_ext()


###################################################################################################
# fonctions graphiques des canevas de l'image 1 et 2 (frame2_L_ext)
###################################################################################################
def ouvre_image_L_ext() :
    """
    Ouvre le(s) image(s) bruts ou normalisées dans le(s) caneva(s) 1 (et 2)
    représentant la (les) zone(s) extraite(s) de tous spectres  du répertoire
    puis appèle la fonction pour les afficher
    """
    global image1_zoom_L_ext, image2_zoom_L_ext
    # global photo1_L_ext, photo2_L_ext

    if flag_image_brute_L_ext.get() is False:
        fichier1 = rep_travail_L_ext+"/" + \
            str(tableau_bornes_L_ext[0, 0])+"_"+str(tableau_bornes_L_ext[0, 1])+"/figure.png"
    if flag_image_brute_L_ext.get() is True:
        fichier1 = rep_travail_L_ext+"/" + \
            str(tableau_bornes_L_ext[0, 0])+"_"+str(tableau_bornes_L_ext[0, 1])+"/figure_brute.png"
    image1_zoom_L_ext = PIL.Image.open(fichier1)


    if flag_zone2_L_ext.get():
        if flag_image_brute_L_ext.get() is False:
            fichier2 = rep_travail_L_ext+"/" + \
                str(tableau_bornes_L_ext[1, 0])+"_"+str(tableau_bornes_L_ext[1, 1])+"/figure.png"
        if flag_image_brute_L_ext.get() is True:
            fichier2 = rep_travail_L_ext+"/" + \
                str(tableau_bornes_L_ext[1, 0])+"_" + \
                str(tableau_bornes_L_ext[1, 1])+"/figure_brute.png"
        image2_zoom_L_ext = PIL.Image.open(fichier2)


def affiche_image_L_ext():
    """
    Affiche le(s) image(s) bruts ou normalisées dans le(s) caneva(s) 1 (et 2)
    représentant la (les) zone(s) extraite(s) de tous spectres  du répertoire
    """
    global image1_zoom_L_ext, image2_zoom_L_ext
    global photo1_L_ext, photo2_L_ext
    image1_zoom_L_ext = image1_zoom_L_ext.resize((int(largeur_canevas_spectres/2),
                                                  int(hauteur_canevas_spectres)))
    photo1_L_ext = PIL.ImageTk.PhotoImage(image1_zoom_L_ext)
    canevas1_L_ext.create_image(largeur_canevas_spectres/4, hauteur_canevas_spectres/2, image=photo1_L_ext)
    if flag_zone2_L_ext.get():
        image2_zoom_L_ext = image2_zoom_L_ext.resize((int(largeur_canevas_spectres/2),
                                                      int(hauteur_canevas_spectres)))
        photo2_L_ext = PIL.ImageTk.PhotoImage(image2_zoom_L_ext)
        canevas2_L_ext.create_image(largeur_canevas_spectres/4, hauteur_canevas_spectres/2, image=photo2_L_ext)


def change_flag_image_brute_L_ext():
    """
    Bascule entre l'affichage de l'image des spectres normalisés
    et celle des spectres bruts dans les canevas 1 et 2
    quand on clique sur la case à cocher correspondante
    """
    ouvre_image_L_ext()
    affiche_image_L_ext()
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()


def change_bool_spectre_L_ext():
    """
    Met à jour la liste des spectres à inclure dans le calcul de(s) spectre(s) moyen(s)
    lorsqu'on clique dans la case à cocher correspondante
    Ceci concerne uniquement le spectre affiché
    """
    global liste_bool_L_ext
    liste_bool_L_ext[variable_6_L_ext.get()-1] = flag_spectre_inclus_moyenne_L_ext.get()
    print("==================================")
    print(liste_bool_L_ext)


###################################################################################################
# fonctions graphiques du caneva de l'image 1 (frame2_L_ext)
###################################################################################################
def coordonnees1_L_ext(event):
    """
    Récupère les coordonnées en pixels sur l'image 1 lorsqu'on relache le clic gauche sur l'image
    x correspond à lambda et y au spectre
    appel de la fonction pour convertir les pixels en valeurs de lambda et de n° de spectre
    déplace les cibles sur l'image à l'endroit cliqué
    """
    global x1_L_ext, y_L_ext
    x1_L_ext = event.x
    y_L_ext = event.y
    coord1_to_vars_5_6_L_ext(x1_L_ext, y_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()


def deplace_cible1_L_ext():
    """
    Déplace la cible sur l'image 1 à l'endroit cliqué dans l'une des deux images
    """
    # global x1_L_ext, y_L_ext  #Inutile ? changement le 18/03/2022
    global ligne1_vert_L_ext, ligne1_hori_L_ext
    canevas1_L_ext.delete(ligne1_vert_L_ext)
    canevas1_L_ext.delete(ligne1_hori_L_ext)
    ligne1_vert_L_ext = canevas1_L_ext.create_line(x1_L_ext, 0, x1_L_ext, hauteur_canevas_spectres, fill="white")
    ligne1_hori_L_ext = canevas1_L_ext.create_line(0, y_L_ext, largeur_canevas_spectres/2, y_L_ext, fill="white")


def coord1_to_vars_5_6_L_ext(x, y):
    """
    Convertit les coord x et y en pixels en valeur de lambda et de n° de spectre
    puis de nom de fichier correspondant
    Met à jour l'affichage du nom dans la barre de titre, l'affichage du spectre
    dans le canevas 0 , l'affichage des spinbox sous l' image 1
    et la valeur de la case à cocher suivant si le spectre
    est inclu ou non dans le calcul des spectres moyens
    """
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    variable_5_L_ext.set(format(
        (variable_1_L_ext.get() + (x * (variable_2_L_ext.get()-variable_1_L_ext.get()) / (largeur_canevas_spectres/2))), "4.1f"))
    variable_6_L_ext.set(math.ceil(y * nombre_fichiers_L_ext / hauteur_canevas_spectres))
    nom_fichier_seul_L_ext = liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ext)


def vars_5_6_to_coord1_L_ext():
    """
    Convertit les coord x et y en valeur de lambda et de n° de spectre en pixels
    lorsqu'on change les valeurs des spinbox de l'image 1
    Met à jour l'affichage du nom dans la barre de titre, l'affichage du spectre
    dans le canevas 0 , l'affichage des spinbox sous l' image 1
    et la valeur de la case à cocher suivant si le spectre
    est inclu ou non dans le calcul des spectres moyens
    """
    global x1_L_ext, y_L_ext
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    x1_L_ext = round(((variable_5_L_ext.get()-variable_1_L_ext.get())*(largeur_canevas_spectres/2)) /
                     (variable_2_L_ext.get()-variable_1_L_ext.get()))
    y_L_ext = round(hauteur_canevas_spectres*(variable_6_L_ext.get()-0.5)/nombre_fichiers_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()
    nom_fichier_seul_L_ext = liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ext)


def vars_5_6_to_coord1_return_L_ext(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans les spinbox sous l'image 1
    """
    vars_5_6_to_coord1_L_ext()


###################################################################################################
# fonctions graphiques du caneva de l'image 2 (frame2_L_ext)
###################################################################################################
def coordonnees2_L_ext(event):
    """
    Récupère les coordonnées en pixels sur l'image 2 lorsqu'on relache le clic gauche sur l'image
    x correspond à lambda et y au spectre
    appel de la fonction pour convertir les pixels en valeurs de lambda et de n° de spectre
    déplace les cibles sur l'image à l'endroit cliqué
    """
    global x2_L_ext, y_L_ext
    x2_L_ext = event.x
    y_L_ext = event.y
    coord2_to_vars_7_8_L_ext(x2_L_ext, y_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()


def deplace_cible2_L_ext():
    """
    Déplace la cible sur l'image 2 à l'endroit cliqué dans l'une des deux images
    """
    # global x2_L_ext, y_L_ext
    global ligne2_vert_L_ext, ligne2_hori_L_ext
    canevas2_L_ext.delete(ligne2_vert_L_ext)
    canevas2_L_ext.delete(ligne2_hori_L_ext)
    ligne2_vert_L_ext = canevas2_L_ext.create_line(x2_L_ext, 0, x2_L_ext, hauteur_canevas_spectres, fill="white")
    ligne2_hori_L_ext = canevas2_L_ext.create_line(0, y_L_ext, largeur_canevas_spectres/2, y_L_ext, fill="white")


def coord2_to_vars_7_8_L_ext(x, y):
    """
    Convertit les coord x et y en pixels en valeur de lambda et de n° de spectre
    puis de nom de fichier correspondant
    Met à jour l'affichage du nom dans la barre de titre, l'affichage du spectre
    dans le canevas 0 , l'affichage des spinbox sous l' image 1
    et la valeur de la case à cocher suivant si le spectre
    est inclu ou non dans le calcul des spectres moyens
    """
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    variable_7_L_ext.set(format(
        (variable_3_L_ext.get() + (x * (variable_4_L_ext.get()-variable_3_L_ext.get()) / (largeur_canevas_spectres/2))), "4.1f"))
    variable_6_L_ext.set(math.ceil(y * nombre_fichiers_L_ext / hauteur_canevas_spectres))
    nom_fichier_seul_L_ext = liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ext)


def vars_7_8_to_coord2_L_ext():
    """
    Convertit les coord x et y en valeur de lambda et de n° de spectre en pixels
    lorsqu'on change les valeurs des spinbox de l'image 2
    Met à jour l'affichage du nom dans la barre de titre, l'affichage du spectre
    dans le canevas 0 , l'affichage des spinbox sous l' image 1
    et la valeur de la case à cocher suivant si le spectre
    est inclu ou non dans le calcul des spectres moyens
    """
    global x2_L_ext, y_L_ext
    global spectre_entier_L_ext
    global nom_fichier_seul_L_ext
    # ATTENTION PAS CORRECT IL FAUT RECUPERER LES BORNES D'UNE AUTRE FAÇON !!!!!
    x2_L_ext = round((variable_7_L_ext.get()-variable_3_L_ext.get()) *
                     (largeur_canevas_spectres/2)/(variable_4_L_ext.get()-variable_3_L_ext.get()))
    y_L_ext = round(hauteur_canevas_spectres*(variable_6_L_ext.get()-0.5)/nombre_fichiers_L_ext)
    deplace_cible1_L_ext()
    deplace_cible2_L_ext()
    nom_fichier_seul_L_ext = liste_fichiers_L_ext[int(variable_6_L_ext.get())-1]
    flag_spectre_inclus_moyenne_L_ext.set(liste_bool_L_ext[variable_6_L_ext.get()-1])
    os.chdir(rep_travail_L_ext)
    spectre_entier_L_ext = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ext, type_fichier_L_ext.get())
    affiche_spectre_L_ext()
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ext)


def vars_7_8_to_coord2_return_L_ext(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans les spinbox sous l'image 2
    """
    vars_7_8_to_coord2_L_ext()


###################################################################################################
#  fonctions graphiques du choix des spectres à moyenner (frame3_L_ext)
###################################################################################################
def retro_action_entree10_L_ext():
    """
    Met à jour de la liste des spectres pris en compte
    dans le calcul de(s) spectre(s) moyen(s)
    lorsqu'on change la valeur dans la spinbox (Du spectre n°)
    """
    global liste_bool_L_ext
    if variable_9_L_ext.get() > variable_10_L_ext.get():
        variable_10_L_ext.set(variable_9_L_ext.get())
        retro_action_entree9_L_ext()
    if variable_9_L_ext.get() > 1:
        if variable_9_L_ext.get() > variable_9_avant_L_ext.get():              # si on augmente la valeur de la borne inf
            for i in range(variable_9_avant_L_ext.get()-1, variable_9_L_ext.get()-1):
                liste_bool_L_ext[i] = False
                if liste_bool_L_ext[i+1] is False:
                    liste_bool_L_ext[i+1] = True
        if variable_9_L_ext.get() < variable_9_avant_L_ext.get():              # si on diminue la valeur de la borne inf
            for i in range(variable_9_L_ext.get()-1, variable_9_avant_L_ext.get()-1):
                liste_bool_L_ext[i] = True
    if variable_9_L_ext.get() == 1:
        for i in range(variable_9_L_ext.get()-1, variable_9_avant_L_ext.get()-1):
            liste_bool_L_ext[i] = True
    variable_9_avant_L_ext.set(variable_9_L_ext.get())
#    print("==================================")
#    print (liste_bool_L_ext)


def retro_action_entree9_L_ext():
    """
    Met à jour de la liste des spectres pris en compte
    dans le calcul de(s) spectre(s) moyen(s)
    lorsqu'on change la valeur dans la spinbox (Au spectre n°)
    """
    global liste_bool_L_ext
    if variable_10_L_ext.get() < variable_9_L_ext.get():
        variable_9_L_ext.set(variable_10_L_ext.get())
        retro_action_entree10_L_ext()
    if variable_10_L_ext.get() < nombre_fichiers_L_ext:
        if variable_10_L_ext.get() < variable_10_avant_L_ext.get():            # si on diminue la valeur de la borne sup
            for i in range(variable_10_L_ext.get(), variable_10_avant_L_ext.get()):
                liste_bool_L_ext[i] = False
                # if liste_bool_L_ext[i-1] is False :
                #     liste_bool_L_ext[i-1] = True
        if variable_10_L_ext.get() > variable_10_avant_L_ext.get():            # si on augmente la valeur de la borne sup
            for i in range(variable_10_avant_L_ext.get(), variable_10_L_ext.get()):
                liste_bool_L_ext[i] = True
    if variable_10_L_ext.get() == nombre_fichiers_L_ext:
        for i in range(variable_10_avant_L_ext.get(), variable_10_L_ext.get()):
            liste_bool_L_ext[i] = True
    variable_10_avant_L_ext.set(variable_10_L_ext.get())
#    print("==================================")
#    print (liste_bool_L_ext)


def change_entree9_L_ext(event):
    """
    Déclenche la mise à jour de la liste des spectres pris en compte
    dans le calcul de(s) spectre(s) moyen(s)
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox (Du spectre n°)
    """
    retro_action_entree10_L_ext()


def change_entree10_L_ext(event):
    """
    Déclenche la mise à jour de la liste des spectres pris en compte
    dans le calcul de(s) spectre(s) moyen(s)
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox (Au spectre n°)
    """
    retro_action_entree9_L_ext()


###################################################################################################
###################################################################################################
# Fonctions LIBStick_IHM_compare : onglet 3
###################################################################################################
###################################################################################################
def __________L_comp__________():
    """Fonctions LIBStick_IHM_compare : onglet 3"""
###################################################################################################
###################################################################################################


###################################################################################################
# initialisations
###################################################################################################
# limites min et max de l'affichage du spectre
limites_spectre_x_L_comp = np.array([198.0, 1013.0])
# limites de l'affichage du spectre à l'écran
limites_affichage_spectre_L_comp = np.array([198.0, 1013.0])
coord_zoom_L_comp = np.array([198, 0, 1013, 0])
delta_limites_L_comp = limites_affichage_spectre_L_comp[1]-limites_affichage_spectre_L_comp[0]
flag_premier_lamda_L_comp = True
spectre_entier_L_comp = np.zeros((0, 2))
# tableau_bornes_init_L_comp=np.array([ [529.0, 542.0] , [534.7, 535.8] ])
# tableau_bornes_L_comp=np.array([ [529.0, 542.0] , [534.7, 535.8] ])
# rep_travail_L_comp="./"
# rep_travail_L_comp="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1"


def charge_param_L_comp():
    """
    Initialisation des paramètres de comparaison
    """
    dictionnaire_ini = lit_section_fichier_ini("LIBStick_compare")
    borne_zone1_inf = float(dictionnaire_ini["borne_zone1_inf_L_comp"])
    borne_zone1_sup = float(dictionnaire_ini["borne_zone1_sup_L_comp"])
    borne_zone2_inf = float(dictionnaire_ini["borne_zone2_inf_L_comp"])
    borne_zone2_sup = float(dictionnaire_ini["borne_zone2_sup_L_comp"])
    tableau_bornes_init = np.array([[borne_zone1_inf, borne_zone1_sup], [
        borne_zone2_inf, borne_zone2_sup]])
    tableau_bornes = np.array([[borne_zone1_inf, borne_zone1_sup], [
        borne_zone2_inf, borne_zone2_sup]])
    rep_travail = dictionnaire_ini["rep_travail_L_comp"]
    flag_denominateur_init = dictionnaire_ini["flag_denominateur_L_comp"]
    flag_2D_init = dictionnaire_ini["flag_2D_L_comp"]
    flag_3D_init = dictionnaire_ini["flag_3D_L_comp"]
    flag_traitement_init = dictionnaire_ini["flag_traitement_L_comp"]
    flag_stat_init = dictionnaire_ini["flag_stat_L_comp"]
    return tableau_bornes_init, tableau_bornes, rep_travail, flag_denominateur_init, flag_2D_init, flag_3D_init, flag_traitement_init, flag_stat_init


tableau_bornes_init_L_comp, tableau_bornes_L_comp, rep_travail_L_comp, flag_denominateur_init_L_comp, flag_2D_init_L_comp, flag_3D_init_L_comp, flag_traitement_init_L_comp, flag_stat_init_L_comp = charge_param_L_comp()

x1_L_comp = 250.0
y1_L_comp = 100.0
# x2_L_comp=250.0
# y2_L_comp=100.0


def affiche_nom_spectre_onglet3():
    """
    Affichage de la version de LIBStick et du nom du spectre à l'écran pour l'onglet Comparaison
    """
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)


###################################################################################################
# fonctions traitement des données
###################################################################################################
def creation_tab_bornes_L_comp():
    """
    Lecture de(s) Spinbox et création du tableau des bornes de mesure(s) de zone(s) du spectre
    dénominateur en option
    """
    tableau_bornes_L_comp[0, 0] = variable_1_L_comp.get()
    tableau_bornes_L_comp[0, 1] = variable_2_L_comp.get()
    # entree5_L_comp.configure(from_=tableau_bornes_L_comp[0,0], to=tableau_bornes_L_comp[0,1])
    if flag_denominateur_L_comp.get():
        tableau_bornes_L_comp[1, 0] = variable_3_L_comp.get()
        tableau_bornes_L_comp[1, 1] = variable_4_L_comp.get()
    return tableau_bornes_L_comp


def reset_tableau_L_comp():
    """
    Réinitialisation des valeurs par défaut enregistrées dans le fichier LIBStick.ini
    """
    global tableau_bornes_L_comp
    tableau_bornes_L_comp = tableau_bornes_init_L_comp.copy()
    variable_1_L_comp.set(tableau_bornes_L_comp[0, 0])
    variable_2_L_comp.set(tableau_bornes_L_comp[0, 1])
    variable_3_L_comp.set(tableau_bornes_L_comp[1, 0])
    variable_4_L_comp.set(tableau_bornes_L_comp[1, 1])
    deplace_lignes_L_comp()


def choix_fichier_L_comp():
    """
    Ouverture/affichage d'un fichier spectre et récupération du chemin du répertoire. Bouton Fichier
    """
    global nom_fichier_seul_L_comp
    global rep_travail_L_comp
    global nombre_fichiers_L_comp
    global liste_fichiers_L_comp
    nom_fichier_L_comp = fd.askopenfilename(title='Choisissez un fichier spectre',
                                                            initialdir=rep_travail_L_comp,
                                                            filetypes=(("fichiers LIBStick moyen", "*.mean"),
                                                                       ("fichiers LIBStick", "*.tsv"),
                                                                       ("fichiers IVEA", "*.asc"),
                                                                       ("fichiers SciAps", "*.csv")), multiple=False)
    nom_fichier_seul_L_comp = os.path.basename(nom_fichier_L_comp)
    type_fichier_L_comp.set(pathlib.Path(nom_fichier_seul_L_comp).suffix)
    rep_travail_L_comp = os.path.dirname(nom_fichier_L_comp)
    liste_fichiers_L_comp = LIBStick_outils.creation_liste_fichiers(rep_travail_L_comp,
                                                                    type_fichier_L_comp.get())
    nombre_fichiers_L_comp = len(liste_fichiers_L_comp)
    lit_affiche_spectre_L_comp()
    bouton_execute_L_comp.configure(state="normal")
    entree6_L_comp.configure(from_=1, to=nombre_fichiers_L_comp)
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)


def lit_affiche_spectre_L_comp():
    """
    Lecture d'un fichier spectre et affichage du spectre
    """
    global spectre_entier_L_comp
    global limites_spectre_x_L_comp, limites_spectre_y_L_comp
    global maximum_spectre_L_comp
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp = LIBStick_outils.lit_spectre(nom_fichier_seul_L_comp,
                                                        type_fichier_L_comp.get())
    limites_spectre_x_L_comp, limites_spectre_y_L_comp = lit_limites_L_comp(spectre_entier_L_comp)
    maximum_spectre_L_comp = limites_spectre_y_L_comp[1]
    affiche_spectre_L_comp()


def lit_limites_L_comp(spectre):
    """
    Lit les limites hautes et basses d'un spectre
    et fixe les valeurs du zoom à ces valeurs min et max
    """
    limites_spectre_x = np.zeros((2))
    limites_spectre_x[0] = spectre[0, 0]             # lit les abscisses min et max du spectre
    limites_spectre_x[1] = spectre[-1, 0]
    limites_spectre_y = np.zeros((2))
    limites_spectre_y[0] = spectre[:, 1].min()             # lit les valeurs min et max du spectre
    limites_spectre_y[1] = spectre[:, 1].max()
    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_inf_L_comp.set(limites_spectre_x[0])
    variable_zoom_sup_L_comp.set(limites_spectre_x[1])
    # fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_inf_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree_zoom_sup_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree1_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree2_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree3_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree4_L_ext.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    return limites_spectre_x,limites_spectre_y


def execute_scripts_L_comp():
    """
    Lance les mesures sur la (des) zone(s) sur tous les spectres
    ayant la même extension du répertoire sélectionné.
    Affiche l'image des spectres extraits classés par ordre croissant de mesure
    dans les canevas 1 et affiche les résultats classés par ordre croissant de mesure
    dans le tableau avec éventuellemnt les statistiques
    """
    global DataFrame_resultats_L_comp
    global image_zoom_L_comp
    tableau_bornes = creation_tab_bornes_L_comp()
    DataFrame_resultats_L_comp = LIBStick_comp_spectres.main(rep_travail_L_comp, liste_fichiers_L_comp,
                                                             type_fichier_L_comp.get(), tableau_bornes,
                                                             flag_traitement_L_comp.get(),
                                                             flag_denominateur_L_comp.get(),
                                                             flag_2D_L_comp.get(), flag_3D_L_comp.get())
    fichier = rep_travail_L_comp+"/figure.png"
    image_zoom_L_comp = PIL.Image.open(fichier)
    # image_zoom_L_comp = image_zoom_L_comp.resize((int(largeur_canevas_spectres), int(hauteur_canevas_spectres)))
    # photo_L_comp = PIL.ImageTk.PhotoImage(image_zoom_L_comp)
    # canevas1_L_comp.create_image(largeur_canevas_spectres/2, hauteur_canevas_spectres/2, image=photo_L_comp)
    affiche_image_L_comp()
    affiche_tableau_resultats_L_comp()
    if flag_stat_L_comp.get() == 0:
        texte_statistiques_L_comp.grid_forget()
    if flag_stat_L_comp.get() == 1:
        texte_statistiques_L_comp.grid(row=1, column=3, sticky=tk.N)
        calcule_moyenne_ecarttype_L_comp()


def affiche_image_L_comp() :
    global image_zoom_L_comp, photo_L_comp
    image_zoom_L_comp = image_zoom_L_comp.resize((int(largeur_canevas_spectres),
                                                  int(hauteur_canevas_spectres)))
    photo_L_comp = PIL.ImageTk.PhotoImage(image_zoom_L_comp)
    canevas1_L_comp.create_image(largeur_canevas_spectres/2, hauteur_canevas_spectres/2, image=photo_L_comp)




###################################################################################################
# fonctions graphiques du caneva du spectre (frame1_L_comp)
###################################################################################################
def change_flag_denominateur_L_comp():
    """
    Change l'état des entrées (grisé ou non) en fonction du nombre de zones de mesures
    (dénominateur ou non) et efface ou affiche les lignes bleues des limites
    inf et sup de la seconde zone de mesure
    """
    if flag_denominateur_L_comp.get() == 0:
        efface_lignes_3_4_L_comp()
        entree3_L_comp.configure(state="disable")
        entree4_L_comp.configure(state="disable")
    if flag_denominateur_L_comp.get() == 1:
        affiche_lignes_3_4_L_comp()
        entree3_L_comp.configure(state="normal")
        entree4_L_comp.configure(state="normal")


# def change_flag_2D_L_comp():
#     pass


# def change_flag_3D_L_comp():
#     pass


def affiche_lambda_L_comp(event):
    """
    Affiche la valeur de la longueur d'onde sur le spectre du canevas 0
    et dans la zone de texte dédiée
    """
    global lambda_texte_spectre_L_comp
    global flag_premier_lamda_L_comp
    # affiche_spectre_L_comp()
    if flag_premier_lamda_L_comp is False:
        canevas0_L_comp.delete(lambda_texte_spectre_L_comp)
    l = event.x*delta_limites_L_comp/largeur_canevas_spectres+limites_affichage_spectre_L_comp[0]
    lambda_texte_spectre_L_comp = canevas0_L_comp.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_comp.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_comp = False


def affiche_position_souris_L_comp(event):
    """
    Affiche la position du curseur sur le caneva 0 lors du déplacement
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_x_L_comp
    global ligne_position_y_L_comp
    canevas0_L_comp.delete(ligne_position_x_L_comp)
    canevas0_L_comp.delete(ligne_position_y_L_comp)
    ligne_position_x_L_comp = canevas0_L_comp.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_comp = canevas0_L_comp.create_line(
            0, event.y, largeur_canevas_spectres, event.y, fill="green")


def affiche_position_souris_motion_L_comp(event):
    """
    Affiche la position du curseur et la valeur de lambda
    sur le canevas 0 lors du déplacement avec clic droit maintenu
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_x_L_comp
    global ligne_position_y_L_comp
    global lambda_texte_spectre_L_comp
    global flag_premier_lamda_L_comp
    canevas0_L_comp.delete(ligne_position_x_L_comp)
    canevas0_L_comp.delete(ligne_position_y_L_comp)
    ligne_position_x_L_comp = canevas0_L_comp.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_comp = canevas0_L_comp.create_line(
            0, event.y, largeur_canevas_spectres, event.y, fill="green")
    if flag_premier_lamda_L_comp is False:
        canevas0_L_comp.delete(lambda_texte_spectre_L_comp)
    l = event.x*delta_limites_L_comp/largeur_canevas_spectres+limites_affichage_spectre_L_comp[0]
    lambda_texte_spectre_L_comp = canevas0_L_comp.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_comp.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_comp = False


def affiche_spectre_L_comp():
    """
    Affichage du spectre dans le canevas 0 avec gestion du zoom y auto ou non
    """
    global limites_affichage_spectre_L_comp
    global delta_limites_L_comp
    global minimum_spectre_lineaire_L_comp
    # global minimum_spectre_L_comp
    global maximum_spectre_L_comp
    global flag_echelle_log_L_comp
    limites_affichage_spectre_L_comp[0] = variable_zoom_inf_L_comp.get()
    limites_affichage_spectre_L_comp[1] = variable_zoom_sup_L_comp.get()
    # gestion du zoom avec y personnalisé
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_comp is False and flag_bouton_zoom_L_comp is False:
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_comp:
            if (ligne[0] >= limites_affichage_spectre_L_comp[0] and ligne[0] <= limites_affichage_spectre_L_comp[1]):
                spectre = np.row_stack((spectre, ligne))
        # minimum_spectre_L_comp = spectre[:, 1].min()
        coord_y_min = min(coord_zoom_L_comp[1],coord_zoom_L_comp[3])
        ratio_y_max = (hauteur_canevas_spectres-coord_y_min)/hauteur_canevas_spectres
        if  flag_change_fenetre is False :
            maximum = maximum_spectre_L_comp * ratio_y_max
            # maximum = (maximum_spectre_L_comp-minimum_spectre_L_comp) * ratio_y_max
            maximum_spectre_L_comp = maximum
        else :
            maximum = maximum_spectre_L_comp

        delta_limites_L_comp = limites_affichage_spectre_L_comp[1] - limites_affichage_spectre_L_comp[0]
        canevas0_L_comp.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_comp:
            if (ligne[0] >= limites_affichage_spectre_L_comp[0] and ligne[0] <= limites_affichage_spectre_L_comp[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_comp.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_comp = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y personnalisé par les boutons de zoom
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_comp is False and flag_bouton_zoom_L_comp is True:
        maximum = maximum_spectre_L_comp
        delta_limites_L_comp = limites_affichage_spectre_L_comp[1] - limites_affichage_spectre_L_comp[0]
        canevas0_L_comp.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_comp:
            if (ligne[0] >= limites_affichage_spectre_L_comp[0] and ligne[0] <= limites_affichage_spectre_L_comp[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_comp.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_comp = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y automatique
    if flag_zoom_auto_y.get() is True or flag_dezoom_L_comp is True:
        delta_limites_L_comp = limites_affichage_spectre_L_comp[1] - \
            limites_affichage_spectre_L_comp[0]
        canevas0_L_comp.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_comp:
            if (ligne[0] >= limites_affichage_spectre_L_comp[0] and ligne[0] <= limites_affichage_spectre_L_comp[1]):
                spectre = np.row_stack((spectre, ligne))
        if flag_echelle_log_L_comp.get() == True :
            spectre[spectre<0] = 0
            minimum_spectre_lineaire_L_comp = spectre[:, 1].min()
            spectre[:,1] = np.log(spectre[:,1]-spectre[:, 1].min()+1)
        minimum = spectre[:, 1].min()
        maximum_spectre_L_comp = maximum = spectre[:, 1].max()

    # dessin du spectre
    spectre[:, 1] = (hauteur_canevas_spectres-(spectre[:, 1] - minimum)*hauteur_canevas_spectres/(maximum - minimum))
    spectre[:, 0] = (spectre[:, 0] - limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp
    for i in range(len(spectre) - 1):
        canevas0_L_comp.create_line(spectre[i, 0], spectre[i, 1], spectre[i+1, 0], spectre[i+1, 1])
    affiche_lignes_spectre_L_comp()


def mise_a_jour_affichage_L_comp() :
    affiche_spectre_L_comp()


def affiche_lignes_spectre_L_comp():
    """
    Affichages des limites de(s) mesure(s) sur le spectre sous forme de deux lignes
    rouges verticales (et deux lignes bleues verticale). Les valeurs sont fixées par les spinbox
    Numerateur borne inf. et borne sup. (et Dénominateur borne inf. et borne sup.)
    """
    global ligne0_1_L_comp
    global ligne0_2_L_comp
    global ligne0_3_L_comp
    global ligne0_4_L_comp
    x_ligne0_1 = ((variable_1_L_comp.get() -
                   limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
    x_ligne0_2 = ((variable_2_L_comp.get() -
                   limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
    ligne0_1_L_comp = canevas0_L_comp.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    ligne0_2_L_comp = canevas0_L_comp.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if flag_denominateur_L_comp.get():
        x_ligne0_3 = ((variable_3_L_comp.get() -
                       limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
        x_ligne0_4 = ((variable_4_L_comp.get() -
                       limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
        ligne0_3_L_comp = canevas0_L_comp.create_line(
            x_ligne0_3, 0, x_ligne0_3, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
        ligne0_4_L_comp = canevas0_L_comp.create_line(
            x_ligne0_4, 0, x_ligne0_4, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)


def deplace_lignes_L_comp():
    """
    Déplace les lignes rouges (et bleues) des limites inf et sup
    de(s) zone(s) de mesure(s) sur le canevas 0
    """
    deplace_ligne0_1_L_comp()
    deplace_ligne0_2_L_comp()
    if flag_denominateur_L_comp.get():
        deplace_ligne0_3_L_comp()
        deplace_ligne0_4_L_comp()


def deplace_ligne0_1_L_comp():
    """
    Déplace la ligne rouge de la limite inf. de la zone de mesure 1 sur le canevas 0
    """
    global ligne0_1_L_comp
    canevas0_L_comp.delete(ligne0_1_L_comp)
    x_ligne0_1 = ((variable_1_L_comp.get() -
                   limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
    ligne0_1_L_comp = canevas0_L_comp.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if variable_1_L_comp.get() >= variable_2_L_comp.get():
        variable_2_L_comp.set(variable_1_L_comp.get())
        deplace_ligne0_2_L_comp()


def deplace_ligne0_2_L_comp():
    """
    Déplace la ligne rouge de la limite sup. de la zone de mesure 1 sur le canevas 0
    """
    global ligne0_2_L_comp
    canevas0_L_comp.delete(ligne0_2_L_comp)
    x_ligne0_2 = ((variable_2_L_comp.get() -
                   limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
    ligne0_2_L_comp = canevas0_L_comp.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if variable_2_L_comp.get() <= variable_1_L_comp.get():
        variable_1_L_comp.set(variable_2_L_comp.get())
        deplace_ligne0_1_L_comp()


def deplace_ligne0_3_L_comp():
    """
    Déplace la ligne bleue de la limite inf. de la zone de mesure 2 sur le canevas 0
    """
    global ligne0_3_L_comp
    canevas0_L_comp.delete(ligne0_3_L_comp)
    if flag_denominateur_L_comp.get():
        x_ligne0_3 = ((variable_3_L_comp.get() -
                       limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
        ligne0_3_L_comp = canevas0_L_comp.create_line(
            x_ligne0_3, 0, x_ligne0_3, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
        if variable_3_L_comp.get() >= variable_4_L_comp.get():
            variable_4_L_comp.set(variable_3_L_comp.get())
            deplace_ligne0_4_L_comp()


def deplace_ligne0_4_L_comp():
    """
    Déplace la ligne bleue de la limite sup. de la zone de mesure 2 sur le canevas 0
    """
    global ligne0_4_L_comp
    canevas0_L_comp.delete(ligne0_4_L_comp)
    if flag_denominateur_L_comp.get():
        x_ligne0_4 = ((variable_4_L_comp.get() -
                       limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
        ligne0_4_L_comp = canevas0_L_comp.create_line(
            x_ligne0_4, 0, x_ligne0_4, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
        if variable_4_L_comp.get() <= variable_3_L_comp.get():
            variable_3_L_comp.set(variable_4_L_comp.get())
            deplace_ligne0_3_L_comp()


def efface_lignes_3_4_L_comp():
    """
    Efface les lignes bleues de la zone de mesure 2 sur le canevas 0
    si pas de seconde mesure (denominateur) choisie par la case à cocher
    """
    global ligne0_3_L_comp
    global ligne0_4_L_comp
    canevas0_L_comp.delete(ligne0_3_L_comp)
    canevas0_L_comp.delete(ligne0_4_L_comp)


def affiche_lignes_3_4_L_comp():
    """
    Affiche les lignes bleues de la zone de mesure 2 sur le canevas 0
    si pas de seconde mesure (denominateur) choisie par la case à cocher
    """
    global ligne0_3_L_comp
    global ligne0_4_L_comp
    canevas0_L_comp.delete(ligne0_3_L_comp)
    canevas0_L_comp.delete(ligne0_4_L_comp)
    x_ligne0_3 = ((variable_3_L_comp.get() -
                   limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
    x_ligne0_4 = ((variable_4_L_comp.get() -
                   limites_affichage_spectre_L_comp[0])*largeur_canevas_spectres/delta_limites_L_comp)
    ligne0_3_L_comp = canevas0_L_comp.create_line(
        x_ligne0_3, 0, x_ligne0_3, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)
    ligne0_4_L_comp = canevas0_L_comp.create_line(
        x_ligne0_4, 0, x_ligne0_4, hauteur_canevas_spectres, fill="blue", width=LARGEUR_LIGNES)


def deplace_ligne0_1_return_L_comp(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite inf. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne inf. de la zone de mesure 1
    """
    deplace_ligne0_1_L_comp()


def deplace_ligne0_2_return_L_comp(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite sup. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne sup. de la zone de mesure 1
    """
    deplace_ligne0_2_L_comp()


def deplace_ligne0_3_return_L_comp(event):
    """
    Déclenche le déplacement de la ligne bleue de la limite inf. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne inf. de la zone de mesure 2
    """
    deplace_ligne0_3_L_comp()


def deplace_ligne0_4_return_L_comp(event):
    """
    Déclenche le déplacement de la ligne bleue de la limite sup. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne sup. de la zone de mesure 2
    """
    deplace_ligne0_4_L_comp()


###################################################################################################
# fonctions graphiques de zoom du caneva du spectre (frame1_L_comp)
###################################################################################################
def change_zoom_inf_L_comp():
    """
    Déclenche la mise à jour des différents affichages lors d'un changement
    des valeurs de la bornes inf de la spinbox de zoom inf
    """
    global flag_bouton_zoom_L_comp
#    global limites_affichage_spectre_L_comp
    if variable_zoom_inf_L_comp.get() >= variable_zoom_sup_L_comp.get():
        variable_zoom_sup_L_comp.set(variable_zoom_inf_L_comp.get())
    flag_bouton_zoom_L_comp = True
#    limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
#    limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()
    affiche_spectre_L_comp()
    flag_bouton_zoom_L_comp = False


def change_zoom_sup_L_comp():
    """
    Déclenche la mise à jour des différents affichages lors d'un changement
    des valeurs de la bornes sup de la spinbox de zoom sup
    """
    global flag_bouton_zoom_L_comp
#    global limites_affichage_spectre_L_comp
    if variable_zoom_sup_L_comp.get() <= variable_zoom_inf_L_comp.get():
        variable_zoom_inf_L_comp.set(variable_zoom_sup_L_comp.get())
    flag_bouton_zoom_L_comp = True
#    limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
#    limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()
    affiche_spectre_L_comp()
    flag_bouton_zoom_L_comp = False


def change_zoom_inf_return_L_comp(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom inf.
    """
    change_zoom_inf_L_comp()


def change_zoom_sup_return_L_comp(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom sup.
    """
    change_zoom_sup_L_comp()


def zoom_clic_L_comp(event):
    """
    Récupère les coordonnées du curseur lors d'un clic gauche
    sur le canevas 0 (position x et y  en pixels sur le canevas)
    et affiche la valeur de lambda
    """
    global coord_zoom_L_comp
    affiche_lambda_L_comp(event)
    coord_zoom_L_comp[0] = event.x
    coord_zoom_L_comp[1] = event.y


def zoom_drag_and_drop_L_comp(event):
    """
    Gestion du zoom ou dé-zoom à l'aide d'un cliqué-glissé avec le
    bouton gauche de la souris
    """
    global ligne_position_x_L_comp
    global ligne_position_y_L_comp
    global coord_zoom_L_comp
    global limites_affichage_spectre_L_comp
    global lambda_texte_spectre_L_comp
    global flag_premier_lamda_L_comp
    global flag_dezoom_L_comp
    canevas0_L_comp.delete(ligne_position_x_L_comp)
    canevas0_L_comp.delete(ligne_position_y_L_comp)
    ligne_position_x_L_comp = canevas0_L_comp.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_comp = canevas0_L_comp.create_line(
            0, event.y, largeur_canevas_spectres, event.y, fill="green")
    coord_zoom_L_comp[2] = event.x
    coord_zoom_L_comp[3] = event.y
    if coord_zoom_L_comp[3] < 0 :
        coord_zoom_L_comp[3] = 0
    if coord_zoom_L_comp[3] >  hauteur_canevas_spectres :
        coord_zoom_L_comp[3] = hauteur_canevas_spectres

    # drag and drop bouton droit de gauche à droite : zoom
    if coord_zoom_L_comp[2] > coord_zoom_L_comp[0]:
        flag_dezoom_L_comp = False
        debut = coord_zoom_L_comp[0]*delta_limites_L_comp/largeur_canevas_spectres+limites_affichage_spectre_L_comp[0]
        fin = coord_zoom_L_comp[2]*delta_limites_L_comp/largeur_canevas_spectres+limites_affichage_spectre_L_comp[0]
        variable_zoom_inf_L_comp.set(format(debut, "4.1f"))
        variable_zoom_sup_L_comp.set(format(fin, "4.1f"))
        # affiche la longueur d'onde :
        if flag_premier_lamda_L_comp is False:
            canevas0_L_comp.delete(lambda_texte_spectre_L_comp)
        l = event.x*delta_limites_L_comp/largeur_canevas_spectres+limites_affichage_spectre_L_comp[0]
        lambda_texte_spectre_L_comp = canevas0_L_comp.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_comp.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
        flag_premier_lamda_L_comp = False

    # drag and drop bouton droit de droite à gauche : dézoom, retour visu de tout le spectre
    if coord_zoom_L_comp[2] < coord_zoom_L_comp[0]:
        flag_dezoom_L_comp = True
        variable_zoom_inf_L_comp.set(limites_spectre_x_L_comp[0])
        variable_zoom_sup_L_comp.set(limites_spectre_x_L_comp[1])
        # limites_affichage_spectre_L_comp[0]=variable_zoom_inf_L_comp.get()
        # limites_affichage_spectre_L_comp[1]=variable_zoom_sup_L_comp.get()


def zoom_clic_release_L_comp(event):
    """
    Mise à jour des affichages du canevas 0 au moment du relachement
    du clic gauche à la fin du cliqué-glissé pour zoomer
    """
    affiche_spectre_L_comp()


###################################################################################################
# fonctions graphiques du caneva de l'image 1 (frame2_L_comp)
###################################################################################################
def coordonnees1_L_comp(event):
    """
    Récupère les coordonnées en pixels sur l'image 1 lorsqu'on relache le clic gauche sur l'image
    x correspond à lambda et y au spectre
    appel de la fonction pour convertir les pixels en valeurs de lambda et de n° de spectre
    déplace les cibles sur l'image à l'endroit cliqué
    """
    global x1_L_comp, y1_L_comp
    x1_L_comp = event.x
    y1_L_comp = event.y
    coord1_to_vars_5_6_L_comp(x1_L_comp, y1_L_comp)
    deplace_cible1_L_comp()


def deplace_cible1_L_comp():
    """
    Déplace la cible sur l'image 1 à l'endroit cliqué dans l'image
    """
    global x1_L_comp, y1_L_comp
    global ligne1_vert_L_comp, ligne1_hori_L_comp
    canevas1_L_comp.delete(ligne1_vert_L_comp)
    canevas1_L_comp.delete(ligne1_hori_L_comp)
    ligne1_vert_L_comp = canevas1_L_comp.create_line(x1_L_comp, 0, x1_L_comp, hauteur_canevas_spectres, fill="white")
    ligne1_hori_L_comp = canevas1_L_comp.create_line(0, y1_L_comp, largeur_canevas_spectres, y1_L_comp, fill="white")
#    canevas1_L_comp.coords(ligne1_vert_L_comp, x1_L_comp,0,x1_L_comp,hauteur_canevas_spectres)
#    canevas1_L_comp.coords(ligne1_hori_L_comp, 0,y1_L_comp,400,y1_L_comp)


def coord1_to_vars_5_6_L_comp(x, y):
    """
    Convertit les coord x et y en pixels en valeur de lambda et de n° de spectre
    puis de nom de fichier correspondant
    Met à jour l'affichage du nom dans la barre de titre, l'affichage du spectre
    dans le canevas 0
    """
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    variable_5_L_comp.set(format(
        limites_spectre_x_L_comp[0] + (x * (limites_spectre_x_L_comp[1]-limites_spectre_x_L_comp[0]) / largeur_canevas_spectres), "4.1f"))
    variable_6_L_comp.set(math.ceil(y * nombre_fichiers_L_comp / hauteur_canevas_spectres))
    child_id = tree_resultats_L_comp.get_children()[variable_6_L_comp.get()-1]
    tree_resultats_L_comp.selection_set(child_id)
    selection = tree_resultats_L_comp.item(tree_resultats_L_comp.selection())["values"]
    nom_fichier_seul_L_comp = selection[1]
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


def vars_5_6_to_coord1_L_comp():
    """
    Convertit les coord x et y en valeur de lambda et de n° de spectre en pixels
    lorsqu'on change les valeurs des spinbox de l'image 1
    Met à jour l'affichage du nom dans la barre de titre, l'affichage du spectre
    dans le canevas 0
    """
    global x1_L_comp, y1_L_comp
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    x1_L_comp = round(((variable_5_L_comp.get()-limites_spectre_x_L_comp[0])*largeur_canevas_spectres) / (limites_spectre_x_L_comp[1]-limites_spectre_x_L_comp[0]))
    y1_L_comp = round(hauteur_canevas_spectres*(variable_6_L_comp.get()-0.5)/nombre_fichiers_L_comp)
    child_id = tree_resultats_L_comp.get_children()[variable_6_L_comp.get()-1]
    tree_resultats_L_comp.selection_set(child_id)
    selection = tree_resultats_L_comp.item(tree_resultats_L_comp.selection())["values"]
    nom_fichier_seul_L_comp = selection[1]
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    deplace_cible1_L_comp()
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


def vars_5_6_to_coord1_return_L_comp(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans les spinbox à coté de l'image 1
    """
    vars_5_6_to_coord1_L_comp()


###################################################################################################
# fonctions graphiques du tableau de résultats (frame3_L_comp)
###################################################################################################
def affiche_tableau_resultats_L_comp():
    """
    Affiche les résultats des mesures dans le tableau (ttk.Treeview) de la frame 3
    """
    efface_tableau_resultats_L_comp()
    num_ligne = 1
    if flag_denominateur_L_comp.get() == 1:
        tree_resultats_L_comp.heading(3, text="Rapport zone1/zone2")
        for ligne_tableau in DataFrame_resultats_L_comp.iterrows():
            tree_resultats_L_comp.insert("", "end", values=(
                num_ligne, ligne_tableau[0], DataFrame_resultats_L_comp.iloc[num_ligne-1, 2]))
            num_ligne = num_ligne+1
    if flag_denominateur_L_comp.get() == 0:
        tree_resultats_L_comp.heading(3, text="Aire zone 1")
        for ligne_tableau in DataFrame_resultats_L_comp.iterrows():
            tree_resultats_L_comp.insert("", "end", values=(
                num_ligne, ligne_tableau[0], DataFrame_resultats_L_comp.iloc[num_ligne-1, 0]))
            num_ligne = num_ligne+1


def efface_tableau_resultats_L_comp():
    """
    Efface les résultats des mesures dans le tableau (ttk.Treeview) de la frame 3
    """
    for i in tree_resultats_L_comp.get_children():
        tree_resultats_L_comp.delete(i)


def selectionne_spectre_L_comp(event):
    """
    Mise à jour des affichages du spectre du canevas 0, de la spinbox du n° de spectre
    et du nom du spectre dans la barre de titre au moment du relachement
    du clic gauche sur un des spectres du tableau de résultats(Treeview)
    """
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    selection = tree_resultats_L_comp.selection()
    item = tree_resultats_L_comp.item(selection)["values"]
    print(item)
    variable_6_L_comp.set(item[0])
    nom_fichier_seul_L_comp = item[1]
    vars_5_6_to_coord1_L_comp()
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()


def selectionne_spectre_up_L_comp(event):
    """
    Mise à jour des affichages du spectre du canevas 0, de la spinbox du n° de spectre
    et du nom du spectre dans la barre de titre lorsqu'on change la selection
    du spectre du tableau de résultats(Treeview) à l'aide de la flèche HAUT du clavier
    """
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    selection = tree_resultats_L_comp.prev(tree_resultats_L_comp.selection())
    item = tree_resultats_L_comp.item(selection)["values"]
    print(item)
    variable_6_L_comp.set(item[0])
    nom_fichier_seul_L_comp = item[1]
    vars_5_6_to_coord1_L_comp()
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    tree_resultats_L_comp.see(selection)


def selectionne_spectre_down_L_comp(event):
    """
    Mise à jour des affichages du spectre du canevas 0, de la spinbox du n° de spectre
    et du nom du spectre dans la barre de titre lorsqu'on change la selection
    du spectre du tableau de résultats(Treeview) à l'aide de la flèche BAS du clavier
    """
    global spectre_entier_L_comp
    global nom_fichier_seul_L_comp
    selection = tree_resultats_L_comp.next(tree_resultats_L_comp.selection())
    item = tree_resultats_L_comp.item(selection)["values"]
    print(item)
    variable_6_L_comp.set(item[0])
    nom_fichier_seul_L_comp = item[1]
    vars_5_6_to_coord1_L_comp()
    os.chdir(rep_travail_L_comp)
    spectre_entier_L_comp = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_comp, type_fichier_L_comp.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_comp)
    affiche_spectre_L_comp()
    tree_resultats_L_comp.see(selection)


def calcule_moyenne_ecarttype_L_comp():
    """
    Calcule et affiche les statistiques sur les mesures à droite du tableau
    (Median, moyenne, ecart type, min et max)
    """
    if flag_denominateur_L_comp.get() == 1:
        median_L_comp = DataFrame_resultats_L_comp["Rapport"].median()
        moyenne_L_comp = DataFrame_resultats_L_comp["Rapport"].mean()
        ecarttype_L_comp = DataFrame_resultats_L_comp["Rapport"].std()
        min_L_comp = DataFrame_resultats_L_comp["Rapport"].min()
        max_L_comp = DataFrame_resultats_L_comp["Rapport"].max()
    if flag_denominateur_L_comp.get() == 0:
        median_L_comp = DataFrame_resultats_L_comp["Somme zone 1"].median()
        moyenne_L_comp = DataFrame_resultats_L_comp["Somme zone 1"].mean()
        ecarttype_L_comp = DataFrame_resultats_L_comp["Somme zone 1"].std()
        min_L_comp = DataFrame_resultats_L_comp["Somme zone 1"].min()
        max_L_comp = DataFrame_resultats_L_comp["Somme zone 1"].max()
    texte_median = "Median :\n" + str(format(median_L_comp, "3.4f"))
    texte_moyenne = "Moyenne :\n" + str(format(moyenne_L_comp, "3.4f"))
    texte_ecarttype = "Ecart type :\n" + str(format(ecarttype_L_comp, "3.4f"))
    texte_min = "Minimum :\n" + str(format(min_L_comp, "3.4f"))
    texte_max = "Maximum :\n" + str(format(max_L_comp, "3.4f"))
    texte_statistiques_L_comp.configure(
        text=texte_median + "\n" + texte_moyenne + "\n"+texte_ecarttype + "\n" + texte_min + "\n" + texte_max)


###################################################################################################
###################################################################################################
# Fonctions LIBStick_IHM_ACP : onglet 4
###################################################################################################
###################################################################################################
def __________L_ACP__________():
    """ Fonctions LIBStick_IHM_ACP : onglet 4"""
###################################################################################################
###################################################################################################


###################################################################################################
# initialisations
###################################################################################################
def charge_param_L_ACP():
    """
    Initialisation des paramètres de ACP
    """
    dictionnaire_ini = lit_section_fichier_ini("LIBStick_ACP")
    borne_zone1_inf = float(dictionnaire_ini["borne_zone1_inf_L_ACP"])
    borne_zone1_sup = float(dictionnaire_ini["borne_zone1_sup_L_ACP"])
    tableau_bornes_init = np.array([borne_zone1_inf, borne_zone1_sup])
    tableau_bornes = np.array([borne_zone1_inf, borne_zone1_sup])
    rep_travail = dictionnaire_ini["rep_travail_L_ACP"]
    return tableau_bornes_init, tableau_bornes, rep_travail


tableau_bornes_init_L_ACP, tableau_bornes_L_ACP, rep_travail_L_ACP = charge_param_L_ACP()

# limites min et max de l'affichage du spectre
limites_spectre_x_L_ACP = np.array([198.0, 1013.0])
# limites de l'affichage du spectre à l'écran
limites_affichage_spectre_L_ACP = np.array([198.0, 1013.0])
coord_zoom_L_ACP = np.array([198, 0, 1013, 0])
delta_limites_L_ACP = limites_affichage_spectre_L_ACP[1]-limites_affichage_spectre_L_ACP[0]
flag_premier_lamda_L_ACP = True
spectre_entier_L_ACP = np.zeros((0, 2))
spectre_corrige_L_ACP = np.zeros((0, 2))
# tableau_bornes_L_ACP=np.array([300.0, 608.0])


def affiche_nom_spectre_onglet4():
    """
    Affichage de la version de LIBStick et du nom du spectre à l'écran pour l'onglet ACP
    """
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ACP)


###################################################################################################
# fonctions traitement des données
###################################################################################################
def creation_tab_bornes_L_ACP():
    """
    Lecture de(s) Spinbox et création du tableau des bornes de calcul de l'ACP
    """
    tableau_bornes_L_ACP[0] = variable_1_L_ACP.get()
    tableau_bornes_L_ACP[1] = variable_2_L_ACP.get()
    return tableau_bornes_L_ACP


def reset_tableau_L_ACP():
    """
    Réinitialisation des valeurs par défaut enregistrées dans le fichier LIBStick.ini
    """
    global tableau_bornes_L_ACP
    tableau_bornes_L_ACP = tableau_bornes_init_L_ACP.copy()
    variable_1_L_ACP.set(tableau_bornes_L_ACP[0])
    variable_2_L_ACP.set(tableau_bornes_L_ACP[1])
    deplace_lignes_L_ACP()


def choix_fichier_L_ACP():
    """
    Ouverture/affichage d'un fichier spectre et récupération du chemin du répertoire. Bouton Fichier.
    """
    global nom_fichier_seul_L_ACP
    global rep_travail_L_ACP
    global nombre_fichiers_L_ACP
    global liste_fichiers_L_ACP
    global DataFrame_complet_L_ACP
    nom_fichier_L_ACP = fd.askopenfilename(title='Choisissez un fichier spectre',
                                                           initialdir=rep_travail_L_ACP,
                                                           filetypes=(("fichiers LIBStick", "*.tsv"),
                                                                      ("fichiers LIBStick moyen", "*.mean"),
                                                                      ("fichiers IVEA", "*.asc"),
                                                                      ("fichiers SciAps", "*.csv")), multiple=False)
    nom_fichier_seul_L_ACP = os.path.basename(nom_fichier_L_ACP)
    type_fichier_L_ACP.set(pathlib.Path(nom_fichier_seul_L_ACP).suffix)
    rep_travail_L_ACP = os.path.dirname(nom_fichier_L_ACP)
    liste_fichiers_L_ACP = LIBStick_outils.creation_liste_fichiers(rep_travail_L_ACP,
                                                                   type_fichier_L_ACP.get())
    nombre_fichiers_L_ACP = len(liste_fichiers_L_ACP)
#    entree6_L_ACP.configure(from_=1, to=nombre_fichiers_L_ACP)
    tableau_spectres_L_ACP = LIBStick_outils.creer_tableau_avec_x_colonne1(liste_fichiers_L_ACP,
                                                                           type_fichier_L_ACP.get())
    DataFrame_complet_L_ACP = LIBStick_outils.creer_dataframe_x_tableau_en_colonnes(tableau_spectres_L_ACP,
                                                                                    liste_fichiers_L_ACP)
    lit_affiche_spectre_L_ACP()
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ACP)
    bouton_execute_L_ACP.configure(state="normal")
    bouton_applique_ind_sup_L_ACP.configure(state="disable")
    # bouton_ouvre_L_ACP.configure(state="normal")


def lit_affiche_spectre_L_ACP():
    """
    Lecture d'un fichier spectre et affichage du spectre
    """
    global spectre_entier_L_ACP
    global limites_spectre_x_L_ACP, limites_spectre_y_L_ACP
    global maximum_spectre_L_ACP
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP = LIBStick_outils.lit_spectre(nom_fichier_seul_L_ACP,
                                                       type_fichier_L_ACP.get())
    limites_spectre_x_L_ACP, limites_spectre_y_L_ACP = lit_limites_L_ACP(spectre_entier_L_ACP)
    maximum_spectre_L_ACP = limites_spectre_y_L_ACP[1]
    affiche_spectre_L_ACP()
    affiche_tableau_L_ACP()


def lit_limites_L_ACP(spectre):
    """
    Lit les limites hautes et basses d'un spectre
    et fixe les valeurs du zoom à ces valeurs min et max
    """
    limites_spectre_x = np.zeros((2))
    limites_spectre_x[0] = spectre[0, 0]             # lit les abscisses min et max du spectre
    limites_spectre_x[1] = spectre[-1, 0]
    limites_spectre_y = np.zeros((2))
    limites_spectre_y[0] = spectre[:, 1].min()             # lit les valeurs min et max du spectre
    limites_spectre_y[1] = spectre[:, 1].max()
    # fixe les valeurs du zoom à ces valeurs min et max
    variable_zoom_inf_L_ACP.set(limites_spectre_x[0])
    variable_zoom_sup_L_ACP.set(limites_spectre_x[1])
    # fixe les valeurs limites pour le zoom et la zone de selection
    entree_zoom_inf_L_ACP.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree_zoom_sup_L_ACP.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree1_L_ACP.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    entree2_L_ACP.configure(from_=limites_spectre_x[0], to=limites_spectre_x[1])
    return limites_spectre_x,limites_spectre_y


def dataframe_treeview_L_ACP():
    """
    Remplit un DataFrame à partir du tableau (TreeView) de l'interface
    """
    treeview_columns = ["numero", "nom", "calcul ACP", "label"]  # list of names here
    treeview_df = pd.DataFrame(columns=treeview_columns)
    print (tree_L_ACP)
    for ligne in tree_L_ACP.get_children():
        # each row will come as a list under name "values"
        values = pd.DataFrame([tree_L_ACP.item(ligne)["values"]], columns=treeview_columns)
        # treeview_df = treeview_df.append(values, ignore_index=True)
        treeview_df = pd.concat([treeview_df,values], ignore_index=True)
    lignes = treeview_df.shape[0]
    treeview_df = treeview_df.set_index([pd.Index(range(1, lignes+1))])
    return treeview_df


def coupe_dataframe_L_ACP(dataframe, treeview_dataframe, tableau_bornes):
    """
    Création de 2 DataFrame des spectres coupés entre les bornes inf. et sup.
    et 2 DataFrames reproduisants le tableau (TreeView) de l'interface :
    1 pour les individus inclus dans le calcul de l'ACP et
    1 pour les individus supplémentaires
    """
    tableau = dataframe.values
    n = dataframe.shape[0]  # nbre d'observation en lignes
    index_numeros = range(1, n+1)
    dataframe_coupe = pd.DataFrame(tableau, index=index_numeros,
                                       columns=dataframe.columns)
    dataframe_individus_supp = pd.DataFrame(tableau, index=index_numeros,
                                                columns=dataframe.columns)
    treeview_dataframe_coupe = treeview_dataframe.copy(deep=True)
    treeview_dataframe_individus_supp = treeview_dataframe.copy(deep=True)
    i = 1
    for selection in treeview_dataframe["calcul ACP"]:
        if selection == "Non":
            # print("supprime la ligne n° " + str(i))
            dataframe_coupe = dataframe_coupe.drop(index=i)
            treeview_dataframe_coupe = treeview_dataframe_coupe.drop(index=i)
        if selection == "Oui":
            dataframe_individus_supp = dataframe_individus_supp.drop(index=i)
            treeview_dataframe_individus_supp = treeview_dataframe_individus_supp.drop(index=i)
        i = i+1
    for nom_colonne in dataframe.columns:
        if float(nom_colonne) < tableau_bornes[0] or float(nom_colonne) > tableau_bornes[1]:
            dataframe_coupe = dataframe_coupe.drop(nom_colonne, axis=1)
            dataframe_individus_supp = dataframe_individus_supp.drop(nom_colonne, axis=1)
    # print(dataframe_coupe)
    # print("----------------------------")
    # print(treeview_dataframe_coupe)
    # print("----------------------------")
    # print(dataframe_individus_supp)
    # print("----------------------------")
    # print(treeview_dataframe_individus_supp)
    return dataframe_coupe, treeview_dataframe_coupe, dataframe_individus_supp, treeview_dataframe_individus_supp


def change_flag_3D_L_ACP():
    """
    Change l'état de la Spinbox de sélection de la dimension 3 en fonction de la case à cocher 3D
    """
    if flag_3D_L_ACP.get() is True:
        entree_dim3_L_ACP.configure(state="normal")
    if flag_3D_L_ACP.get() is False:
        entree_dim3_L_ACP.configure(state="disable")


def change_flag_traitement_L_ACP():
    """
    Change l'état du bouton +ind supp lorsqu'on change une des cases à cocher Spectres normalisés ou Centré réduit
    """
    bouton_applique_ind_sup_L_ACP.configure(state="disable")


def execute_ACP_L_ACP():
    """
    Récupère de Dataframes tronqués entre les bornes inf et sup pour les individus entrant dans
    le calcul de l'ACP et pour les individus supplémentaires puis les normalise ou non suivant
    l'état de la case à côcher Spectres normalisés.
    Récupère les dimensions de l'ACP à afficher.
    Récupère le modèle de l'ACP calculé et l'applique aux individus entrant dans le calcul de l'ACP.
    Affiche les graphes dans des fenêtres matplotlib.pyplot.
    Calcule les facteurs propres corrigées et les affiche dans le canevas1 de la frame3.
    Change l'état du bouton +ind. supp
    """
    global modele_ACP_L_ACP, tableau_bornes_L_ACP, tableau_ACP_L_ACP
    # global dataframe_L_ACP, treeview_dataframe_L_ACP
    # global dataframe_individus_supp_L_ACP, treeview_dataframe_individus_supp_L_ACP
    global dataframe_facteurs_ACP_L_ACP
    tableau_bornes = creation_tab_bornes_L_ACP()
    # copie indispensable car la suite modifierait DataFrame_complet_L_ACP !
    dataframe = DataFrame_complet_L_ACP.copy(deep=True)
    treeview_dataframe = dataframe_treeview_L_ACP()
    dataframe, treeview_dataframe, dataframe_individus_supp, treeview_dataframe_individus_supp = coupe_dataframe_L_ACP(dataframe,
                                                                                                                       treeview_dataframe,
                                                                                                                       tableau_bornes)  # suprime les lignes non incluses dans le calcul de l'ACP
    if flag_normalise_L_ACP.get() is True:
        dataframe = LIBStick_outils.normalise_dataframe_aire(dataframe)

    # flag_ACP = True
    # if flag_ACP is True :   # cas normal, ACP et non pas test de l'ICA. Dancs ce cas penser à indenter le bloc suivant

    if flag_3D_L_ACP.get():
        dim_L_ACP = [dim_1_L_ACP.get(), dim_2_L_ACP.get(), dim_3_L_ACP.get()]
    else:
        dim_L_ACP = [dim_1_L_ACP.get(), dim_2_L_ACP.get()]
    nbr_spectres = dataframe.shape[0]
    nbr_variables = dataframe.shape[1]
    if nbr_spectres >= 20:
        nbr_composantes = 20
    else:
        nbr_composantes = nbr_spectres

    tableau = dataframe.values
    modele_ACP_L_ACP = LIBStick_ACP.calcul_ACP_sklearn(tableau, nbr_composantes,
                                                       flag_centre_reduit_L_ACP.get())
    tableau_ACP_L_ACP = LIBStick_ACP.applique_ACP(modele_ACP_L_ACP, tableau)
    LIBStick_ACP.affiche_ACP(treeview_dataframe, modele_ACP_L_ACP, tableau_ACP_L_ACP, dim_L_ACP,
                             flag_3D_L_ACP.get(), flag_echelle_L_ACP.get(), flag_eboulis_L_ACP.get())

    valeurs_propres_corrigees = modele_ACP_L_ACP.explained_variance_ * (nbr_spectres-1)/nbr_spectres
    sqrt_valeurs_propres_corrigees = np.sqrt(valeurs_propres_corrigees)
    facteurs_ACP_corrigees = np.zeros((nbr_composantes, nbr_variables))
    for i in range(nbr_composantes):
        facteurs_ACP_corrigees[i, :] = modele_ACP_L_ACP.components_[i, :] * sqrt_valeurs_propres_corrigees[i]
    dataframe_facteurs_ACP_L_ACP = pd.DataFrame(facteurs_ACP_corrigees, columns=dataframe.columns)
    affiche_spectres_var_ACP_L_ACP()
    bouton_enregistre_L_ACP.configure(state="normal")
    # bouton_sauve_L_ACP.configure(state="normal")
    bouton_applique_ind_sup_L_ACP.configure(state="normal")

    # if flag_ACP is False : # test de calcul ICA
    #     nbr_composantes = dim_2_L_ACP.get()
    #     modele_ACP_L_ACP=LIBStick_ACP.calcul_ICA_sklearn(dataframe,treeview_dataframe, flag_centre_reduit_L_ACP.get(),nbr_composantes)
    #     nbr_spectres = dataframe.shape[0]
    #     nbr_variables = dataframe.shape[1]
    #     facteurs_ACP_corrigees = np.zeros((nbr_composantes,nbr_variables))
    #     for i in range(nbr_composantes) :
    #         facteurs_ACP_corrigees[i,:] = modele_ACP_L_ACP.components_[i,:]
    #     dataframe_facteurs_ACP_L_ACP=pd.DataFrame(facteurs_ACP_corrigees, columns=dataframe.columns)
    #     affiche_spectres_var_ACP_L_ACP()


def applique_ACP_ind_sup_L_ACP():
    """
    A OPTIMISER AVEC LA FONCTION execute_ACP_L_ACP EN PASSANT dataframe, treeview_dataframe, dataframe_individus_supp
    EN VARIABLES GLOBALES POUR NE PAS REFFAIRE LE CALCUL UNE SECONDE FOIS...

    Récupère de Dataframes tronqués entre les bornes inf et sup pour les individus entrant dans
    le calcul de l'ACP et pour les individus supplémentaires puis les normalise ou non suivant
    l'état de la case à côcher Spectres normalisés.
    Récupère les dimensions de l'ACP à afficher.
    Applique le modèle de l'ACP aux individus entrant dans le calcul de l'ACP et aux individus supplémentaires.
    Affiche les graphes dans des fenêtres matplotlib.pyplot. avec les individus supplémentaires
    Calcule les facteurs propres corrigées et les affiche dans le canevas1 de la frame3.
    """
    # global modele_ACP_L_ACP
    global dataframe_facteurs_ACP_L_ACP
    tableau_bornes = creation_tab_bornes_L_ACP()
    # copie indispensable car la suite modifierait DataFrame_complet_L_ACP !
    dataframe = DataFrame_complet_L_ACP.copy(deep=True)
    treeview_dataframe = dataframe_treeview_L_ACP()
    dataframe, treeview_dataframe, dataframe_individus_supp, treeview_dataframe_individus_supp = coupe_dataframe_L_ACP(dataframe,
                                                                                                                       treeview_dataframe,
                                                                                                                       tableau_bornes)  # suprime les lignes non incluses dans le calcul de l'ACP
    if flag_normalise_L_ACP.get() is True:
        dataframe = LIBStick_outils.normalise_dataframe_aire(dataframe)
        dataframe_individus_supp = LIBStick_outils.normalise_dataframe_aire(dataframe_individus_supp)

    if flag_3D_L_ACP.get():
        dim_L_ACP = [dim_1_L_ACP.get(), dim_2_L_ACP.get(), dim_3_L_ACP.get()]
    else:
        dim_L_ACP = [dim_1_L_ACP.get(), dim_2_L_ACP.get()]
    nbr_spectres = dataframe.shape[0]
    nbr_variables = dataframe.shape[1]
    if nbr_spectres >= 20:
        nbr_composantes = 20
    else:
        nbr_composantes = nbr_spectres

    # tableau = dataframe.values
    tableau_individus_supp = dataframe_individus_supp.values
    # tableau_ACP = LIBStick_ACP.applique_ACP(modele_ACP_L_ACP, tableau)

    if tableau_individus_supp.shape[0] != 0:
        tableau_ACP_individus_supp = LIBStick_ACP.applique_ACP(modele_ACP_L_ACP,
                                                               tableau_individus_supp)
        LIBStick_ACP.affiche_ACP_ind_supp(treeview_dataframe_individus_supp,
                                          treeview_dataframe, modele_ACP_L_ACP,
                                          tableau_ACP_L_ACP, tableau_ACP_individus_supp,
                                          dim_L_ACP, flag_3D_L_ACP.get(),
                                          flag_echelle_L_ACP.get(), flag_eboulis_L_ACP.get())
    else:
        LIBStick_ACP.affiche_ACP(treeview_dataframe, modele_ACP_L_ACP,
                                 tableau_ACP_L_ACP, dim_L_ACP, flag_3D_L_ACP.get(),
                                 flag_echelle_L_ACP.get(), flag_eboulis_L_ACP.get())

    valeurs_propres_corrigees = modele_ACP_L_ACP.explained_variance_ * (nbr_spectres-1)/nbr_spectres
    sqrt_valeurs_propres_corrigees = np.sqrt(valeurs_propres_corrigees)
    facteurs_ACP_corrigees = np.zeros((nbr_composantes, nbr_variables))
    for i in range(nbr_composantes):
        facteurs_ACP_corrigees[i, :] = modele_ACP_L_ACP.components_[i, :] * sqrt_valeurs_propres_corrigees[i]
    dataframe_facteurs_ACP_L_ACP = pd.DataFrame(facteurs_ACP_corrigees, columns=dataframe.columns)
    affiche_spectres_var_ACP_L_ACP()
    bouton_enregistre_L_ACP.configure(state="normal")


def enregistre_ACP_L_ACP():
    """
    Non encore utilisé
    """
    LIBStick_ACP.enregistre_ACP(modele_ACP_L_ACP, rep_travail_L_ACP)


def ouvre_ACP_L_ACP():
    """
    Non encore utilisé
    """
    global modele_ACP_L_ACP
    modele_ACP_L_ACP = LIBStick_ACP.ouvre_ACP(rep_travail_L_ACP)
    bouton_applique_ind_sup_L_ACP.configure(state="normal")


def enregistre_facteurs_ACP_L_ACP():
    """
    Enregistre les facteurs de l'ACP dans des fichiers txt et xlsx pour les re-tracer dans un tableur
    """
    suffixe_L_ACP = "_"
    if flag_normalise_L_ACP.get() is True:
        suffixe_L_ACP = suffixe_L_ACP + "norm_"
    if flag_centre_reduit_L_ACP.get() is True:
        suffixe_L_ACP = suffixe_L_ACP + "reduit_"
    nom_fichier_sauvegarde_L_ACP = fd.asksaveasfilename(title='Sauvegarde de variables explicites',
                                                                        initialdir=rep_travail_L_ACP)
    nom_fichier_sauvegarde_L_ACP = nom_fichier_sauvegarde_L_ACP + suffixe_L_ACP
#    pd.DataFrame(spectre_dim1_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP+"dim1.csv")
    pd.DataFrame(spectre_dim1_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP + str(dim_1_L_ACP.get()) + ".txt",
                                                sep='\t', decimal=",", header=None, index=None)
    pd.DataFrame(spectre_dim1_L_ACP).to_excel(nom_fichier_sauvegarde_L_ACP + str(dim_1_L_ACP.get()) + ".xlsx",
                                                  header=None, index=None)
#    pd.DataFrame(spectre_dim2_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP+"dim2.csv")
    pd.DataFrame(spectre_dim2_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP + str(dim_2_L_ACP.get()) + ".txt",
                                                sep='\t', decimal=",", header=None, index=None)
    pd.DataFrame(spectre_dim2_L_ACP).to_excel(nom_fichier_sauvegarde_L_ACP + str(dim_2_L_ACP.get()) + ".xlsx",
                                                  header=None, index=None)
    if flag_3D_L_ACP.get() is True:
        pd.DataFrame(spectre_dim3_L_ACP).to_csv(nom_fichier_sauvegarde_L_ACP + str(dim_3_L_ACP.get()) + ".txt",
                                                    sep='\t', decimal=",", header=None, index=None)
        pd.DataFrame(spectre_dim3_L_ACP).to_excel(nom_fichier_sauvegarde_L_ACP + str(dim_3_L_ACP.get()) + ".xlsx",
                                                      header=None, index=None)


###################################################################################################
# fonctions graphiques du caneva du spectre (frame1_L_ACP)
###################################################################################################
def affiche_lambda_L_ACP(event):
    """
    Affiche la valeur de la longueur d'onde sur le spectre du canevas 0 et du canevas 1
    et dans la zone de texte dédiée
    """
    global lambda_texte_spectre_0_L_ACP
    global lambda_texte_spectre_1_L_ACP
    global flag_premier_lamda_L_ACP
    # affiche_spectre_L_ACP()
    if flag_premier_lamda_L_ACP is False:
        canevas0_L_ACP.delete(lambda_texte_spectre_0_L_ACP)
        canevas1_L_ACP.delete(lambda_texte_spectre_1_L_ACP)
    l = event.x*delta_limites_L_ACP/largeur_canevas_spectres+limites_affichage_spectre_L_ACP[0]
    lambda_texte_spectre_0_L_ACP = canevas0_L_ACP.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_ACP = canevas1_L_ACP.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_ACP.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_ACP = False


def affiche_position_souris_L_ACP(event):
    """
    Affiche la position du curseur sur les canevas 0 et 1 lors du déplacement
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_x_L_ACP
    global ligne_position_y_L_ACP
    global ligne_position_1_L_ACP
    canevas0_L_ACP.delete(ligne_position_x_L_ACP)
    canevas0_L_ACP.delete(ligne_position_y_L_ACP)
    ligne_position_x_L_ACP = canevas0_L_ACP.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_ACP = canevas0_L_ACP.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    canevas1_L_ACP.delete(ligne_position_1_L_ACP)
    ligne_position_1_L_ACP = canevas1_L_ACP.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")


def affiche_position_souris_motion_L_ACP(event):
    """
    Affiche la position du curseur et la valeur de lambda
    sur les canevas 0 et 1 lors du déplacement avec clic droit maintenu
    sous la forme d'un trait vert verticale si zoom y en automatique
    sous la forme de deux traits verts vertical et horizontal si pas zoom y auto
    """
    global ligne_position_x_L_ACP
    global ligne_position_y_L_ACP
    global ligne_position_1_L_ACP
    global lambda_texte_spectre_0_L_ACP
    global lambda_texte_spectre_1_L_ACP
    global flag_premier_lamda_L_ACP
    canevas0_L_ACP.delete(ligne_position_x_L_ACP)
    canevas0_L_ACP.delete(ligne_position_y_L_ACP)
    canevas1_L_ACP.delete(ligne_position_1_L_ACP)
    ligne_position_x_L_ACP = canevas0_L_ACP.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_ACP = canevas0_L_ACP.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    ligne_position_1_L_ACP = canevas1_L_ACP.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_premier_lamda_L_ACP is False:
        canevas0_L_ACP.delete(lambda_texte_spectre_0_L_ACP)
        canevas1_L_ACP.delete(lambda_texte_spectre_1_L_ACP)
    l = event.x*delta_limites_L_ACP/largeur_canevas_spectres+limites_affichage_spectre_L_ACP[0]
    lambda_texte_spectre_0_L_ACP = canevas0_L_ACP.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_spectre_1_L_ACP = canevas1_L_ACP.create_text(
        event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
    lambda_texte_L_ACP.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
    flag_premier_lamda_L_ACP = False


def affiche_spectre_L_ACP():
    """
    Affichage du spectre dans le canevas 0 avec gestion du zoom y auto ou non
    """
    global limites_affichage_spectre_L_ACP
    global delta_limites_L_ACP
    global maximum_spectre_L_ACP
    limites_affichage_spectre_L_ACP[0] = variable_zoom_inf_L_ACP.get()
    limites_affichage_spectre_L_ACP[1] = variable_zoom_sup_L_ACP.get()
    # gestion du zoom avec y personnalisé
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_ACP is False and flag_bouton_zoom_L_ACP is False:
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ACP:
            if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
                spectre = np.row_stack((spectre, ligne))
        coord_y_min = min(coord_zoom_L_ACP[1],coord_zoom_L_ACP[3])
        ratio_y_max = (hauteur_canevas_spectres-coord_y_min)/hauteur_canevas_spectres
        if  flag_change_fenetre is False :
            maximum = maximum_spectre_L_ACP * ratio_y_max
            # maximum = (maximum_spectre_L_comp-minimum_spectre_L_comp) * ratio_y_max
            maximum_spectre_L_ACP = maximum
        else :
            maximum = maximum_spectre_L_ACP
        # minimum_spectre_ancien_L_ACP = spectre[:, 1].min()
        # maximum = (maximum_spectre_L_ACP-minimum_spectre_ancien_L_ACP) * \
        #     (hauteur_canevas_spectres-coord_zoom_L_ACP[1])/hauteur_canevas_spectres
        # maximum_spectre_L_ACP = maximum

        delta_limites_L_ACP = limites_affichage_spectre_L_ACP[1]-limites_affichage_spectre_L_ACP[0]
        canevas0_L_ACP.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ACP:
            if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
                spectre = np.row_stack((spectre, ligne))
        minimum = spectre[:, 1].min()

    # gestion du zoom avec y personnalisé par les boutons de zoom
    if flag_zoom_auto_y.get() is False and flag_dezoom_L_ACP is False and flag_bouton_zoom_L_ACP is True:
        maximum = maximum_spectre_L_ACP
        delta_limites_L_ACP = limites_affichage_spectre_L_ACP[1]-limites_affichage_spectre_L_ACP[0]
        canevas0_L_ACP.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ACP:
            if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
                spectre = np.row_stack((spectre, ligne))

        minimum = spectre[:, 1].min()

    # gestion du zoom avec y automatique
    if flag_zoom_auto_y.get() is True or flag_dezoom_L_ACP is True:
        delta_limites_L_ACP = limites_affichage_spectre_L_ACP[1]-limites_affichage_spectre_L_ACP[0]
        canevas0_L_ACP.delete("all")
        spectre = np.zeros((0, 2))
        for ligne in spectre_entier_L_ACP:
            if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
                spectre = np.row_stack((spectre, ligne))
        minimum = spectre[:, 1].min()
        maximum_spectre_L_ACP = maximum = spectre[:, 1].max()

    # dessin du spectre
    spectre[:, 1] = (hauteur_canevas_spectres-(spectre[:, 1] - minimum)*hauteur_canevas_spectres/(maximum - minimum))
    spectre[:, 0] = (spectre[:, 0] - limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP
    for i in range(len(spectre) - 1):
        canevas0_L_ACP.create_line(spectre[i, 0], spectre[i, 1], spectre[i+1, 0], spectre[i+1, 1])
    affiche_lignes_spectre_L_ACP()


def affiche_lignes_spectre_L_ACP():
    """
    Affichages des limites de(s) mesure(s) sur le spectre sous forme de deux lignes
    rouges verticales. Les valeurs sont fixées par les spinbox Borne inf. et Borne sup.
    """
    global ligne0_1_L_ACP
    global ligne0_2_L_ACP
    x_ligne0_1 = (
        (variable_1_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP)
    x_ligne0_2 = (
        (variable_2_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP)
    ligne0_1_L_ACP = canevas0_L_ACP.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    ligne0_2_L_ACP = canevas0_L_ACP.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)


def deplace_lignes_L_ACP():
    """
    Déplace les lignes rouges des limites inf et sup
    de la zone de calcul de l'ACP sur le canevas 0
    """
    deplace_ligne0_1_L_ACP()
    deplace_ligne0_2_L_ACP()
#    if flag_denominateur_L_ACP.get() :
#        deplace_ligne0_3_L_ACP()
#        deplace_ligne0_4_L_ACP()


def deplace_ligne0_1_L_ACP():
    """
    Déplace la ligne rouge de la limite inf. de la zone de calcul de l'ACP sur le canevas 0
    """
    global ligne0_1_L_ACP
    canevas0_L_ACP.delete(ligne0_1_L_ACP)
    x_ligne0_1 = (
        (variable_1_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP)
    ligne0_1_L_ACP = canevas0_L_ACP.create_line(
        x_ligne0_1, 0, x_ligne0_1, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if variable_1_L_ACP.get() >= variable_2_L_ACP.get():
        variable_2_L_ACP.set(variable_1_L_ACP.get())
        deplace_ligne0_2_L_ACP()
    bouton_applique_ind_sup_L_ACP.configure(state="disable")


def deplace_ligne0_2_L_ACP():
    """
    Déplace la ligne rouge de la limite sup. de la zone de calcul de l'ACP sur le canevas 0
    """
    global ligne0_2_L_ACP
    canevas0_L_ACP.delete(ligne0_2_L_ACP)
    x_ligne0_2 = (
        (variable_2_L_ACP.get()-limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP)
    ligne0_2_L_ACP = canevas0_L_ACP.create_line(
        x_ligne0_2, 0, x_ligne0_2, hauteur_canevas_spectres, fill="red", width=LARGEUR_LIGNES)
    if variable_2_L_ACP.get() <= variable_1_L_ACP.get():
        variable_1_L_ACP.set(variable_2_L_ACP.get())
        deplace_ligne0_1_L_ACP()
    bouton_applique_ind_sup_L_ACP.configure(state="disable")


def deplace_ligne0_1_return_L_ACP(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite inf. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne inf.
    """
    deplace_ligne0_1_L_ACP()


def deplace_ligne0_2_return_L_ACP(event):
    """
    Déclenche le déplacement de la ligne rouge de la limite sup. sur le canevas 0
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox borne sup.
    """
    deplace_ligne0_2_L_ACP()


###################################################################################################
# fonctions graphiques du caneva des "spectres de variable de l'ACP" (frame3_L_ACP)
###################################################################################################
def affiche_spectres_var_ACP_L_ACP():
    """
    Affichage des spectres des variables de l'ACP (2 ou 3 variables)
    dans le canevas 1 uniquement avec gestion du zoom y auto
    """
    global spectre_dim1_L_ACP
    global spectre_dim2_L_ACP
    global spectre_dim3_L_ACP

    spectres = dataframe_facteurs_ACP_L_ACP.values
    canevas1_L_ACP.delete("all")

    dim1 = dim_1_L_ACP.get()-1
    dim2 = dim_2_L_ACP.get()-1
    spectre_dim1_L_ACP = dataframe_facteurs_ACP_L_ACP.columns
    spectre_dim2_L_ACP = dataframe_facteurs_ACP_L_ACP.columns
    spectre_dim1_L_ACP = np.column_stack((spectre_dim1_L_ACP, spectres[dim1, :]))
    spectre_dim2_L_ACP = np.column_stack((spectre_dim2_L_ACP, spectres[dim2, :]))

    spectre1 = np.zeros((0, 2))
    spectre2 = np.zeros((0, 2))
    for ligne in spectre_dim1_L_ACP:
        if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
            spectre1 = np.row_stack((spectre1, ligne))
    for ligne in spectre_dim2_L_ACP:
        if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
            spectre2 = np.row_stack((spectre2, ligne))

    minimum1 = spectre1[:, 1].min()
    maximum1 = spectre1[:, 1].max()
    minimum2 = spectre2[:, 1].min()
    maximum2 = spectre2[:, 1].max()
    minimum = min(minimum1, minimum2)
    maximum = max(maximum1, maximum2)

    if flag_3D_L_ACP.get() is True:
        dim3 = dim_3_L_ACP.get()-1
        spectre_dim3_L_ACP = dataframe_facteurs_ACP_L_ACP.columns
        spectre_dim3_L_ACP = np.column_stack((spectre_dim3_L_ACP, spectres[dim3, :]))
        spectre3 = np.zeros((0, 2))
        for ligne in spectre_dim3_L_ACP:
            if (ligne[0] >= limites_affichage_spectre_L_ACP[0] and ligne[0] <= limites_affichage_spectre_L_ACP[1]):
                spectre3 = np.row_stack((spectre3, ligne))
        minimum3 = spectre3[:, 1].min()
        maximum3 = spectre3[:, 1].max()
        minimum = min(minimum, minimum3)
        maximum = max(maximum, maximum3)

    spectre1[:, 1] = (hauteur_canevas_spectres-(spectre1[:, 1] - minimum)*hauteur_canevas_spectres/((maximum - minimum)+0.000000001))
    spectre1[:, 0] = (spectre1[:, 0] - limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP
    for i in range(len(spectre1) - 1):
        canevas1_L_ACP.create_line(spectre1[i, 0], spectre1[i, 1],
                                   spectre1[i+1, 0], spectre1[i+1, 1], fill="red")

    spectre2[:, 1] = (hauteur_canevas_spectres-(spectre2[:, 1] - minimum)*hauteur_canevas_spectres/((maximum - minimum)+0.000000001))
    spectre2[:, 0] = (spectre2[:, 0] - limites_affichage_spectre_L_ACP[0])*largeur_canevas_spectres/delta_limites_L_ACP
    for i in range(len(spectre2) - 1):
        canevas1_L_ACP.create_line(spectre2[i, 0], spectre2[i, 1],
                                   spectre2[i+1, 0], spectre2[i+1, 1], fill="blue")

    if flag_3D_L_ACP.get() is True:
        spectre3[:, 1] = (hauteur_canevas_spectres-(spectre3[:, 1] - minimum)*hauteur_canevas_spectres/((maximum - minimum)+0.000000001))
        spectre3[:, 0] = (spectre3[:, 0] - limites_affichage_spectre_L_ACP[0]) * \
            largeur_canevas_spectres/delta_limites_L_ACP
        for i in range(len(spectre3) - 1):
            canevas1_L_ACP.create_line(
                spectre3[i, 0], spectre3[i, 1], spectre3[i+1, 0], spectre3[i+1, 1], fill="green")

    y = (hauteur_canevas_spectres-(0 - minimum)*hauteur_canevas_spectres/((maximum - minimum)+0.000000001))
    canevas1_L_ACP.create_line(0, y, largeur_canevas_spectres, y, fill="grey")


###################################################################################################
# fonctions graphiques de zoom du caneva du spectre (frame1_L_ACP)
###################################################################################################
def change_zoom_inf_L_ACP():
    """
    Déclenche la mise à jour des différents affichages lors d'un changement
    des valeurs de la bornes inf de la spinbox de zoom inf
    """
    global flag_bouton_zoom_L_ACP
#    global limites_affichage_spectre_L_ACP
    if variable_zoom_inf_L_ACP.get() >= variable_zoom_sup_L_ACP.get():
        variable_zoom_sup_L_ACP.set(variable_zoom_inf_L_ACP.get())
    flag_bouton_zoom_L_ACP = True
#    limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
#    limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()
    affiche_spectre_L_ACP()
    affiche_spectres_var_ACP_L_ACP()
    flag_bouton_zoom_L_ACP = False


def change_zoom_sup_L_ACP():
    """
    Déclenche la mise à jour des différents affichages lors d'un changement
    des valeurs de la bornes sup de la spinbox de zoom sup
    """
    global flag_bouton_zoom_L_ACP
#    global limites_affichage_spectre_L_ACP
    if variable_zoom_sup_L_ACP.get() <= variable_zoom_inf_L_ACP.get():
        variable_zoom_inf_L_ACP.set(variable_zoom_sup_L_ACP.get())
    flag_bouton_zoom_L_ACP = True
#    limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
#    limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()
    affiche_spectre_L_ACP()
    affiche_spectres_var_ACP_L_ACP()
    flag_bouton_zoom_L_ACP = False


def change_zoom_inf_return_L_ACP(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom inf.
    """
    change_zoom_inf_L_ACP()


def change_zoom_sup_return_L_ACP(event):
    """
    Déclenche la mise à jour des affichages
    lors d'un appuie sur ENTER, TAB ou ENTER du pavé numérique
    aprés saisie d'une valeur dans la spinbox Zoom sup.
    """
    change_zoom_sup_L_ACP()


def zoom_clic_L_ACP(event):
    """
    Récupère les coordonnées du curseur lors d'un clic gauche
    sur le canevas 0 ou 1 (position x et y  en pixels sur le canevas)
    et affiche la valeur de lambda
    """
    global coord_zoom_L_ACP
    affiche_lambda_L_ACP(event)
    coord_zoom_L_ACP[0] = event.x
    coord_zoom_L_ACP[1] = event.y


def zoom_drag_and_drop_L_ACP(event):
    """
    Gestion du zoom ou dé-zoom à l'aide d'un cliqué-glissé avec le
    bouton gauche de la souris
    """
    global ligne_position_x_L_ACP
    global ligne_position_y_L_ACP
    global ligne_position_1_L_ACP
    global coord_zoom_L_ACP
    global limites_affichage_spectre_L_ACP
    global lambda_texte_spectre_0_L_ACP
    global lambda_texte_spectre_1_L_ACP
    global flag_premier_lamda_L_ACP
    global flag_dezoom_L_ACP
    canevas0_L_ACP.delete(ligne_position_x_L_ACP)
    canevas0_L_ACP.delete(ligne_position_y_L_ACP)
    canevas1_L_ACP.delete(ligne_position_1_L_ACP)
    ligne_position_x_L_ACP = canevas0_L_ACP.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    if flag_zoom_auto_y.get() is False:
        ligne_position_y_L_ACP = canevas0_L_ACP.create_line(0, event.y, largeur_canevas_spectres, event.y, fill="green")
    ligne_position_1_L_ACP = canevas1_L_ACP.create_line(event.x, 0, event.x, hauteur_canevas_spectres, fill="green")
    coord_zoom_L_ACP[2] = event.x
    coord_zoom_L_ACP[3] = event.y
    if coord_zoom_L_ACP[3] < 0 :
        coord_zoom_L_ACP[3] = 0
    if coord_zoom_L_ACP[3] >  hauteur_canevas_spectres :
        coord_zoom_L_ACP[3] = hauteur_canevas_spectres


    if coord_zoom_L_ACP[2] > coord_zoom_L_ACP[0]:
        flag_dezoom_L_ACP = False
        debut = coord_zoom_L_ACP[0]*delta_limites_L_ACP/largeur_canevas_spectres+limites_affichage_spectre_L_ACP[0]
        fin = coord_zoom_L_ACP[2]*delta_limites_L_ACP/largeur_canevas_spectres+limites_affichage_spectre_L_ACP[0]
        variable_zoom_inf_L_ACP.set(format(debut, "4.1f"))
        variable_zoom_sup_L_ACP.set(format(fin, "4.1f"))
        # affiche la longueur d'onde :
        if flag_premier_lamda_L_ACP is False:
            canevas0_L_ACP.delete(lambda_texte_spectre_0_L_ACP)
            canevas1_L_ACP.delete(lambda_texte_spectre_1_L_ACP)
        l = event.x*delta_limites_L_ACP/largeur_canevas_spectres+limites_affichage_spectre_L_ACP[0]
        lambda_texte_spectre_0_L_ACP = canevas0_L_ACP.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_spectre_1_L_ACP = canevas1_L_ACP.create_text(
            event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_ACP.configure(text="Lambda = " + str(format(l, "4.1f") + " nm"))
        flag_premier_lamda_L_ACP = False
    if coord_zoom_L_ACP[2] < coord_zoom_L_ACP[0]:
        flag_dezoom_L_ACP = True
        variable_zoom_inf_L_ACP.set(limites_spectre_x_L_ACP[0])
        variable_zoom_sup_L_ACP.set(limites_spectre_x_L_ACP[1])
        # limites_affichage_spectre_L_ACP[0]=variable_zoom_inf_L_ACP.get()
        # limites_affichage_spectre_L_ACP[1]=variable_zoom_sup_L_ACP.get()


def zoom_clic_release_L_ACP(event):
    """
    Mise à jour des affichages du canevas 0 et 1 au moment du relachement
    du clic gauche à la fin du cliqué-glissé sur le canevas 0 pour zoomer
    """
    affiche_spectre_L_ACP()
    try :
        affiche_spectres_var_ACP_L_ACP()
    except :
        pass


def zoom_clic_release_canevas1_L_ACP(event):
    """
    Mise à jour des affichages du canevas 0 au moment du relachement
    du clic gauche à la fin du cliqué-glissé sur le canevas 1 pour zoomer
    """
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    affiche_spectre_L_ACP()
    affiche_spectres_var_ACP_L_ACP()
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


###################################################################################################
# fonctions graphiques du tableau de résultats (frame2_L_ACP)
###################################################################################################
def affiche_tableau_L_ACP():
    """
    Remplit le tableau de l'interface (TreeView) avec les noms de fichiers spectres de même extension
    du répertoire de travail
    """
    efface_tableau_L_ACP()
    num_ligne = 1
    for ligne_tableau in DataFrame_complet_L_ACP.iterrows():
        # ID_L_ACP = tree_L_ACP.insert("", "end", values=(num_ligne, ligne_tableau[0], "Oui", 0))
        tree_L_ACP.insert("", "end", values=(num_ligne, ligne_tableau[0], "Oui", 0))
        num_ligne = num_ligne+1


def efface_tableau_L_ACP():
    """
    Efface le contenu du tableau de l'interface (TreeView)
    """
    for i in tree_L_ACP.get_children():
        tree_L_ACP.delete(i)


def selectionne_spectre_L_ACP(event):
    """
    Mise à jour des affichages du spectre du canevas 0
    et du nom du spectre dans la barre de titre au moment du relachement
    du clic gauche sur un des spectres du tableau de l'interface (Treeview)
    """
    global spectre_entier_L_ACP
    global nom_fichier_seul_L_ACP
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    selection = tree_L_ACP.selection()
    item = tree_L_ACP.item(selection[0])["values"]
#    print(tree_L_ACP.focus())
#    print(tree_L_ACP.item(tree_L_ACP.focus()))
    nom_fichier_seul_L_ACP = item[1]
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ACP)
    affiche_spectre_L_ACP()
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


def selectionne_spectre_up_L_ACP(event):
    """
    Mise à jour des affichages du spectre du canevas 0
    et du nom du spectre dans la barre de titre lorsqu'on change la selection
    du spectre du tableau de résultats(Treeview) à l'aide de la flèche HAUT du clavier
    """
    global spectre_entier_L_ACP
    global nom_fichier_seul_L_ACP
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    selection = tree_L_ACP.prev(tree_L_ACP.selection())
    item = tree_L_ACP.item(selection)["values"]
    nom_fichier_seul_L_ACP = item[1]
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ACP)
    affiche_spectre_L_ACP()
    tree_L_ACP.see(selection)
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


def selectionne_spectre_down_L_ACP(event):
    """
    Mise à jour des affichages du spectre du canevas 0
    et du nom du spectre dans la barre de titre lorsqu'on change la selection
    du spectre du tableau de résultats(Treeview) à l'aide de la flèche BAS du clavier
    """
    global spectre_entier_L_ACP
    global nom_fichier_seul_L_ACP
    sauve_flag_zoom_auto_y = flag_zoom_auto_y.get()
    flag_zoom_auto_y.set(True)
    selection = tree_L_ACP.next(tree_L_ACP.selection())
    item = tree_L_ACP.item(selection)["values"]
    nom_fichier_seul_L_ACP = item[1]
    os.chdir(rep_travail_L_ACP)
    spectre_entier_L_ACP = LIBStick_outils.lit_spectre(
        nom_fichier_seul_L_ACP, type_fichier_L_ACP.get())
    fenetre_principale.title("LIBStick v3.0"+"\t spectre : "+nom_fichier_seul_L_ACP)
    affiche_spectre_L_ACP()
    tree_L_ACP.see(selection)
    flag_zoom_auto_y.set(sauve_flag_zoom_auto_y)


def change_tree_selection_L_ACP(event):
    """
    Change le status du spectre (OUI ou NON) pour le calcul de l'ACP
    lorsqu'on double-clic sur la ligne du spectre ou qu'on appuie sur ESPACE.
    OUI : spectre inclu dans le calcul de l'ACP
    NON : spectre non inclu dans le calcul de l'ACP (individu supplémentaire)
    Le changement de status obligue à recalculer l'ACP et donc invalide le bouton
    + ind. supp tant qu'un nouveau calcul n'a pas été fait
    """
    selection = tree_L_ACP.selection()
    for selection_i in selection :
        item = tree_L_ACP.item(selection_i)["values"]
        if item[2] == "Non":
            #        tree_L_ACP.item(selection, values=(item[0],item[1], "Oui"))
            tree_L_ACP.item(selection_i, values=(item[0], item[1], "Oui", item[3]), tags="select")
        if item[2] == "Oui":
            #        tree_L_ACP.item(selection, values=(item[0],item[1],"Non"))
            tree_L_ACP.item(selection_i, values=(item[0], item[1], "Non", item[3]), tags="deselect")
    bouton_applique_ind_sup_L_ACP.configure(state="disable")


def ouvre_fenetre_change_tree_label_L_ACP(event):
    """
    Ouvre un fenêtre Toplevel permettant d'appliquer un n° de label au spectre en surbrillance
    en tapant sur la touche [l] (comme label)
    Tous les spectres ayant le même n° de label auront la même couleur dans les graphes
    """
    global fenetre_label_L_ACP
    global tableau_label_ouvert_flag_L_ACP
    selection = tree_L_ACP.selection()
    for selection_i in selection :
        item = tree_L_ACP.item(selection_i)["values"]
        if tableau_label_ouvert_flag_L_ACP is False:
            tableau_label_ouvert_flag_L_ACP = True
            fenetre_label_L_ACP = tk.Toplevel(fenetre_principale)
            fenetre_label_L_ACP.geometry("200x150")
            fenetre_label_L_ACP.resizable(False, False)
            frame_label_L_ACP = ttk.Frame(fenetre_label_L_ACP)
            frame_label_L_ACP.pack()
            label_L_ACP.set(value=item[3])
            entree_label_L_ACP = ttk.Spinbox(frame_label_L_ACP, from_=0, to=20, increment=1, width=200,
                                             textvariable=label_L_ACP, foreground="black")
            entree_label_L_ACP.pack(ipadx=0, ipady=0)
            buttonFont = font.Font(family='Helvetica', size=30)
            bouton_label_L_ACP = tk.Button(frame_label_L_ACP, text="Valider", font=buttonFont, width=200, height=100,
                                           command=validation_label_L_ACP)
            # bouton_label_L_ACP = ttk.Button(frame_label_L_ACP, text="Valider", font=buttonFont, width=200, height=100,
            #                                     command=validation_label_L_ACP)
            bouton_label_L_ACP.pack(ipadx=0, ipady=0)
            fenetre_label_L_ACP.protocol("WM_DELETE_WINDOW", ferme_fenetre_change_tree_label_L_ACP)
        else:
            validation_label_L_ACP()
    #        fenetre_label_L_ACP.focus_force()
    #        fenetre_label_L_ACP.focus_set()
            fenetre_label_L_ACP.protocol("WM_DELETE_WINDOW", ferme_fenetre_change_tree_label_L_ACP)


def ferme_fenetre_change_tree_label_L_ACP():
    """
    Ferme la fenêtre Toplevel de labels
    """
    global tableau_label_ouvert_flag_L_ACP
    tableau_label_ouvert_flag_L_ACP = False
    fenetre_label_L_ACP.destroy()


def validation_label_L_ACP():
    """
    Valide le n° de label dans la colonne dédiée du tableau de l'interface (Treeview)
    """
    selection = tree_L_ACP.selection()
    for selection_i in selection :
        item = tree_L_ACP.item(selection_i)["values"]
        tree_L_ACP.item(selection_i, values=(item[0], item[1], item[2], label_L_ACP.get()))


###################################################################################################
###################################################################################################
# Fonctions LIBStick_elements : fenetre Toplevel
###################################################################################################
###################################################################################################
def __________L_ele__________():
    """ Fonctions LIBStick_elements : fenetre Toplevel"""
###################################################################################################
###################################################################################################


###################################################################################################
# initialisations
###################################################################################################
tableau_periodique_ouvert_L_ele = False


###################################################################################################
# fonctions d'affichage du tableau périodique et des positions sur le spectre
###################################################################################################
def lit_tableau_periodique_L_ele():
    """
    Lit le fichier LIBStick_classification.tsv permettant de construire la classification
    périodique : pour chaque élément de la classification ses coordonnées en ligne et colonne
    ainsi que la couleur de la case sont documentés
    """
    DataFrame_tableau_periodique_L_ele = pd.read_table(
        rep_LIBStick+"/LIBStick_datas/LIBStick_classification.tsv")
    return DataFrame_tableau_periodique_L_ele


def lit_element_L_ele(symbole):
    """
    Lit le contenu du fichier csv coreespondant à l'élément sélectionné (neutre ou ion)
    contenant les position des raies et leurs intensités relatives.
    Si le fichier de l'élément n'existe pas une fenêtre de message apparait
    """
    try:
        if flag_neutres_ions_L_ele.get() == 1:
            DataFrame_element = pd.read_table(
                rep_LIBStick+"/LIBStick_datas/elements/"+symbole+".csv")
            return DataFrame_element
        if flag_neutres_ions_L_ele.get() == 2:
            DataFrame_element = pd.read_table(
                rep_LIBStick+"/LIBStick_datas/ions/"+symbole+".csv")
            return DataFrame_element
    except:
        messagebox.showinfo(title=_("Attention !"),
                                    message=_("Pas d'informations pour cet élément."))
        # print("Pas de fichier de données pour cet éléments")


def affiches_lignes_element_L_ele():
    """
    Affiche les positions des raies de l'élément sélectionné dans la classification périodique
    L'affichage différencie les raies dont l'intensité relative est >10%, entre 1% et 10%
    et celles <1%
    L'affichage ne se fait que sur les spectres de l'onglet en cours
    """
    global flag_bouton_zoom_L_trait, flag_bouton_zoom_L_ext
    global flag_bouton_zoom_L_comp, flag_bouton_zoom_L_ACP
    ID_onglet = onglets.index("current")
    if ID_onglet == 0:
        limites_affichage_spectre = limites_affichage_spectre_L_trait
        flag_bouton_zoom_L_trait = True
        affiche_spectre_L_trait()
        try :
            affiche_fond_L_trait()
        except :
             pass
        try :
            affiche_spectre_corrige_L_trait()
        except :
            pass
        flag_bouton_zoom_L_trait = False
    if ID_onglet == 1:
        flag_bouton_zoom_L_ext = True
        limites_affichage_spectre = limites_affichage_spectre_L_ext
        affiche_spectre_L_ext()
        flag_bouton_zoom_L_ext = False
    if ID_onglet == 2:
        flag_bouton_zoom_L_comp = True
        limites_affichage_spectre = limites_affichage_spectre_L_comp
        affiche_spectre_L_comp()
        flag_bouton_zoom_L_comp = False
    if ID_onglet == 3:
        flag_bouton_zoom_L_ACP = True
        limites_affichage_spectre = limites_affichage_spectre_L_ACP
        affiche_spectre_L_ACP()
        try :
            affiche_spectres_var_ACP_L_ACP()
        except :
            pass
        flag_bouton_zoom_L_ACP = False
    if flag_neutres_ions_L_ele.get() == 1:
        couleur_lignes = "magenta2"
    if flag_neutres_ions_L_ele.get() == 2:
        couleur_lignes = "cyan3"
    for ligne_tableau in DataFrame_element_L_ele.itertuples():
        if float(ligne_tableau[2]) > limites_affichage_spectre[0] and float(ligne_tableau[2]) < limites_affichage_spectre[1]:
            delta_limites = limites_affichage_spectre[1]-limites_affichage_spectre[0]
            long_onde = ligne_tableau[2]
            intensite_relative = ligne_tableau[5]
            if intensite_relative >= 10 and flag_sup10_L_ele.get() == 1:
                # affiche_ligne_element(long_onde, canevas0_L_ext)
                x_ligne = ((long_onde-limites_affichage_spectre[0])*largeur_canevas_spectres/delta_limites)
                if ID_onglet == 0:
                    canevas0_L_trait.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres+170, fill=couleur_lignes, dash=(4, 1))
                    canevas1_L_trait.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres, fill=couleur_lignes, dash=(4, 1))
                if ID_onglet == 1:
                    canevas0_L_ext.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres, fill=couleur_lignes, dash=(4, 1))
                if ID_onglet == 2:
                    canevas0_L_comp.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres, fill=couleur_lignes, dash=(4, 1))
                if ID_onglet == 3:
                    canevas0_L_ACP.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres, fill=couleur_lignes, dash=(4, 1))
                    canevas1_L_ACP.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres, fill=couleur_lignes, dash=(4, 1))
            if intensite_relative < 10 and intensite_relative >= 1 and flag_sup1_L_ele.get() == 1:
                x_ligne = ((long_onde-limites_affichage_spectre[0])*largeur_canevas_spectres/delta_limites)
                if ID_onglet == 0:
                    canevas0_L_trait.create_line(x_ligne, (hauteur_canevas_spectres+170)/2, x_ligne, hauteur_canevas_spectres+170,
                                                 fill=couleur_lignes, dash=(4, 2))
                    canevas1_L_trait.create_line(x_ligne, hauteur_canevas_spectres/2, x_ligne, hauteur_canevas_spectres,
                                                 fill=couleur_lignes, dash=(4, 2))
                if ID_onglet == 1:
                    canevas0_L_ext.create_line(x_ligne, hauteur_canevas_spectres/2, x_ligne, hauteur_canevas_spectres,
                                               fill=couleur_lignes, dash=(4, 2))
                if ID_onglet == 2:
                    canevas0_L_comp.create_line(x_ligne, hauteur_canevas_spectres/2, x_ligne, hauteur_canevas_spectres,
                                                fill=couleur_lignes, dash=(4, 2))
                if ID_onglet == 3:
                    canevas0_L_ACP.create_line(x_ligne, hauteur_canevas_spectres/2, x_ligne, hauteur_canevas_spectres,
                                               fill=couleur_lignes, dash=(4, 2))
                    canevas1_L_ACP.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres,
                                               fill=couleur_lignes, dash=(4, 1))
            if intensite_relative < 1 and flag_inf1_L_ele.get() == 1:
                x_ligne = ((long_onde-limites_affichage_spectre[0])*largeur_canevas_spectres/delta_limites)
                if ID_onglet == 0:
                    canevas0_L_trait.create_line(x_ligne, (hauteur_canevas_spectres+170)*0.825, x_ligne, hauteur_canevas_spectres+170,
                                                 fill=couleur_lignes, dash=(4, 3))
                    canevas1_L_trait.create_line(x_ligne, hauteur_canevas_spectres*0.825, x_ligne, hauteur_canevas_spectres,
                                                 fill=couleur_lignes, dash=(4, 3))
                if ID_onglet == 1:
                    canevas0_L_ext.create_line(x_ligne, hauteur_canevas_spectres*0.825, x_ligne, hauteur_canevas_spectres,
                                               fill=couleur_lignes, dash=(4, 3))
                if ID_onglet == 2:
                    canevas0_L_comp.create_line(x_ligne, hauteur_canevas_spectres*0.825, x_ligne, hauteur_canevas_spectres,
                                                fill=couleur_lignes, dash=(4, 3))
                if ID_onglet == 3:
                    canevas0_L_ACP.create_line(x_ligne, hauteur_canevas_spectres*0.825, x_ligne, hauteur_canevas_spectres,
                                               fill=couleur_lignes, dash=(4, 3))
                    canevas1_L_ACP.create_line(x_ligne, 0, x_ligne, hauteur_canevas_spectres, fill=couleur_lignes, dash=(4, 1))


def affiches_lignes_neutres_ions_L_ele():
    """
    Met à jour l'affichage des raies de l'élément sélectionné lors d'un changement
    sur les boutons radio
    """
    global DataFrame_element_L_ele
    DataFrame_element_L_ele = lit_element_L_ele(symbole_L_ele)
    affiches_lignes_element_L_ele()


def affiche_tableau_periodique_L_ele(DataFrame_tableau_periodique_L_ele, frame1, bouton_affichage_L_ele):
    """
    Construit le tableau périodique en parcourant tous les éléments et en créant
    un ensemble d'objets boutons de type case_classification correspondant
    dans une grille aux coordonnées x et y de l'élément.
    Ces informations sont lues par lit_tableau_periodique_L_ele
    """
    for ligne_tableau in DataFrame_tableau_periodique_L_ele.itertuples():
        Z = ligne_tableau[1]
        symbole = ligne_tableau[2]
        nom = ligne_tableau[3]
        ligne = ligne_tableau[5]
        colonne = ligne_tableau[6]
        couleur = ligne_tableau[8]
        case_classification(frame1, nom, symbole,  Z, ligne,
                            colonne, couleur, bouton_affichage_L_ele)


def ouvre_fenetre_classification_L_ele():
    """
    Ouvre une fenêtre Toplevel et y construit l'interface de la classification périodique
    """
    global fenetre_classification_L_ele
    global tableau_periodique_ouvert_L_ele
    if tableau_periodique_ouvert_L_ele is False:
        fenetre_classification_L_ele = tk.Toplevel(fenetre_principale)
        fenetre_classification_L_ele.resizable(False, False)
        frame1_L_ele = ttk.Frame(fenetre_classification_L_ele)
        frame1_L_ele.pack()

        bouton_ferme_L_ele = tk.Button(frame1_L_ele, width=TAILLE_CASE[0], height=TAILLE_CASE[1],
                                       text=_("Ferme"), font=font.Font(size=TAILLE_FONT_CLASSIFICATION))
        bouton_ferme_L_ele.configure(command=ferme_fenetre_classification_L_ele)
        bouton_ferme_L_ele.grid(row=1, column=3, rowspan=3, columnspan=2)

        bouton_affichage_L_ele = tk.Button(
            frame1_L_ele, width=TAILLE_CASE[0], height=TAILLE_CASE[1])
        bouton_affichage_L_ele.configure(command=affiches_lignes_element_L_ele)
        bouton_affichage_L_ele.grid(row=1, column=7, rowspan=3, columnspan=2)

        coche_El_I_L_ele = ttk.Radiobutton(frame1_L_ele, text=_("Neutres"),
                                               variable=flag_neutres_ions_L_ele, value=1,
                                               command=affiches_lignes_neutres_ions_L_ele)
        coche_El_I_L_ele.grid(row=1, column=5, columnspan=3, sticky=tk.W)
        coche_El_II_L_ele = ttk.Radiobutton(frame1_L_ele, text=_("Ions +"),
                                                variable=flag_neutres_ions_L_ele, value=2,
                                                command=affiches_lignes_neutres_ions_L_ele)
        coche_El_II_L_ele.grid(row=2, column=5, columnspan=3, sticky=tk.W)

        coche_sup10_L_ele = ttk.Checkbutton(frame1_L_ele, text=_("I relative >= 10%"),
                                                variable=flag_sup10_L_ele,
                                                command=affiches_lignes_element_L_ele)
        coche_sup10_L_ele.grid(row=1, column=9, columnspan=4, sticky=tk.W)
        coche_sup1_L_ele = ttk.Checkbutton(frame1_L_ele, text=_("1% <= I relative < 10%"),
                                               variable=flag_sup1_L_ele,
                                               command=affiches_lignes_element_L_ele)
        coche_sup1_L_ele.grid(row=2, column=9, columnspan=4, sticky=tk.W)
        coche_inf1_L_ele = ttk.Checkbutton(frame1_L_ele, text=_("I relative < 1%"),
                                               variable=flag_inf1_L_ele,
                                               command=affiches_lignes_element_L_ele)
        coche_inf1_L_ele.grid(row=3, column=9, columnspan=4, sticky=tk.W)

        DataFrame_tableau_periodique_L_ele = lit_tableau_periodique_L_ele()
        affiche_tableau_periodique_L_ele(DataFrame_tableau_periodique_L_ele,
                                         frame1_L_ele, bouton_affichage_L_ele)
        tableau_periodique_ouvert_L_ele = True
        fenetre_classification_L_ele.protocol(
            "WM_DELETE_WINDOW", ferme_fenetre_classification_L_ele)
    else:
        fenetre_classification_L_ele.attributes("-topmost", True)
        fenetre_classification_L_ele.attributes("-topmost", False)


def ferme_fenetre_classification_L_ele():
    """
    Ferme la fenêtre Toplevel classification périodique
    """
    global tableau_periodique_ouvert_L_ele
    tableau_periodique_ouvert_L_ele = False
    fenetre_classification_L_ele.destroy()


###################################################################################################
###################################################################################################
# LIBStick : interface principale
###################################################################################################
###################################################################################################
def __________IHM_LIBStick__________():
    """ LIBStick : interface principale"""
###################################################################################################
###################################################################################################


###################################################################################################
#  Interface graphique : nouvelles classes
###################################################################################################
class AutoScrollbar(ttk.Scrollbar):
    """
    """
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    # cf. : http://effbot.org/zone/tk-autoscrollbar.htm

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from tk!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)


class case_classification(tk.Button):
    # TAILLE_CASE = [2,2]
    def __init__(self, boss, nom, symbole,  Z, ligne, colonne, couleur, bouton_affichage):
        texte = "    "+str(Z)+"\n"+symbole
        tk.Button.__init__(self, boss, text=texte, bg=couleur, command=lambda: self.affiche_pics(
            nom, symbole, Z, couleur, bouton_affichage))
        self.configure(width=TAILLE_CASE[0], height=TAILLE_CASE[1])
        self.config(font=font.Font(size=TAILLE_FONT_CLASSIFICATION))
        self.grid(row=ligne, column=colonne)

    def affiche_pics(self, nom, symbole, Z, couleur, bouton_affichage):
        global symbole_L_ele
        global DataFrame_element_L_ele
        symbole_L_ele = symbole
        texte = "     "+str(Z)+"\n"+symbole
        bouton_affichage.configure(text=texte, bg=couleur,
                                   width=TAILLE_CASE[0], height=TAILLE_CASE[1])
        # bouton_affichage.config(font=font.Font(weight="bold"))
        bouton_affichage.config(font=font.Font(
            size=TAILLE_FONT_CLASSIFICATION, weight="bold"))
        DataFrame_element_L_ele = lit_element_L_ele(symbole)
        affiches_lignes_element_L_ele()
        print(nom)


###################################################################################################
# Interface graphique : création fenêtre principale avec scrolls et onglets
###################################################################################################
# fenetre_principale = tk.Tk()
fenetre_principale =ThemedTk(theme = style_interface_LIBStick)
style_LIBStick = ttk.Style()
if flag_style_LIBStick_ini == str(True) :
    # Create style used by default for all Frames
    style_LIBStick.configure('TFrame', background = COULEUR_INTERFACE)
    style_LIBStick.configure('TButton', background  = COULEUR_INTERFACE)
    style_LIBStick.configure('TSpinbox', background = COULEUR_INTERFACE)
    style_LIBStick.configure('TCheckbutton', background = COULEUR_INTERFACE)
    style_LIBStick.configure('TLabel', background = COULEUR_INTERFACE)
    style_LIBStick.configure('TNotebook', background = COULEUR_INTERFACE)
    style_LIBStick.configure('TCombobox', background = COULEUR_INTERFACE)
    style_LIBStick.configure('TRadiobutton', background = COULEUR_INTERFACE)
    style_LIBStick.configure('Treeview', background = COULEUR_INTERFACE)

bg_couleur = fenetre_principale._get_bg_color()
# print(fenetre_principale.get_themes())
fenetre_principale.title("LIBStick v3.0")
fenetre_principale.geometry("1155x750+100+50")

# vscrollbar = AutoScrollbar(fenetre_principale, orient=tk.VERTICAL)
# vscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
# hscrollbar = AutoScrollbar(fenetre_principale, orient=tk.HORIZONTAL)
# hscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)
vscrollbar = AutoScrollbar(fenetre_principale, orient=tk.VERTICAL)
vscrollbar.grid(row=0, column=1, sticky=tk.N+tk.S)
hscrollbar = AutoScrollbar(fenetre_principale, orient=tk.HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=tk.E+tk.W)

canevas_scroll = tk.Canvas(fenetre_principale, yscrollcommand=vscrollbar.set,
                                xscrollcommand=hscrollbar.set, bg = bg_couleur)
canevas_scroll.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

vscrollbar.config(command=canevas_scroll.yview)
hscrollbar.config(command=canevas_scroll.xview)
# make the canvas expandable
fenetre_principale.grid_rowconfigure(0, weight=1)
fenetre_principale.grid_columnconfigure(0, weight=1)

frame_scroll = ttk.Frame(canevas_scroll)
# frame_scroll.rowconfigure(1, weight=1)
# frame_scroll.columnconfigure(1, weight=1)

onglets = ttk.Notebook(frame_scroll)
onglets.pack()
onglet1 = ttk.Frame(onglets)
onglet2 = ttk.Frame(onglets)
onglet3 = ttk.Frame(onglets)
onglet4 = ttk.Frame(onglets)
onglet1.pack()
onglet2.pack()
onglet3.pack()
onglet4.pack()

onglets.add(onglet1, text=_("LIBStick pré-traitements"))
onglets.add(onglet2, text=_("LIBStick extraction"))
onglets.add(onglet3, text=_("LIBStick comparaison"))
onglets.add(onglet4, text=_("LIBStick ACP"))

barre_menus = tk.Menu(fenetre_principale)
menu_fichier = tk.Menu(barre_menus)
menu_traitement = tk.Menu(barre_menus)
menu_extraction = tk.Menu(barre_menus)
menu_comparaison = tk.Menu(barre_menus)
menu_outils = tk.Menu(barre_menus)
sous_menu_langue = tk.Menu(menu_outils)
sous_menu_style = tk.Menu(menu_outils)

barre_menus.add_cascade(label=_("Fichier"), menu=menu_fichier)
menu_fichier.add_command(label=_("Sauvegarde des paramètres actuels"), command=ecrit_fichier_ini)
menu_fichier.add_command(
    label=_("Restaure les paramètres par défaut au prochain démarrage"), command=reset_fichier_ini)
menu_fichier.add_command(label=_("Quitter"), command=fenetre_principale.destroy)
menu_fichier.add_command(label=_("Redémarrer"), command=redemarre_programme)

barre_menus.add_cascade(label=_("Traitement"), menu=menu_traitement)
flag_echelle_log_L_trait = tk.BooleanVar(value=False)
menu_traitement.add_checkbutton(label=_("Echelle log y"), variable=flag_echelle_log_L_trait,
                                command = mise_a_jour_affichage_L_trait)

barre_menus.add_cascade(label=_("Extraction"), menu=menu_extraction)
flag_echelle_log_L_ext = tk.BooleanVar(value=False)
menu_extraction.add_checkbutton(label=_("Echelle log y"), variable=flag_echelle_log_L_ext,
                                command = mise_a_jour_affichage_L_ext)

barre_menus.add_cascade(label=_("Comparaison"), menu=menu_comparaison)
flag_echelle_log_L_comp = tk.BooleanVar(value=False)
menu_comparaison.add_checkbutton(label=_("Echelle log y"), variable=flag_echelle_log_L_comp,
                                command = mise_a_jour_affichage_L_comp)

barre_menus.add_cascade(label=_("Outils"), menu=menu_outils)
flag_zoom_auto_y = tk.BooleanVar(value=True)
menu_outils.add_checkbutton(label=_("Zoom auto en y"), variable=flag_zoom_auto_y)
menu_outils.add_command(label=_("Fenetre principale premier plan"),
                        command=fenetre_pricipale_en_avant)

menu_outils.add_separator()
menu_outils.add_cascade(label=_("Langue au prochain démarage"), menu=sous_menu_langue)
langue_menu = tk.StringVar(value=langue_LIBStick)
sous_menu_langue.add_radiobutton(label=_("Français"), value="fr", variable=langue_menu,
                                 command=ecrit_param_langue)
sous_menu_langue.add_radiobutton(label=_("Anglais"), value="en", variable=langue_menu,
                                 command=ecrit_param_langue)
sous_menu_langue.add_radiobutton(label=_("Espagnol"), value="es", variable=langue_menu,
                                 command=ecrit_param_langue)
sous_menu_langue.add_radiobutton(label=_("Italien"), value="it", variable=langue_menu,
                                 command=ecrit_param_langue)

menu_outils.add_separator()
menu_outils.add_cascade(label=_("Style au prochain démarage"), menu=sous_menu_style)
flag_style_LIBStick_couleur = tk.BooleanVar(value=flag_style_LIBStick_ini)
sous_menu_style.add_checkbutton(label=_("Couleur de LIBStick"), variable=flag_style_LIBStick_couleur,
                            command=ecrit_param_interface)
sous_menu_style.add_separator()
style_menu = tk.StringVar(value=style_interface_LIBStick)
sous_menu_style.add_radiobutton(label="keramik", value="keramik", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="plastik", value="plastik", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="scidsand", value="scidsand", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="aquativo", value="aquativo", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="winxpblue", value="winxpblue", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="black", value="black", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_separator()
sous_menu_style.add_radiobutton(label="ubuntu", value="ubuntu", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="kroc", value="kroc", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="clearlooks", value="clearlooks", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="itft1", value="itft1", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="elegance", value="elegance", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="smog", value="smog", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_separator()
sous_menu_style.add_radiobutton(label="alt", value="alt", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="default", value="default", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="classic", value="classic", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="clam", value="clam", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="breeze", value="breeze", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="arc", value="arc", variable=style_menu,
                                 command=ecrit_param_interface)
sous_menu_style.add_radiobutton(label="blue", value="blue", variable=style_menu,
                                 command=ecrit_param_interface)

fenetre_principale.config(menu=barre_menus)


###################################################################################################
# Interface graphique : gestion de évènements
###################################################################################################
def clic_onglets(event):
    #   onglet_clic = onglets.tk.call(onglets._w, "identify", "tab", event.x, event.y)
    onglet_actif = onglets.index(onglets.select())
    if onglet_actif == 0:
        affiche_nom_spectre_onglet1()
    if onglet_actif == 1:
        affiche_nom_spectre_onglet2()
    if onglet_actif == 2:
        affiche_nom_spectre_onglet3()
    if onglet_actif == 3:
        affiche_nom_spectre_onglet4()


onglets.bind("<ButtonRelease-1>", clic_onglets)


###################################################################################################
###################################################################################################
# Interface graphique LIBStick_IHM_traitement : onglet 1
###################################################################################################
###################################################################################################
def __________IHM_traitement__________():
    """ Interface graphique LIBStick_IHM_traitement : onglet 1"""
###################################################################################################
###################################################################################################


###################################################################################################
# Interface graphique : création des différentes zones/étapes (frames 1-2)
###################################################################################################
frame1_L_trait = ttk.Frame(onglet1, borderwidth=2, relief=tk.RAISED)
frame2_L_trait = ttk.Frame(onglet1, borderwidth=2, relief=tk.RAISED)

frame1_L_trait.grid(row=10, column=10, sticky="nsew")
frame2_L_trait.grid(row=20, column=10, sticky="nsew")
# frame1_L_trait.grid(row=10, column=10, padx=5, pady=5,sticky = tk.W)
# frame2_L_trait.grid(row=20, column=10, padx=5, pady=5,sticky = tk.W)
# frame1_L_trait.grid_propagate(False)
# frame2_L_trait.grid_propagate(False)


###################################################################################################
# Interface graphique frame1_L_trait :
###################################################################################################
canevas0_L_trait = tk.Canvas(frame1_L_trait, width=largeur_canevas_spectres,
                             height=(hauteur_canevas_spectres+170), bg="white")
canevas0_L_trait.grid(row=1, column=1, columnspan=6)

ligne_position_0_x_L_trait = canevas0_L_trait.create_line(0, 0, 0, hauteur_canevas_spectres+170, fill="white")
ligne_position_0_y_L_trait = canevas0_L_trait.create_line(0, 0, largeur_canevas_spectres, 0, fill="white")

lambda_texte_L_trait = ttk.Label(
    frame1_L_trait, text="Lambda = " + str(format(lambda_texte_spectre_0_L_trait, "4.1f") + " nm"))
lambda_texte_L_trait.grid(row=2, column=5)

text1_L_trait = ttk.Label(frame1_L_trait, text=_("Borne inf :"))
text2_L_trait = ttk.Label(frame1_L_trait, text=_("Borne sup :"))
text1_L_trait.grid(row=2, column=1, sticky=tk.E)
text2_L_trait.grid(row=2, column=3, sticky=tk.E)
variable_1_L_trait = tk.DoubleVar(value=tableau_bornes_L_trait[0])
variable_2_L_trait = tk.DoubleVar(value=tableau_bornes_L_trait[1])
entree1_L_trait = ttk.Spinbox(frame1_L_trait, from_=198, to=1013, textvariable=variable_1_L_trait,
                              command=deplace_ligne0_1_L_trait, foreground="red", width=5)
entree2_L_trait = ttk.Spinbox(frame1_L_trait, from_=198, to=1013, textvariable=variable_2_L_trait,
                              command=deplace_ligne0_2_L_trait, foreground="red", width=5)
entree1_L_trait.grid(row=2, column=2, sticky=tk.W)
entree2_L_trait.grid(row=2, column=4, sticky=tk.W)

text3_L_trait = ttk.Label(frame1_L_trait, text=_("Filtre :"))
text4_L_trait = ttk.Label(frame1_L_trait, text=_("Taille :"))
text5_L_trait = ttk.Label(frame1_L_trait, text=_("Ordre :"))
text5_2_L_trait = ttk.Label(frame1_L_trait, text=_("Dérivée :"))
text3_L_trait.grid(row=3, column=1, sticky=tk.E)
text4_L_trait.grid(row=3, column=3, sticky=tk.E)
text5_L_trait.grid(row=4, column=3, sticky=tk.E)
text5_2_L_trait.grid(row=4, column=5, sticky=tk.E)
type_filtre_L_trait = tk.StringVar(value="Savitzky-Golay")
taille_filtre_L_trait = tk.IntVar(value=5)
ordre_filtre_L_trait = tk.IntVar(value=2)
derivee_filtre_L_trait = tk.IntVar(value=0)
# entree3_L_trait=ttk.Combobox(frame1_L_trait, textvariable=type_filtre_L_trait,
#                                     values=["Aucun", "Savitzky-Golay", "Median", "Passe-bas"])
entree3_L_trait = ttk.Combobox(frame1_L_trait, textvariable=type_filtre_L_trait,
                               values=[_("Aucun"), "Savitzky-Golay", "Median"], width=14)
entree4_L_trait = ttk.Spinbox(frame1_L_trait, from_=3, to=199,increment=2,
                              textvariable=taille_filtre_L_trait, width=5, foreground="black")
entree5_L_trait = ttk.Spinbox(frame1_L_trait, from_=2, to=9,
                              textvariable=ordre_filtre_L_trait, width=5, foreground="black")
entree5_2_L_trait = ttk.Spinbox(frame1_L_trait, from_=0, to=2,
                                textvariable=derivee_filtre_L_trait, width=5, foreground="black")
entree3_L_trait.grid(row=3, column=2, sticky=tk.W)
entree4_L_trait.grid(row=3, column=4, sticky=tk.W)
entree5_L_trait.grid(row=4, column=4, sticky=tk.W)
entree5_2_L_trait.grid(row=4, column=6, sticky=tk.W)

text6_L_trait = ttk.Label(frame1_L_trait, text=_("Fond :"))
text7_L_trait = ttk.Label(frame1_L_trait, text=_("Itérations :"))
text8_L_trait = ttk.Label(frame1_L_trait, text="LLS :")
text6_L_trait.grid(row=5, column=1, sticky=tk.E)
text7_L_trait.grid(row=5, column=3, sticky=tk.E)
text8_L_trait.grid(row=5, column=5, sticky=tk.E)
type_fond_L_trait = tk.StringVar(value="SNIP")
param1_fond_L_trait = tk.IntVar(value=20)
param2_fond_L_trait = tk.IntVar(value=10)
param3_fond_L_trait = tk.BooleanVar(value=False)
# entree6_L_trait=ttk.Combobox(frame1_L_trait, textvariable=type_fond_L_trait,
#                                     values=["Aucun", "Rolling ball", "SNIP", "Top-hat", "Peak filling"])
entree6_L_trait = ttk.Combobox(frame1_L_trait, textvariable=type_fond_L_trait,
                               values=[_("Aucun"), "Rolling ball", "SNIP"], width=14)
entree7_L_trait = ttk.Spinbox(frame1_L_trait, from_=3, to=100, textvariable=param1_fond_L_trait,
                              width=5, foreground="black")
entree8_L_trait = ttk.Spinbox(frame1_L_trait, from_=1, to=100, textvariable=param2_fond_L_trait,
                              width=5, foreground="black")
entree8bis_L_trait = ttk.Checkbutton(frame1_L_trait, text="LLS", variable=param3_fond_L_trait)
entree6_L_trait.grid(row=5, column=2, sticky=tk.W)
entree7_L_trait.grid(row=5, column=4, sticky=tk.W)
entree8_L_trait.grid(row=5, column=6, sticky=tk.W)
entree8_L_trait.grid_remove()
entree8bis_L_trait.grid(row=5, column=6, sticky=tk.W)

frame1_1_L_trait = ttk.Frame(frame1_L_trait)
frame1_1_L_trait.grid(row=1, column=7, rowspan=4, sticky=tk.N+tk.S)

text_zoom_L_trait = ttk.Label(frame1_1_L_trait, text="Zoom : ", width=8)
text_zoom_L_trait.grid(row=1, column=1, sticky=tk.N)
variable_zoom_inf_L_trait = tk.DoubleVar(value=198)
variable_zoom_sup_L_trait = tk.DoubleVar(value=1013)
entree_zoom_inf_L_trait = ttk.Spinbox(frame1_1_L_trait, from_=198, to=1013, increment=5, textvariable=variable_zoom_inf_L_trait,
                                      command=change_zoom_inf_L_trait, width=8, foreground="black")
entree_zoom_sup_L_trait = ttk.Spinbox(frame1_1_L_trait, from_=198, to=1013, increment=5, textvariable=variable_zoom_sup_L_trait,
                                      command=change_zoom_sup_L_trait, width=8, foreground="black")
entree_zoom_inf_L_trait.grid(row=2, column=1, sticky=tk.N)
entree_zoom_sup_L_trait.grid(row=3, column=1, sticky=tk.N)
type_fichier_L_trait = tk.StringVar(value=".asc")
bouton_rep_L_trait = ttk.Button(frame1_1_L_trait, text=_("Fichier"),
                                    command=choix_fichier_L_trait, width=10)
bouton_visualisation_L_trait = ttk.Button(frame1_1_L_trait, text=_("Visualisation"),
                                          command=visualisation_L_trait, state="disable", width=10)
# bouton_rep_L_trait = ttk.Button(frame1_1_L_trait, text=_("Fichier"),
#                                 command=choix_fichier_L_trait, width=8)
# bouton_visualisation_L_trait = ttk.Button(frame1_1_L_trait, text=_("Visualisation"),
#                                           command=visualisation_L_trait, state="disable", width=8)
bouton_rep_L_trait.grid(row=4, column=1, sticky=tk.N)
bouton_visualisation_L_trait.grid(row=5, column=1, sticky=tk.N)

image_classification = tk.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")

bouton_classification_L_trait = tk.Button(frame1_1_L_trait, image=image_classification,
                                          command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_trait.grid(row=8, column=1, sticky=tk.S)


###################################################################################################
# Interface graphique frame2_L_trait
###################################################################################################
canevas1_L_trait = tk.Canvas(frame2_L_trait, width=largeur_canevas_spectres,
                             height=hauteur_canevas_spectres, bg="white")
canevas1_L_trait.grid(row=1, column=1, columnspan=2)

ligne_position_1_x_L_trait = canevas1_L_trait.create_line(0, 0, 0, hauteur_canevas_spectres, fill="white")
ligne_position_1_y_L_trait = canevas0_L_trait.create_line(0, 0, largeur_canevas_spectres, 0, fill="white")

frame2_1_L_trait = ttk.Frame(frame2_L_trait)
frame2_1_L_trait.grid(row=1, column=5, rowspan=3, sticky=tk.N)

flag_tous_fichiers_init_L_trait = False
flag_tous_fichiers_L_trait = tk.BooleanVar(value=flag_tous_fichiers_init_L_trait)
coche_tous_fichiers_L_trait = ttk.Checkbutton(frame2_1_L_trait, text=_("Appliquer sur\ntous les fichiers\ndu répertoire"),
                                                  variable=flag_tous_fichiers_L_trait)
coche_tous_fichiers_L_trait.grid(row=1, column=1)

flag_sauve_fond_init_L_trait = False
flag_sauve_fond_L_trait = tk.BooleanVar(value=flag_sauve_fond_init_L_trait)
coche_sauve_fond_L_trait = ttk.Checkbutton(frame2_1_L_trait, text=_("Sauvegarde du\nfond continu"),
                                               variable=flag_sauve_fond_L_trait)
coche_sauve_fond_L_trait.grid(row=2, column=1)

bouton_execute_L_trait = ttk.Button(frame2_1_L_trait, text=_("Executer"), state="disable",
                                        command=execute_L_trait, width=10)
bouton_execute_L_trait.grid(row=3, column=1)

text_spectre_L_trait = ttk.Label(frame2_1_L_trait, text=_("Spectre : "))
text_spectre_L_trait.grid(row=4, column=1, sticky=tk.N)
numero_spectre_L_trait = tk.IntVar(value=1)
entree_spectre_L_trait = ttk.Spinbox(frame2_1_L_trait, from_=1, to=50, textvariable=numero_spectre_L_trait,
                                     command=lit_affiche_spectre_numero_L_trait, width=8, foreground="black")
entree_spectre_L_trait.grid(row=5, column=1, sticky=tk.N)


###################################################################################################
# Interface graphique : gestion de évènements
###################################################################################################
entree_zoom_inf_L_trait.bind("<Return>", change_zoom_inf_return_L_trait)
entree_zoom_sup_L_trait.bind("<Return>", change_zoom_sup_return_L_trait)
entree_zoom_inf_L_trait.bind("<KP_Enter>", change_zoom_inf_return_L_trait)
entree_zoom_sup_L_trait.bind("<KP_Enter>", change_zoom_sup_return_L_trait)
entree_zoom_inf_L_trait.bind("<Tab>", change_zoom_inf_return_L_trait)
entree_zoom_sup_L_trait.bind("<Tab>", change_zoom_sup_return_L_trait)
# entree_zoom_inf_L_trait.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_trait)
# entree_zoom_sup_L_trait.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_trait)

canevas0_L_trait.bind("<Button-1>", zoom_clic_0_L_trait)
canevas0_L_trait.bind("<B1-Motion>", zoom_drag_and_drop_0_L_trait)
canevas0_L_trait.bind("<ButtonRelease-1>", zoom_clic_release_L_trait)
canevas0_L_trait.bind("<ButtonRelease-3>", affiche_lambda_L_trait)
canevas0_L_trait.bind("<Motion>", affiche_position_souris_0_L_trait)
canevas0_L_trait.bind("<B3-Motion>", affiche_position_souris_motion_0_L_trait)

canevas1_L_trait.bind("<Button-1>", zoom_clic_1_L_trait)
canevas1_L_trait.bind("<B1-Motion>", zoom_drag_and_drop_1_L_trait)
canevas1_L_trait.bind("<ButtonRelease-1>", zoom_clic_release_L_trait)
canevas1_L_trait.bind("<ButtonRelease-3>", affiche_lambda_L_trait)
canevas1_L_trait.bind("<Motion>", affiche_position_souris_1_L_trait)
canevas1_L_trait.bind("<B3-Motion>", affiche_position_souris_motion_1_L_trait)

entree1_L_trait.bind("<Return>", deplace_ligne0_1_return_L_trait)
entree2_L_trait.bind("<Return>", deplace_ligne0_2_return_L_trait)
entree1_L_trait.bind("<KP_Enter>", deplace_ligne0_1_return_L_trait)
entree2_L_trait.bind("<KP_Enter>", deplace_ligne0_2_return_L_trait)
entree1_L_trait.bind("<Tab>", deplace_ligne0_1_return_L_trait)
entree2_L_trait.bind("<Tab>", deplace_ligne0_2_return_L_trait)
# entree1_L_trait.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_1_return_L_trait)
# entree2_L_trait.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_2_return_L_trait)

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


###################################################################################################
###################################################################################################
# Interface graphique LIBStick_IHM_extraction : onglet 2
###################################################################################################
###################################################################################################
def __________IHM_extraction__________():
    """ Interface graphique LIBStick_IHM_extraction : onglet 2"""
###################################################################################################
###################################################################################################


###################################################################################################
# Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###################################################################################################
frame1_L_ext = ttk.Frame(onglet2, borderwidth=2, relief=tk.RAISED)
frame2_L_ext = ttk.Frame(onglet2, borderwidth=2, relief=tk.RAISED)
frame3_L_ext = ttk.Frame(onglet2, borderwidth=2, relief=tk.RAISED)

frame1_L_ext.grid(row=10, column=10, sticky="nsew")
frame2_L_ext.grid(row=20, column=10, sticky="nsew")
frame3_L_ext.grid(row=30, column=10, sticky="nsew")
# frame1_L_ext.grid(row=10, column=10, padx=5, pady=5,sticky = tk.W)
# frame2_L_ext.grid(row=20, column=10, padx=5, pady=5,sticky = tk.W)
# frame3_L_ext.grid(row=30, column=10, padx=5, pady=5, sticky = tk.W)


###################################################################################################
# Interface graphique frame1_L_ext : création selection répertoire, affiche spectre et bouton executer
###################################################################################################
canevas0_L_ext = tk.Canvas(frame1_L_ext, width=largeur_canevas_spectres,
                           height=hauteur_canevas_spectres, bg="white")
canevas0_L_ext.grid(row=1, column=1, columnspan=6)

ligne_position_x_L_ext = canevas0_L_ext.create_line(0, 0, 0, hauteur_canevas_spectres, fill="white")
ligne_position_y_L_ext = canevas0_L_ext.create_line(0, 0, largeur_canevas_spectres, 0, fill="white")

lambda_texte_L_ext = ttk.Label(
    frame1_L_ext, text="Lambda = " + str(format(lambda_texte_spectre_L_ext, "4.1f") + " nm"))
lambda_texte_L_ext.grid(row=2, column=5)

text1_L_ext = ttk.Label(frame1_L_ext, text=_("Première borne inf (nm)"))
text2_L_ext = ttk.Label(frame1_L_ext, text=_("Première borne sup (nm)"))
text3_L_ext = ttk.Label(frame1_L_ext, text=_("Seconde borne inf (nm)"))
text4_L_ext = ttk.Label(frame1_L_ext, text=_("Seconde borne sup (nm)"))
text1_L_ext.grid(row=2, column=1, sticky=tk.E)
text2_L_ext.grid(row=2, column=3, sticky=tk.E)
text3_L_ext.grid(row=3, column=1, sticky=tk.E)
text4_L_ext.grid(row=3, column=3, sticky=tk.E)

variable_1_L_ext = tk.DoubleVar(value=tableau_bornes_L_ext[0, 0])
variable_2_L_ext = tk.DoubleVar(value=tableau_bornes_L_ext[0, 1])
variable_3_L_ext = tk.DoubleVar(value=tableau_bornes_L_ext[1, 0])
variable_4_L_ext = tk.DoubleVar(value=tableau_bornes_L_ext[1, 1])
entree1_L_ext = ttk.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_1_L_ext,
                            command=deplace_ligne0_1_L_ext, foreground="red", width=5)
entree2_L_ext = ttk.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_2_L_ext,
                            command=deplace_ligne0_2_L_ext, foreground="red", width=5)
entree3_L_ext = ttk.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_3_L_ext,
                            command=deplace_ligne0_3_L_ext, foreground="blue", width=5)
entree4_L_ext = ttk.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_4_L_ext,
                            command=deplace_ligne0_4_L_ext, foreground="blue", width=5)
entree1_L_ext.grid(row=2, column=2, sticky=tk.W)
entree2_L_ext.grid(row=2, column=4, sticky=tk.W)
entree3_L_ext.grid(row=3, column=2, sticky=tk.W)
entree4_L_ext.grid(row=3, column=4, sticky=tk.W)

flag_zone2_L_ext = tk.IntVar(value=flag_zone2_init_L_ext)
coche_zone2_L_ext = ttk.Checkbutton(frame1_L_ext, text=_("Seconde extraction"),
                                        variable=flag_zone2_L_ext, command=change_flag_zone2_L_ext)
coche_zone2_L_ext.grid(row=3, column=5)

bouton_reset_L_ext = ttk.Button(frame1_L_ext, text=_("Reset"),
                                    command=reset_tableau_L_ext, width=10)
bouton_reset_L_ext.grid(row=2, column=6, rowspan=2)

frame1_1_L_ext = ttk.Frame(frame1_L_ext)
frame1_1_L_ext.grid(row=1, column=7, rowspan=3, sticky=tk.N)

text_zoom_L_ext = ttk.Label(frame1_1_L_ext, text="Zoom : ", width=8)
text_zoom_L_ext.grid(row=1, column=1)
variable_zoom_inf_L_ext = tk.DoubleVar(value=198)
variable_zoom_sup_L_ext = tk.DoubleVar(value=1013)
entree_zoom_inf_L_ext = ttk.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_zoom_inf_L_ext,
                                    command=change_zoom_inf_L_ext, width=8, foreground="black")
entree_zoom_sup_L_ext = ttk.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_zoom_sup_L_ext,
                                    command=change_zoom_sup_L_ext, width=8, foreground="black")
entree_zoom_inf_L_ext.grid(row=2, column=1)
entree_zoom_sup_L_ext.grid(row=3, column=1)

type_fichier_L_ext = tk.StringVar(value=".asc")
# bouton_rep_L_ext=ttk.Button(frame1_1_L_ext, text="Repertoire\nde travail" ,command=choix_rep_L_ext, width=8)
bouton_rep_L_ext = ttk.Button(frame1_1_L_ext, text=_("Fichier"),
                                  command=choix_fichier_L_ext, width=10)
bouton_execute_L_ext = ttk.Button(
    frame1_1_L_ext, text=_("Exécute"), command=execute_scripts_L_ext, state="disable", width=10)
bouton_rep_L_ext.grid(row=4, column=1)
bouton_execute_L_ext.grid(row=5, column=1)

flag_2D_L_ext = tk.IntVar(value=flag_2D_init_L_ext)
# coche_2D_L_ext=ttk.Checkbutton(frame1_1_L_ext, text="Sortie 2D", variable=flag_2D_L_ext, command=change_flag_2D_L_ext)
coche_2D_L_ext = ttk.Checkbutton(
    frame1_1_L_ext, text=_("Sortie 2D"), variable=flag_2D_L_ext)
coche_2D_L_ext.grid(row=6, column=1)

flag_3D_L_ext = tk.IntVar(value=flag_3D_init_L_ext)
# coche_3D_L_ext=ttk.Checkbutton(frame1_1_L_ext, text="Sortie 3D", variable=flag_3D_L_ext, command=change_flag_3D_L_ext)
coche_3D_L_ext = ttk.Checkbutton(
    frame1_1_L_ext, text=_("Sortie 3D"), variable=flag_3D_L_ext)
coche_3D_L_ext.grid(row=7, column=1)

# image_classification=tk.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")
bouton_classification_L_ext = tk.Button(frame1_1_L_ext, image=image_classification,
                                        command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_ext.grid(row=8, column=1, sticky=tk.S)


###################################################################################################
# Interface graphique frame2_L_ext : création visues des résultats et aide à la sélection
###################################################################################################
canevas1_L_ext = tk.Canvas(frame2_L_ext, width=largeur_canevas_spectres/2,
                           height=hauteur_canevas_spectres, bg="white")
canevas2_L_ext = tk.Canvas(frame2_L_ext, width=largeur_canevas_spectres/2,
                           height=hauteur_canevas_spectres, bg="white")
canevas1_L_ext.grid(row=1, column=1, columnspan=4)
canevas2_L_ext.grid(row=1, column=5, columnspan=4)

text5_L_ext = ttk.Label(frame2_L_ext, text=_("Position x (nm) : "))
text6_L_ext = ttk.Label(
    frame2_L_ext, text=_("Position y (n° de spectre) : "))
text7_L_ext = ttk.Label(frame2_L_ext, text=_("Position x (nm) : "))
text8_L_ext = ttk.Label(
    frame2_L_ext, text=_("Position y (n° de spectre) : "))
text5_L_ext.grid(row=2, column=1, sticky=tk.E)
text6_L_ext.grid(row=2, column=3, sticky=tk.E)
text7_L_ext.grid(row=2, column=5, sticky=tk.E)
text8_L_ext.grid(row=2, column=7, sticky=tk.E)

variable_5_L_ext = tk.DoubleVar(value=0)
variable_6_L_ext = tk.IntVar(value=0)
variable_7_L_ext = tk.DoubleVar(value=0)
entree5_L_ext = ttk.Spinbox(frame2_L_ext, from_=198, to=1013, textvariable=variable_5_L_ext,
                            command=vars_5_6_to_coord1_L_ext, increment=0.5, width=5, foreground="red")
entree6_L_ext = ttk.Spinbox(frame2_L_ext, from_=1, to=hauteur_canevas_spectres, textvariable=variable_6_L_ext,
                            command=vars_5_6_to_coord1_L_ext, width=5, foreground="red")
entree7_L_ext = ttk.Spinbox(frame2_L_ext, from_=198, to=1013, textvariable=variable_7_L_ext,
                            command=vars_7_8_to_coord2_L_ext, increment=0.5, width=5, foreground="blue")
entree8_L_ext = ttk.Spinbox(frame2_L_ext, from_=1, to=hauteur_canevas_spectres, textvariable=variable_6_L_ext,
                            command=vars_7_8_to_coord2_L_ext, width=5, foreground="blue")
entree5_L_ext.grid(row=2, column=2, sticky=tk.W)
entree6_L_ext.grid(row=2, column=4, sticky=tk.W)
entree7_L_ext.grid(row=2, column=6, sticky=tk.W)
entree8_L_ext.grid(row=2, column=8, sticky=tk.W)

frame2_1_L_ext = ttk.Frame(frame2_L_ext)
frame2_1_L_ext.grid(row=1, column=9, rowspan=3, sticky=tk.N)

flag_image_brute_L_ext = tk.BooleanVar(value=flag_image_brute_init_L_ext)
coche_image_brute_L_ext = ttk.Checkbutton(frame2_1_L_ext, text=_("Image brute\nspectres non\nnormalisés"),
                                          variable=flag_image_brute_L_ext, command=change_flag_image_brute_L_ext)
coche_image_brute_L_ext.grid(row=1, column=1)

flag_spectre_inclus_moyenne_L_ext = tk.BooleanVar(value=True)
coche_spectre_inclus_moyenne_L_ext = ttk.Checkbutton(frame2_1_L_ext, text=_("Spectre inclus\ndans spectre\nmoyen"), variable=flag_spectre_inclus_moyenne_L_ext,
                                                         command=change_bool_spectre_L_ext)
coche_spectre_inclus_moyenne_L_ext.grid(row=2, column=1)

ligne1_vert_L_ext = canevas1_L_ext.create_line(x1_L_ext, 0, x1_L_ext, 200, fill="white")
ligne1_hori_L_ext = canevas1_L_ext.create_line(0, y_L_ext, largeur_canevas_spectres/2, y_L_ext, fill="white")
ligne2_vert_L_ext = canevas1_L_ext.create_line(x1_L_ext, 0, x1_L_ext, 200, fill="white")
ligne2_hori_L_ext = canevas1_L_ext.create_line(0, y_L_ext, largeur_canevas_spectres/2, y_L_ext, fill="white")

affiche_lignes_spectre_L_ext()


###################################################################################################
# Interface graphique frame3_L_ext : création selection des spectres à moyenner
###################################################################################################
canevas3_L_ext = tk.Canvas(frame3_L_ext, width=largeur_canevas_spectres/2,
                           height=200, bg="white")
canevas4_L_ext = tk.Canvas(frame3_L_ext, width=largeur_canevas_spectres/2,
                           height=200, bg="white")
canevas3_L_ext.grid(row=3, column=1, columnspan=2)
canevas4_L_ext.grid(row=3, column=3, columnspan=2)

frame3_1_L_ext = ttk.Frame(frame3_L_ext)
frame3_1_L_ext.grid(row=1, column=5, rowspan=4, sticky=tk.N)

text9_L_ext = ttk.Label(frame3_1_L_ext, text=_("Du spectre n° :"))
text10_L_ext = ttk.Label(frame3_1_L_ext, text=_("Au spectre n° :"))
text9_L_ext.grid(row=1, column=1)
text10_L_ext.grid(row=3, column=1)

variable_9_L_ext = tk.IntVar(value=0)
variable_9_avant_L_ext = tk.IntVar(value=1)
variable_10_L_ext = tk.IntVar(value=0)
variable_10_avant_L_ext = tk.IntVar(value=0)
entree9_L_ext = ttk.Spinbox(frame3_1_L_ext, from_=1, to=hauteur_canevas_spectres,textvariable=variable_9_L_ext,
                            command=retro_action_entree10_L_ext, width=5, foreground="black")
entree10_L_ext = ttk.Spinbox(frame3_1_L_ext, from_=1, to=hauteur_canevas_spectres,textvariable=variable_10_L_ext,
                             command=retro_action_entree9_L_ext, width=5, foreground="black")
entree9_L_ext.grid(row=2, column=1)
entree10_L_ext.grid(row=4, column=1)

bouton_extraction_L_ext = ttk.Button(
    frame3_1_L_ext, text=_("Extraction"), state="disable", command=creation_spectre_moyen_L_ext, width=10)
bouton_extraction_L_ext.grid(row=5, column=1)

flag_spectres_normalises_moyenne_L_ext = tk.BooleanVar(value=True)
coche_spectres_normalises_moyenne_L_ext = ttk.Checkbutton(frame3_1_L_ext, text=_("Moyenne des\nspectres \nnormalisés"),
                                                         variable=flag_spectres_normalises_moyenne_L_ext)
coche_spectres_normalises_moyenne_L_ext.grid(row=6, column=1)


###################################################################################################
# Interface graphique : gestion de évènements
###################################################################################################
canevas0_L_ext.bind("<Button-1>", zoom_clic_L_ext)
canevas0_L_ext.bind("<B1-Motion>", zoom_drag_and_drop_L_ext)
canevas0_L_ext.bind("<ButtonRelease-1>", zoom_clic_release_L_ext)
canevas0_L_ext.bind("<ButtonRelease-3>", affiche_lambda_L_ext)
canevas0_L_ext.bind("<Motion>", affiche_position_souris_L_ext)
canevas0_L_ext.bind("<B3-Motion>", affiche_position_souris_motion_L_ext)

entree_zoom_inf_L_ext.bind("<Return>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<Return>", change_zoom_sup_return_L_ext)
entree_zoom_inf_L_ext.bind("<KP_Enter>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<KP_Enter>", change_zoom_sup_return_L_ext)
entree_zoom_inf_L_ext.bind("<Tab>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<Tab>", change_zoom_sup_return_L_ext)
# entree_zoom_inf_L_ext.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_ext)
# entree_zoom_sup_L_ext.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_ext)

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
# entree1_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_1_return_L_ext)
# entree2_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_2_return_L_ext)
# entree3_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_3_return_L_ext)
# entree4_L_ext.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_4_return_L_ext)


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
# entree9_L_ext.bind("<Shift-ISO_Left_Tab>", change_entree9_L_ext)
# entree10_L_ext.bind("<Shift-ISO_Left_Tab>", change_entree10_L_ext)


###################################################################################################
###################################################################################################
# Interface graphique LIBStick_IHM_compare : onglet 3
###################################################################################################
###################################################################################################
def __________IHM_compare__________():
    """ Interface graphique LIBStick_IHM_compare : onglet 3"""
###################################################################################################
###################################################################################################


###################################################################################################
# Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###################################################################################################
frame1_L_comp = ttk.Frame(onglet3, borderwidth=2, relief=tk.RAISED)
frame2_L_comp = ttk.Frame(onglet3, borderwidth=2, relief=tk.RAISED)
frame3_L_comp = ttk.Frame(onglet3, borderwidth=2, relief=tk.RAISED)

frame1_L_comp.grid(row=10, column=10, sticky="nsew")
frame2_L_comp.grid(row=20, column=10, sticky="nsew")
frame3_L_comp.grid(row=30, column=10, sticky="nsew")
# frame1_L_comp.grid(row=10, column=10, padx=5, pady=5,sticky = tk.W)
# frame2_L_comp.grid(row=20, column=10, padx=5, pady=5,sticky = tk.W)
# frame3_L_comp.grid(row=30, column=10, padx=5, pady=5, sticky = tk.W)


###################################################################################################
# Interface graphique frame1_L_comp : création selection répertoire, affiche spectre et bouton executer
###################################################################################################
canevas0_L_comp = tk.Canvas(frame1_L_comp, width=largeur_canevas_spectres,
                            height=hauteur_canevas_spectres, bg="white")
canevas0_L_comp.grid(row=1, column=1, columnspan=6)

ligne_position_x_L_comp = canevas0_L_comp.create_line(0, 0, 0, hauteur_canevas_spectres, fill="white")
ligne_position_y_L_comp = canevas0_L_comp.create_line(0, 0, largeur_canevas_spectres, 0, fill="white")

lambda_texte_L_comp = ttk.Label(
    frame1_L_comp, text="Lambda = " + str(format(lambda_texte_spectre_L_comp, "4.1f") + " nm"))
lambda_texte_L_comp.grid(row=2, column=5)

text1_L_comp = ttk.Label(frame1_L_comp, text=_(
    "Numérateur borne inf (nm)"))
text2_L_comp = ttk.Label(frame1_L_comp, text=_(
    "Numérateur borne sup (nm)"))
text3_L_comp = ttk.Label(
    frame1_L_comp, text=_("Dénominateur borne inf (nm)"))
text4_L_comp = ttk.Label(
    frame1_L_comp, text=_("Dénominateur borne sup( nm)"))
text1_L_comp.grid(row=2, column=1, sticky=tk.E)
text2_L_comp.grid(row=2, column=3, sticky=tk.E)
text3_L_comp.grid(row=3, column=1, sticky=tk.E)
text4_L_comp.grid(row=3, column=3, sticky=tk.E)

variable_1_L_comp = tk.DoubleVar(value=tableau_bornes_L_comp[0, 0])
variable_2_L_comp = tk.DoubleVar(value=tableau_bornes_L_comp[0, 1])
variable_3_L_comp = tk.DoubleVar(value=tableau_bornes_L_comp[1, 0])
variable_4_L_comp = tk.DoubleVar(value=tableau_bornes_L_comp[1, 1])
entree1_L_comp = ttk.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_1_L_comp,
                             command=deplace_ligne0_1_L_comp, foreground="red", width=5)
entree2_L_comp = ttk.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_2_L_comp,
                             command=deplace_ligne0_2_L_comp, foreground="red", width=5)
entree3_L_comp = ttk.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5, textvariable=variable_3_L_comp,
                             command=deplace_ligne0_3_L_comp, foreground="blue", width=5)
entree4_L_comp = ttk.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5, textvariable=variable_4_L_comp,
                             command=deplace_ligne0_4_L_comp, foreground="blue", width=5)
entree1_L_comp.grid(row=2, column=2, sticky=tk.W)
entree2_L_comp.grid(row=2, column=4, sticky=tk.W)
entree3_L_comp.grid(row=3, column=2, sticky=tk.W)
entree4_L_comp.grid(row=3, column=4, sticky=tk.W)

flag_denominateur_L_comp = tk.IntVar(value=flag_denominateur_init_L_comp)
coche_denominateur_L_comp = ttk.Checkbutton(frame1_L_comp, text=_("Dénominateur ?"), variable=flag_denominateur_L_comp,
                                                command=change_flag_denominateur_L_comp)
coche_denominateur_L_comp.grid(row=3, column=5)

bouton_reset_L_comp = ttk.Button(frame1_L_comp, text=_("Reset"),
                                     command=reset_tableau_L_comp,
                                     width=10)
bouton_reset_L_comp.grid(row=2, column=6, rowspan=2)

frame1_1_L_comp = ttk.Frame(frame1_L_comp)
frame1_1_L_comp.grid(row=1, column=7, rowspan=3, sticky=tk.N)

text_zoom_L_comp = ttk.Label(frame1_1_L_comp, text="Zoom : ", width=8)
text_zoom_L_comp.grid(row=1, column=1)
variable_zoom_inf_L_comp = tk.DoubleVar(value=198)
variable_zoom_sup_L_comp = tk.DoubleVar(value=1013)
entree_zoom_inf_L_comp = ttk.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_inf_L_comp,
                                     command=change_zoom_inf_L_comp, width=8, foreground="black")
entree_zoom_sup_L_comp = ttk.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_sup_L_comp,
                                     command=change_zoom_sup_L_comp, width=8, foreground="black")
entree_zoom_inf_L_comp.grid(row=2, column=1)
entree_zoom_sup_L_comp.grid(row=3, column=1)

type_fichier_L_comp = tk.StringVar(value=".mean")
# bouton_rep_L_comp=ttk.Button(frame1_1_L_comp, text="Repertoire\nde travail" ,
#                                  command=choix_rep_L_comp, width=8)
bouton_rep_L_comp = ttk.Button(frame1_1_L_comp, text=_("Fichier"),
                                   command=choix_fichier_L_comp, width=10)
bouton_execute_L_comp = ttk.Button(frame1_1_L_comp, text=_("Exécute"),
                                       command=execute_scripts_L_comp,
                                       state="disable", width=10)
bouton_rep_L_comp.grid(row=4, column=1)
bouton_execute_L_comp.grid(row=5, column=1)

flag_2D_L_comp = tk.IntVar(value=flag_2D_init_L_comp)
coche_2D_L_comp = ttk.Checkbutton(frame1_1_L_comp, text=_("Sortie 2D"),
                                      variable=flag_2D_L_comp)
# coche_2D_L_comp=ttk.Checkbutton(
#     frame1_1_L_comp, text="Sortie 2D", variable=flag_2D_L_comp, command=change_flag_2D_L_comp)
coche_2D_L_comp.grid(row=6, column=1)

flag_3D_L_comp = tk.IntVar(value=flag_3D_init_L_comp)
coche_3D_L_comp = ttk.Checkbutton(frame1_1_L_comp, text=_("Sortie 3D"),
                                      variable=flag_3D_L_comp)
# coche_3D_L_comp=ttk.Checkbutton(
#     frame1_1_L_comp, text="Sortie 3D", variable=flag_3D_L_comp, command=change_flag_3D_L_comp)
coche_3D_L_comp.grid(row=7, column=1)

# image_classification=tk.PhotoImage(file=rep_LIBStick+"/LIBStick_datas/icons/Classification.png")
bouton_classification_L_comp = tk.Button(frame1_1_L_comp,image=image_classification,
                                         command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_comp.grid(row=8, column=1, sticky=tk.S)


###################################################################################################
# Interface graphique frame2_L_comp : affichage des spectres classés
###################################################################################################
canevas1_L_comp = tk.Canvas(frame2_L_comp, width=largeur_canevas_spectres,
                            height=hauteur_canevas_spectres, bg="white")
canevas1_L_comp.grid(row=1, column=1, columnspan=4)

# text5_L_comp = ttk.Label(frame2_L_comp, text="Position x (nm) : ")
# text6_L_comp = ttk.Label(frame2_L_comp, text="Position y (n° de spectre) : ")
# text5_L_comp.grid(row=2, column=1, sticky=tk.E)
# text6_L_comp.grid(row=2, column=3, sticky=tk.E)

# variable_5_L_comp=tk.DoubleVar(value=0)
# variable_6_L_comp=tk.IntVar(value=0)
# entree5_L_comp=ttk.Spinbox(frame2_L_comp, from_=198, to=1013, textvariable=variable_5_L_comp,
#                            command=vars_5_6_to_coord1_L_comp, increment=0.5, width=8)
# entree6_L_comp=ttk.Spinbox(frame2_L_comp, from_=1, to=100, textvariable=variable_6_L_comp,
#                            command=vars_5_6_to_coord1_L_comp, width=8)
# entree5_L_comp.grid(row=2, column=2, sticky=tk.W)
# entree6_L_comp.grid(row=2, column=4, sticky=tk.W)

frame2_1_L_comp = ttk.Frame(frame2_L_comp)
frame2_1_L_comp.grid(row=1, column=5, rowspan=3, sticky=tk.N)

# text7_L_comp=ttk.Label(frame2_1_L_comp, text="Type de\nfichiers à\ncomparer :")
# text7_L_comp.grid(row=1, column=1)

flag_traitement_L_comp = tk.IntVar(value=flag_traitement_init_L_comp)
coche_traitement_L_comp = ttk.Checkbutton(
    frame2_1_L_comp, text=_("Normalisation\ndes spectres"), variable=flag_traitement_L_comp)
coche_traitement_L_comp.grid(row=1, column=1)

# type_traitement_L_comp=tk.StringVar(value="Echantillons différents")
# type_traitement_combobox_L_comp=ttk.Combobox(frame2_1_L_comp, textvariable=type_traitement_L_comp,
#                                              width=8, values=["Echantillons différents", "Même échantillon"])
# type_traitement_combobox_L_comp.grid(row=2, column=1)

# text8_L_comp=ttk.Label(frame2_1_L_comp, text="\nEchantillons différents :\nspectres moyens\nd'échantillons\ndifférents\n\nMême échantillon :\nspectres du même\néchantillon")
# text8_L_comp.grid(row=3, column=1)

flag_stat_L_comp = tk.IntVar(value=flag_stat_init_L_comp)
coche_stat_L_comp = ttk.Checkbutton(
    frame2_1_L_comp, text=_("Statistiques"), variable=flag_stat_L_comp)
coche_stat_L_comp.grid(row=2, column=1)

ligne1_vert_L_comp = canevas1_L_comp.create_line(x1_L_comp, 0, x1_L_comp, hauteur_canevas_spectres, fill="white")
ligne1_hori_L_comp = canevas1_L_comp.create_line(0, y1_L_comp, largeur_canevas_spectres/2, y1_L_comp, fill="white")

text5_L_comp = ttk.Label(frame2_1_L_comp, text=_("\nPosition x (nm) : "))
text6_L_comp = ttk.Label(
    frame2_1_L_comp, text=_("Position y \n(n° de spectre) : "))
text5_L_comp.grid(row=4, column=1)
text6_L_comp.grid(row=6, column=1)

variable_5_L_comp = tk.DoubleVar(value=0)
variable_6_L_comp = tk.IntVar(value=0)
entree5_L_comp = ttk.Spinbox(frame2_1_L_comp, from_=198, to=1013,textvariable=variable_5_L_comp,
                             command=vars_5_6_to_coord1_L_comp, increment=0.5, width=5, foreground="black")
entree6_L_comp = ttk.Spinbox(frame2_1_L_comp, from_=1, to=100, textvariable=variable_6_L_comp,
                             command=vars_5_6_to_coord1_L_comp, width=5, foreground="black")
entree5_L_comp.grid(row=5, column=1)
entree6_L_comp.grid(row=7, column=1)

affiche_lignes_spectre_L_comp()


###################################################################################################
# Interface graphique frame3_L_comp : affichage des résultats sous forme de TreeView
###################################################################################################
tree_resultats_L_comp = ttk.Treeview(
    frame3_L_comp, columns=(1, 2, 3), height=10, show="headings")
tree_resultats_L_comp.column(1, width=hauteur_canevas_spectres)
tree_resultats_L_comp.column(2, width=600)
tree_resultats_L_comp.column(3, width=hauteur_canevas_spectres)
tree_resultats_L_comp.heading(1, text=_("n°"))
tree_resultats_L_comp.heading(2, text=_("Nom du spectre"))
tree_resultats_L_comp.heading(3, text=_("Rapport zone1/zone2"))
tree_resultats_L_comp.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
scroll_tree_resultat_L_comp = ttk.Scrollbar(
    frame3_L_comp, orient=tk.VERTICAL, command=tree_resultats_L_comp.yview)
scroll_tree_resultat_L_comp.grid(row=1, column=2, sticky=tk.N+tk.S)
tree_resultats_L_comp.configure(yscrollcommand=scroll_tree_resultat_L_comp.set)

texte_statistiques_L_comp = tk.Message(frame3_L_comp)
# texte_statistiques_L_comp.grid(row=1, column=3, sticky=tk.N)


###################################################################################################
# Interface graphique : gestion de évènements
###################################################################################################
canevas0_L_comp.bind("<Button-1>", zoom_clic_L_comp)
canevas0_L_comp.bind("<B1-Motion>", zoom_drag_and_drop_L_comp)
canevas0_L_comp.bind("<ButtonRelease-1>", zoom_clic_release_L_comp)
canevas0_L_comp.bind("<ButtonRelease-3>", affiche_lambda_L_comp)
canevas0_L_comp.bind("<Motion>", affiche_position_souris_L_comp)
canevas0_L_comp.bind("<B3-Motion>", affiche_position_souris_motion_L_comp)

entree_zoom_inf_L_comp.bind("<Return>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<Return>", change_zoom_sup_return_L_comp)
entree_zoom_inf_L_comp.bind("<KP_Enter>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<KP_Enter>", change_zoom_sup_return_L_comp)
entree_zoom_inf_L_comp.bind("<Tab>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<Tab>", change_zoom_sup_return_L_comp)
# entree_zoom_inf_L_comp.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_comp)
# entree_zoom_sup_L_comp.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_comp)

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
# entree1_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_1_return_L_comp)
# entree2_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_2_return_L_comp)
# entree3_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_3_return_L_comp)
# entree4_L_comp.bind("<Shift-ISO_Left_Tab>", deplace_ligne0_4_return_L_comp)

entree5_L_comp.bind("<Return>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<Return>", vars_5_6_to_coord1_return_L_comp)
entree5_L_comp.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_comp)
entree5_L_comp.bind("<Tab>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<Tab>", vars_5_6_to_coord1_return_L_comp)

tree_resultats_L_comp.bind("<ButtonRelease-1>", selectionne_spectre_L_comp)
tree_resultats_L_comp.bind("<Up>", selectionne_spectre_up_L_comp)
tree_resultats_L_comp.bind("<Down>", selectionne_spectre_down_L_comp)


###################################################################################################
###################################################################################################
# Interface graphique LIBStick_IHM_ACP : onglet 4
###################################################################################################
###################################################################################################
def __________IHM_ACP__________():
    """ Interface graphique LIBStick_IHM_ACP : onglet 4"""
###################################################################################################
###################################################################################################


###################################################################################################
# Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###################################################################################################
frame1_L_ACP = ttk.Frame(onglet4, borderwidth=2, relief=tk.RAISED)
frame2_L_ACP = ttk.Frame(onglet4, borderwidth=2, relief=tk.RAISED)
frame3_L_ACP = ttk.Frame(onglet4, borderwidth=2, relief=tk.RAISED)

frame1_L_ACP.grid(row=10, column=10, sticky="nsew")
frame2_L_ACP.grid(row=20, column=10, sticky="nsew")
frame3_L_ACP.grid(row=30, column=10, sticky="nsew")
# frame1_L_ACP.grid(row=10, column=10, padx=5, pady=5,sticky = tk.W)
# frame2_L_ACP.grid(row=20, column=10, padx=5, pady=5,sticky = tk.W)
# frame3_L_ACP.grid(row=30, column=10, padx=5, pady=5, sticky = tk.W)


###################################################################################################
# Interface graphique frame1_L_ACP : création selection répertoire, affiche spectre et bouton executer
###################################################################################################
canevas0_L_ACP = tk.Canvas(frame1_L_ACP, width=largeur_canevas_spectres,
                           height=hauteur_canevas_spectres, bg="white")
canevas0_L_ACP.grid(row=1, column=1, columnspan=6)

ligne_position_x_L_ACP = canevas0_L_ACP.create_line(0, 0, 0, hauteur_canevas_spectres, fill="white")
ligne_position_y_L_ACP = canevas0_L_ACP.create_line(0, 0, largeur_canevas_spectres, 0, fill="white")

lambda_texte_L_ACP = ttk.Label(
    frame1_L_ACP, text="Lambda = " + str(format(lambda_texte_spectre_0_L_ACP, "4.1f") + " nm"))
lambda_texte_L_ACP.grid(row=2, column=5)

text1_L_ACP = ttk.Label(frame1_L_ACP, text=_("Borne inf :"))
text2_L_ACP = ttk.Label(frame1_L_ACP, text=_("Borne sup :"))
text1_L_ACP.grid(row=2, column=1, sticky=tk.E)
text2_L_ACP.grid(row=2, column=3, sticky=tk.E)

variable_1_L_ACP = tk.DoubleVar(value=tableau_bornes_L_ACP[0])
variable_2_L_ACP = tk.DoubleVar(value=tableau_bornes_L_ACP[1])
entree1_L_ACP = ttk.Spinbox(frame1_L_ACP, from_=198, to=1013, increment=0.5, textvariable=variable_1_L_ACP,
                            command=deplace_ligne0_1_L_ACP, width=5, foreground="black")
entree2_L_ACP = ttk.Spinbox(frame1_L_ACP, from_=198, to=1013, increment=0.5, textvariable=variable_2_L_ACP,
                            command=deplace_ligne0_2_L_ACP, width=5, foreground="black")
entree1_L_ACP.grid(row=2, column=2, sticky=tk.W)
entree2_L_ACP.grid(row=2, column=4, sticky=tk.W)

# bouton_reset_L_ACP=ttk.Button(frame1_L_ACP, text="Reset", command=reset_tableau_L_ACP, width=8)
# bouton_reset_L_ACP.grid(row=2, column=6, rowspan=2)

frame1_1_L_ACP = ttk.Frame(frame1_L_ACP)
frame1_1_L_ACP.grid(row=1, column=7, rowspan=3, sticky=tk.N)

text_zoom_L_ACP = ttk.Label(frame1_1_L_ACP, text="Zoom : ", width=8)
text_zoom_L_ACP.grid(row=1, column=1, sticky=tk.N)
variable_zoom_inf_L_ACP = tk.DoubleVar(value=198)
variable_zoom_sup_L_ACP = tk.DoubleVar(value=1013)
entree_zoom_inf_L_ACP = ttk.Spinbox(frame1_1_L_ACP, from_=198, to=1013, increment=1, textvariable=variable_zoom_inf_L_ACP,
                                    command=change_zoom_inf_L_ACP, width=8, foreground="black")
entree_zoom_sup_L_ACP = ttk.Spinbox(frame1_1_L_ACP, from_=198, to=1013, increment=1, textvariable=variable_zoom_sup_L_ACP,
                                    command=change_zoom_sup_L_ACP, width=8, foreground="black")
entree_zoom_inf_L_ACP.grid(row=2, column=1, sticky=tk.N)
entree_zoom_sup_L_ACP.grid(row=3, column=1, sticky=tk.N)

type_fichier_L_ACP = tk.StringVar(value=".mean")
bouton_rep_L_ACP = ttk.Button(frame1_1_L_ACP, text=_("Fichier"),
                                  command=choix_fichier_L_ACP, width=10)
bouton_rep_L_ACP.grid(row=4, column=1, sticky=tk.N)

bouton_classification_L_ACP = tk.Button(frame1_1_L_ACP, image=image_classification,
                                        command=ouvre_fenetre_classification_L_ele)
bouton_classification_L_ACP.grid(row=8, column=1, sticky=tk.S)


###################################################################################################
# Interface graphique frame2_L_ACP : affichage des résultats sous forme de TreeView
###################################################################################################
tableau_label_ouvert_flag_L_ACP = False
label_L_ACP = tk.IntVar(value=0)

tree_L_ACP = ttk.Treeview(frame2_L_ACP, columns=(1, 2, 3, 4), height=10, show="headings")
tree_L_ACP.tag_configure("deselect", foreground="red")
if style_interface_LIBStick == "black" :
    tree_L_ACP.tag_configure("select", foreground="white")
else :
    tree_L_ACP.tag_configure("select", foreground="black")
tree_L_ACP.column(1, width=50)
tree_L_ACP.column(2, width=600)
tree_L_ACP.column(3, width=hauteur_canevas_spectres)
tree_L_ACP.column(4, width=80)
tree_L_ACP.heading(1, text=_("n°"))
tree_L_ACP.heading(2, text=_("Nom du spectre"))
tree_L_ACP.heading(3, text=_("Utlisé pour l'ACP :"))
tree_L_ACP.heading(4, text=_("Label :"))
tree_L_ACP.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
scroll_tree_L_ACP = ttk.Scrollbar(
    frame2_L_ACP, orient=tk.VERTICAL, command=tree_L_ACP.yview)
scroll_tree_L_ACP.grid(row=1, column=2, sticky=tk.N+tk.S)
tree_L_ACP.configure(yscrollcommand=scroll_tree_L_ACP.set)

frame2_1_L_ACP = ttk.Frame(frame2_L_ACP)
frame2_1_L_ACP.grid(row=1, column=7, rowspan=3, sticky=tk.N)

flag_normalise_L_ACP = tk.BooleanVar(value=True)
coche_normalise_L_ACP = ttk.Checkbutton(frame2_1_L_ACP, text=_("Spectres normalisés"), variable=flag_normalise_L_ACP,
                                            command=change_flag_traitement_L_ACP)
coche_normalise_L_ACP.grid(row=1, column=1, sticky=tk.W, columnspan=2)

flag_centre_reduit_L_ACP = tk.BooleanVar(value=False)
coche_centre_reduit_L_ACP = ttk.Checkbutton(frame2_1_L_ACP, text=_("Centré reduit"), variable=flag_centre_reduit_L_ACP,
                                            command=change_flag_traitement_L_ACP)
coche_centre_reduit_L_ACP.grid(row=2, column=1, sticky=tk.W, columnspan=2)

bouton_execute_L_ACP = ttk.Button(frame2_1_L_ACP, text=_("ACP"),
                                  command=execute_ACP_L_ACP, state="disable", width=6)
bouton_execute_L_ACP.grid(row=3, column=1, sticky=tk.W)

bouton_applique_ind_sup_L_ACP = ttk.Button(frame2_1_L_ACP, text=_("+ ind. supp."),
                                   command=applique_ACP_ind_sup_L_ACP, state="disable", width=6)
bouton_applique_ind_sup_L_ACP.grid(row=3, column=2, sticky=tk.W)

bouton_ouvre_L_ACP = ttk.Button(frame2_1_L_ACP, text=_("Ouvre"),
                                command=ouvre_ACP_L_ACP, state="disable", width=6)
bouton_ouvre_L_ACP.grid(row=4, column=1, sticky=tk.W)

bouton_sauve_L_ACP = ttk.Button(frame2_1_L_ACP, text=_("Sauve"),
                                command=enregistre_ACP_L_ACP, state="disable", width=6)
bouton_sauve_L_ACP.grid(row=4, column=2, sticky=tk.W)

text_dim_L_ACP = ttk.Label(frame2_1_L_ACP, text=_("Dimensions : "))
text_dim_L_ACP.grid(row=5, column=1, sticky=tk.W, columnspan=2)
dim_1_L_ACP = tk.IntVar(value=1)
entree_dim1_L_ACP = ttk.Spinbox(frame2_1_L_ACP, from_=1, to=10, increment=1, textvariable=dim_1_L_ACP,
                                width=5, foreground="red", command=affiche_spectres_var_ACP_L_ACP)
dim_2_L_ACP = tk.IntVar(value=2)
entree_dim2_L_ACP = ttk.Spinbox(frame2_1_L_ACP, from_=1, to=10, increment=1, textvariable=dim_2_L_ACP,
                                width=5, foreground="blue", command=affiche_spectres_var_ACP_L_ACP)
dim_3_L_ACP = tk.IntVar(value=3)
entree_dim3_L_ACP = ttk.Spinbox(frame2_1_L_ACP, from_=1, to=10, increment=1, textvariable=dim_3_L_ACP, state="disable",
                                width=5, foreground="green", command=affiche_spectres_var_ACP_L_ACP)
entree_dim1_L_ACP.grid(row=6, column=1, sticky=tk.W)
entree_dim2_L_ACP.grid(row=6, column=2, sticky=tk.W)
entree_dim3_L_ACP.grid(row=7, column=1, sticky=tk.W)

flag_3D_L_ACP = tk.BooleanVar(value=False)
coche_3D_L_ACP = ttk.Checkbutton(frame2_1_L_ACP, text="3D", variable=flag_3D_L_ACP, command=change_flag_3D_L_ACP)
coche_3D_L_ACP.grid(row=7, column=2, sticky=tk.W)

flag_echelle_L_ACP = tk.BooleanVar(value=True)
coche_echelle_L_ACP = ttk.Checkbutton(frame2_1_L_ACP, text=_("Même echelle x et y"), variable=flag_echelle_L_ACP)
coche_echelle_L_ACP.grid(row=8, column=1, sticky=tk.W, columnspan=2)

flag_eboulis_L_ACP = tk.BooleanVar(value=True)
coche_eboulis_L_ACP = ttk.Checkbutton(frame2_1_L_ACP, text=_("Diag. éboulis"), variable=flag_eboulis_L_ACP)
coche_eboulis_L_ACP.grid(row=9, column=1, sticky=tk.W, columnspan=2)

# flag_calcul_L_ACP=tk.BooleanVar(value=False)
# coche_calcul_L_ACP=ttk.Checkbutton(frame2_1_L_ACP, text="fanalysis ?", variable=flag_calcul_L_ACP)
# coche_calcul_L_ACP.grid(row=8, column=1)


###################################################################################################
# Interface graphique frame3_L_ACP : affichage des "spectres" des variables de l'ACP
###################################################################################################
canevas1_L_ACP = tk.Canvas(frame3_L_ACP, width=largeur_canevas_spectres,
                           height=hauteur_canevas_spectres, bg="white")
canevas1_L_ACP.grid(row=1, column=1, columnspan=6)

frame3_1_L_ACP = ttk.Frame(frame3_L_ACP)
frame3_1_L_ACP.grid(row=1, column=7, rowspan=3, sticky=tk.N)

bouton_enregistre_L_ACP = ttk.Button(frame3_1_L_ACP, text=_("Enregistrer \nfacteurs \nde l'ACP"),
                                         command=enregistre_facteurs_ACP_L_ACP,
                                         state="disable", width=10)
bouton_enregistre_L_ACP.grid(row=1, column=1)

ligne_position_1_L_ACP = canevas0_L_ACP.create_line(0, 0, 0, hauteur_canevas_spectres, fill="white")


###################################################################################################
# Interface graphique : gestion de évènements
###################################################################################################
canevas0_L_ACP.bind("<Button-1>", zoom_clic_L_ACP)
canevas0_L_ACP.bind("<B1-Motion>", zoom_drag_and_drop_L_ACP)
canevas0_L_ACP.bind("<ButtonRelease-1>", zoom_clic_release_L_ACP)
canevas0_L_ACP.bind("<ButtonRelease-3>", affiche_lambda_L_ACP)
canevas0_L_ACP.bind("<Motion>", affiche_position_souris_L_ACP)
canevas0_L_ACP.bind("<B3-Motion>", affiche_position_souris_motion_L_ACP)

entree_zoom_inf_L_ACP.bind("<Return>", change_zoom_inf_return_L_ACP)
entree_zoom_sup_L_ACP.bind("<Return>", change_zoom_sup_return_L_ACP)
entree_zoom_inf_L_ACP.bind("<KP_Enter>", change_zoom_inf_return_L_ACP)
entree_zoom_sup_L_ACP.bind("<KP_Enter>", change_zoom_sup_return_L_ACP)
entree_zoom_inf_L_ACP.bind("<Tab>", change_zoom_inf_return_L_ACP)
entree_zoom_sup_L_ACP.bind("<Tab>", change_zoom_sup_return_L_ACP)
# entree_zoom_inf_L_ACP.bind("<Shift-ISO_Left_Tab>", change_zoom_inf_return_L_ACP)
# entree_zoom_sup_L_ACP.bind("<Shift-ISO_Left_Tab>", change_zoom_sup_return_L_ACP)

# canevas1_L_ACP.bind("<ButtonRelease-1>", coordonnees1_L_ACP)

entree1_L_ACP.bind("<Return>", deplace_ligne0_1_return_L_ACP)
entree2_L_ACP.bind("<Return>", deplace_ligne0_2_return_L_ACP)
entree1_L_ACP.bind("<KP_Enter>", deplace_ligne0_1_return_L_ACP)
entree2_L_ACP.bind("<KP_Enter>", deplace_ligne0_2_return_L_ACP)
entree1_L_ACP.bind("<Tab>", deplace_ligne0_1_return_L_ACP)
entree2_L_ACP.bind("<Tab>", deplace_ligne0_2_return_L_ACP)

tree_L_ACP.bind("<ButtonRelease-1>", selectionne_spectre_L_ACP)
# tree_L_ACP.bind("<Button-1>", selectionne_spectre_L_ACP)
tree_L_ACP.bind("<Up>", selectionne_spectre_up_L_ACP)
tree_L_ACP.bind("<Down>", selectionne_spectre_down_L_ACP)
tree_L_ACP.bind("<Double-Button-1>", change_tree_selection_L_ACP)
tree_L_ACP.bind("<space>", change_tree_selection_L_ACP)
tree_L_ACP.bind("l", ouvre_fenetre_change_tree_label_L_ACP)

canevas1_L_ACP.bind("<Button-1>", zoom_clic_L_ACP)
canevas1_L_ACP.bind("<B1-Motion>", zoom_drag_and_drop_L_ACP)
canevas1_L_ACP.bind("<ButtonRelease-1>", zoom_clic_release_canevas1_L_ACP)
canevas1_L_ACP.bind("<ButtonRelease-3>", affiche_lambda_L_ACP)
canevas1_L_ACP.bind("<Motion>", affiche_position_souris_L_ACP)
canevas1_L_ACP.bind("<B3-Motion>", affiche_position_souris_motion_L_ACP)


###################################################################################################
###################################################################################################
# Interface graphique LIBStick : classification périodique
###################################################################################################
###################################################################################################
def __________IHM_tableau_periodique__________():
    """ Interface graphique LIBStick : classification périodique"""
###################################################################################################
###################################################################################################


flag_neutres_ions_L_ele = tk.IntVar(value=1)

flag_sup10_L_ele = tk.IntVar(value=1)
flag_sup1_L_ele = tk.IntVar(value=1)
flag_inf1_L_ele = tk.IntVar(value=0)


###################################################################################################
###################################################################################################
# LIBStick : interface principale
###################################################################################################
###################################################################################################
def __________IHM_divers__________():
    """ LIBStick : interface principale"""
###################################################################################################
###################################################################################################


###################################################################################################
#  Interface graphique : gestion du redimentionnement de la fenêtre principale
###################################################################################################
canevas_scroll.create_window(0, 0, anchor='nw', window=frame_scroll)
frame_scroll.update_idletasks()
canevas_scroll.config(scrollregion=canevas_scroll.bbox("all"))

fenetre_principale.bind("<Configure>", change_taille_fenetre)
# fenetre_principale.bind("<Expose>", change_taille_fenetre)
# fenetre_principale.bind("<Visibility>", applique_change_taille_fenetre_event)
# fenetre_principale.bind("<Property>", applique_change_taille_fenetre_event)


fenetre_principale.mainloop()
