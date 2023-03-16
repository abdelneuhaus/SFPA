import math

def localization_precision(photon, sigma, a=160):
    """Implementation of Localization Precision (nm)

    Args:
        photon: number of photon (count)
        sigma: standard deviation (in nm)
        a: pixel size (nm)
    """
    sigma *= a
    return sigma/math.sqrt(photon)