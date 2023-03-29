import math

# def localization_precision(photon, sigma, a=160, median=0):
#     """Implementation of Localization Precision (nm)

#     Args:
#         photon: number of photon (count)
#         sigma: standard deviation (in nm)
#         a: pixel size (nm)
#     """
#     sigma *= a
#     try:
#         return sigma/math.sqrt(photon)
#     except ZeroDivisionError:
#         return sigma/math.sqrt(median)
    
    

def localization_precision(photon, sigma, a=160, median=0, bckg=20.968):
    """Implementation of Localization Precision (nm)

    Args:
        photon: number of photon (count)
        sigma: standard deviation (in nm)
        a: pixel size (nm)
    """
    sigma *= a
    if photon == 0:
        photon = median
    first_term = (sigma*sigma+a*a/12)/photon
    second_term = 16/9 + (8*math.pi*sigma*sigma*bckg*bckg)/(a*a*photon*photon)
    try:
        return math.sqrt(first_term*second_term)
    except ZeroDivisionError:
        return sigma/math.sqrt(median)