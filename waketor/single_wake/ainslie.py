from scipy.integrate import odeint
from scipy.interpolate import interp1d
import numpy as np

def ainslie(rel_pos, c_t, D, ti):
    """Ainslei wake deficit model
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
    kappa = 0.4
    K1 = 0.015
    C1 = 3.56
    C2 = 0.05
    C3 = 16.0
    C4 = 0.5

    # For the F equation
    C5 = 5.5
    C6 = 0.65
    C7 = 4.5
    C8 = 23.32

    Ld = 1.0 #Downstream distance where the Ainslie model is starting

    N = 100 #Inegration discretization

    I0 = TI * 100.0
    ## Initial Centerline wake deficit
    DMi = c_t - C2 - ((C3 * c_t - C4) * I0 / 1000.0)

    # Eddy diffusivity of momentum
    Km = kappa**2.0 * I0 / 100.0
    def F(x):
        """
        Ainslie's Filter function,
        with a twist, because (x0-c7)**(1/3) is not real when x0<C7
        """
        if x> 5.5:
            return 1.0
        #else:
        elif x>4.5:
            return 0.65+((x-4.5)/23.32)**(1.0/3.0)
        else:
            return 0.65-((4.5-x)/23.32)**(1.0/3.0)

    def dUc(Uc, x):
        DM = 1 - Uc / 1.0

        ## Initial wake width parameter
        b = np.sqrt(C1 * c_t / (8 * DM * (1-0.5*DM)) )

        ## Eddy viscosity model
        epsilon = F(x) * (K1 * b * (1.0 - Uc) + Km)

        return 16.0 * epsilon * (Uc**3.0 - Uc**2.0 - Uc + 1) / (Uc * c_t)

    ## Uc, current centerline wake deficit
    Uci = 1.0 * (1-DMi)

    xs = np.linspace(Ld, 200, N)
    Ucx = odeint(dUc, Uci, xs)
    iUcx = interp1d(np.array(xs).T, np.array(Ucx).T)

    ## Normalized axial distance
    x = rel_pos[:,0] / D
    r = np.sqrt(rel_pos[:,1]**2.0 + rel_pos[:,2]**2.0) / D

    Uc = iUcx(Ld) * np.ones(x.shape)
    Uc[x > Ld] = iUcx(x[x > Ld])

    DM = 1 - Uc / 1.0
    ## Initial wake width parameter
    b = np.sqrt(C1 * c_t / (8 * DM * (1-0.5*DM)) )

    ## Current deficit
    DU = DM * np.exp(-C1*(r/b)**2.0)

    return -DU
