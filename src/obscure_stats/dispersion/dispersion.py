"""
Module for measures of dispersion
"""

import warnings

import numpy as np
from scipy import stats  # type: ignore

EPS = 1e-6


def efficiency(x: np.ndarray) -> float:
    """
    Function for calculating array efficiency (squared CV)

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    eff : float or array_like.
        The value of the efficiency.

    References
    ----------
    Grubbs, Frank (1965).
    Statistical Measures of Accuracy for Riflemen and Missile Engineers. pp. 26-27.
    """
    mean = np.nanmean(x)
    if abs(mean) <= EPS:
        warnings.warn("Mean is close to 0. Statistic is undefined.")
        return np.inf
    return np.nanvar(x) / mean**2


def studentized_range(x: np.ndarray) -> float:
    """
    Function for calculating range normalized by standard deviation.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    sr : float or array_like.
        The value of the studentized range.

    References
    ----------
    Student (1927).
    Errors of routine analysis.
    Biometrika. 19 (1/2): 151-164.
    """
    maximum = np.nanmax(x)
    minimum = np.nanmin(x)
    std = np.nanstd(x)
    return (maximum - minimum) / std


def coefficient_of_lvariation(x: np.ndarray) -> float:
    """
    Function for calculating linear coefficient of variation (MeanAbsDev / Mean).

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    lcv : float or array_like.
        The value of the linear coefficient of variation.

    References
    ----------
    Hosking, J.R.M. (1990).
    L-moments: analysis and estimation of distributions
    using linear combinations of order statistics.
    Journal of the Royal Statistical Society, Series B. 52 (1): 105-124.
    """
    l1 = np.nanmean(x)
    if abs(l1) <= EPS:
        warnings.warn("Mean is close to 0. Statistic is undefined.")
        return np.inf
    else:
        l2 = np.nanmean(np.abs(x - l1)) * 0.5
        return l2 / l1


def coefficient_of_variation(x: np.ndarray) -> float:
    """
    Function for calculating coefficient of variation (Std / Mean).

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    cv : float or array_like.
        The value of the coefficient of variation.

    References
    ----------
    Brown, C.E. (1998).
    Coefficient of Variation.
    Applied Multivariate Statistics in Geohydrology and Related Sciences. Springer.
    """
    mean = np.nanmean(x)
    if abs(mean) <= EPS:
        warnings.warn("Mean is close to 0. Statistic is undefined.")
        return np.inf
    else:
        return np.nanstd(x) / mean


def robust_coefficient_of_variation(x: np.ndarray) -> float:
    """
    Function for calculating robust coefficient of variation based on
    median absolute deviation from the median (MedAbsDev / Median).

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    rcv : float or array_like.
        The value of the robust coefficient of variation.

    References
    ----------
    Reimann, C., Filzmoser, P., Garrett, R.G. and Dutter, R. (2008).
    Statistical Data Analysis Explained: Applied Environmental Statistics with R.
    John Wiley and Sons, New York.
    """
    med = np.nanmedian(x)
    if abs(med) <= EPS:
        warnings.warn("Median is close to 0. Statistic is undefined.")
        return np.inf
    else:
        med_abs_dev = np.nanmedian(np.abs(x - med))
        return med_abs_dev / med


def quartile_coef_of_dispersion(x: np.ndarray) -> float:
    """
    Function for calculating Quartile Coefficient of Dispersion (IQR / Midhinge).

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    qcd : float or array_like.
        The value of the quartile coefficient of dispersion.

    References
    ----------
    Bonett, D. G. (2006).
    Confidence interval for a coefficient of quartile variation.
    Computational Statistics & Data Analysis. 50 (11): 2953-2957.
    """
    q1, q3 = np.nanquantile(x, [0.25, 0.75])
    if abs(q3 + q1) <= EPS:
        warnings.warn("Midhinge is close to 0. Statistic is undefined.")
        return np.inf
    else:
        return (q3 - q1) / (q3 + q1)


def dispersion_ratio(x: np.ndarray) -> float:
    """
    Function for calculating dispersion ratio (Mean / GMean).

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    dr : float or array_like.
        The value of the dispersion ratio.

    References
    ----------
    Soobramoney, J., Chifurira, R., & Zewotir, T. (2022)
    Selecting key features of online behaviour on South African informative websites
    prior to unsupervised machine learning.
    Statistics, Optimization & Information Computing.
    """
    return np.nanmean(x) / (stats.gmean(x, nan_policy="omit") + EPS)


def hoover_index(x: np.ndarray) -> float:
    """
    Function for calculating Hoover index (also known as the Robin Hood index,
    Schutz index or Pietra ratio). Mostly used as measure of income inequality.
    A value of 0 represents total equality, and 1 represents perfect inequality.
    In general - measure of uniformity of the distribution.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    hi : float or array_like.
        The value of the Hoover index.

    References
    ----------
    Edgar Malone Hoover Jr. (1936).
    The Measurement of Industrial Localization.
    Review of Economics and Statistics, 18, No. 162-71.
    """
    return 0.5 * np.nansum(x - np.nanmean(x)) / np.nansum(x)


def lloyds_index(x: np.ndarray) -> float:
    """
    Function for calculating Lloyd's index of mean crowding.
    Lloyd's index of mean crowding (IMC) is the average number of other points
    contained in the sample unit that contains a randomly chosen point.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    li : float or array_like.
        The value of the Lloyd's index.

    References
    ----------
    Lloyd, M (1967).
    Mean crowding.
    J Anim Ecol. 36 (1): 1-30.
    """
    m = np.nanmean(x)
    s = np.nanvar(x)
    return m + s / (m - 1)


def morisita_index(x: np.ndarray) -> float:
    """
    Function for calculating Morisita's index of dispersion.
    Morisita's index of dispersion (Im) is the scaled probability
    that two points chosen at random from the whole population are in the same sample.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    mi : float or array_like.
        The value of the Morisita's index.

    References
    ----------
    Morisita, M (1959).
    Measuring the dispersion and the analysis of distribution patterns.
    Memoirs of the Faculty of Science, Kyushu University Series e. Biol. 2: 215–235
    """
    x_sum = np.sum(x)
    return len(x) * (np.sum(np.square(x)) - x_sum) / (x_sum**2 - x_sum)


def sqad(x: np.ndarray) -> float:
    """
    Function for calculating Standard quantile absolute deviation.
    This measure is a robust measure of dispersion, that does not need
    normalizing constant like MAD.

    Parameters
    ----------
    x : array_like
        Input array.

    Returns
    -------
    sqad : float or array_like.
        The value of the SQAD.

    References
    ----------
    Akinshin, A. (2022).
    Quantile absolute deviation.
    arXiv preprint arXiv:2208.13459.
    """
    med = np.nanmedian(x)
    return np.nanquantile(np.abs(x - med), q=0.682689492137086)  # constant