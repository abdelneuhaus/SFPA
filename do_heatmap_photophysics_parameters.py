from utils import read_poca_files
from get_length_on_off import get_length_off, get_length_on

import os
import csv 
import seaborn as sns
import numpy as np
import statistics
import pandas as pd 
import matplotlib.pyplot as plt
import math


def get_num_fov_idx_results_dir(i, PT_561, PT_405):
    if 'FOV' in i and PT_561 in i:
        num_fov = os.path.basename(os.path.normpath(i.replace(PT_561, '')))
        idx = os.path.basename(os.path.normpath(i.replace(num_fov + PT_561, '')))
        title_plot = os.path.join(idx, num_fov)
        
    elif 'FOV' in i and PT_405 in i:
        num_fov = os.path.basename(os.path.normpath(i.replace(PT_405, '')))
        idx = os.path.basename(os.path.normpath(i.replace(num_fov + PT_405, '')))
        title_plot = os.path.join(idx, num_fov)

    elif PT_561 in i:
        idx = os.path.basename(os.path.normpath(i.replace(PT_561, '')))
        title_plot = os.path.join(idx)

    elif PT_405 in i:
        idx = os.path.basename(os.path.normpath(i.replace(PT_405, '')))
        title_plot = os.path.join(idx)

    return title_plot

def lire_csv(nom_fichier):
    lignes = []
    with open(nom_fichier, 'r') as f:
        lecteur = csv.reader(f)
        for ligne in lecteur:
            # Convertir chaque élément de la ligne en entier (integer)
            ligne = [float(element) for element in ligne]
            lignes.append(ligne[1:])
    return lignes

def pre_process_single_intensity(file, on_filter=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if len(line) != 1: 
                tmp.append(line)
        else:
            tmp.append(line)
    return [j for i in tmp for j in i]

def pre_process_on_frame_csv(file, on_filter=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter:
            if (len(line) != 1):
                tmp.append(get_length_on(line))
        else:
            tmp.append(get_length_on(line))
    return [j for i in tmp for j in i]

def pre_process_off_frame_csv(file, on_filter=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if len(line) != 1:
                tmp.append(get_length_off(line))
        else:
            tmp.append(get_length_off(line))
    return [j for i in tmp for j in i]

def pre_process_sigma(file, on_filter=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if len(line) != 1: 
                tmp.append(line)
        else:
            tmp.append(line)
    return [j for i in tmp for j in i]

def photon_calculation(liste, sigma=1):
    exp_liste = []
    # sigma = 1
    for valeur in liste:
        exp_liste.append(valeur*0.04)
    return exp_liste

def loc_prec_calculation(sigma, photon_loc):
    otp = []
    for i in range(len(sigma)):
        otp.append(float(sigma[i]*160/(math.sqrt(photon_loc[i]))))
    return otp  


def do_heatmap_photophysics_parameters(exp, list_of_poca_files, list_of_frame_csv, list_of_int_csv, list_of_sigma_csv, isPT=True, stats=statistics.mean, drop_one_event=False):
    heatmap_data = []
    cpt = 0
    tmp_pho_loc = list()
    for f in range(len(list_of_poca_files)):
        raw_file_poca = read_poca_files(list_of_poca_files[f])
        if drop_one_event == True:
            init = len(raw_file_poca)
            raw_file_poca = raw_file_poca[raw_file_poca['total ON'] > 1]
            post = len(raw_file_poca)
            print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%')
        well_data = dict()
        well_data['_on_times'] = int(stats(pre_process_on_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event)))
        well_data['_off_times'] = int(stats(pre_process_off_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event)))
        tmp = photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event))
        tmp_pho_loc.append(tmp)
        well_data['_phot_per_loc'] = int(stats(photon_calculation(tmp)))
        well_data['_total_on'] = int(stats(raw_file_poca.loc[:, 'total ON'].values.tolist()))
        well_data['_num_blinks'] = int(stats(raw_file_poca.loc[:, 'blinks'].values.tolist()))
        well_data['_phot_per_cluster'] = int(stats(photon_calculation(raw_file_poca.loc[:, 'intensity'].values.tolist())))
        well_data['_num_on_times'] = int(stats(raw_file_poca.loc[:, '# seq ON'].values.tolist()))
        well_data['_num_off_times'] = int(stats(raw_file_poca.loc[:, '# seq OFF'].values.tolist()))
        well_data['_sigma'] = float(stats(loc_prec_calculation(pre_process_sigma(list_of_sigma_csv[f], on_filter=drop_one_event), tmp_pho_loc[cpt])))
        cpt += 1
        heatmap_data.append(well_data)


    # Convert dict to pd.dataframe
    data = []
    if isPT == True:
        for d in range(len(heatmap_data)):
            name = get_num_fov_idx_results_dir(list_of_poca_files[d],'/561.PT/locPALMTracer_cleaned.txt', '/561-405.PT/locPALMTracer_cleaned.txt')
            b=pd.DataFrame.from_dict(heatmap_data[d], orient='index').rename({0:name}, axis='columns')
            data.append(b)
    else:
        name = list()
        for d in range(len(heatmap_data)):
            name = os.path.basename(os.path.normpath(list_of_poca_files[d].replace('.PT/locPALMTracer_cleaned.txt', '')))
            b=pd.DataFrame.from_dict(heatmap_data[d], orient='index').rename({0:name}, axis='columns')
            data.append(b)
            
    # Create figure and convert dataframe to heatmap data
    fig, ax = plt.subplots(figsize=(14, 7))
    heatmap_data = pd.concat(data)
    heatmap_data = heatmap_data.groupby(heatmap_data.index).sum()
    heatmap_data = heatmap_data.replace(np.nan, 0)

    # Normalise les MOYENNES (ON PEUT FAIRE LES MEDIANES) car sinon on a un trop gros écart sur une même plaque
    tab_n = heatmap_data.div(heatmap_data.max(axis=1), axis=0)
    sns.heatmap(tab_n, annot=True)
    # sns.heatmap(heatmap_data, annot=True)

    # Axis
    ax.set_xticks(np.arange(heatmap_data.shape[1])+0.5, minor=False)
    ax.set_yticks(np.arange(heatmap_data.shape[0])+0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    # Columns & Rows labels
    column_labels = heatmap_data.columns
    row_labels = heatmap_data.index
    ax.set_xticklabels(column_labels, minor=False)
    ax.set_yticklabels(row_labels, minor=False)
    
    # Save figure
    results_dir = os.path.join('results/'+exp+'/')
    sample_file = 'experiment_heatmap.pdf'
    sample_file = sample_file.replace('.PT', '')
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    plt.savefig(results_dir+sample_file)
    plt.close('all')
    
