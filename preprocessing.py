import csv 
import os
from get_length_on_off import get_length_off, get_length_on


def lire_csv(nom_fichier):
    lignes = []
    with open(nom_fichier, 'r') as f:
        lecteur = csv.reader(f)
        for ligne in lecteur:
            # Convertir chaque élément de la ligne en entier (integer)
            ligne = [float(element) for element in ligne]
            lignes.append(ligne[1:])
    return lignes


def pre_process_single_intensity(file, on_filter=False, beads=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if beads==True:
                if (len(line) != 1) and (len(line) < 4000*0.6): 
                    tmp.append(line)
            else:
                if len(line) != 1:
                    tmp.append(line)

        if on_filter==False and beads==True:
            if len(line) < 4000*0.6: 
                tmp.append(line)
        else:
            tmp.append(line)            
    return [j for i in tmp for j in i]


def pre_process_on_frame_csv(file, on_filter=False, beads=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if beads==True:
                if (len(line) != 1) and (len(line) < 4000*0.6): 
                    tmp.append(get_length_on(line))
            else:
                if len(line) != 1:
                    tmp.append(get_length_on(line))

        if on_filter==False and beads==True:
            if len(line) < 4000*0.6: 
                tmp.append(get_length_on(line))
        else:
            tmp.append(get_length_on(line))           
    return [j for i in tmp for j in i]


def pre_process_off_frame_csv(file, on_filter=False, beads=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if beads==True:
                if (len(line) != 1) and (len(line) < 4000*0.6): 
                    tmp.append(get_length_off(line))
            else:
                if len(line) != 1:
                    tmp.append(get_length_off(line))

        if on_filter==False and beads==True:
            if len(line) < 4000*0.6: 
                tmp.append(get_length_off(line))
        else:
            tmp.append(get_length_off(line))      
    return [j for i in tmp for j in i]


def pre_process_sigma(file, on_filter=False, beads=False):
    tmp = list()
    file = lire_csv(file)
    for line in file:
        if on_filter==True:
            if beads==True:
                if (len(line) != 1) and (len(line) < 4000*0.6): 
                    tmp.append(line)
            else:
                if len(line) != 1:
                    tmp.append(line)

        if on_filter==False and beads==True:
            if len(line) < 4000*0.6: 
                tmp.append(line)
        else:
            tmp.append(line)
    return [j for i in tmp for j in i]


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