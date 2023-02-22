import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from utils import get_poca_files

files = get_poca_files('230126_stablefp/P24/B2/561-405.PT')


def read_cluster_from_PoCA(file):
    df = pd.read_csv(file)
    return df[df.columns[:-1]]['frame'].tolist()


tmp = list()
for i in files:
    if "cluster" in i:
        tmp.append(read_cluster_from_PoCA(i))
        
def plot_binary_on_off(df, frames_num):
    for j in df:
        ddf = np.array(j)
        tmp = []
        for i in range(0,frames_num+1):
            if i in ddf:
                tmp.append(1)
            else:
                tmp.append(0)
        bbin = tmp
        bxaxis = np.arange(0, len(bbin))
        byaxis = np.array(bbin)
        plt.step(bxaxis, byaxis)
        plt.xlabel('Time (in frames)')
        plt.ylabel("ON/OFF")
        # plt.title(str(title))
        plt.yticks([0,1])
        plt.show()


plot_binary_on_off(tmp, 3000)