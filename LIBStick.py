#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 15:05:40 2020

@author: yannick
"""

import tkinter, numpy, tkinter.filedialog
import os, math
import PIL.Image, PIL.ImageTk
import LIBStick_extraction_spectres
import LIBStick_echange_vars

###############################################################################
# 0- initialisations
###############################################################################
tableau_bornes=numpy.array([[528, 543],[592, 608]])
rep_travail="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1"
x1=250.0
y1=100.0
x2=250.0
y2=100.0

###############################################################################
# 1- fonctions traitement des données
###############################################################################
def affiche_tableau() :
#    tableau_bornes=numpy.array([[eval(entree1.get()), eval(entree2.get())],[eval(entree3.get()), eval(entree4.get())]])
    print(tableau_bornes)
    
#def creation_tab_bornes_0() :
#    global tableau_bornes
#    #tableau_bornes=numpy.array([[528, 543],[592, 608]])
#    tableau_bornes=numpy.array([[variable1.get(),variable2.get()],[variable3.get(),variable4.get()]])
#    #print (tableau_bornes)

def creation_tab_bornes() :
    tableau_bornes[0,0]=variable1.get()
    tableau_bornes[0,1]=variable2.get()
    tableau_bornes[1,0]=variable3.get()
    tableau_bornes[1,1]=variable4.get()    
    
def reset_tableau() :
    tableau_bornes[0,0]=528
    tableau_bornes[0,1]=543
    tableau_bornes[1,0]=592
    tableau_bornes[1,1]=608
    variable1.set(tableau_bornes[0,0])
    variable2.set(tableau_bornes[0,1])
    variable3.set(tableau_bornes[1,0])
    variable4.set(tableau_bornes[1,1])
    deplace_lignes()
    #affiche_tableau()

def choix_rep():
    global rep_travail
    rep_travail = tkinter.filedialog.askdirectory(initialdir="~/Bureau/LIBS/Scripts_divers_pour_LIBS/repertoire_Zone_1",title='Choisissez un repertoire')
    LIBStick_echange_vars.liste_fichiers=LIBStick_extraction_spectres.creation_liste_fichiers(rep_travail)
    affiche_spectre()
    bouton_execute.configure(state="normal")
    
def affiche_rep():
    print(rep_travail)
    
def execute_scripts():
    creation_tab_bornes()
    LIBStick_extraction_spectres.main(rep_travail, tableau_bornes)
    global photo1, photo2
    global nbr_fichier
    fichier1=rep_travail+"/"+str(tableau_bornes[0,0])+"_"+str(tableau_bornes[0,1])+"/figure.png"
    fichier2=rep_travail+"/"+str(tableau_bornes[1,0])+"_"+str(tableau_bornes[1,1])+"/figure.png"
    image1_zoom=PIL.Image.open(fichier1)
    image2_zoom=PIL.Image.open(fichier2)
#    image1_zoom=image1_zoom.resize((image1_zoom.width*2, image1_zoom.height*2))
#    image2_zoom=image2_zoom.resize((image2_zoom.width*2, image2_zoom.height*2))
    image1_zoom=image1_zoom.resize((500, 200))
    image2_zoom=image2_zoom.resize((500,200))
    photo1=PIL.ImageTk.PhotoImage(image1_zoom)
    photo2=PIL.ImageTk.PhotoImage(image2_zoom)
    canevas1.create_image(250 ,100 ,image=photo1)
    canevas2.create_image(250,100  ,image=photo2)
    nbr_fichier=LIBStick_echange_vars.nombre_fichiers
    print("nombre de spectres : " + str(nbr_fichier))
    #plt.show(block=False)

#def affiche_images() :
#    global image1
#    global image2
#    image1=tkinter.PhotoImage(file=rep_travail+"/528_543/figure.png")
#    image2=tkinter.PhotoImage(file=rep_travail+"/592_608/figure.png")
#    canevas1.create_image(150 ,50 ,image=image1)
#    canevas2.create_image(150,50  ,image=image2)

def change_flag_3D():
    LIBStick_echange_vars.flag_3D=flag_3D.get()

###############################################################################
# 2- fonctions graphiques du caneva du spectre (frame1)
###############################################################################
def affiche_spectre():
    os.chdir(rep_travail)
    canevas0.delete("all")
    #if LIBStick_echange_vars.nombre_fichiers > 0 :
    spectre=LIBStick_extraction_spectres.lit_spectre(LIBStick_echange_vars.liste_fichiers[0])
    minimum=spectre[:,1].min()
    maximum=spectre[:,1].max()
    spectre[:,1] = (200-(spectre[:,1] - minimum)*200/(maximum - minimum))
    #spectre[:,0] = (spectre[:,0] - spectre[0,0])*1000/(spectre[len(spectre),0]-spectre[0,0])
    spectre[:,0] = (spectre[:,0] - 197)*1000/(608-197)
    for i in range(len(spectre) - 1) :
        canevas0.create_line(spectre[i,0],spectre[i,1],spectre[i+1,0],spectre[i+1,1])
    affiche_lignes_spectre()
    
def affiche_lignes_spectre():
    global ligne0_1
    global ligne0_2
    global ligne0_3
    global ligne0_4    
    ligne0_1=canevas0.create_line(((variable1.get()-198)*1000/410),0,((variable1.get()-198)*1000/410),200, fill="red")
    ligne0_2=canevas0.create_line(((variable2.get()-198)*1000/410),0,((variable2.get()-198)*1000/410),200, fill="red")
    ligne0_3=canevas0.create_line(((variable3.get()-198)*1000/410),0,((variable3.get()-198)*1000/410),200, fill="blue")
    ligne0_4=canevas0.create_line(((variable4.get()-198)*1000/410),0,((variable4.get()-198)*1000/410),200, fill="blue")
        
def deplace_lignes():
    deplace_ligne0_1()
    deplace_ligne0_2()
    deplace_ligne0_3()
    deplace_ligne0_4()

def deplace_ligne0_1():
    global ligne0_1
    canevas0.delete(ligne0_1)
    ligne0_1=canevas0.create_line(((variable1.get()-198)*1000/410),0,((variable1.get()-198)*1000/410),200, fill="red")
    if variable1.get() > variable2.get():
        variable2.set(variable1.get())
        deplace_ligne0_2()
        
def deplace_ligne0_2():
    global ligne0_2
    canevas0.delete(ligne0_2)
    ligne0_2=canevas0.create_line(((variable2.get()-198)*1000/410),0,((variable2.get()-198)*1000/410),200, fill="red")
    if variable2.get() < variable1.get() :
        variable1.set(variable2.get())
        deplace_ligne0_1()

def deplace_ligne0_3():
    global ligne0_3
    canevas0.delete(ligne0_3)
    ligne0_3=canevas0.create_line(((variable3.get()-198)*1000/410),0,((variable3.get()-198)*1000/410),200, fill="blue")
    if variable3.get() > variable4.get():
        variable4.set(variable3.get())
        deplace_ligne0_4()
        
def deplace_ligne0_4():
    global ligne0_4
    canevas0.delete(ligne0_4)
    ligne0_4=canevas0.create_line(((variable4.get()-198)*1000/410),0,((variable4.get()-198)*1000/410),200, fill="blue")
    if variable4.get() < variable3.get() :
        variable3.set(variable4.get())
        deplace_ligne0_3()
        
def deplace_ligne0_1_return(event):
    deplace_ligne0_1()
    
def deplace_ligne0_2_return(event):
    deplace_ligne0_2()
    
def deplace_ligne0_3_return(event):
    deplace_ligne0_3()
    
def deplace_ligne0_4_return(event):
    deplace_ligne0_4()

###############################################################################
# 3- fonctions graphiques du caneva de l'image 1 (frame2)
###############################################################################
def coordonnees1 (event) :
    global x1,y1
    x1=event.x
    y1=event.y
    coord1_to_vars_5_6(x1,y1)
    deplace_cible1()
   
def deplace_cible1():
    global x1,y1
    global ligne1_vert, ligne1_hori
    canevas1.delete(ligne1_vert)
    canevas1.delete(ligne1_hori)
    ligne1_vert=canevas1.create_line(x1,0,x1,200, fill="white")
    ligne1_hori=canevas1.create_line(0,y1,500,y1, fill="white")    
#    canevas1.coords(ligne1_vert, x1,0,x1,200)
#    canevas1.coords(ligne1_hori, 0,y1,400,y1)
    
def coord1_to_vars_5_6(x,y):
    variable5.set(variable1.get() + (x * (variable2.get()-variable1.get()) / 500))
    variable6.set(math.ceil(y * nbr_fichier / 200))

def vars_5_6_to_coord1():
    global x1,y1
    x1=round( ((variable5.get()-variable1.get())*500) / (variable2.get()-variable1.get())) 
    y1= round(200*(variable6.get()-0.5)/nbr_fichier)
    deplace_cible1()
    
def vars_5_6_to_coord1_return(event):
    vars_5_6_to_coord1()

###############################################################################
# 4- fonctions graphiques du caneva de l'image 2 (frame2)
###############################################################################      
def coordonnees2 (event) :
    global x2,y2
    x2=event.x
    y2=event.y
    coord2_to_vars_7_8(x2,y2)
    deplace_cible2()
    
def deplace_cible2():
    global x2,y2
    global ligne2_vert, ligne2_hori
    canevas2.delete(ligne2_vert)
    canevas2.delete(ligne2_hori)
    ligne2_vert=canevas2.create_line(x2,0,x2,200, fill="white")
    ligne2_hori=canevas2.create_line(0,y2,500,y2, fill="white")
    
def coord2_to_vars_7_8(x,y):
    variable7.set(variable3.get() + (x * (variable4.get()-variable3.get()) / 500))
    variable8.set(math.ceil(y * nbr_fichier / 200))

def vars_7_8_to_coord2():
    global x2,y2
    x2= round((variable7.get()-variable3.get())*500/(variable4.get()-variable3.get()))
    y2= round(200*(variable8.get()-0.5)/nbr_fichier)
    deplace_cible2()
    
def vars_7_8_to_coord2_return(event):
    vars_7_8_to_coord2()

###############################################################################
# 5- fonctions graphiques du choix des spectres à moyenner (frame3)
###############################################################################
def creation_spectre_moyen():
    LIBStick_echange_vars.bornes_moyenne_spectres.insert(0,variable9.get())
    LIBStick_echange_vars.bornes_moyenne_spectres.insert(1,variable10.get())
    
    
def retro_action_entree10():
    if variable9.get() > variable10.get():
        variable10.set(variable9.get())

def retro_action_entree9():
    if variable10.get() < variable9.get():
        variable9.set(variable10.get())

def change_entree9(event):
    retro_action_entree10()
    
def change_entree10(event):
    retro_action_entree9()
    
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
fenetre.title("LIBStick")
fenetre.geometry("1020x600+100+50")
fenetre.maxsize(width=1035, height=615)

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
frame1=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)
frame2=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)
frame3=tkinter.Frame(frame_scroll,borderwidth=2,relief=tkinter.RAISED)

frame1.grid(row=10, column=10, padx=5, pady=5,sticky = tkinter.W)
frame2.grid(row=20, column=10, padx=5, pady=5,sticky = tkinter.W)
frame3.grid(row=30, column=10, padx=5, pady=5, sticky = tkinter.W)

###############################################################################
# 9- Interface graphique frame1: création selection répertoire, affiche spectre et bouton executer
###############################################################################
canevas0=tkinter.Canvas(frame1, width=1000, height=200, bg="white")
canevas0.grid(row=1, column=0, columnspan=5)

text1=tkinter.Label(frame1, text="Première borne inf. en nm")
text2=tkinter.Label(frame1, text="Première borne sup. en nm")
text3=tkinter.Label(frame1, text="Seconde borne inf. en nm")
text4=tkinter.Label(frame1, text="Seconde borne sup. en nm")
text1.grid(row=2, column=0)
text2.grid(row=2, column=2)
text3.grid(row=3, column=0)
text4.grid(row=3, column=2)

variable1=tkinter.IntVar(value=528)
variable2=tkinter.IntVar(value=543)
variable3=tkinter.IntVar( value=592)
variable4=tkinter.IntVar(value=608)
entree1=tkinter.Spinbox(frame1, from_=198, to=1013, textvariable=variable1, command=deplace_ligne0_1)
entree2=tkinter.Spinbox(frame1, from_=198, to=1013, textvariable=variable2, command=deplace_ligne0_2)
entree3=tkinter.Spinbox(frame1, from_=198, to=1013, textvariable=variable3, command=deplace_ligne0_3)
entree4=tkinter.Spinbox(frame1, from_=198, to=1013, textvariable=variable4, command=deplace_ligne0_4)
entree1.grid(row=2, column=1)
entree2.grid(row=2, column=3)
entree3.grid(row=3, column=1)
entree4.grid(row=3, column=3)

bouton_reset=tkinter.Button(frame1, text="Reset", command=reset_tableau)
bouton_rep=tkinter.Button(frame1, text="Repertoire de travail" ,command=choix_rep)
bouton_execute=tkinter.Button(frame1, text="Exécute", command=execute_scripts, state="disable")
bouton_reset.grid(row=2, column=4, rowspan=2)
bouton_rep.grid(row=4, column=0)
bouton_execute.grid(row=4, column=1)

flag_3D=tkinter.IntVar(value=0)
coche_3D=tkinter.Checkbutton(frame1, text="Sortie 3D", variable=flag_3D, command=change_flag_3D)
coche_3D.grid(row=4, column=2)

###############################################################################
# 10- Interface graphique frame2: création visues des résultats et aide à la sélection
###############################################################################
canevas1=tkinter.Canvas(frame2, width=500, height=200, bg="white")
canevas2=tkinter.Canvas(frame2, width=500, height=200, bg="white")
canevas1.grid(row=1, column=0, columnspan=2)
canevas2.grid(row=1, column=2, columnspan=2)

variable5=tkinter.DoubleVar(value=0)
variable6=tkinter.IntVar(value=0)
variable7=tkinter.DoubleVar(value=0)
variable8=tkinter.IntVar(value=0)
entree5=tkinter.Spinbox(frame2, from_=198, to=1013, textvariable=variable5, command=vars_5_6_to_coord1, increment=0.5)
entree6=tkinter.Spinbox(frame2, from_=0, to=100, textvariable=variable6, command=vars_5_6_to_coord1)
entree7=tkinter.Spinbox(frame2, from_=198, to=1013, textvariable=variable7, command=vars_7_8_to_coord2, increment=0.5)
entree8=tkinter.Spinbox(frame2, from_=0, to=100, textvariable=variable8, command=vars_7_8_to_coord2)
entree5.grid(row=2, column=0)
entree6.grid(row=2, column=1)
entree7.grid(row=2, column=2)
entree8.grid(row=2, column=3)

text5 = tkinter.Label(frame2, text="Position x (nm)")
text6 = tkinter.Label(frame2, text="Position y (n° de spectre)")
text7 = tkinter.Label(frame2, text="Position x (nm)")
text8 = tkinter.Label(frame2, text="Position y (n° de spectre)")
text5.grid(row=3, column=0)
text6.grid(row=3, column=1)
text7.grid(row=3, column=2)
text8.grid(row=3, column=3)

ligne1_vert=canevas1.create_line(x1,0,x1,200, fill="white")
ligne1_hori=canevas1.create_line(0,y1,500,y1, fill="white")
ligne2_vert=canevas1.create_line(x1,0,x1,200, fill="white")
ligne2_hori=canevas1.create_line(0,y1,500,y1, fill="white")

affiche_lignes_spectre()

###############################################################################
# 11- Interface graphique frame3 : création selection des spectres à moyenner
###############################################################################
text9=tkinter.Label(frame3, text="Du spectre n° :")
text10=tkinter.Label(frame3, text="Au spectre n° :")
text9.grid(row=1, column=0)
text10.grid(row=1, column=2)

variable9=tkinter.IntVar(value=0)
variable10=tkinter.IntVar(value=0)
entree9=tkinter.Spinbox(frame3,from_=0, to=100, textvariable=variable9, command=retro_action_entree10)
entree10=tkinter.Spinbox(frame3,from_=0, to=100, textvariable=variable10, command=retro_action_entree9)
entree9.grid(row=1, column=1)
entree10.grid(row=1, column=3)

bouton_extraction=tkinter.Button(frame3, text="Extraction", command=creation_spectre_moyen)
bouton_extraction.grid(row=1, column=4)

###############################################################################
# 12- Interface graphique : gestion du redimentionnement de la fenêtre principale
###############################################################################
canevas_scroll.create_window(0, 0, anchor='nw', window=frame_scroll)
frame_scroll.update_idletasks()
canevas_scroll.config(scrollregion=canevas_scroll.bbox("all"))

###############################################################################
# 13- Interface graphique : gestion de évènements
###############################################################################
canevas1.bind("<Button-1>", coordonnees1)
canevas2.bind("<Button-1>", coordonnees2)

entree1.bind("<Return>", deplace_ligne0_1_return)
entree2.bind("<Return>", deplace_ligne0_2_return)
entree3.bind("<Return>", deplace_ligne0_3_return)
entree4.bind("<Return>", deplace_ligne0_4_return)

entree5.bind("<Return>", vars_5_6_to_coord1_return)
entree6.bind("<Return>", vars_5_6_to_coord1_return)
entree7.bind("<Return>", vars_7_8_to_coord2_return)
entree8.bind("<Return>", vars_7_8_to_coord2_return)

entree9.bind("<Return>", change_entree9)
entree10.bind("<Return>", change_entree10)

fenetre.mainloop()