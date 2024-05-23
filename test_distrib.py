from utils import read_poca_files, get_poca_files, get_PALMTracer_files, read_locPALMTracer_file
from localization_precision import localization_precision
import statistics as statistics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 
import os 

def loc_prec_calculation(sigma, photon_loc):
    otp = []
    median = statistics.median(sigma)
    for i in range(len(sigma)):
        otp.append(localization_precision(photon_loc[i], sigma[i], median=median))
    return otp  

def photon_calculation(liste, gain=3.6, emgain=300, qe=0.95):
    exp_liste = []
    otp = gain/emgain
    for valeur in liste:
        exp_liste.append(valeur*otp/qe)
    return exp_liste


def get_poca_files(repertory):
    a = [os.path.join(dirpath,filename) for dirpath, _, filenames in os.walk(repertory) for filename in filenames if filename.endswith('merged.txt')]
    return [x.replace("\\", "/") for x in a]

# POCA
# list_of_poca_files = get_poca_files('./argon_oxygen_last/argon')
# for poca_file in list_of_poca_files:
#     raw_file_poca = read_poca_files(poca_file)
#     filtered_data = raw_file_poca[raw_file_poca['total ON'] < 50]
#     filtered_data = filtered_data[filtered_data['blinks'] < 20]
#     grouped_data = filtered_data.groupby(pd.cut(filtered_data['frame'], list(range(0, 5001, 500)))).median()
#     photons = photon_calculation(grouped_data['intensity'])
#     # photons = list(grouped_data['total ON'])
#     plt.plot(photons, label=poca_file)
# plt.xlabel('Time Intervals of 50 sec')
# plt.ylabel('Number of photons per molecule')
# plt.legend()
# plt.show()


#PT
list_of_pt_files = get_PALMTracer_files('./argon_oxygen_last/oxygen')
for poca_file in list_of_pt_files:
    raw_file_poca = read_locPALMTracer_file(poca_file)
    filtered_data = raw_file_poca[raw_file_poca['SigmaX(px)'] < 1.1]
    filtered_data = filtered_data[filtered_data['SigmaX(px)'] > 0.9]
    filtered_data = filtered_data[filtered_data['Integrated_Intensity'] <= 13500]
    grouped_data = filtered_data.groupby(pd.cut(filtered_data['Plane'], list(range(0, 5001, 500)))).median()
    photons = photon_calculation(grouped_data['Integrated_Intensity'])
    # photons = grouped_data['SigmaX(px)']*160
    plt.plot(list(photons), label=poca_file)
plt.xlabel('Time Intervals of 25 sec')
plt.legend()
plt.ylabel('Number of Photons per Localization')
plt.show()


# densité par frame
# list_of_pt_files = get_PALMTracer_files('./240313_HCS_totransfer/')
# alldata = []
# for poca_file in list_of_pt_files:
#     raw_file_poca = read_locPALMTracer_file(poca_file)
#     print(poca_file, raw_file_poca['Integrated_Intensity'].mean(), raw_file_poca['Integrated_Intensity'].median())
#     alldata.append(raw_file_poca['Integrated_Intensity'])
#     plt.boxplot(alldata, showfliers=False)
# #     filtered =  raw_file_poca[raw_file_poca['Plane'] < 10001]
# #     grouped_data = filtered.groupby(filtered['Plane'])['Plane'].count()
# #     plt.plot(list(grouped_data), label=poca_file)
# #     print(poca_file, grouped_data.mean())
# # plt.xlabel('Frames')
# # plt.ylabel('Number of Localization')
# plt.show()

