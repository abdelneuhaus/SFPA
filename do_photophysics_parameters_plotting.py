from utils import read_poca_files
from preprocessing import pre_process_off_frame_csv, pre_process_on_frame_csv, pre_process_sigma, pre_process_single_intensity, get_num_fov_idx_results_dir
from localization_precision import localization_precision

import matplotlib.pyplot as plt
import os
import statistics
import numpy as np


def photon_calculation(liste):
    exp_liste = []
    for valeur in liste:
        exp_liste.append(valeur*0.04/0.95)
    return exp_liste

def loc_prec_calculation(sigma, photon_loc):
    otp = []
    for i in range(len(sigma)):
        otp.append(localization_precision(photon_loc[i], sigma[i]))
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



def crop_x(x_vals, y_vals, x_min, x_max):
    """ Crops the x values and y values of a PDF outside of the specified range """
    crop_mask = (x_vals >= x_min) & (x_vals <= x_max)
    x_vals = x_vals[crop_mask]
    y_vals = y_vals[crop_mask]
    return x_vals, y_vals



def do_photophysics_parameters_plotting(list_of_poca_files, list_of_frame_csv, list_of_int_csv, list_of_sigma_csv, exp=None, isPT=True,
                                        on_times=True, off_times=True, total_on=True, num_blinks=True,
                                        phot_per_loc=True, phot_per_cluster=True, num_on_times=True, 
                                        num_off_times=True, sigma=True, drop_one_event=False, boxplot=True,
                                        drop_beads=False):
    tmp_pho_loc = list()
    cpt = 0
    for j in range(len(list_of_frame_csv)):
        # length of each ON time
        _on_times = pre_process_on_frame_csv(list_of_frame_csv[j], on_filter=drop_one_event) if on_times else None
        # length of each OFF time
        _off_times = pre_process_off_frame_csv(list_of_frame_csv[j], on_filter=drop_one_event) if off_times else None
        # photon per localization
        _phot_per_loc = photon_calculation(pre_process_single_intensity(list_of_int_csv[j], on_filter=drop_one_event)) if phot_per_loc else None
        tmp_pho_loc.append(photon_calculation(pre_process_single_intensity(list_of_int_csv[j], on_filter=drop_one_event)))
        
        raw_file_poca = read_poca_files(list_of_poca_files[j])
        if drop_one_event == True:
            init = len(raw_file_poca)
            raw_file_poca = raw_file_poca[raw_file_poca['total ON'] > 1]
            post = len(raw_file_poca)
            print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%')
        if drop_beads == True:
                raw_file_poca = raw_file_poca[raw_file_poca['total ON'] < max(raw_file_poca['total ON'])*0.6]
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
        _sigma = loc_prec_calculation(pre_process_sigma(list_of_sigma_csv[j], on_filter=drop_one_event), tmp_pho_loc[cpt]) if sigma else None
        cpt += 1
        
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
            
            if boxplot ==  True:
            # Boxplot version
                ax.boxplot(df, showfliers=False)

            # Histogram version
            elif boxplot == False:
                median = np.median(df)
                left = np.percentile(df, 5)
                right = np.percentile(df, 95)
                cropped_data = [x for x in df if left <= x <= right]
                ax.hist(cropped_data, bins=50, density=True)
                ax.axvline(median, color='red', linestyle='dashed', linewidth=1)
                
            # retrouver le pdf comme sur le diapo UNE FOIS QUE LE RESTE EST FINI
                
        # Si pas PT experiment (pas de 561-405) et que le nom du PT est le nom du dossier (dossier -> dossier.PT)
        title_plot = os.path.basename(os.path.normpath(list_of_poca_files[j].replace('.PT/locPALMTracer_cleaned.txt', '')))
        results_dir = os.path.join('results/'+exp+'/'+title_plot+'/')
        plt.suptitle(title_plot, fontsize=14)

        if isPT == True:
            PT_405 = '/561-405.PT/locPALMTracer_cleaned.txt'
            PT_561 = '/561.PT/locPALMTracer_cleaned.txt'
            results_dir, title_plot = get_num_fov_idx_results_dir(list_of_poca_files[j], exp, PT_561, PT_405)
            plt.suptitle(title_plot, fontsize=14)
        
        sample_file = '/photophysics_plots.pdf'
        sample_file = sample_file.replace('.PT', '')
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir+sample_file)
        plt.close('all')