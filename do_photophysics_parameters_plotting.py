from utils import read_poca_files, get_poca_files, get_csv_poca_frame_files, get_csv_poca_intensity_files, read_csv_poca
from get_length_on_off import get_length_off, get_length_on
import matplotlib.pyplot as plt
import os
import pandas as pd


def pre_process_on_frame_csv(file):
    tmp = list()
    file = read_csv_poca(file)
    for line in file:
        tmp.append(get_length_on(line))
    return [j for i in tmp for j in i]


def pre_process_off_frame_csv(file):
    tmp = list()
    file = read_csv_poca(file)
    for line in file:
        tmp.append(get_length_off(line))
    return [j for i in tmp for j in i]


def pre_process_single_intensity(file):
    tmp = list()
    file = read_csv_poca(file)
    for line in file:
        tmp.append(line)
    return [j for i in tmp for j in i]


def do_photophysics_parameters_plotting(list_of_poca_files, list_of_frame_csv, list_of_int_csv, exp=None, idx=None,
                                        on_times=False, off_times=False, total_on=True, num_blinks=True,
                                        phot_per_loc=False, phot_per_cluster=True, num_on_times=True, 
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
        _total_on = raw_file_poca.loc[:, 'total ON'] if total_on else None
        # num blinks
        _num_blinks = raw_file_poca.loc[:, 'blinks'] if num_blinks else None
        # photon per cluster
        _phot_per_cluster = raw_file_poca.loc[:, 'intensity'] if phot_per_cluster else None
        # number of ON times per cluster
        _num_on_times = raw_file_poca.loc[:, '# seq ON'] if num_on_times else None
        # number of OFF times per cluster
        _num_off_times = raw_file_poca.loc[:, '# seq OFF'] if num_off_times else None
        
        # imprime les éléments qui ne sont pas égaux à None
        non_none_elements = [_on_times, _off_times, _total_on, _num_blinks, _phot_per_loc, _phot_per_cluster, _num_on_times, _num_off_times]
        non_none_elements = [elem for elem in non_none_elements if elem is not None]

        fig, axes = plt.subplots(nrows=2, ncols=4, figsize=(15,8))
        plt.subplots_adjust(wspace=0.3, hspace=0.5)
        for m, df in enumerate(non_none_elements):
            row = m // 4
            col = m % 4
            ax = axes[row][col]
            ax.set_title("DataFrame " + str(m+1))
            pd.DataFrame(df).hist(ax=ax)
        plt.title(i)
        plt.show()
        
        # fig, axis = plt.subplots(2, 2)
        # axis[0,0].boxplot(raw_file['total ON'], showfliers=False)
        # axis[0,0].set_title("total ON (=bleach time)")
        # axis[0,1].boxplot(raw_file['blinks'], showfliers=False)
        # axis[0,1].set_title("#blinks")
        # axis[1,0].boxplot(raw_file['intensity'], showfliers=False)
        # axis[1,0].set_title("grey levels per clusters")
        # fig.suptitle(str(i))
        # results_dir = os.path.join('results/'+exp+'/'+idx+'/')
        # sample_file = 'photophysics_plots.pdf'
        # if not os.path.isdir(results_dir):
        #     os.makedirs(results_dir)
        # plt.savefig(results_dir+sample_file)
        # plt.close('all')

exp = "230227_gradient_data"
files = get_poca_files(exp)
csv_frame = get_csv_poca_frame_files(exp)
# print(pd.read_csv('230227_gradient_data/dom_sim/mEos3.2_3_ch1 (1-5000).PT/frame.csv', error_bad_lines=False))
csv_int = get_csv_poca_intensity_files(exp)
do_photophysics_parameters_plotting(files, csv_frame, csv_int)













# from scipy.stats import mannwhitneyu
# mannwhitney = mannwhitneyu(phot_per_mol[0], phot_per_mol[1])
# print(mannwhitney)