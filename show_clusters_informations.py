from utils import read_poca_files, get_poca_files
import matplotlib.pyplot as plt

def show_clusters_informations(files):
    """
    Global information about clusters:
        - real number of clusters
        - average/mean number of blinks per clusters
        - average/mean lifetime
    """
    for i in files:
        if "_cleaned" in i:
            tmp = read_poca_files(i)
            plt.hist(tmp['# seq ON'], bins=len(tmp['# seq ON']))
            plt.show()
            

files = get_poca_files('230126_stablefp/P24/B2/561-405.PT')
show_clusters_informations(files)
