#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 11:51:24 2020

@author: yannick
"""

import tkinter as tk
import tkinter.font as font
import pandas as pd


taille_case = [3,2]


class case_classification(tk.Button) :
    def __init__(self, boss, nom, symbole,  Z, ligne, colonne, couleur):
        texte="    "+str(Z)+"\n"+symbole
        tk.Button.__init__(self, boss, text=texte, bg=couleur, command=lambda : self.affiche_pics(nom, symbole,Z,couleur))
        self.configure(width=taille_case[0], height=taille_case[1])
        #self.config(fonte=font.Font(size=8,weight="bold"))
        self.grid(row=ligne, column=colonne)

    def affiche_pics(self,nom, symbole,Z,couleur):
#        print(nom)
        texte="     "+str(Z)+"\n"+symbole
        bouton_affichage.configure(text=texte, bg=couleur)
        bouton_affichage.config(fonte=font.Font(size=10 , weight="bold"))


def lit_tableau_periodique() :
    DataFrame_tableau_periodique= pd.read_table("./LIBStick_classification.tsv")
    return DataFrame_tableau_periodique

def affiche_tableau_periodique(DataFrame_tableau_periodique):
    for ligne_tableau in DataFrame_tableau_periodique.itertuples() :
        Z=ligne_tableau[1]
        symbole=ligne_tableau[2]
        nom=ligne_tableau[3]
        ligne=ligne_tableau[5]
        colonne=ligne_tableau[6]
        couleur=ligne_tableau[8]
        bouton = case_classification(frame1, nom, symbole,  Z, ligne, colonne, couleur)


fenetre=tk.Tk()
frame1=tk.Frame(fenetre, bg="linen")
frame1.pack()

DataFrame_tableau_periodique=lit_tableau_periodique()
#print(DataFrame_tableau_periodique)
#print (DataFrame_tableau_periodique.shape)
affiche_tableau_periodique(DataFrame_tableau_periodique)

bouton_affichage=tk.Button(frame1, width=taille_case[0]*2, height=taille_case[1]*2)
bouton_affichage.grid(row=1, column=7, rowspan=3, columnspan=2)
