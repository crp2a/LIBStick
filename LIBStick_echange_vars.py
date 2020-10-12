#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 16:21:55 2020

@author: yannick
"""
import numpy, pandas

#nombre_fichiers=50
#liste_fichiers=[]
#flag_2D=1
#flag_3D=0
#flag_zone2=1
#bornes_moyenne_spectres=[]
#nom_echantillon=str()
#
#flag_denominateur=1
#limites_spectre=[]
#DataFrame_resultats=pandas.DataFrame()

###############################################################################
# 1- variables pour LIBStick_extraction (L_ext_)
###############################################################################
L_ext_nombre_fichiers=50
L_ext_liste_fichiers=[]
L_ext_flag_2D=1
L_ext_flag_3D=0
L_ext_flag_zone2=1
L_ext_bornes_moyenne_spectres=[]
L_ext_nom_echantillon=str()


###############################################################################
# 2- variables pour LIBStick_compare (L_comp_)
###############################################################################
L_comp_nombre_fichiers=50
L_comp_liste_fichiers=[]
L_comp_flag_2D=1
L_comp_flag_3D=0
L_comp_bornes_moyenne_spectres=[]
L_comp_nom_echantillon=str()
L_comp_flag_denominateur=1
L_comp_limites_spectre=[]
L_comp_DataFrame_resultats=pandas.DataFrame()


###############################################################################
# 3- variables pour LIBStick_tableau_periodique
###############################################################################
tableau_periodique_ouvert= False
DataFrame_element=pandas.DataFrame()
L_ele_symbole=""

