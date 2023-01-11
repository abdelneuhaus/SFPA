from utils import read_poca_files



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
            print(i)
            print("Clusters number:", len(tmp))
            print("Median lifetime (frames):", float(tmp['lifetime'].quantile([0.5])))
            print("Median #blinks (frames):", float(tmp['blinks'].quantile([0.5])))
            print("Median #ON (frames):", float(tmp['# seq ON'].quantile([0.5])))
            print("Median #OFF (frames):", float(tmp['# seq OFF'].quantile([0.5])))
            print("")