from utils import read_poca_files
from get_length_on_off import get_length_off, get_length_on

import matplotlib.pyplot as plt
import csv
import os
import statistics
import math


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
            tmp.append(line)
    return [j for i in tmp for j in i]

def pre_process_off_frame_csv(file, on_filter=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if len(line) != 1:
                tmp.append(get_length_off(line))
        else:
            tmp.append(line)
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
        exp_liste.append(int(valeur/(math.sqrt(2*math.pi))))
    return exp_liste


def loc_prec_calculation(sigma, photon_loc):
    otp = []
    for i in range(len(sigma)):
        otp.append(float(sigma[i]/(math.sqrt(photon_loc[i]))))
    return otp    


# Define helper function
def get_num_fov_idx_results_dir(i, exp, PT_561, PT_405):
    if 'FOV' in i and PT_561 in i:
        num_fov = os.path.basename(os.path.normpath(i.replace(PT_561, '')))
        idx = os.path.basename(os.path.normpath(i.replace(num_fov + PT_561, '')))
        results_dir = os.path.join('results', exp, idx, num_fov)
        title_plot = os.path.join(idx, num_fov)
        
    elif 'FOV' in i and PT_405 in i:
        num_fov = os.path.basename(os.path.normpath(i.replace(PT_405, '')))
        idx = os.path.basename(os.path.normpath(i.replace(num_fov + PT_405, '')))
        results_dir = os.path.join('results', exp, idx, num_fov)
        title_plot = os.path.join(idx, num_fov)

    elif PT_561 in i:
        idx = os.path.basename(os.path.normpath(i.replace(PT_561, '')))
        results_dir = os.path.join('results', exp, idx)
        title_plot = os.path.join(idx)

    elif PT_405 in i:
        idx = os.path.basename(os.path.normpath(i.replace(PT_405, '')))
        results_dir = os.path.join('results', exp, idx)
        title_plot = os.path.join(idx)
    return results_dir, title_plot


def do_photophysics_parameters_plotting(list_of_poca_files, list_of_frame_csv, list_of_int_csv, list_of_sigma_csv, exp=None, isPT=True,
                                        on_times=True, off_times=True, total_on=True, num_blinks=True,
                                        phot_per_loc=True, phot_per_cluster=True, num_on_times=True, 
                                        num_off_times=True, sigma=True, drop_one_event=False):
    for j in list_of_frame_csv:
        # length of each ON time
        _on_times = pre_process_on_frame_csv(j, on_filter=drop_one_event) if on_times else None
        # length of each OFF time
        _off_times = pre_process_off_frame_csv(j, on_filter=drop_one_event) if off_times else None
    
    tmp_pho_loc = list()
    for k in list_of_int_csv:
        # photon per localization
        _phot_per_loc = photon_calculation(pre_process_single_intensity(k, on_filter=drop_one_event)) if phot_per_loc else None
        tmp_pho_loc.append(pre_process_single_intensity(k, on_filter=drop_one_event))
        
    for i in list_of_poca_files:
        raw_file_poca = read_poca_files(i)
        if drop_one_event == True:
            init = len(raw_file_poca)
            raw_file_poca = raw_file_poca[raw_file_poca['total ON'] > 1]
            post = len(raw_file_poca)
            print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%')
        # = bleachtime or total ON in frame number
        _total_on = raw_file_poca.loc[:, 'total ON'].values.tolist() if total_on else None
        # num blinks
        _num_blinks = raw_file_poca.loc[:, 'blinks'].values.tolist() if num_blinks else None
        # photon per cluster
        _phot_per_cluster = photon_calculation(raw_file_poca.loc[:, 'intensity'].values.tolist()) if phot_per_cluster else None
        # number of ON times per cluster
        _num_on_times = raw_file_poca.loc[:, '# seq ON'].values.tolist() if num_on_times else None
        # number of OFF times per cluster
        _num_off_times = raw_file_poca.loc[:, '# seq OFF'].values.tolist() if num_off_times else None

    cpt = 0
    for h in list_of_sigma_csv:
        _sigma = loc_prec_calculation(pre_process_sigma(h, on_filter=drop_one_event), tmp_pho_loc[cpt]) if sigma else None
        cpt += 1
        

    for i in list_of_poca_files:
        # imprime les éléments qui ne sont pas égaux à None
        non_none_elements = [_on_times, _off_times, _total_on, _num_blinks, _phot_per_loc, _phot_per_cluster, _num_on_times, _num_off_times, _sigma]
        non_none_elements = [elem for elem in non_none_elements if elem is not None]
        label = ['ON times', "OFF times", "Total ON (Bleachtime)", "#Blinks", "Photon/loc", "Photon/cluster", "#ON times", "#OFF times", "Loc. Precision"]
        
        fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(15,8))
        plt.subplots_adjust(wspace=0.3, hspace=0.5)
        for m, df in enumerate(non_none_elements):
            row = m // 4
            col = m % 4
            ax = axes[row][col]
            ax.set_title(label[m]+', median:'+ str(statistics.median((df))))
            ax.boxplot(df, showfliers=False)
            # ax.hist(df, bins=50)
            
        # Si pas PT experiment (pas de 561-405) et que le nom du PT est le nom du dossier (dossier -> dossier.PT)
        title_plot = os.path.basename(os.path.normpath(i.replace('.PT/locPALMTracer_cleaned.txt', '')))
        results_dir = os.path.join('results/'+exp+'/'+title_plot+'/')
        plt.suptitle(title_plot, fontsize=14)

        if isPT == True:
            PT_405 = '/561-405.PT/locPALMTracer_cleaned.txt'
            PT_561 = '/561.PT/locPALMTracer_cleaned.txt'
            results_dir, title_plot = get_num_fov_idx_results_dir(i, exp, PT_561, PT_405)
            plt.suptitle(title_plot, fontsize=14)
        
        sample_file = '/photophysics_plots.pdf'
        sample_file = sample_file.replace('.PT', '')
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir+sample_file)
        plt.close('all')


# from scipy.stats import mannwhitneyu
# mannwhitney = mannwhitneyu(phot_per_mol[0], phot_per_mol[1])
# print(mannwhitney)