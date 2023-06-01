from utils import read_poca_files
from preprocessing import pre_process_sigma, get_length_off, get_length_on, pre_process_off_frame_csv, pre_process_on_frame_csv, pre_process_single_intensity, lire_csv
from localization_precision import localization_precision

import matplotlib.pyplot as plt
import os
import statistics
import numpy as np


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


def crop_x(x_vals, y_vals, x_min, x_max):
    """ Crops the x values and y values of a PDF outside of the specified range """
    crop_mask = (x_vals >= x_min) & (x_vals <= x_max)
    x_vals = x_vals[crop_mask]
    y_vals = y_vals[crop_mask]
    return x_vals, y_vals



def do_photophysics_number_super_supra_clusters(list_of_poca_files, list_of_frame_csv, list_of_int_csv, list_of_sigma_csv, 
                                        exp=None, isPT=True, boxplot=True, use_one_event=False, use_super_blinkers=False):
    tmp_pho_loc = list()
    cpt = 0
    for j in range(len(list_of_frame_csv)):
        raw_file_poca = read_poca_files(list_of_poca_files[j])
        
        # Get one-event cluster        
        if use_one_event == True:
            raw_file_poca = raw_file_poca[raw_file_poca['total ON'] == 1]
            _on_times = pre_process_on_frame_csv(list_of_frame_csv[j], get_sm_only=use_one_event, beads=False)
            _off_times = pre_process_off_frame_csv(list_of_frame_csv[j], get_sm_only=use_one_event, beads=False)
            _phot_per_loc = photon_calculation(pre_process_single_intensity(list_of_int_csv[j], get_sm_only=use_one_event, beads=False))
            tmp_pho_loc.append(photon_calculation(pre_process_single_intensity(list_of_int_csv[j], get_sm_only=use_one_event, beads=False)))
            _sigma = loc_prec_calculation(pre_process_sigma(list_of_sigma_csv[j], get_sm_only=use_one_event), tmp_pho_loc[cpt])
            cpt += 1
            
        # Get "long-blinkers"
        if use_super_blinkers == True:
            _on_times, _off_times, _tmp_phot_per_loc, _sigma = list(), list(), list(), list()
            on_time_file = lire_csv(list_of_frame_csv[j])
            off_time_file = lire_csv(list_of_frame_csv[j])
            phot_per_loc_file = lire_csv(list_of_int_csv[j])
            sigma_file = lire_csv(list_of_sigma_csv[j])
            
            for i in range(len(raw_file_poca)):
                if raw_file_poca['blinks'][i] > 25:# and raw_file_poca['total ON'][i] > 1000:
                    if statistics.median(get_length_on(on_time_file[i])) > 3:
                        _on_times.append(get_length_on(on_time_file[i])) 
                        _off_times.append(get_length_off(off_time_file[i]))
                        _tmp_phot_per_loc.append(phot_per_loc_file[i])
                        _sigma.append(sigma_file[i])
                        
            _phot_per_loc = [photon_calculation(i) for i in _tmp_phot_per_loc]
            _sigma = [loc_prec_calculation(_sigma[i], _tmp_phot_per_loc[i]) for i in range(len(_sigma))]
            _on_times = [j for i in _on_times for j in i]
            _off_times = [j for i in _off_times for j in i]
            _phot_per_loc = [j for i in _phot_per_loc for j in i]
            _sigma = [j for i in _sigma for j in i]
            
            init = len(raw_file_poca)
            raw_file_poca = raw_file_poca[raw_file_poca['blinks'] > 25]
            # raw_file_poca = raw_file_poca[raw_file_poca['total ON'] < 2000]
            post = len(raw_file_poca)
            print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%, which is', post, 'clusters over', init)
            
        _total_on = raw_file_poca.loc[:, 'total ON'].values.tolist()
        _num_blinks = raw_file_poca.loc[:, 'blinks'].values.tolist()
        _phot_per_cluster = photon_calculation(raw_file_poca.loc[:, 'intensity'].values.tolist())
        _num_on_times = raw_file_poca.loc[:, '# seq ON'].values.tolist()
        _num_off_times = raw_file_poca.loc[:, '# seq OFF'].values.tolist()
        # print(_off_times)
        non_none_elements = [_on_times, _off_times, _total_on, _num_blinks, _phot_per_loc, _phot_per_cluster, _num_on_times, _num_off_times, _sigma]
        non_none_elements = [elem for elem in non_none_elements]
        label = ['ON times', "OFF times", "Total ON (Bleachtime)", "#Blinks", "Photon/loc", "Photon/cluster", "#ON times", "#OFF times", "Loc. Precision"]
        
        fig, axes = plt.subplots(nrows=3, ncols=4, figsize=(15,8))
        plt.subplots_adjust(wspace=0.3, hspace=0.5)
        for m, df in enumerate(non_none_elements):
            row = m // 4
            col = m % 4
            ax = axes[row][col]
            try:
                ax.set_title(label[m]+', median:'+ str(round(float(statistics.median((df))), 3)))
            except statistics.StatisticsError:
                ax.set_title(label[m]+', median: 0')
            
            if boxplot ==  True:
            # Boxplot version
                ax.boxplot(df, showfliers=False)

            # Histogram version
            elif boxplot == False:
                try:
                    median = np.median(df)
                    left = np.percentile(df, 5)
                    right = np.percentile(df, 95)
                    cropped_data = [x for x in df if left <= x <= right]
                    ax.hist(cropped_data, bins=50, density=True)
                    ax.axvline(median, color='red', linestyle='dashed', linewidth=1)
                except IndexError:
                    pass
                
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