"""Collection of tests of association module."""

import typing

import numpy as np
import pytest
from obscure_stats.association import (
    blomqvistbeta,
    chatterjeexi,
    concordance_corrcoef,
    concordance_rate,
    rank_minrelation_coefficient,
    symmetric_chatterjeexi,
    tanimoto_similarity,
    tukey_correlation,
    winsorized_correlation,
    zhangi,
)

all_functions = [
    blomqvistbeta,
    chatterjeexi,
    concordance_corrcoef,
    concordance_rate,
    rank_minrelation_coefficient,
    symmetric_chatterjeexi,
    tanimoto_similarity,
    tukey_correlation,
    winsorized_correlation,
    zhangi,
]


@pytest.mark.parametrize(
    "func",
    all_functions,
)
@pytest.mark.parametrize(
    "x_array",
    ["x_list_float", "x_list_int", "x_array_int", "x_array_float"],
)
@pytest.mark.parametrize(
    "y_array",
    ["y_list_float", "y_list_int", "y_array_int", "y_array_float"],
)
def test_mock_association_functions(
    func: typing.Callable,
    x_array: str,
    y_array: str,
    request: pytest.FixtureRequest,
) -> None:
    """Test for different data types."""
    x_array = request.getfixturevalue(x_array)
    y_array = request.getfixturevalue(y_array)
    func(x_array, y_array)


@pytest.mark.parametrize(
    "func",
    [
        blomqvistbeta,
        concordance_corrcoef,
        concordance_rate,
        rank_minrelation_coefficient,
        tanimoto_similarity,
        tukey_correlation,
        winsorized_correlation,
    ],
)
def test_signed_corr_sensibility(
    func: typing.Callable, y_array_float: np.ndarray
) -> None:
    """Testing for result correctness."""
    res = func(y_array_float, -y_array_float)
    if res > 0:
        msg = f"Corr coeff should be negative, got {res}"
        raise ValueError(msg)


@pytest.mark.parametrize(
    "func",
    [
        zhangi,
        chatterjeexi,
        symmetric_chatterjeexi,
    ],
)
def test_unsigned_corr_sensibility(
    func: typing.Callable, y_array_float: np.ndarray
) -> None:
    """Testing for result correctness."""
    w = np.ones(shape=len(y_array_float))
    w[0] = 2
    res_ideal = func(y_array_float, -y_array_float)
    res_normal = func(y_array_float, w)
    if res_ideal < res_normal:
        msg = f"Corr coeff higher in the first case, got {res_ideal} < {res_normal}"
        raise ValueError(msg)


@pytest.mark.parametrize(
    "func",
    [
        blomqvistbeta,
        chatterjeexi,
        concordance_corrcoef,
        concordance_rate,
        rank_minrelation_coefficient,
        tukey_correlation,
        symmetric_chatterjeexi,
        winsorized_correlation,
        zhangi,
    ],
)
def test_const(func: typing.Callable, y_array_float: np.ndarray) -> None:
    """Testing for constant input."""
    x = np.ones(shape=(len(y_array_float),))
    with pytest.warns(match="is constant"):
        res = func(x, y_array_float)
        if res is not np.nan:
            msg = f"Corr coef should be 0 with constant input, got {res}"
            raise ValueError(msg)


@pytest.mark.parametrize(
    "func",
    [
        blomqvistbeta,
        concordance_corrcoef,
        concordance_rate,
        tanimoto_similarity,
        symmetric_chatterjeexi,
        winsorized_correlation,
    ],
)
def test_invariance(
    func: typing.Callable, x_array_float: np.ndarray, y_array_float: np.ndarray
) -> None:
    """Testing for invariance."""
    xy = func(x_array_float, y_array_float)
    yx = func(y_array_float, x_array_float)
    if pytest.approx(xy) != pytest.approx(yx):
        msg = f"Corr coef should symmetrical, got {xy}, {yx}"
        raise ValueError(msg)


@pytest.mark.parametrize(
    "func",
    all_functions,
)
def test_notfinite_association(
    func: typing.Callable,
    x_array_nan: np.ndarray,
    x_array_int: np.ndarray,
    y_array_inf: np.ndarray,
    y_array_int: np.ndarray,
) -> None:
    """Test for correct nan behaviour."""
    if np.isnan(func(x_array_nan, y_array_int)):
        msg = "Corr coef should support nans."
        raise ValueError(msg)
    with pytest.warns(match="too many missing values"):
        func(x_array_nan[:2], x_array_int[:2])
    with pytest.warns(match="contains inf"):
        if not np.isnan(func(x_array_int, y_array_inf)):
            msg = "Corr coef should support infs."
            raise ValueError(msg)


@pytest.mark.parametrize(
    "func",
    all_functions,
)
def test_unequal_arrays(
    func: typing.Callable,
    x_array_int: np.ndarray,
    y_array_int: np.ndarray,
) -> None:
    """Test for unequal arrays."""
    with pytest.warns(match="Lenghts of the inputs do not match"):
        func(x_array_int[:4], y_array_int[:3])


@pytest.mark.parametrize(
    "func",
    all_functions,
)
def test_corr_boundries(func: typing.Callable, y_array_float: np.ndarray) -> None:
    """Testing for result correctness."""
    res = func(y_array_float, -y_array_float)
    if abs(res) > 1:
        msg = f"Corr coeff should not be higher than 1, got {res}"
        raise ValueError(msg)
