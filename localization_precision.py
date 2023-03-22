import math

def localization_precision(photon, sigma, a=160, median=0):
    """Implementation of Localization Precision (nm)

    Args:
        photon: number of photon (count)
        sigma: standard deviation (in nm)
        a: pixel size (nm)
    """
    sigma *= a
    try:
        return sigma/math.sqrt(photon)
    except ZeroDivisionError:
        return sigma/math.sqrt(median)