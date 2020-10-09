#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:05:40 2020

@author: yannick
"""

import tkinter, numpy, tkinter.filedialog
import os, math
import PIL.Image, PIL.ImageTk
import LIBStick_echange_vars
import LIBStick_extraction_spectres
import LIBStick_creation_spectre_moyen

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
tableau_bornes_init_L_ext=numpy.array([[528, 543],[592, 608]])
tableau_bornes_L_ext=numpy.array([[528, 543],[592, 608]])
rep_travail_L_ext="./"
#rep_travail="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1"
x1_L_ext=250.0
y1_L_ext=100.0
x2_L_ext=250.0
y2_L_ext=100.0

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def creation_tab_bornes_L_ext() :
    global tableau_bornes_L_ext
    tableau_bornes_L_ext[0,0]=variable_L_ext_1.get()
    tableau_bornes_L_ext[0,1]=variable_L_ext_2.get()
    entree5_L_ext.configure(from_=tableau_bornes_L_ext[0,0], to=tableau_bornes_L_ext[0,1])  
    if flag_zone2_L_ext.get() :
        tableau_bornes_L_ext[1,0]=variable_L_ext_3.get()
        tableau_bornes_L_ext[1,1]=variable_L_ext_4.get()
        entree7_L_ext.configure(from_=tableau_bornes_L_ext[1,0], to=tableau_bornes_L_ext[1,1]) 
    return tableau_bornes_L_ext

def reset_tableau_L_ext() :
    global tableau_bornes_L_ext
    tableau_bornes_L_ext=tableau_bornes_init_L_ext.copy()
    variable_L_ext_1.set(tableau_bornes_L_ext[0,0])
    variable_L_ext_2.set(tableau_bornes_L_ext[0,1])
    variable_L_ext_3.set(tableau_bornes_L_ext[1,0])
    variable_L_ext_4.set(tableau_bornes_L_ext[1,1])
    deplace_lignes_L_ext()

def choix_rep_L_ext():
    global rep_travail
    global nbr_fichier
    #rep_travail = tkinter.filedialog.askdirectory(initialdir="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1",title='Choisissez un repertoire')
    rep_travail = tkinter.filedialog.askdirectory(initialdir="./",title='Choisissez un repertoire')    
    LIBStick_echange_vars.L_ext_liste_fichiers=LIBStick_extraction_spectres.creation_liste_fichiers(rep_travail)
    LIBStick_echange_vars.L_ext_nombre_fichiers=len(LIBStick_echange_vars.L_ext_liste_fichiers)
    nbr_fichier=LIBStick_echange_vars.L_ext_nombre_fichiers
    lit_affiche_spectre_L_ext()
    bouton_execute_L_ext.configure(state="normal")
    entree6_L_ext.configure(to=LIBStick_echange_vars.L_ext_nombre_fichiers)
    entree8_L_ext.configure(to=LIBStick_echange_vars.L_ext_nombre_fichiers)
    entree9_L_ext.configure(to=LIBStick_echange_vars.L_ext_nombre_fichiers)
    entree10_L_ext.configure(to=LIBStick_echange_vars.L_ext_nombre_fichiers)
    
def execute_scripts_L_ext():
    tableau_bornes_L_ext=creation_tab_bornes_L_ext()
    if flag_zone2_L_ext.get() == 0 :
        canevas2_L_ext.delete("all")
    LIBStick_extraction_spectres.main(rep_travail, tableau_bornes_L_ext)
    global photo1, photo2
    fichier1=rep_travail+"/"+str(tableau_bornes_L_ext[0,0])+"_"+str(tableau_bornes_L_ext[0,1])+"/figure.png"
    image1_zoom=PIL.Image.open(fichier1)    
    image1_zoom=image1_zoom.resize((500, 200))
    photo1=PIL.ImageTk.PhotoImage(image1_zoom)
    canevas1_L_ext.create_image(250 ,100 ,image=photo1)
    if flag_zone2_L_ext.get() :
        fichier2=rep_travail+"/"+str(tableau_bornes_L_ext[1,0])+"_"+str(tableau_bornes_L_ext[1,1])+"/figure.png"
        image2_zoom=PIL.Image.open(fichier2)
        image2_zoom=image2_zoom.resize((500,200))
        photo2=PIL.ImageTk.PhotoImage(image2_zoom)
        canevas2_L_ext.create_image(250,100  ,image=photo2)
    #print("nombre de spectres : " + str(nbr_fichier))
    bouton_extraction_L_ext.configure(state="normal")
    #plt.show(block=False)

def creation_spectre_moyen_L_ext():
    LIBStick_echange_vars.L_ext_bornes_moyenne_spectres.insert(0,variable_L_ext_9.get())
    LIBStick_echange_vars.L_ext_bornes_moyenne_spectres.insert(1,variable_L_ext_10.get())
    tableau_bornes_copy_L_ext=tableau_bornes_L_ext.copy()
    i=3
    if flag_zone2_L_ext.get() == 0:
        tableau_bornes_copy_L_ext=numpy.delete(tableau_bornes_copy_L_ext, (1), axis=0)
        #print ("copy tableau bornes pour extraction : ")
        #print (tableau_bornes_copy_L_ext)
        canevas4_L_ext.delete("all")
    for bornes in tableau_bornes_copy_L_ext :
        repertoire=rep_travail+"/"+str(bornes[0])+"_"+ str(bornes[1])+"/"
        spectre=LIBStick_creation_spectre_moyen.main(repertoire,LIBStick_echange_vars.L_ext_nom_echantillon,bornes)
        if i==3 :
            canevas3_L_ext.delete("all")
            minimum=spectre[:].min()
            maximum=spectre[:].max()
            spectre[:] = (200-(spectre[:] - minimum)*200/(maximum - minimum))
            for j in range(len(spectre) - 1) :
                dx=500/len(spectre)
                x=j*dx
                canevas3_L_ext.create_line(x,spectre[j],x+dx,spectre[j+1], width=1, fill="red", smooth=1)
        if i==4 :
            canevas4_L_ext.delete("all")
            minimum=spectre[:].min()
            maximum=spectre[:].max()
            spectre[:] = (200-(spectre[:] - minimum)*200/(maximum - minimum))
            for j in range(len(spectre) - 1) :
                dx=500/len(spectre)
                x=j*dx
                canevas4_L_ext.create_line(x,spectre[j],x+dx,spectre[j+1], width=1, fill="blue", smooth=1)
        i=i+1

###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1_L_ext)
###############################################################################
def change_flag_2D_L_ext():
    LIBStick_echange_vars.L_ext_flag_2D=flag_2D_L_ext.get()
    
def change_flag_3D_L_ext():
    LIBStick_echange_vars.L_ext_flag_3D=flag_3D_L_ext.get()

def change_flag_zone2_L_ext():
    LIBStick_echange_vars.L_ext_flag_zone2=flag_zone2_L_ext.get()
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
    if variable_L_ext__zoom_inf.get() >= variable_L_ext__zoom_sup.get() :
        variable_L_ext__zoom_sup.set(variable_L_ext__zoom_inf.get())
#    limites_affichage_spectre_L_ext[0]=variable_L_ext__zoom_inf.get()
#    limites_affichage_spectre_L_ext[1]=variable_L_ext__zoom_sup.get()
    affiche_spectre_L_ext()
    
def change_zoom_sup_L_ext():
#    global limites_affichage_spectre_L_ext
    if variable_L_ext__zoom_sup.get() <= variable_L_ext__zoom_inf.get() :
        variable_L_ext__zoom_inf.set(variable_L_ext__zoom_sup.get())
#    limites_affichage_spectre_L_ext[0]=variable_L_ext__zoom_inf.get()
#    limites_affichage_spectre_L_ext[1]=variable_L_ext__zoom_sup.get()
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
        variable_L_ext__zoom_inf.set(format(debut, "4.1f"))
        variable_L_ext__zoom_sup.set(format(fin, "4.1f"))
        #affiche la longueur d'onde :
        if flag_premier_lamda_L_ext == False :
            canevas0_L_ext.delete(lambda_texte_spectre_L_ext)
        l= event.x*delta_limites_L_ext/1000+limites_affichage_spectre_L_ext[0]
        lambda_texte_spectre_L_ext = canevas0_L_ext.create_text(event.x, event.y, text=str(format(l, "4.1f")), fill="blue")
        lambda_texte_L_ext.configure(text="Lambda = " + str(format(l, "4.1f") + " nm" ))
        flag_premier_lamda_L_ext=False
    if coord_zoom_L_ext[2] < coord_zoom_L_ext[0] :
        variable_L_ext__zoom_inf.set(limites_spectre_L_ext[0])
        variable_L_ext__zoom_sup.set(limites_spectre_L_ext[1])
        limites_affichage_spectre_L_ext[0]=variable_L_ext__zoom_inf.get()
        limites_affichage_spectre_L_ext[1]=variable_L_ext__zoom_sup.get()

def zoom_clic_release_L_ext(event):
    affiche_spectre_L_ext()
         
def lit_affiche_spectre_L_ext():
    global spectre_entier 
    os.chdir(rep_travail)
    #if LIBStick_echange_vars.L_ext_nombre_fichiers > 0 :
    spectre_entier=LIBStick_extraction_spectres.lit_spectre(LIBStick_echange_vars.L_ext_liste_fichiers[0])
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
    limites_affichage_spectre_L_ext[0]=variable_L_ext__zoom_inf.get()
    limites_affichage_spectre_L_ext[1]=variable_L_ext__zoom_sup.get()
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
    global ligne0_1
    global ligne0_2
    global ligne0_3
    global ligne0_4
    x_ligne0_1=((variable_L_ext_1.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    x_ligne0_2=((variable_L_ext_2.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_1=canevas0_L_ext.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red")
    ligne0_2=canevas0_L_ext.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red")
    if flag_zone2_L_ext.get() :
        x_ligne0_3=((variable_L_ext_3.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        x_ligne0_4=((variable_L_ext_4.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_3=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue")
        ligne0_4=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue")
        
def deplace_lignes_L_ext():
    deplace_ligne0_1_L_ext()
    deplace_ligne0_2_L_ext()
    if flag_zone2_L_ext.get() :
        deplace_ligne0_3_L_ext()
        deplace_ligne0_4_L_ext()

def deplace_ligne0_1_L_ext():
    global ligne0_1
    canevas0_L_ext.delete(ligne0_1)
    x_ligne0_1=((variable_L_ext_1.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_1=canevas0_L_ext.create_line(x_ligne0_1,0,x_ligne0_1,200, fill="red")
    if variable_L_ext_1.get() >= variable_L_ext_2.get():
        variable_L_ext_2.set(variable_L_ext_1.get())
        deplace_ligne0_2_L_ext()
        
def deplace_ligne0_2_L_ext():
    global ligne0_2
    canevas0_L_ext.delete(ligne0_2)
    x_ligne0_2=((variable_L_ext_2.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_2=canevas0_L_ext.create_line(x_ligne0_2,0,x_ligne0_2,200, fill="red")
    if variable_L_ext_2.get() <= variable_L_ext_1.get() :
        variable_L_ext_1.set(variable_L_ext_2.get())
        deplace_ligne0_1_L_ext()

def deplace_ligne0_3_L_ext():
    global ligne0_3
    canevas0_L_ext.delete(ligne0_3)
    if flag_zone2_L_ext.get() :
        x_ligne0_3=((variable_L_ext_3.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_3=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue")
        if variable_L_ext_3.get() >= variable_L_ext_4.get():
            variable_L_ext_4.set(variable_L_ext_3.get())
            deplace_ligne0_4_L_ext()
        
def deplace_ligne0_4_L_ext():
    global ligne0_4
    canevas0_L_ext.delete(ligne0_4)
    if flag_zone2_L_ext.get() :
        x_ligne0_4=((variable_L_ext_4.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
        ligne0_4=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue")
        if variable_L_ext_4.get() <= variable_L_ext_3.get() :
            variable_L_ext_3.set(variable_L_ext_4.get())
            deplace_ligne0_3_L_ext()

def efface_lignes_3_4_L_ext():
    global ligne0_3
    global ligne0_4
    canevas0_L_ext.delete(ligne0_3)
    canevas0_L_ext.delete(ligne0_4)

def affiche_lignes_3_4_L_ext():
    global ligne0_3
    global ligne0_4
    canevas0_L_ext.delete(ligne0_3)
    canevas0_L_ext.delete(ligne0_4)
    x_ligne0_3=((variable_L_ext_3.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    x_ligne0_4=((variable_L_ext_4.get()-limites_affichage_spectre_L_ext[0])*1000/delta_limites_L_ext)
    ligne0_3=canevas0_L_ext.create_line(x_ligne0_3,0,x_ligne0_3,200, fill="blue")
    ligne0_4=canevas0_L_ext.create_line(x_ligne0_4,0,x_ligne0_4,200, fill="blue")
        
def deplace_ligne0_1_return_L_ext(event):
    deplace_ligne0_1_L_ext()
    
def deplace_ligne0_2_return_L_ext(event):
    deplace_ligne0_2_L_ext()
    
def deplace_ligne0_3_return_L_ext(event):
    deplace_ligne0_3_L_ext()
    
def deplace_ligne0_4_return_L_ext(event):
    deplace_ligne0_4_L_ext()

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
    variable_L_ext_6.set(math.ceil(y * nbr_fichier / 200))

def vars_5_6_to_coord1_L_ext():
    global x1_L_ext,y1_L_ext
    x1_L_ext=round( ((variable_L_ext_5.get()-variable_L_ext_1.get())*500) / (variable_L_ext_2.get()-variable_L_ext_1.get())) 
    y1_L_ext= round(200*(variable_L_ext_6.get()-0.5)/nbr_fichier)
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
    variable_L_ext_8.set(math.ceil(y * nbr_fichier / 200))

def vars_7_8_to_coord2_L_ext():
    global x2_L_ext,y2_L_ext
    x2_L_ext= round((variable_L_ext_7.get()-variable_L_ext_3.get())*500/(variable_L_ext_4.get()-variable_L_ext_3.get()))
    y2_L_ext= round(200*(variable_L_ext_8.get()-0.5)/nbr_fichier)
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
fenetre.title("LIBStick : Extraction de spectres moyens")
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
frame1_L_ext=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)
frame2_L_ext=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)
frame3_L_ext=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)

#frame1_L_ext=tkinter.Frame(onglet1,borderwidth=2,relief=tkinter.RAISED)
#frame2_L_ext=tkinter.Frame(onglet1,borderwidth=2,relief=tkinter.RAISED)
#frame3_L_ext=tkinter.Frame(onglet1,borderwidth=2,relief=tkinter.RAISED)

frame1_L_ext.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
frame2_L_ext.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
frame3_L_ext.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# 9- Interface graphique frame1_L_ext : création selection répertoire, affiche spectre et bouton executer
###############################################################################
canevas0_L_ext=tkinter.Canvas(frame1_L_ext, width=1000, height=200, bg="white")
canevas0_L_ext.grid(row=1, column=1, columnspan=5)

ligne_position_L_ext=canevas0_L_ext.create_line(0,0,0,200, fill="white")

lambda_texte_L_ext = tkinter.Label(frame1_L_ext, text="Lambda = " + str(format(l_L_ext, "4.1f") + " nm"))
lambda_texte_L_ext.grid(row=2, column=5)

text1_L_ext=tkinter.Label(frame1_L_ext, text="Première borne inf. en nm")
text2_L_ext=tkinter.Label(frame1_L_ext, text="Première borne sup. en nm")
text3_L_ext=tkinter.Label(frame1_L_ext, text="Seconde borne inf. en nm")
text4_L_ext=tkinter.Label(frame1_L_ext, text="Seconde borne sup. en nm")
text1_L_ext.grid(row=2, column=1)
text2_L_ext.grid(row=2, column=3)
text3_L_ext.grid(row=3, column=1)
text4_L_ext.grid(row=3, column=3)

variable_L_ext_1=tkinter.DoubleVar(value=528)
variable_L_ext_2=tkinter.DoubleVar(value=543)
variable_L_ext_3=tkinter.DoubleVar( value=592)
variable_L_ext_4=tkinter.DoubleVar(value=608)
entree1_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_1, command=deplace_ligne0_1_L_ext)
entree2_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_2, command=deplace_ligne0_2_L_ext)
entree3_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_3, command=deplace_ligne0_3_L_ext)
entree4_L_ext=tkinter.Spinbox(frame1_L_ext, from_=198, to=1013, textvariable=variable_L_ext_4, command=deplace_ligne0_4_L_ext)
entree1_L_ext.grid(row=2, column=2)
entree2_L_ext.grid(row=2, column=4)
entree3_L_ext.grid(row=3, column=2)
entree4_L_ext.grid(row=3, column=4)

flag_zone2_L_ext=tkinter.IntVar(value=1)
coche_zone2_L_ext=tkinter.Checkbutton(frame1_L_ext, text="Seconde extraction ?", variable=flag_zone2_L_ext, command=change_flag_zone2_L_ext)
coche_zone2_L_ext.grid(row=3, column=5)

bouton_reset_L_ext=tkinter.Button(frame1_L_ext, text="Reset", command=reset_tableau_L_ext, width=9)
bouton_reset_L_ext.grid(row=2, column=6, rowspan=2)

frame1_1_L_ext=tkinter.Frame(frame1_L_ext)
frame1_1_L_ext.grid(row=1, column=6)

text_zoom_L_ext=tkinter.Label(frame1_1_L_ext, text="Zoom : ", width=9)
text_zoom_L_ext.grid(row=1, column=1)
variable_L_ext__zoom_inf=tkinter.DoubleVar(value=198)
variable_L_ext__zoom_sup=tkinter.DoubleVar(value=1013)
entree_zoom_inf_L_ext=tkinter.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_L_ext__zoom_inf, command=change_zoom_inf_L_ext, width=9)
entree_zoom_sup_L_ext=tkinter.Spinbox(frame1_1_L_ext, from_=198, to=1013, increment=5, textvariable=variable_L_ext__zoom_sup, command=change_zoom_sup_L_ext, width=9)
entree_zoom_inf_L_ext.grid(row=2, column=1)
entree_zoom_sup_L_ext.grid(row=3, column=1)

bouton_rep_L_ext=tkinter.Button(frame1_1_L_ext, text="Repertoire\nde travail" ,command=choix_rep_L_ext, width=9)
bouton_execute_L_ext=tkinter.Button(frame1_1_L_ext, text="Exécute", command=execute_scripts_L_ext, state="disable", width=9)
bouton_rep_L_ext.grid(row=4, column=1)
bouton_execute_L_ext.grid(row=5, column=1)

flag_2D_L_ext=tkinter.IntVar(value=1)
coche_2D_L_ext=tkinter.Checkbutton(frame1_1_L_ext, text="Sortie 2D", variable=flag_2D_L_ext, command=change_flag_2D_L_ext)
coche_2D_L_ext.grid(row=6, column=1)

flag_3D_L_ext=tkinter.IntVar(value=0)
coche_3D_L_ext=tkinter.Checkbutton(frame1_1_L_ext, text="Sortie 3D", variable=flag_3D_L_ext, command=change_flag_3D_L_ext)
coche_3D_L_ext.grid(row=7, column=1)


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

text5_L_ext = tkinter.Label(frame2_L_ext, text="Position x (nm)")
text6_L_ext = tkinter.Label(frame2_L_ext, text="Position y (n° de spectre)")
text7_L_ext = tkinter.Label(frame2_L_ext, text="Position x (nm)")
text8_L_ext = tkinter.Label(frame2_L_ext, text="Position y (n° de spectre)")
text5_L_ext.grid(row=3, column=1)
text6_L_ext.grid(row=3, column=2)
text7_L_ext.grid(row=3, column=3)
text8_L_ext.grid(row=3, column=4)

ligne1_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
ligne1_hori_L_ext=canevas1_L_ext.create_line(0,y1_L_ext,500,y1_L_ext, fill="white")
ligne2_vert_L_ext=canevas1_L_ext.create_line(x1_L_ext,0,x1_L_ext,200, fill="white")
ligne2_hori_L_ext=canevas1_L_ext.create_line(0,y1_L_ext,500,y1_L_ext, fill="white")

affiche_lignes_spectre_L_ext()

###############################################################################
# 11- Interface graphique frame3_L_ext : création selection des spectres à moyenner
###############################################################################
text9_L_ext=tkinter.Label(frame3_L_ext, text="Du spectre n° :")
text10_L_ext=tkinter.Label(frame3_L_ext, text="Au spectre n° :")
text9_L_ext.grid(row=1, column=1)
text10_L_ext.grid(row=1, column=3)

variable_L_ext_9=tkinter.IntVar(value=0)
variable_L_ext_10=tkinter.IntVar(value=0)
entree9_L_ext=tkinter.Spinbox(frame3_L_ext,from_=1, to=200, textvariable=variable_L_ext_9, command=retro_action_entree10_L_ext)
entree10_L_ext=tkinter.Spinbox(frame3_L_ext,from_=1, to=200, textvariable=variable_L_ext_10, command=retro_action_entree9_L_ext)
entree9_L_ext.grid(row=1, column=2)
entree10_L_ext.grid(row=1, column=4)

fram3_1_L_ext=tkinter.Frame(frame3_L_ext)
fram3_1_L_ext.grid(row=1, column=5)
bouton_extraction_L_ext=tkinter.Button(fram3_1_L_ext, text="Extraction", state="disable", command=creation_spectre_moyen_L_ext, width=9)
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
entree_zoom_inf_L_ext.bind("<Shift-Tab>", change_zoom_inf_return_L_ext)
entree_zoom_sup_L_ext.bind("<Shift-Tab>", change_zoom_sup_return_L_ext)

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
entree1_L_ext.bind("<Shift-Tab>", deplace_ligne0_1_return_L_ext)
entree2_L_ext.bind("<Shift-Tab>", deplace_ligne0_2_return_L_ext)
entree3_L_ext.bind("<Shift-Tab>", deplace_ligne0_3_return_L_ext)
entree4_L_ext.bind("<Shift-Tab>", deplace_ligne0_4_return_L_ext)


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
entree9_L_ext.bind("<Shift-Tab>", change_entree9_L_ext)
entree10_L_ext.bind("<Shift-Tab>", change_entree10_L_ext)


###############################################################################
# 13- Interface graphique : gestion du redimentionnement de la fenêtre principale
###############################################################################
canevas_scroll.create_window(0, 0, anchor='nw', window=frame_scroll)
frame_scroll.update_idletasks()
canevas_scroll.config(scrollregion=canevas_scroll.bbox("all"))

fenetre.mainloop()
