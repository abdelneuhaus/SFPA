from utils import read_poca_files
import matplotlib.pyplot as plt
import os

def do_cumulative_number_clusters(list_of_poca_files, exp):
    tmp = list()
    for i in list_of_poca_files:
        raw_file = read_poca_files(i)
        loc_per_frame = raw_file.groupby(['frame']).size()
        cum_loc_per_frame = loc_per_frame.cumsum()
        tmp.append(cum_loc_per_frame)
 
    fig = plt.figure()
    fig.tight_layout()
    ax = plt.subplot(111)
    for i in tmp:
        i.plot(ax=ax)
    plt.xlabel('Time (in frames)')
    plt.ylabel('Cumulative Number of Clusters')
    plt.legend(list_of_poca_files)
    results_dir = os.path.join('results/'+exp+'/')
    sample_file = 'cumulative_clusters.pdf'
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    plt.savefig(results_dir+sample_file)
    plt.close('all')


