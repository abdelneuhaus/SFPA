from utils import get_poca_files, get_csv_poca_frame_files, get_csv_poca_intensity_files, read_poca_files
from get_length_on_off import get_length_off, get_length_on

import os
import csv 
import seaborn as sns
import numpy as np
import statistics
import pandas as pd 
import matplotlib.pyplot as plt

import numpy as np 
from pandas import DataFrame
import seaborn as sns


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

def pre_process_single_intensity(file):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        tmp.append(line)
    return [j for i in tmp for j in i]

exp = '230227_gradient_data/exp_data/'
list_of_poca_files = get_poca_files(exp)
heatmap_data = []

index = "total ON"
for f in range(len(list_of_poca_files)):
    raw_file_poca = read_poca_files(list_of_poca_files[f])
    heatmap_data.append(int(statistics.mean(raw_file_poca.loc[:, index].values.tolist())))

well_name = []
for d in range(len(list_of_poca_files)):
    name = get_num_fov_idx_results_dir(list_of_poca_files[d],'/561.PT/locPALMTracer_cleaned.txt', '/561-405.PT/locPALMTracer_cleaned.txt')
    well_name.append(name)

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


# Plaque 8 puits, uniquement manuel
idx = ['1', '2', '3', '4']
cols = ['A', 'B']
all_wells = fusion(cols, idx)
legend = fusion_position(all_wells, well_name)

df = DataFrame(np.array(heatmap_data).reshape(2,4), index=cols, columns=idx)

sns.heatmap(df, annot=True, fmt='g')
plt.yticks(rotation=0)

# Récupération de la position de l'échelle de couleur
colorbar = plt.gcf().axes[-1]
colorbar_pos = colorbar.get_position()

# Ajout de la boîte de texte à droite de l'échelle de couleur
boite_texte = plt.text(colorbar_pos.x1 + 0.05, colorbar_pos.y1, "\n".join(legend),
                       transform=plt.gcf().transFigure, fontsize=10,
                       verticalalignment='top', horizontalalignment='left',
                       bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.gcf().set_size_inches((12, 5))
plt.title(index + ' mean')        
plt.show()



# def get_num_fov_idx_results_dir(i, PT_561, PT_405):
#     if 'FOV' in i and PT_561 in i:
#         num_fov = os.path.basename(os.path.normpath(i.replace(PT_561, '')))
#         idx = os.path.basename(os.path.normpath(i.replace(num_fov + PT_561, '')))
#         title_plot = os.path.join(idx, num_fov)
        
#     elif 'FOV' in i and PT_405 in i:
#         num_fov = os.path.basename(os.path.normpath(i.replace(PT_405, '')))
#         idx = os.path.basename(os.path.normpath(i.replace(num_fov + PT_405, '')))
#         title_plot = os.path.join(idx, num_fov)

#     elif PT_561 in i:
#         idx = os.path.basename(os.path.normpath(i.replace(PT_561, '')))
#         title_plot = os.path.join(idx)

#     elif PT_405 in i:
#         idx = os.path.basename(os.path.normpath(i.replace(PT_405, '')))
#         title_plot = os.path.join(idx)

#     return title_plot

# def lire_csv(nom_fichier):
#     lignes = []
#     with open(nom_fichier, 'r') as f:
#         lecteur = csv.reader(f)
#         for ligne in lecteur:
#             # Convertir chaque élément de la ligne en entier (integer)
#             ligne = [float(element) for element in ligne]
#             lignes.append(ligne)
#     return lignes

# def pre_process_on_frame_csv(file):
#     tmp = list()
#     file = lire_csv(file)
#     for line in file:
#         tmp.append(get_length_on(line))
#     return [j for i in tmp for j in i]

# def pre_process_off_frame_csv(file):
#     tmp = list()
#     file = lire_csv(file)
#     for line in file:
#         tmp.append(get_length_off(line))
#     return [j for i in tmp for j in i]

# def pre_process_single_intensity(file):
#     tmp = list()
#     file = lire_csv(file)
#     for line in file:
#         tmp.append(line)
#     return [j for i in tmp for j in i]

# exp = '230227_gradient_data/exp_data/'
# list_of_frame_csv = get_csv_poca_frame_files(exp)
# list_of_int_csv = get_csv_poca_intensity_files(exp)
# list_of_poca_files = get_poca_files(exp)
# heatmap_data = []

# for f in range(len(list_of_poca_files)):
#     well_data = dict()
#     well_data['_on_times'] = int(statistics.median(pre_process_on_frame_csv(list_of_frame_csv[f])))
#     well_data['_off_times'] = int(statistics.median(pre_process_off_frame_csv(list_of_frame_csv[f])))
#     well_data['_phot_per_loc'] = int(statistics.median(pre_process_single_intensity(list_of_int_csv[f])))
#     raw_file_poca = read_poca_files(list_of_poca_files[f])
#     well_data['_total_on'] = int(statistics.median(raw_file_poca.loc[:, 'total ON'].values.tolist()))
#     well_data['_num_blinks'] = int(statistics.median(raw_file_poca.loc[:, 'blinks'].values.tolist()))
#     well_data['_phot_per_cluster'] = int(statistics.median(raw_file_poca.loc[:, 'intensity'].values.tolist()))
#     well_data['_num_on_times'] = int(statistics.median(raw_file_poca.loc[:, '# seq ON'].values.tolist()))
#     well_data['_num_off_times'] = int(statistics.median(raw_file_poca.loc[:, '# seq OFF'].values.tolist()))
#     heatmap_data.append(well_data)


# # Convert dict to pd.dataframe
# data = []
# for d in range(len(heatmap_data)):
#     name = get_num_fov_idx_results_dir(list_of_poca_files[d],'/561.PT/locPALMTracer_cleaned.txt', '/561-405.PT/locPALMTracer_cleaned.txt')
#     b=pd.DataFrame.from_dict(heatmap_data[d], orient='index').rename({0:name}, axis='columns')
#     data.append(b)

# # Create figure and convert dataframe to heatmap data
# fig, ax = plt.subplots(figsize=(10, 5))
# heatmap_data = pd.concat(data)
# heatmap_data = heatmap_data.groupby(heatmap_data.index).sum()
# heatmap_data = heatmap_data.replace(np.nan, 0)
# # tab_n = heatmap_data.div(heatmap_data.max(axis=1), axis=0)
# heatmap = sns.heatmap(heatmap_data, annot=True)

# # Axis
# ax.set_xticks(np.arange(heatmap_data.shape[1])+0.5, minor=False)
# ax.set_yticks(np.arange(heatmap_data.shape[0])+0.5, minor=False)
# ax.invert_yaxis()
# ax.xaxis.tick_top()

# # Columns & Rows labels
# column_labels = heatmap_data.columns
# row_labels = heatmap_data.index
# ax.set_xticklabels(column_labels, minor=False)
# ax.set_yticklabels(row_labels, minor=False)
# plt.show()


