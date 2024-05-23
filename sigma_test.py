from utils import get_PALMTracer_files, read_locPALMTracer_file
from localization_precision import localization_precision
import statistics as statistics
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np 

def calculate_FWMH(sigma_pxl):
    return 2.3548*sigma_pxl


def loc_prec_calculation(sigma, photon_loc, pixel_size=160):
    otp = []
    median = statistics.median(sigma)*pixel_size
    for i in range(len(sigma)):
        otp.append(localization_precision(photon_loc[i], sigma[i], median=median))
    return otp  

def photon_calculation(liste, gain=3.6, emgain=300, qe=0.95):
    otp = gain/emgain
    return np.array(liste)*otp/qe
    for valeur in liste:
        exp_liste.append(valeur*otp/qe)
    return exp_liste



list_of_pt_files = get_PALMTracer_files('./240313_HCS_totransfer')
bins = 500
for poca_file in list_of_pt_files:
    raw_file_poca = read_locPALMTracer_file(poca_file)
    intensity_threshold = raw_file_poca['Integrated_Intensity'].quantile(0.75)
    filtered_data = raw_file_poca[raw_file_poca['Integrated_Intensity'] < 12500]
    sigma = np.array(filtered_data['SigmaX(px)'].groupby(pd.cut(filtered_data['Plane'], list(range(0, 5001, bins)))).mean())
    nPhotons = photon_calculation(list(filtered_data['Integrated_Intensity'].groupby(pd.cut(filtered_data['Plane'], list(range(0, 5001, bins)))).mean()))
    loc_prec = loc_prec_calculation(sigma, nPhotons)
    plt.plot(calculate_FWMH(sigma*160), label=poca_file)
plt.xlabel('Time Intervals of 50 sec')
plt.ylabel('Sigma (nm)')
# plt.legend()
plt.show()
