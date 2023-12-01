from utils import read_poca_files
from preprocessing import pre_process_off_frame_csv, pre_process_on_frame_csv, pre_process_sigma, pre_process_single_intensity, get_num_fov_idx_results_dir
from localization_precision import localization_precision

import os
import seaborn as sns
import pandas as pd
import numpy as np
import statistics
import matplotlib.pyplot as plt
import numpy as np
import re

from collections import defaultdict

def pad_list(lst):
    while len(lst) < 8:
        lst.append(float('nan'))
    return lst


def fusion(liste1, liste2):
    fusions = []
    for mot1 in liste1:
        for mot2 in liste2:
            fusions.append(mot1 + mot2)
    return fusions

def fusion_position(liste1, liste2):
    resultat = []
    for i in range(len(liste2)):
        resultat.append(liste1[i] + ': ' + liste2[i])
    return resultat

def photon_calculation(liste, gain=3.6, emgain=300, qe=0.95):
    exp_liste = []
    otp = gain/emgain
    for valeur in liste:
        exp_liste.append(valeur*otp/qe)
    return exp_liste


def loc_prec_calculation(sigma, photon_loc):
    otp = []
    median = statistics.median(sigma)
    for i in range(len(sigma)):
        otp.append(localization_precision(photon_loc[i], sigma[i], median=median))
    return otp  


def creer_matrice_et_moyennes(noms_fichiers, valeurs, positions):
    # Initialiser une matrice avec des valeurs par défaut (par exemple, None)
    matrice_puits = np.full((len(positions),), float('nan'))
    valeurs_par_position = defaultdict(list)
    for nom_fichier, valeur in zip(noms_fichiers, valeurs):
        match = re.search(r'([A-Z]\d+)', nom_fichier)
        if match:
            position = match.group(1)
            valeurs_par_position[position].append(valeur)

    for i, position in enumerate(positions):
        if position in valeurs_par_position:
            moyenne = sum(valeurs_par_position[position]) / len(valeurs_par_position[position])
            matrice_puits[i] = int(moyenne)

    return matrice_puits


# Fonction pour convertir les coordonnées de la plaque (ex: A1) en indices de matrice (ex: (0, 0))
def convertir_coordonnees(coordonnees):
    colonne = ord(coordonnees[0]) - ord('A')
    ligne = int(coordonnees[1:]) - 1
    return ligne, colonne



