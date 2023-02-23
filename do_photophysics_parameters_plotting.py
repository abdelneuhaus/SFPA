from utils import read_poca_files
import matplotlib.pyplot as plt
import os

def do_photophysics_parameters_plotting(list_of_poca_files, exp):
    total_on, num_blinks, phot_per_mol = list(), list(), list()
    for i in list_of_poca_files:
        raw_file = read_poca_files(i)
        total_on.append(raw_file['total ON'])
        num_blinks.append(raw_file['blinks'])
        tmp = raw_file['intensity']
        phot_per_mol.append(tmp)
    
        fig, axis = plt.subplots(2, 2)
        axis[0,0].boxplot(raw_file['total ON'], showfliers=False)
        axis[0,0].set_title("total ON (=bleach time)")
        axis[0,1].boxplot(raw_file['blinks'], showfliers=False)
        axis[0,1].set_title("#blinks")
        axis[1,0].boxplot(raw_file['intensity'], showfliers=False)
        axis[1,0].set_title("grey levels per clusters")
        fig.suptitle(str(i))
        results_dir = os.path.join('results/'+exp+'/')
        sample_file = 'photophysics_plots.pdf'
        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)
        plt.savefig(results_dir+sample_file)
        plt.close('all')

# exp = "230210-ANR-FP"
# files = get_poca_files(exp)
# do_photophysics_parameters_plotting(files,exp)

# from scipy.stats import mannwhitneyu
# mannwhitney = mannwhitneyu(phot_per_mol[0], phot_per_mol[1])
# print(mannwhitney)