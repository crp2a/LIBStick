#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:05:40 2020

@author: yannick
"""

import tkinter, numpy, pandas
import tkinter.ttk, tkinter.filedialog
import os, math
import PIL.Image, PIL.ImageTk
import LIBStick_echange_vars
import LIBStick_comp_spectres

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
tableau_bornes_init_L_comp=numpy.array([ [529.0, 542.0] , [534.7, 535.8] ])
tableau_bornes_L_comp=numpy.array([ [529.0, 542.0] , [534.7, 535.8] ])
rep_travail_L_comp="./"
#rep_travail_L_comp="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1"
x1_L_comp=250.0
y1_L_comp=100.0
#x2_L_comp=250.0
#y2_L_comp=100.0

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_comp() :
    global tableau_bornes_L_comp
    tableau_bornes_L_comp[0,0]=variable_1_L_comp.get()
    tableau_bornes_L_comp[0,1]=variable_2_L_comp.get()
    #entree5_L_comp.configure(from_=tableau_bornes_L_comp[0,0], to=tableau_bornes_L_comp[0,1])  
    if flag_denominateur_L_comp.get() :
        tableau_bornes_L_comp[1,0]=variable_3_L_comp.get()
        tableau_bornes_L_comp[1,1]=variable_4_L_comp.get()
    return tableau_bornes_L_comp
    
def reset_tableau_L_comp() :
    global tableau_bornes_L_comp
    tableau_bornes_L_comp=tableau_bornes_init_L_comp.copy()
    variable_1_L_comp.set(tableau_bornes_L_comp[0,0])
    variable_2_L_comp.set(tableau_bornes_L_comp[0,1])
    variable_3_L_comp.set(tableau_bornes_L_comp[1,0])
    variable_4_L_comp.set(tableau_bornes_L_comp[1,1])
    deplace_lignes_L_comp()

def choix_rep_L_comp():
    global rep_travail_L_comp
    global nbr_fichier
    rep_travail_L_comp = tkinter.filedialog.askdirectory(initialdir="./",title='Choisissez un repertoire')    
    LIBStick_echange_vars.L_comp_liste_fichiers=LIBStick_comp_spectres.creation_liste_fichiers(rep_travail_L_comp)
    LIBStick_echange_vars.L_comp_nombre_fichiers=len(LIBStick_echange_vars.L_comp_liste_fichiers)
    nbr_fichier=LIBStick_echange_vars.L_comp_nombre_fichiers
    lit_affiche_spectre_L_comp()
    bouton_execute_L_comp.configure(state="normal")
    entree6_L_comp.configure(to=LIBStick_echange_vars.L_comp_nombre_fichiers)
         
def lit_affiche_spectre_L_comp():
    global spectre_entier_L_comp 
    os.chdir(rep_travail_L_comp)
    #if LIBStick_echange_vars.L_comp_nombre_fichiers > 0 :
    tableau_abscisses=lit_fichier_abscisses_L_comp()
    spectre_entier_L_comp=LIBStick_comp_spectres.lit_spectre(LIBStick_echange_vars.L_comp_liste_fichiers[0], tableau_abscisses)
    spectre_entier_L_comp=numpy.transpose(spectre_entier_L_comp)
    #print(spectre_entier_L_comp.shape)
    affiche_spectre_L_comp()

def lit_fichier_abscisses_L_comp():
    global tableau_abscisses
    global limites_spectre_L_comp
    tableau_abscisses=LIBStick_comp_spectres.lit_tableau_abscisses()
    limites_spectre_L_comp[0]=limites_affichage_spectre_L_comp[0]=tableau_abscisses[0]
    limites_spectre_L_comp[1]=limites_affichage_spectre_L_comp[1]=tableau_abscisses[-1]
    LIBStick_echange_vars.L_comp_limites_affichage_spectre=limites_affichage_spectre_L_comp
    variable_zoom_inf_L_comp.set(limites_affichage_spectre_L_comp[0])
    variable_zoom_sup_L_comp.set(limites_affichage_spectre_L_comp[1])
    entree_zoom_inf_L_comp.configure(from_=limites_spectre_L_comp[0], to=limites_spectre_L_comp[1])
    entree_zoom_sup_L_comp.configure(from_=limites_spectre_L_comp[0], to=limites_spectre_L_comp[1])
    entree1_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    entree2_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    entree3_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    entree4_L_comp.configure(from_=limites_affichage_spectre_L_comp[0], to=limites_affichage_spectre_L_comp[1])
    return tableau_abscisses
   
def execute_scripts_L_comp():
    tableau_bornes_L_comp=creation_tab_bornes_L_comp()
    LIBStick_comp_spectres.main(rep_travail_L_comp, tableau_bornes_L_comp)
    global photo
    fichier=rep_travail_L_comp+"/figure.png"
    image_zoom=PIL.Image.open(fichier)    
    image_zoom=image_zoom.resize((1000, 200))
    photo=PIL.ImageTk.PhotoImage(image_zoom)
    canevas1_L_comp.create_image(500 ,100 ,image=photo)
    affiche_tableau_resultats_L_comp()

###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1_L_comp)
###############################################################################
def change_flag_denominateur_L_comp():
    LIBStick_echange_vars.L_comp_flag_denominateur=flag_denominateur_L_comp.get()
    if flag_denominateur_L_comp.get() == 0 :
        efface_lignes_3_4_L_comp()
        entree3_L_comp.configure(state="disable")
        entree4_L_comp.configure(state="disable")
    if flag_denominateur_L_comp.get() == 1 :
        affiche_lignes_3_4_L_comp()
        entree3_L_comp.configure(state="normal")
        entree4_L_comp.configure(state="normal")
        
def change_flag_2D_L_comp():
    LIBStick_echange_vars.L_comp_flag_2D=flag_2D_L_comp.get()

def change_flag_3D_L_comp():
    LIBStick_echange_vars.L_comp_flag_3D=flag_3D_L_comp.get()

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
    global ligne0_1
    global ligne0_2
    global ligne0_3
    global ligne0_4
    x_ligne0_1=((variable_1_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    x_ligne0_2=((variable_2_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_1=canevas0_L_comp.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red")
    ligne0_2=canevas0_L_comp.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red")
    if flag_denominateur_L_comp.get() :
        x_ligne0_3=((variable_3_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        x_ligne0_4=((variable_4_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        ligne0_3=canevas0_L_comp.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue")
        ligne0_4=canevas0_L_comp.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue")
        
def deplace_lignes_L_comp():
    deplace_ligne0_1_L_comp()
    deplace_ligne0_2_L_comp()
    if flag_denominateur_L_comp.get() :
        deplace_ligne0_3_L_comp()
        deplace_ligne0_4_L_comp()

def deplace_ligne0_1_L_comp():
    global ligne0_1
    canevas0_L_comp.delete(ligne0_1)
    x_ligne0_1=((variable_1_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_1=canevas0_L_comp.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red")
    if variable_1_L_comp.get() >= variable_2_L_comp.get():
        variable_2_L_comp.set(variable_1_L_comp.get())
        deplace_ligne0_2_L_comp()
        
def deplace_ligne0_2_L_comp():
    global ligne0_2
    canevas0_L_comp.delete(ligne0_2)
    x_ligne0_2=((variable_2_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_2=canevas0_L_comp.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red")
    if variable_2_L_comp.get() <= variable_1_L_comp.get() :
        variable_1_L_comp.set(variable_2_L_comp.get())
        deplace_ligne0_1_L_comp()

def deplace_ligne0_3_L_comp():
    global ligne0_3
    canevas0_L_comp.delete(ligne0_3)
    if flag_denominateur_L_comp.get() :
        x_ligne0_3=((variable_3_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        ligne0_3=canevas0_L_comp.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue")
        if variable_3_L_comp.get() >= variable_4_L_comp.get():
            variable_4_L_comp.set(variable_3_L_comp.get())
            deplace_ligne0_4_L_comp()
        
def deplace_ligne0_4_L_comp():
    global ligne0_4
    canevas0_L_comp.delete(ligne0_4)
    if flag_denominateur_L_comp.get() :
        x_ligne0_4=((variable_4_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
        ligne0_4=canevas0_L_comp.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue")
        if variable_4_L_comp.get() <= variable_3_L_comp.get() :
            variable_3_L_comp.set(variable_4_L_comp.get())
            deplace_ligne0_3_L_comp()

def efface_lignes_3_4_L_comp():
    global ligne0_3
    global ligne0_4
    canevas0_L_comp.delete(ligne0_3)
    canevas0_L_comp.delete(ligne0_4)

def affiche_lignes_3_4_L_comp():
    global ligne0_3
    global ligne0_4
    canevas0_L_comp.delete(ligne0_3)
    canevas0_L_comp.delete(ligne0_4)
    x_ligne0_3=((variable_3_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    x_ligne0_4=((variable_4_L_comp.get()-limites_affichage_spectre_L_comp[0])*1000/delta_limites_L_comp)
    ligne0_3=canevas0_L_comp.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue")
    ligne0_4=canevas0_L_comp.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue")
        
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
    variable_6_L_comp.set(math.ceil(y * nbr_fichier / 200))

def vars_5_6_to_coord1_L_comp():
    global x1_L_comp,y1_L_comp
    x1_L_comp=round( ((variable_5_L_comp.get()-limites_spectre_L_comp[0])*1000) / (limites_spectre_L_comp[1]-limites_spectre_L_comp[0])) 
    y1_L_comp= round(200*(variable_6_L_comp.get()-0.5)/nbr_fichier)
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
    num_ligne=1
    for ligne_tableau in LIBStick_echange_vars.L_comp_DataFrame_resultats.iterrows() :
        ID_L_comp=tree_resultats_L_comp.insert("","end", values=(num_ligne, ligne_tableau[0], LIBStick_echange_vars.L_comp_DataFrame_resultats.iloc[num_ligne-1, 2]))
        #print(ID)
        num_ligne=num_ligne+1

def selectionne_spectre_L_comp(event):
    selection=tree_resultats_L_comp.item(tree_resultats_L_comp.selection())["values"]
    variable_6_L_comp.set(selection[0])
    vars_5_6_to_coord1_L_comp()
    
###############################################################################
# 6- Interface graphique : nouvelles classes
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
    
###############################################################################
# 7- Interface graphique : création fenêtre principale avec scrolls
###############################################################################
fenetre= tkinter.Tk()
fenetre.title("LIBStick : Comparaison des spectres moyens")
fenetre.geometry("1120x775+100+50")
fenetre.maxsize(width=1125, height=785)

vscrollbar = AutoScrollbar(fenetre,orient=tkinter.VERTICAL)
vscrollbar.grid(row=0, column=1, sticky=tkinter.N+tkinter.S)
hscrollbar = AutoScrollbar(fenetre,orient=tkinter.HORIZONTAL)
hscrollbar.grid(row=1, column=0, sticky=tkinter.E+tkinter.W)

canevas_scroll=tkinter.Canvas(fenetre,yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
canevas_scroll.grid(row=0, column=0, sticky=tkinter.N+tkinter.S+tkinter.E+tkinter.W)

vscrollbar.config(command=canevas_scroll.yview)
hscrollbar.config(command=canevas_scroll.xview)
# make the canvas expandable
fenetre.grid_rowconfigure(0, weight=1)
fenetre.grid_columnconfigure(0, weight=1)

frame_scroll=tkinter.Frame(canevas_scroll)
frame_scroll.rowconfigure(1, weight=1)
frame_scroll.columnconfigure(1, weight=1)

###############################################################################
# 8- Interface graphique : création des différentes zones/étapes (frames 1-2-3)
###############################################################################
frame1_L_comp=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)
frame2_L_comp=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)
frame3_L_comp=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)

frame1_L_comp.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
frame2_L_comp.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
frame3_L_comp.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# 9- Interface graphique frame1_L_comp : création selection répertoire, affiche spectre et bouton executer
###############################################################################
canevas0_L_comp=tkinter.Canvas(frame1_L_comp, width=1000, height=200, bg="white")
canevas0_L_comp.grid(row=1, column=1, columnspan=5)

ligne_position_L_comp=canevas0_L_comp.create_line(0,0,0,200, fill="white")

lambda_texte_L_comp = tkinter.Label(frame1_L_comp, text="Lambda = " + str(format(l_L_comp, "4.1f") + " nm"))
lambda_texte_L_comp.grid(row=2, column=5)

text1_L_comp=tkinter.Label(frame1_L_comp, text="Numérateur borne inf. en nm")
text2_L_comp=tkinter.Label(frame1_L_comp, text="Numérateur borne sup. en nm")
text3_L_comp=tkinter.Label(frame1_L_comp, text="Dénominateur borne inf. en nm")
text4_L_comp=tkinter.Label(frame1_L_comp, text="Dénominateur borne sup. en nm")
text1_L_comp.grid(row=2, column=1)
text2_L_comp.grid(row=2, column=3)
text3_L_comp.grid(row=3, column=1)
text4_L_comp.grid(row=3, column=3)

#variable_1_L_comp=tkinter.DoubleVar(value=534.7)
#variable_2_L_comp=tkinter.DoubleVar(value=535.5)
#variable_3_L_comp=tkinter.DoubleVar( value=529)
#variable_4_L_comp=tkinter.DoubleVar(value=542)
variable_1_L_comp=tkinter.DoubleVar(value=529)
variable_2_L_comp=tkinter.DoubleVar(value=542)
variable_3_L_comp=tkinter.DoubleVar( value=534.7)
variable_4_L_comp=tkinter.DoubleVar(value=535.5)
entree1_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_1_L_comp, command=deplace_ligne0_1_L_comp)
entree2_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013, increment=0.5, textvariable=variable_2_L_comp, command=deplace_ligne0_2_L_comp)
entree3_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5,textvariable=variable_3_L_comp, command=deplace_ligne0_3_L_comp)
entree4_L_comp=tkinter.Spinbox(frame1_L_comp, from_=198, to=1013,  increment=0.5,textvariable=variable_4_L_comp, command=deplace_ligne0_4_L_comp)
entree1_L_comp.grid(row=2, column=2)
entree2_L_comp.grid(row=2, column=4)
entree3_L_comp.grid(row=3, column=2)
entree4_L_comp.grid(row=3, column=4)

flag_denominateur_L_comp=tkinter.IntVar(value=1)
coche_denominateur_L_comp=tkinter.Checkbutton(frame1_L_comp, text="Dénominateur ?", variable=flag_denominateur_L_comp, command=change_flag_denominateur_L_comp)
coche_denominateur_L_comp.grid(row=3, column=5)

bouton_reset_L_comp=tkinter.Button(frame1_L_comp, text="Reset", command=reset_tableau_L_comp, width=9)
bouton_reset_L_comp.grid(row=2, column=6, rowspan=2)

frame1_1_L_comp=tkinter.Frame(frame1_L_comp)
frame1_1_L_comp.grid(row=1, column=6)

text_zoom_L_comp=tkinter.Label(frame1_1_L_comp, text="Zoom : ", width=9)
text_zoom_L_comp.grid(row=1, column=1)
variable_zoom_inf_L_comp=tkinter.DoubleVar(value=198)
variable_zoom_sup_L_comp=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_comp=tkinter.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_inf_L_comp, command=change_zoom_inf_L_comp, width=9)
entree_zoom_sup_L_comp=tkinter.Spinbox(frame1_1_L_comp, from_=198, to=1013, increment=1, textvariable=variable_zoom_sup_L_comp, command=change_zoom_sup_L_comp, width=9)
entree_zoom_inf_L_comp.grid(row=2, column=1)
entree_zoom_sup_L_comp.grid(row=3, column=1)

bouton_rep_L_comp=tkinter.Button(frame1_1_L_comp, text="Repertoire\nde travail" ,command=choix_rep_L_comp, width=9)
bouton_execute_L_comp=tkinter.Button(frame1_1_L_comp, text="Exécute", command=execute_scripts_L_comp, state="disable", width=9)
bouton_rep_L_comp.grid(row=4, column=1)
bouton_execute_L_comp.grid(row=5, column=1)

flag_2D_L_comp=tkinter.IntVar(value=1)
coche_2D_L_comp=tkinter.Checkbutton(frame1_1_L_comp, text="Sortie 2D", variable=flag_2D_L_comp, command=change_flag_2D_L_comp)
coche_2D_L_comp.grid(row=6, column=1)

flag_3D_L_comp=tkinter.IntVar(value=0)
coche_3D_L_comp=tkinter.Checkbutton(frame1_1_L_comp, text="Sortie 3D", variable=flag_3D_L_comp, command=change_flag_3D_L_comp)
coche_3D_L_comp.grid(row=7, column=1)

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

text5_L_comp = tkinter.Label(frame2_L_comp, text="Position x (nm)")
text6_L_comp = tkinter.Label(frame2_L_comp, text="Position y (n° de spectre)")
text5_L_comp.grid(row=3, column=1)
text6_L_comp.grid(row=3, column=2)

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
entree_zoom_inf_L_comp.bind("<Shift-Tab>", change_zoom_inf_return_L_comp)
entree_zoom_sup_L_comp.bind("<Shift-Tab>", change_zoom_sup_return_L_comp)

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
entree1_L_comp.bind("<Shift-Tab>", deplace_ligne0_1_return_L_comp)
entree2_L_comp.bind("<Shift-Tab>", deplace_ligne0_2_return_L_comp)
entree3_L_comp.bind("<Shift-Tab>", deplace_ligne0_3_return_L_comp)
entree4_L_comp.bind("<Shift-Tab>", deplace_ligne0_4_return_L_comp)

entree5_L_comp.bind("<Return>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<Return>", vars_5_6_to_coord1_return_L_comp)
entree5_L_comp.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<KP_Enter>", vars_5_6_to_coord1_return_L_comp)
entree5_L_comp.bind("<Tab>", vars_5_6_to_coord1_return_L_comp)
entree6_L_comp.bind("<Tab>", vars_5_6_to_coord1_return_L_comp)

tree_resultats_L_comp.bind("<ButtonRelease-1>", selectionne_spectre_L_comp)

###############################################################################
# 13- Interface graphique : gestion du redimentionnement de la fenêtre principale
###############################################################################
canevas_scroll.create_window(0, 0, anchor='nw', window=frame_scroll)
frame_scroll.update_idletasks()
canevas_scroll.config(scrollregion=canevas_scroll.bbox("all"))

fenetre.mainloop()