def do_96heatmap_one_photophysics_parameter(exp, index, list_of_poca_files, list_of_frame_csv, list_of_int_csv, list_of_sigma_csv,
                                          isPT=True, stats=statistics.median, drop_one_event=False, drop_beads=False, 
                                          get_boxplot=False):
    csv_frame_label  = ['ON times', "OFF times"]
    csv_int_label =  "Intensity_loc"
    csv_sigma_label = "Loc_Precision"
    
    idx = list(map(str, range(1, 13)))
    cols = list(map(str, [chr(i) for i in range(ord('A'), ord('H')+1)]))
    all_wells = fusion(cols, idx)

    for i in index:
        heatmap_data = []
        boxplot_data = []
        blink_frequency = []
        # Case where index is 'ON times' or 'OFF times'
        if i in csv_frame_label:
            if i == 'ON times':
                for f in range(len(list_of_frame_csv)):
                    heatmap_data.append(int(stats(pre_process_on_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event))))
                    boxplot_data.append(pre_process_on_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event))
            else:
                for f in range(len(list_of_frame_csv)):
                    heatmap_data.append(int(stats(pre_process_off_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event))))
                    boxplot_data.append(pre_process_off_frame_csv(list_of_frame_csv[f], on_filter=drop_one_event))
        # Case where index is 'intensity per loc'
        elif i == csv_int_label:
            for f in range(len(list_of_int_csv)):
                heatmap_data.append(int(stats(photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event, beads=drop_beads)))))
                boxplot_data.append(photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event, beads=drop_beads)))
        # Case where we compute localization precision       
        elif i == csv_sigma_label:
            for f in range(len(list_of_sigma_csv)):
                heatmap_data.append(float(stats(loc_prec_calculation(pre_process_sigma(list_of_sigma_csv[f], on_filter=drop_one_event), photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event))))))
                boxplot_data.append(loc_prec_calculation(pre_process_sigma(list_of_sigma_csv[f], on_filter=drop_one_event), photon_calculation(pre_process_single_intensity(list_of_int_csv[f], on_filter=drop_one_event))))
        # Case where we read from locPALMTracer_cleaned file
        else:
            for f in range(len(list_of_poca_files)):
                raw_file_poca = read_poca_files(list_of_poca_files[f])
                if drop_one_event == True:
                    init = len(raw_file_poca)
                    raw_file_poca = raw_file_poca[raw_file_poca['total ON'] > 1]
                    post = len(raw_file_poca)
                    print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%')
                if drop_beads == True:
                    raw_file_poca = raw_file_poca[raw_file_poca['total ON'] < max(raw_file_poca['total ON'])*0.6]
                if i == 'intensity':
                    heatmap_data.append(int(stats(photon_calculation((raw_file_poca.loc[:, i].values.tolist())))))
                    boxplot_data.append(photon_calculation((raw_file_poca.loc[:, i].values.tolist())))
                else:
                    heatmap_data.append(int(stats(raw_file_poca.loc[:, i].values.tolist())))
                    boxplot_data.append(raw_file_poca.loc[:, i].values.tolist())
    duty_cycle = []
    if get_boxplot == True:
        for f in range(len(list_of_poca_files)):
            raw_file_poca = read_poca_files(list_of_poca_files[f])
            duty_cycle.append(np.array(raw_file_poca.loc[:, 'total ON'])/np.array(raw_file_poca.loc[:, 'lifetime']))
            
        # We initialize well names
        well_name = []
        if isPT == True:
            for d in range(len(list_of_poca_files)):
                name = get_num_fov_idx_results_dir(list_of_poca_files[d],'/561.PT/locPALMTracer_cleaned.txt', '/561-405.PT/locPALMTracer_cleaned.txt')
                well_name.append(name)
        else:
            for d in list_of_poca_files:
                well_name.append(os.path.basename(os.path.normpath(d.replace('.PT/locPALMTracer_cleaned.txt', ''))))
        
        
        matrice_resultante = creer_matrice_et_moyennes(list_of_poca_files, heatmap_data, all_wells)
        df = pd.DataFrame(np.array(matrice_resultante).reshape(8,12), index=cols, columns=idx)
        sns.heatmap(df, annot=True, fmt='g', cmap="YlGnBu", linewidths=1, linecolor='black')
        plt.yticks(rotation=0)

        plt.gcf().set_size_inches((12, 5))
        plt.title(i + ' median')        

        # Save figure
        results_dir = os.path.join('results/'+exp+'/')

        sample_file = i+'.pdf'
        sample_file = sample_file.replace('.PT', '')
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir+sample_file)
        
        fig, ax = plt.subplots()
        boxplot = ax.boxplot(boxplot_data, showfliers=False)
        ax.set_xticklabels(well_name)
        plt.title(i + ' boxplots (no outliers)')        
        plt.show()
        
        fig, ax = plt.subplots()
        boxplot = ax.boxplot(duty_cycle, showfliers=False)
        # ax.set_xticklabels(well_name)
        plt.title('duty cycle boxplots (no outliers)')        
        plt.show()
        # all_values = np.concatenate([values for values in boxplot_data])
        # group_labels = np.concatenate([np.full(len(values), i) for i, values in enumerate(boxplot_data)])
        # f_statistic, p_value = f_oneway(*list(boxplot_data))
        # print(f'ANOVA p-value: {p_value}')
        # tukey_results = pairwise_tukeyhsd(all_values, group_labels)
        # print(tukey_results)
        
        plt.close('all')
