import numpy as np


def noj(rel_pos, c_t, D, k):
    """N.O. Jensen single wake deficit model
    This function checks if r is greater than the wake radius!
    Parameters
    -----------
    rel_pos:  ndarray [n,3]
              x,y,z relative position compared to the upstream turbine
    c_t:      float | ndarray [n]
              upstream wind turbine thrust coefficient
    D:        float | ndarray [n]
              upstream wind turbine rotor diameter
    k:        float | ndarray [n]
              wake expansion parameter

    Returns
    -------
    du:       float | ndarray [n]
              The wind speed deficit at the specified positions
    """
    x = rel_pos[:, 0]
    r = np.sqrt(rel_pos[:, 1] ** 2.0 + rel_pos[:, 2] ** 2.0)
    # Radius
    R = D / 2.0
    # NOJ Specific
    Rw = R + k * x  # upstream turbine wake radius
    DU = - (1.0 - np.sqrt(1.0 - c_t)) / (1.0 + (k * x) / R) ** 2.0
    # Upstream cases
    DU[x < 0.0] = 0.0
    DU[abs(r) > Rw] = 0.0
    return DU
