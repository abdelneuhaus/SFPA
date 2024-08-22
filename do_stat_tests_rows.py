from utils import read_poca_files
from preprocessing import fusion, photon_calculation, loc_prec_calculation, pre_process_off_frame_csv, pre_process_on_frame_csv, pre_process_sigma, pre_process_single_intensity, get_and_save_well_and_FOV
from statistical_test_same_well import statistical_test_same_well

import os
import numpy as np
import matplotlib.pyplot as plt
import numpy as np


def do_stat_tests_rows(exp, col, index, wells_data):
    csv_frame_label = ['ON times', "OFF times"]
    csv_int_label = "Intensity_loc"
    csv_sigma_label = "Loc_Precision"
    for i in index:
        boxplot_data = []
        well_names = []
        for well, data in wells_data.items():
            well_poca_data = data["poca_data"]
            well_frame_data = data["frame_data"]
            well_intensity_data = data["intensity_data"]
            well_sigma_data = data["sigma_data"]
            # Cas où l'index est 'ON times' ou 'OFF times'
            if i in csv_frame_label:
                for f in well_frame_data:
                    if i == 'ON times':
                        boxplot_data.append(pre_process_on_frame_csv(f))
                    else:
                        boxplot_data.append(pre_process_off_frame_csv(f))
            # Cas où l'index est 'intensity per loc'
            elif i == csv_int_label:
                filtered = well_poca_data[well_poca_data['blinks'] < 25]
                filtered = filtered[filtered['total ON'] < 100]
                boxplot_data.append(np.array(filtered['intensity']) / np.array(filtered['total ON']) * (3.6 / 300))
            # Cas où on calcule la précision de localisation       
            elif i == csv_sigma_label:
                for f, int_f in zip(well_sigma_data, well_intensity_data):
                    boxplot_data.append(160 * loc_prec_calculation(pre_process_sigma(f), photon_calculation(pre_process_single_intensity(int_f))))
            # Cas où on lit depuis le fichier locPALMTracer_merged
            else:
                filtered_poca_data = well_poca_data[well_poca_data['blinks'] < 25]
                filtered_poca_data = filtered_poca_data[filtered_poca_data['total ON'] < 100]
                if i == 'intensity':
                    boxplot_data.append(photon_calculation(filtered_poca_data.loc[:, i].values.tolist()))
                else:
                    boxplot_data.append(filtered_poca_data.loc[:, i].values.tolist())
            well_names.append(well)
        fig, ax = plt.subplots()
        ax.boxplot(boxplot_data, showfliers=False, labels=well_names)
        statistical_test_same_well(ax, boxplot_data)
        results_dir = os.path.join('results/' + exp + '/' + col + '/')
        sample_file = i + '_stats.pdf'
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        fig.suptitle(col + '_' + i + '_stats')
        plt.savefig(results_dir + sample_file)
        plt.show()
        plt.close('all')
