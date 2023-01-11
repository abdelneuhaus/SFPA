import numpy as np 
import matplotlib.pyplot as plt

def plot_binary_on_off(df, nbr, frames_num):
    df = df.to_numpy()
    tmp = []
    for i in range(0,frames_num+1):
        if i in df:
            tmp.append(1)
        else:
            tmp.append(0)
    bbin = tmp
    bxaxis = np.arange(0, len(bbin))
    byaxis = np.array(bbin)
    plt.step(bxaxis, byaxis)
    plt.xlabel('Time (in frames)')
    plt.ylabel("ON/OFF")
    plt.title(str(nbr))
    plt.yticks([0,1])
    plt.show()