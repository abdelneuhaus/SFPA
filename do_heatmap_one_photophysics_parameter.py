from utils import read_poca_files
from get_length_on_off import get_length_off, get_length_on

import os
import csv 
import seaborn as sns
import numpy as np
import statistics
import matplotlib.pyplot as plt
import math 

import numpy as np 
from pandas import DataFrame
import seaborn as sns


def pad_list(lst):
    while len(lst) < 8:
        lst.append(float('nan'))
    return lst

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

def fusion(liste1, liste2):
    fusions = []
    for mot1 in liste1:
        for mot2 in liste2:
            fusions.append(mot1 + mot2)
    return fusions

def fusion_position(liste1, liste2):
    resultat = []
    for i in range(len(liste1)):
        resultat.append(liste1[i] + ': ' + liste2[i])
    return resultat

def photon_calculation(liste, sigma=1):
    exp_liste = []
    for valeur in liste:
        exp_liste.append(valeur*0.04/0.95)
    return exp_liste


def loc_prec_calculation(sigma, photon_loc):
    otp = []
    for i in range(len(sigma)):
        otp.append(float(sigma[i]*160/(math.sqrt(photon_loc[i]))))
    return otp  


def do_heatmap_one_photophysics_parameter(exp, index, list_of_poca_files, list_of_frame_csv, list_of_int_csv, list_of_sigma_csv,
                                          isPT=True, stats=statistics.median, drop_one_event=False):
    csv_frame_label  = ['ON times', "OFF times"]
    csv_int_label =  "Intensity_loc"
    csv_sigma_label = "Loc_Precision"
    
    idx = ['1', '2', '3', '4']
    cols = ['A', 'B']
    all_wells = fusion(cols, idx)
    
    for i in index:
        heatmap_data = []
        # Case where index is 'ON times' or 'OFF times'
        if i in csv_frame_label:
            if i == 'ON times':
                for f in range(len(list_of_frame_csv)):
                    heatmap_data.append(int(stats(pre_process_on_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event))))
            else:
                for f in range(len(list_of_frame_csv)):
                    heatmap_data.append(int(stats(pre_process_off_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event))))
        
        # Case where index is 'intensity per loc'
        elif i == csv_int_label:
            for f in range(len(list_of_int_csv)):
                heatmap_data.append(int(stats(photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event)))))
         
        # Case where we compute localization precision       
        elif i == csv_sigma_label:
            for f in range(len(list_of_sigma_csv)):
                heatmap_data.append(float(stats(loc_prec_calculation(pre_process_sigma(list_of_sigma_csv[f], on_filter=drop_one_event), photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event))))))
        
        # Case where we read from locPALMTracer_cleaned file
        else:
            for f in range(len(list_of_poca_files)):
                raw_file_poca = read_poca_files(list_of_poca_files[f])
                if drop_one_event == True:
                    init = len(raw_file_poca)
                    raw_file_poca = raw_file_poca[raw_file_poca['total ON'] > 1]
                    post = len(raw_file_poca)
                    print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%')
                if i == 'intensity':
                    heatmap_data.append(int(stats(photon_calculation((raw_file_poca.loc[:, i].values.tolist())))))
                else:
                    heatmap_data.append(int(stats(raw_file_poca.loc[:, i].values.tolist())))
        
        # We initialize well names
        well_name = []
        if isPT == True:
            for d in range(len(list_of_poca_files)):
                name = get_num_fov_idx_results_dir(list_of_poca_files[d],'/561.PT/locPALMTracer_cleaned.txt', '/561-405.PT/locPALMTracer_cleaned.txt')
                well_name.append(name)
            legend = fusion_position(all_wells, well_name)
        else:
            legend = list()
            for d in list_of_poca_files:
                legend.append(os.path.basename(os.path.normpath(d.replace('.PT/locPALMTracer_cleaned.txt', ''))))
            heatmap_data = pad_list(heatmap_data)

        # Rotation of the 8x1 data to 2x4 and plot it on the heatmap
        df = DataFrame(np.array(heatmap_data).reshape(2,4), index=cols, columns=idx)
        sns.heatmap(df, annot=True, fmt='g')
        plt.yticks(rotation=0)

        # Récupération de la position de l'échelle de couleur
        colorbar = plt.gcf().axes[-1]
        colorbar_pos = colorbar.get_position()

        # Ajout de la boîte de texte à droite de l'échelle de couleur
        plt.text(colorbar_pos.x1 + 0.05, colorbar_pos.y1, "\n".join(legend),
                transform=plt.gcf().transFigure, fontsize=10,
                verticalalignment='top', horizontalalignment='left',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.gcf().set_size_inches((12, 5))
        plt.title(i + ' median')        

        # Save figure
        results_dir = os.path.join('results/'+exp+'/')

        sample_file = i+'.pdf'
        sample_file = sample_file.replace('.PT', '')
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir+sample_file)
        plt.close('all')
