import numpy as np


def _gcl(x, r, D, Ia, Ct):
    """GCLarsen wake deficit model
    This function does not checks if r is greater than the wake radius!
    Parameters
    -----------
    x:  float | ndarray
        Distance downstream
    r:  float | ndarray
        radial position
    D:  float | ndarray
        wind turbine rotor diameter
    Ia: float | ndarray
        inflow turbulence
    Ct: float | ndarray
        turbine ct

    Returns
    -------
    out: list
      - du: float | ndarray
            The wind speed deficit at the specified positions
      - rw: float | ndarray
            The wake width at the specified positions
    """

    Area = np.pi * D ** 2.0 / 4.0
    m = 1.0 / (np.sqrt(1.0 - Ct))
    k = np.sqrt((m + 1.0) / 2.0)

    a1 = 0.435449861  # empirically determined
    a2 = 0.797853685
    a3 = -0.124807893
    a4 = 0.136821858
    b1 = 15.6298
    b2 = 1.0
    R96 = a1 * (np.exp(a2 * Ct * Ct + a3 * Ct + a4)) * (b1 * Ia + b2) * D

    x0 = (9.6 * D) / ((2.0 * R96 / (k * D)) ** 3.0 - 1.0)
    term1 = (k * D / 2.0) ** (5.0 / 2.0)
    term2 = (105.0 / (2.0 * np.pi)) ** (-0.5)
    term3 = (Ct * Area * x0) ** (-5.0 / 6.0)
    c1 = term1 * term2 * term3
    # c45=3*(c1) ** 2

    term10 = 0.1111  # * WindSpeed  # U/9.0
    term20 = (Ct * Area * (x + x0) ** (-2.0)) ** (1.0 / 3.0)
    term310 = (r ** (3.0 / 2.0))
    term320 = (3.0 * c1 * c1 * Ct * Area * (x + x0)) ** (-0.5)
    term30 = term310 * term320
    term40 = ((35.0 / (2.0 * np.pi)) ** (3.0 / 10.0)) * \
        (3.0 * c1 * c1) ** (-1.0 / 5.0)
    DU1 = -term10 * term20 * (term30 - term40) ** 2.0

    DU = DU1     # + w2 * DU2
    Rw = ((105 * c1 ** 2.0 / (2 * np.pi)) ** (1. / 5.)) * \
        (Ct * Area * (x + x0)) ** (1. / 3.)
    return DU, Rw


def gcl(rel_pos, c_t, D, ti):
    """GCLarsen wake deficit model
    This function checks if r is greater than the wake radius!
    Parameters
    -----------
    rel_pos:  ndarray [n,3]
              x,y,z relative position compared to the upstream turbine
    c_t:      float | ndarray [n]
              upstream wind turbine thrust coefficient
    D:        float | ndarray [n]
              upstream wind turbine rotor diameter
    ti:       float | ndarray [n]
              inflow turbulence

    Returns
    -------
    du:       float | ndarray [n]
              The wind speed deficit at the specified positions
    """
    x = rel_pos[:, 0]
    r = np.sqrt(rel_pos[:, 1] ** 2.0 + rel_pos[:, 2] ** 2.0)
    DU = np.zeros_like(x)
    ind = x > 0.0
    DU_, Rw = _gcl(x[ind], r[ind], D[ind], ti[ind], c_t[ind])
    DU_[abs(r[ind]) > Rw] = 0.0
    DU_[DU_ < -1.0] = 0.0     # Avoid some weirdiness
    DU[ind] = DU_
    return DU
