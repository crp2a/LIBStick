#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 09:34:25 2020

@author: yannick
"""

import numpy, pandas
#import os
import matplotlib.pyplot as plt
import sklearn.decomposition
#import sklearn.preprocessing
#from fanalysis.pca import PCA


def tableau_centre_reduit(tableau) :
    moyennes=numpy.mean(tableau, axis=0)
    sigmas=numpy.std(tableau, axis=0, ddof=0)
    tableau_centre_reduit= (tableau-moyennes)/sigmas
    return tableau_centre_reduit


def calcul_ACP_sklearn (dataframe,dim1, dim2,flag_centre_reduit, flag_echelle, flag_eboulis):
    tableau=dataframe.values
    nbr_spectres = tableau.shape[0]
    nbr_variables = tableau.shape[1]
    
    if flag_centre_reduit==True :
        tableau=tableau_centre_reduit(tableau)
    
    acp=sklearn.decomposition.PCA(n_components=20)
    donnees_ACP=acp.fit(tableau)
    
#    print("components_ : \n" )
#    print(donnees_ACP.components_)
#    print("explained_variance_ : \n" )
#    print(donnees_ACP.explained_variance_)
#    print("explained_variance_ratio_ : \n")
#    print(donnees_ACP.explained_variance_ratio_)
#    print("singular_values_ : \n")
#    print(donnees_ACP.singular_values_)
    
#    tableau_ACP=acp.fit_transform(tableau)
    tableau_ACP=acp.transform(tableau)
    
    if flag_eboulis == True :
        variables_explicatives_proportion = donnees_ACP.explained_variance_ratio_*100
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5,5))
        fig.set_tight_layout(True)
        ax1.plot(variables_explicatives_proportion,'-o', label="Variance expliquée %")
        ax1.plot(numpy.cumsum(variables_explicatives_proportion),'-o', label = 'Variance cumulée %')
        ax1.set_xlabel("Composantes Principales")
        ax1.set_title("Diagramme d'éboulis")
        plt.legend()
    
    min_tableau_acp=numpy.min(tableau_ACP, axis=0)
    max_tableau_acp=numpy.max(tableau_ACP, axis=0)
    min_dim1=min_tableau_acp[dim1-1]*1.05
    max_dim1=max_tableau_acp[dim1-1]*1.05
    min_dim2=min_tableau_acp[dim2-1]*1.05
    max_dim2=max_tableau_acp[dim2-1]*1.05
    
    fig, ax = plt.subplots(figsize=(5,5))
    ax.plot (tableau_ACP[:,dim1-1], tableau_ACP[:,dim2-1], color="xkcd:light blue", marker="o", linestyle="None")
    if flag_echelle == True :
        min_dim= min(min_dim1,min_dim2)
        max_dim= max(max_dim1,max_dim2)
        ax.axis([min_dim,max_dim,min_dim,max_dim])
        ax.plot([min_dim,max_dim],[0,0], color="silver", linestyle="--")
        ax.plot([0,0],[min_dim,max_dim], color="silver", linestyle="--")
    else :
        ax.axis([min_dim1,max_dim1,min_dim2,max_dim2])
        ax.plot([min_dim1,max_dim1],[0,0], color="silver", linestyle="--")
        ax.plot([0,0],[min_dim2,max_dim2], color="silver", linestyle="--")
#    lambada=numpy.mean(numpy.power(tableau_ACP,2), axis=0)
#    inerties=100*lambada/numpy.sum(lambada)
    inerties=donnees_ACP.explained_variance_ratio_*100
    ax.set_xlabel("F"+str(dim1) +"( %.2f" %inerties[dim1-1] + " %)")
    ax.set_ylabel("F"+str(dim2) +"( %.2f" %inerties[dim2-1] + " %)")
    n=tableau_ACP.shape[0]
    for i in range(n) :
        ax.text(tableau_ACP[i,dim1-1], tableau_ACP[i,dim2-1], dataframe.index[i])   
    plt.show(block=False)
    
#    dataframe_variables=pandas.DataFrame(donnees_ACP.components_, columns=dataframe.columns)
#    dataframe_variables.to_csv("dataframe_variables", decimal=".", sep="\t")
#    
#    valeurs_propres_corrigees = donnees_ACP.explained_variance_ * (nbr_spectres-1)/nbr_spectres
#    sqrt_valeurs_propres_corrigees = numpy.sqrt(valeurs_propres_corrigees)
#    variables_explicatives_corrigees = numpy.zeros((20,nbr_variables))
#    for i in range(20) :
#        variables_explicatives_corrigees[i,:] = donnees_ACP.components_[i,:] * sqrt_valeurs_propres_corrigees[i]
#    dataframe_variables_2=pandas.DataFrame(variables_explicatives_corrigees, columns=dataframe.columns)
#    dataframe_variables_2.to_csv("dataframe_variables_2", decimal=".", sep="\t")
    
    return donnees_ACP



#def calcul_ACP (dataframe,dim1, dim2, flag_centre_reduit, flag_echelle, flag_eboulis, flag_calcul) :
#    if flag_calcul == True :
#        donnees_ACP=calcul_ACP_fanalysis(dataframe,dim1, dim2,flag_centre_reduit)
#    else :
#        donnees_ACP=calcul_ACP_sklearn (dataframe,dim1, dim2,flag_centre_reduit, flag_echelle, flag_eboulis)
#    return donnees_ACP

#def calcul_ACP_fanalysis (dataframe,dim1, dim2, flag_centre_reduit) :
##    p=dataframe.shape[1]   #nbre de variable en colonnes
##    n=dataframe.shape[0]   #nbre d'observation en lignes
#    tableau=dataframe.values     #matrice des valeurs de D
#    
#    if flag_centre_reduit==True :
#        tableau=tableau_centre_reduit(tableau)
#        
#    tableau_ACP=PCA(std_unit=False, row_labels=dataframe.index, col_labels=dataframe.columns) #si std_unit=True => ACP normée
#    tableau_ACP.fit(tableau)
#    tableau_ACP.mapping_row(num_x_axis=dim1, num_y_axis=dim2,figsize=(5,5))   