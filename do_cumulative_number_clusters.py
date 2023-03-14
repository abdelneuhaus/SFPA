from utils import read_poca_files
import matplotlib.pyplot as plt
import os


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


def do_cumulative_number_clusters(list_of_poca_files, exp, isPT=True, drop_one_event=False, drop_beads=False):
    tmp = list()
    for i in list_of_poca_files:
        raw_file_poca = read_poca_files(i)
        if drop_one_event == True:
            init = len(raw_file_poca)
            raw_file_poca = raw_file_poca[raw_file_poca['total ON'] > 1]
            post = len(raw_file_poca)
            print("After One Event Dropping Step, we keep:", round(post*100/init,2), '%')
        if drop_beads == True:
            raw_file_poca = raw_file_poca[raw_file_poca['total ON'] < max(raw_file_poca['total ON'])*0.6]
        loc_per_frame = raw_file_poca.groupby(['frame']).size()
        cum_loc_per_frame = loc_per_frame.cumsum()
        tmp.append(cum_loc_per_frame)
 
    fig = plt.figure()
    fig.tight_layout()
    ax = plt.subplot(111)
    for i in tmp:
        i.plot(ax=ax)
    plt.xlabel('Time (in frames)')
    plt.ylabel('Cumulative Number of Clusters')
    
    legend = list()
    if isPT == True:
        for d in range(len(list_of_poca_files)):
            name = get_num_fov_idx_results_dir(list_of_poca_files[d],'/561.PT/locPALMTracer_cleaned.txt', '/561-405.PT/locPALMTracer_cleaned.txt')
            legend.append(name)
    else:
        for d in list_of_poca_files:
            legend.append(os.path.basename(os.path.normpath(d.replace('.PT/locPALMTracer_cleaned.txt', ''))))
    
    
    plt.legend(legend, loc='upper left')
    plt.grid(linestyle='-', linewidth=1)
    results_dir = os.path.join('results/'+exp+'/')
    sample_file = 'cumulative_clusters.pdf'
    if not os.path.isdir(results_dir):
        os.makedirs(results_dir)
    plt.savefig(results_dir+sample_file)
    plt.close('all')


