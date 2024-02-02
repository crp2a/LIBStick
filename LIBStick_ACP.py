#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 09:34:25 2020
Module outils pour l'ACP
@author: yannick
"""


import pickle as pk
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import sklearn.decomposition
#import sklearn.preprocessing
#from fanalysis.pca import PCA
import gettext
_ = gettext.gettext


###################################################################################################
# fonctions de sauvegarde et lecture d'ACP
###################################################################################################
def enregistre_ACP(modele_ACP, rep_travail):
    """
    Enregistre le calcul d'ACP. Non encore utilisé
    """
    print(rep_travail)
    pk.dump(modele_ACP, open(rep_travail+"\\ACP_modele.pkl", "wb"))


def ouvre_ACP(rep_travail):
    """
    Ouvre un calcul d'ACP. Non encore utilisé
    """
    modele_ACP = pk.load(open(rep_travail+"\\ACP_modele.pkl", "rb"))
    return modele_ACP


###################################################################################################
# fonctions d'affichage d'ACP
###################################################################################################
def affiche_ACP(treeview_dataframe, modele_ACP, tableau_ACP, dim,
                flag_3D, flag_echelle, flag_eboulis):
    """
    Affiche les graphes de l'ACP(2D ou 3D, ébouli) dans des fenêtres matplotlib.pyplot,
    uniquement des individus ayant servi au calcul de l'ACP
    """
    # print("-----------------------------------------------")
    # print("treeview_dataframe :")
    # print(treeview_dataframe)
    # print("-----------------------------------------------")
    # print("tableau_ACP :")
    # print(tableau_ACP)
    # print("-----------------------------------------------")
    if flag_3D is True:
        dim1 = dim[0]
        dim2 = dim[1]
        dim3 = dim[2]
    else:
        dim1 = dim[0]
        dim2 = dim[1]

    if flag_eboulis is True:
        variables_explicatives_proportion = modele_ACP.explained_variance_ratio_*100
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
        fig.set_tight_layout(True)
        ax1.plot(variables_explicatives_proportion, '-o', label=_("Variance expliquée %"))
        ax1.plot(np.cumsum(variables_explicatives_proportion),
                 '-o', label=_('Variance cumulée %'))
        ax1.set_xlabel(_("Composantes Principales"))
        ax1.set_title(_("Diagramme d'éboulis"))
        plt.legend()

    min_tableau_acp = np.min(tableau_ACP, axis=0)
    max_tableau_acp = np.max(tableau_ACP, axis=0)
    min_dim1 = min_tableau_acp[dim1-1]*1.05
    max_dim1 = max_tableau_acp[dim1-1]*1.05
    min_dim2 = min_tableau_acp[dim2-1]*1.05
    max_dim2 = max_tableau_acp[dim2-1]*1.05

    inerties = modele_ACP.explained_variance_ratio_*100

    fig_px_matrice = px.scatter_matrix(tableau_ACP, dimensions=range(3),
                                        color=treeview_dataframe.values[:, -1],
                                        opacity=0.5,
                                        hover_name=(treeview_dataframe["nom"]),
                                        labels={"0":str("F1"+ "( %.2f" % inerties[0] + " %)"),
                                                "1":str("F2"+ "( %.2f" % inerties[1] + " %)"),
                                                "2":str("F3"+ "( %.2f" % inerties[2] + " %)")})
    fig_px_matrice.update_traces(diagonal_visible=False)
    fig_px_matrice.show()

    if flag_3D is False:
        fig, ax = plt.subplots(figsize=(5, 5))

        if flag_echelle is True:
            min_dim = min(min_dim1, min_dim2)
            max_dim = max(max_dim1, max_dim2)
            ax.axis([min_dim, max_dim, min_dim, max_dim])
            ax.plot([min_dim, max_dim], [0, 0], color="silver", linestyle="--")
            ax.plot([0, 0], [min_dim, max_dim], color="silver", linestyle="--")
        else:
            ax.axis([min_dim1, max_dim1, min_dim2, max_dim2])
            ax.plot([min_dim1, max_dim1], [0, 0], color="silver", linestyle="--")
            ax.plot([0, 0], [min_dim2, max_dim2], color="silver", linestyle="--")

    #    lambada=np.mean(np.power(tableau_ACP,2), axis=0)
    #    inerties=100*lambada/np.sum(lambada)
        # ax.scatter (tableau_ACP[:,dim1-1], tableau_ACP[:,dim2-1],
        #             color="xkcd:light blue", marker="o", linestyle="None")
        # ax.plot (tableau_ACP[:,dim1-1], tableau_ACP[:,dim2-1],
        #          color="xkcd:light blue", marker="o", linestyle="None")
        label = treeview_dataframe.values[:, -1]

        ax.scatter(tableau_ACP[:, dim1-1], tableau_ACP[:, dim2-1],
                   c=label, marker="o", linestyle="None")
        ax.set_xlabel("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)")
        ax.set_ylabel("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)")
        n = tableau_ACP.shape[0]
        for i in range(n):
            ax.text(tableau_ACP[i, dim1-1], tableau_ACP[i, dim2-1], treeview_dataframe.index[i])
        plt.show(block=False)

        fig_px_scatter = px.scatter(tableau_ACP, x=(dim1-1), y=(dim2-1),
                            color=treeview_dataframe.values[:, -1],
                            symbol=treeview_dataframe.values[:, -2],
                            text=treeview_dataframe.index, opacity=0.5,
                            hover_name=(treeview_dataframe["nom"]),
                            labels={"0":str("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)"),
                                    "1":str("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)")})
        fig_px_scatter.update_traces(marker_size=20)
        fig_px_scatter.show()

    if flag_3D is True:
        fig3d = plt.figure()
        ax3d = fig3d.add_subplot(projection='3d')

        min_dim3 = min_tableau_acp[dim3-1]*1.05
        max_dim3 = max_tableau_acp[dim3-1]*1.05
        if flag_echelle is True:
            min_dim = min(min_dim1, min_dim2, min_dim3)
            max_dim = max(max_dim1, max_dim2, max_dim3)
            ax3d.set_xlim3d([min_dim, max_dim])
            ax3d.set_ylim3d([min_dim, max_dim])
            ax3d.set_zlim3d([min_dim, max_dim])
        else:
            ax3d.set_xlim3d([min_dim1, max_dim1])
            ax3d.set_ylim3d([min_dim2, max_dim2])
            ax3d.set_zlim3d([min_dim3, max_dim3])

        label = treeview_dataframe.values[:, -1]
        ax3d.scatter(tableau_ACP[:, dim1-1], tableau_ACP[:, dim2-1],
                     tableau_ACP[:, dim3-1], c=label, marker="o", linestyle="None")
        ax3d.set_xlabel("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)")
        ax3d.set_ylabel("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)")
        ax3d.set_zlabel("F"+str(dim3) + "( %.2f" % inerties[dim3-1] + " %)")
        n = tableau_ACP.shape[0]
        for i in range(n):
            ax3d.text(tableau_ACP[i, dim1-1], tableau_ACP[i, dim2-1],
                      tableau_ACP[i, dim3-1], treeview_dataframe.index[i])
        plt.show(block=False)

        fig_px3D = px.scatter_3d(tableau_ACP,  x=(dim1-1), y=(dim2-1), z=(dim3-1),
                                  color=treeview_dataframe.values[:, -1],
                                  symbol=treeview_dataframe.values[:, -2],
                                  text=treeview_dataframe.index, opacity=0.5,
                                  hover_name=(treeview_dataframe["nom"]),
                                  labels={"0":str("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)"),
                                          "1":str("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)"),
                                          "2":str("F"+str(dim3) + "( %.2f" % inerties[dim3-1] + " %)")})
        fig_px3D.update_traces(marker_size=10)
        fig_px3D.show()


def affiche_ACP_ind_supp(treeview_dataframe_individus_supp, treeview_dataframe,
                         modele_ACP, tableau_ACP, tableau_ACP_individus_supp,
                         dim, flag_3D, flag_echelle, flag_eboulis):
    """
    Affiche les graphes de l'ACP(2D ou 3D, ébouli) dans des fenêtres matplotlib.pyplot,
    avec les individus supplémentaires n'ayant pas servi au calcul de l'ACP, calculé au préalable
    """
    # print("-----------------------------------------------")
    # print("treeview_dataframe :")
    # print(treeview_dataframe)
    # print("-----------------------------------------------")
    # print("-----------------------------------------------")
    # print("treeview_dataframe_individus_supp :")
    # print(treeview_dataframe_individus_supp)
    # print("-----------------------------------------------")

    tableau_complet = np.concatenate([tableau_ACP,tableau_ACP_individus_supp])
    dataframe_complet = pd.concat([treeview_dataframe,treeview_dataframe_individus_supp])

    if flag_3D is True:
        dim1 = dim[0]
        dim2 = dim[1]
        dim3 = dim[2]
    else:
        dim1 = dim[0]
        dim2 = dim[1]

    if flag_eboulis is True:
        variables_explicatives_proportion = modele_ACP.explained_variance_ratio_*100
        fig, ax1 = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
        fig.set_tight_layout(True)
        ax1.plot(variables_explicatives_proportion, '-o', label="Variance expliquée %")
        ax1.plot(np.cumsum(variables_explicatives_proportion), '-o', label='Variance cumulée %')
        ax1.set_xlabel("Composantes Principales")
        ax1.set_title("Diagramme d'éboulis")
        plt.legend()

    # min_tableau_acp = np.min(tableau_ACP, axis=0)
    # max_tableau_acp = np.max(tableau_ACP, axis=0)
    # min_tableau_acp_ind_supp = np.min(tableau_ACP_individus_supp, axis=0)
    # max_tableau_acp_ind_sup = np.max(tableau_ACP_individus_supp, axis=0)
    min_tableau_acp = np.min(tableau_complet, axis=0)
    max_tableau_acp = np.max(tableau_complet, axis=0)

    min_dim1 = min_tableau_acp[dim1-1]*1.05
    max_dim1 = max_tableau_acp[dim1-1]*1.05
    min_dim2 = min_tableau_acp[dim2-1]*1.05
    max_dim2 = max_tableau_acp[dim2-1]*1.05

    # min_dim1_ind_supp = min_tableau_acp_ind_supp[dim1-1]*1.05
    # max_dim1_ind_supp = max_tableau_acp_ind_sup[dim1-1]*1.05
    # min_dim2_ind_supp = min_tableau_acp_ind_supp[dim2-1]*1.05
    # max_dim2_ind_supp = max_tableau_acp_ind_sup[dim2-1]*1.05

    inerties = modele_ACP.explained_variance_ratio_*100

    if flag_3D is False:
        fig, ax = plt.subplots(figsize=(5, 5))

        if flag_echelle is True:
            # min_dim = min(min_dim1, min_dim2, min_dim1_ind_supp, min_dim2_ind_supp)
            # max_dim = max(max_dim1, max_dim2, max_dim1_ind_supp, max_dim2_ind_supp)
            min_dim = min(min_dim1, min_dim2)
            max_dim = max(max_dim1, max_dim2)
            ax.axis([min_dim, max_dim, min_dim, max_dim])
            ax.plot([min_dim, max_dim], [0, 0], color="silver", linestyle="--")
            ax.plot([0, 0], [min_dim, max_dim], color="silver", linestyle="--")
        else:
            ax.axis([min_dim1, max_dim1, min_dim2, max_dim2])
            ax.plot([min_dim1, max_dim1], [0, 0], color="silver", linestyle="--")
            ax.plot([0, 0], [min_dim2, max_dim2], color="silver", linestyle="--")

        label = treeview_dataframe.values[:, -1]

        ax.scatter(tableau_ACP[:, dim1-1], tableau_ACP[:, dim2-1],
                   c=label, marker="o", linestyle="None")
        ax.scatter(tableau_ACP_individus_supp[:, dim1-1], tableau_ACP_individus_supp[:, dim2-1],
                   color='blue', marker="+", linestyle="None")
        ax.set_xlabel("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)")
        ax.set_ylabel("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)")
        n = tableau_ACP.shape[0]
        print(n)
        for i in range(n):
            ax.text(tableau_ACP[i, dim1-1], tableau_ACP[i, dim2-1], treeview_dataframe.index[i])
        m = tableau_ACP_individus_supp.shape[0]
        print(m)
        for j in range(m):
            ax.text(tableau_ACP_individus_supp[j, dim1-1], tableau_ACP_individus_supp[j, dim2-1],
                    treeview_dataframe_individus_supp.index[j])
        plt.show(block=False)

        # tableau_complet = np.concatenate([tableau_ACP,tableau_ACP_individus_supp])
        # dataframe_complet = pd.concat([treeview_dataframe,treeview_dataframe_individus_supp])
        fig_px_scatter = px.scatter(tableau_complet, x=(dim1-1), y=(dim2-1),
                                    color=dataframe_complet.values[:, -1],
                                    symbol=dataframe_complet.values[:, -2],
                                    text=dataframe_complet.index, opacity=0.5,
                                    hover_name=(dataframe_complet["nom"]),
                                    labels={"0":str("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)"),
                                            "1":str("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)")})
        fig_px_scatter.update_traces(marker_size=20)
        fig_px_scatter.show()

    if flag_3D is True:
        fig3d = plt.figure()
        ax3d = fig3d.add_subplot(projection='3d')

        min_dim3 = min_tableau_acp[dim3-1]*1.05
        max_dim3 = max_tableau_acp[dim3-1]*1.05
        # min_dim3_ind_supp = min_tableau_acp_ind_supp[dim3-1]*1.05
        # max_dim3_ind_supp = max_tableau_acp_ind_sup[dim3-1]*1.05
        if flag_echelle is True:
            # min_dim = min(min_dim1, min_dim2, min_dim3, min_dim1_ind_supp,
            #               min_dim2_ind_supp, min_dim3_ind_supp)
            # max_dim = max(max_dim1, max_dim2, max_dim3, max_dim1_ind_supp,
            #               max_dim2_ind_supp, max_dim3_ind_supp)
            min_dim = min(min_dim1, min_dim2, min_dim3)
            max_dim = max(max_dim1, max_dim2, max_dim3)
            ax3d.set_xlim3d([min_dim, max_dim])
            ax3d.set_ylim3d([min_dim, max_dim])
            ax3d.set_zlim3d([min_dim, max_dim])
        else:
            ax3d.set_xlim3d([min_dim1, max_dim1])
            ax3d.set_ylim3d([min_dim2, max_dim2])
            ax3d.set_zlim3d([min_dim3, max_dim3])

        label = treeview_dataframe.values[:, -1]
        ax3d.scatter(tableau_ACP[:, dim1-1], tableau_ACP[:, dim2-1], tableau_ACP[:, dim3-1],
                     c=label, marker="o", linestyle="None")
        ax3d.scatter(tableau_ACP_individus_supp[:, dim1-1], tableau_ACP_individus_supp[:, dim2-1],
                     tableau_ACP_individus_supp[:, dim3-1],
                     color='blue', marker="+", linestyle="None")
        ax3d.set_xlabel("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)")
        ax3d.set_ylabel("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)")
        ax3d.set_zlabel("F"+str(dim3) + "( %.2f" % inerties[dim3-1] + " %)")
        n = tableau_ACP.shape[0]
        for i in range(n):
            ax3d.text(tableau_ACP[i, dim1-1], tableau_ACP[i, dim2-1], tableau_ACP[i, dim3-1],
                      treeview_dataframe.index[i])
        m = tableau_ACP_individus_supp.shape[0]
        for i in range(m):
            ax3d.text(tableau_ACP_individus_supp[i, dim1-1], tableau_ACP_individus_supp[i, dim2-1],
                      tableau_ACP_individus_supp[i, dim3-1], treeview_dataframe_individus_supp.index[i])
        plt.show(block=False)

        fig_px3D = px.scatter_3d(tableau_complet,  x=(dim1-1), y=(dim2-1), z=(dim3-1),
                                 color=dataframe_complet.values[:, -1],
                                 symbol=dataframe_complet.values[:, -2],
                                 text=dataframe_complet.index, opacity=0.5,
                                 hover_name=(dataframe_complet["nom"]),
                                 labels={"0":str("F"+str(dim1) + "( %.2f" % inerties[dim1-1] + " %)"),
                                         "1":str("F"+str(dim2) + "( %.2f" % inerties[dim2-1] + " %)"),
                                         "2":str("F"+str(dim3) + "( %.2f" % inerties[dim3-1] + " %)")})
        fig_px3D.update_traces(marker_size=10)
        fig_px3D.show()


###################################################################################################
# fonctions de calculs d'ACP par scikit-learn (sklearn)
###################################################################################################
def creation_tableau_centre_reduit(tableau):
    """
    transformation des données en données centrées réduites
    """
    moyennes = np.mean(tableau, axis=0)
    sigmas = np.std(tableau, axis=0, ddof=0)
    tableau_centre_reduit = (tableau-moyennes)/sigmas
    return tableau_centre_reduit


def calcul_ACP_sklearn(tableau, nbr_composantes, flag_centre_reduit):
    """
    Calcul de l'ACP par sklearn.decomposition.PCA
    """
    # if flag_centre_reduit == True:
    if flag_centre_reduit:
        tableau = creation_tableau_centre_reduit(tableau)
    # acp = sklearn.decomposition.PCA(n_components=nbr_composantes, svd_solver="randomized")
    acp = sklearn.decomposition.PCA(n_components=nbr_composantes)
    modele_ACP = acp.fit(tableau)
#    tableau_ACP=modele_acp.fit_transform(tableau)
#    print("components_ : \n" )
#    print(modele_ACP.components_)
#    print("explained_variance_ : \n" )
#    print(modele_ACP.explained_variance_)
#    print("explained_variance_ratio_ : \n")
#    print(modele_ACP.explained_variance_ratio_)
#    print("singular_values_ : \n")
#    print(modele_ACP.singular_values_)
    #tableau_ACP=applique_ACP(modele_ACP, tableau)
    # affiche_ACP(dataframe, treeview_dataframe, modele_ACP, tableau_ACP,
    #             dim, flag_3D, flag_echelle, flag_eboulis)
    return modele_ACP


def applique_ACP(modele_ACP, tableau):
    """
    applique l'ACP préalablement calculée sur le tableau de données
    """
    tableau_ACP = modele_ACP.transform(tableau)
    return tableau_ACP

# def calcul_ICA_sklearn (dataframe,treeview_dataframe, flag_centre_reduit,nbr_composantes):
#     tableau=dataframe.values
#     #nbr_spectres = tableau.shape[0]
#     #nbr_variables = tableau.shape[1]
#     if flag_centre_reduit==True :
#         tableau=creation_tableau_centre_reduit(tableau)
#     ica=sklearn.decomposition.FastICA(n_components=nbr_composantes)
#     donnees_ICA=ica.fit(tableau)
#     return donnees_ICA


###################################################################################################
# fonctions de calculs d'ACP par fanalysis
###################################################################################################
# def calcul_ACP (dataframe,dim1, dim2, flag_centre_reduit, flag_echelle,
#                 flag_eboulis, flag_calcul) :
#     if flag_calcul == True :
#         modele_ACP=calcul_ACP_fanalysis(dataframe,dim1, dim2,flag_centre_reduit)
#     else :
#         modele_ACP=calcul_ACP_sklearn (dataframe,dim1, dim2,flag_centre_reduit,
#                                        flag_echelle, flag_eboulis)
#     return modele_ACP

# def calcul_ACP_fanalysis (dataframe,dim1, dim2, flag_centre_reduit) :
# p=dataframe.shape[1]   #nbre de variable en colonnes
# n=dataframe.shape[0]   #nbre d'observation en lignes
#     tableau=dataframe.values     #matrice des valeurs de D

#     if flag_centre_reduit==True :
#         tableau=creation_tableau_centre_reduit(tableau)

#     tableau_ACP=PCA(std_unit=False, row_labels=dataframe.index,
#                     col_labels=dataframe.columns) #si std_unit=True => ACP normée
#     tableau_ACP.fit(tableau)
#     tableau_ACP.mapping_row(num_x_axis=dim1, num_y_axis=dim2,figsize=(5,5))
