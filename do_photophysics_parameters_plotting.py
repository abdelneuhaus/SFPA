from utils import read_poca_files, get_poca_files, get_csv_poca_frame_files, get_csv_poca_intensity_files, read_csv_poca
from get_length_on_off import get_length_off, get_length_on
import matplotlib.pyplot as plt
import pandas as pd
import csv
import os


def lire_csv(nom_fichier):
    lignes = []
    with open(nom_fichier, 'r') as f:
        lecteur = csv.reader(f)
        for ligne in lecteur:
            # Convertir chaque élément de la ligne en entier (integer)
            ligne = [float(element) for element in ligne]
            lignes.append(ligne)
    return lignes


def pre_process_on_frame_csv(file):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        tmp.append(get_length_on(line))
    return [j for i in tmp for j in i]


def pre_process_off_frame_csv(file):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        tmp.append(get_length_off(line))
    return [j for i in tmp for j in i]


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



def pre_process_single_intensity(file):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        tmp.append(line)
    return [j for i in tmp for j in i]


def do_photophysics_parameters_plotting(list_of_poca_files, list_of_frame_csv, list_of_int_csv, exp=None, isPT=True,
                                        on_times=True, off_times=True, total_on=True, num_blinks=True,
                                        phot_per_loc=True, phot_per_cluster=True, num_on_times=True, 
                                        num_off_times=True):
    for j in list_of_frame_csv:
        # length of each ON time
        _on_times = pre_process_on_frame_csv(j) if on_times else None
        # length of each OFF time
        _off_times = pre_process_off_frame_csv(j) if off_times else None
    
    for k in list_of_int_csv:
        # photon per localization
        _phot_per_loc = pre_process_single_intensity(k) if phot_per_loc else None
    
    for i in list_of_poca_files:
        raw_file_poca = read_poca_files(i)
        # = bleachtime or total ON in frame number
        _total_on = raw_file_poca.loc[:, 'total ON'].values.tolist() if total_on else None
        # num blinks
        _num_blinks = raw_file_poca.loc[:, 'blinks'].values.tolist() if num_blinks else None
        # photon per cluster
        _phot_per_cluster = raw_file_poca.loc[:, 'intensity'].values.tolist() if phot_per_cluster else None
        # number of ON times per cluster
        _num_on_times = raw_file_poca.loc[:, '# seq ON'].values.tolist() if num_on_times else None
        # number of OFF times per cluster
        _num_off_times = raw_file_poca.loc[:, '# seq OFF'].values.tolist() if num_off_times else None


        # imprime les éléments qui ne sont pas égaux à None
        non_none_elements = [_on_times, _off_times, _total_on, _num_blinks, _phot_per_loc, _phot_per_cluster, _num_on_times, _num_off_times]
        non_none_elements = [elem for elem in non_none_elements if elem is not None]
        label = ['ON times', "OFF times", "Total ON (Bleachtime)", "#Blinks", "Photon/loc", "Photon/cluster", "#ON times", "#OFF times"]
        
        fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(15,8))
        plt.subplots_adjust(wspace=0.3, hspace=0.5)
        for m, df in enumerate(non_none_elements):
            row = m // 4
            col = m % 4
            ax = axes[row][col]
            ax.set_title(label[m])
            pd.DataFrame(df).boxplot(ax=ax)
            ax.grid(visible=None)
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