import numpy as np
import matplotlib.pylab as pl

dist = lambda x: np.sqrt(x[:,0]**2. + x[:,1]**2)
def mindist(x):
    I,J = np.meshgrid(range(len(x)),range(len(x)))
    d2d = np.sqrt((x[I,0]-x[J,0])**2. + (x[I,1]-x[J,1])**2)
    d2d[d2d==0.0] = np.inf
    return d2d.min(0)

def generate_random_coord(N, maxR, minD, starting_coord=None):
    """Generate a random coordinate
    Params:
    -------
    N:      int
            number of wind turbines

    maxR:   float [m]
            maximum radius of the layout

    minD:   float [m]
            minimum distance between the turbines

    sc:     ndarray([n,2]) (optional)
            starting coordinate, to implement a recursivity when the
            algorithm can't find enough points

    Returns:
    --------
    coord:  ndarray([n,2]) [m]
            coordinate of the wind turbines
    """
    coord = np.random.random(40*N).reshape(20*N,2)
    if not starting_coord is None:
        coord = np.vstack([coord, starting_coord])
    # remove all the points that are closer than epsilon
    coord = coord[mindist(coord)>1.E-2]
    coord *= minD / min(mindist(coord))
    coord = coord[dist(coord-coord.mean(0))<maxR]
    if coord.shape[0]<N:
        return generate_random_coord(N, maxR, minD, starting_coord=coord)
    return coord[0:N,:]

def plot_coord(coord):
    pl.plot(coord[:,0], coord[:,1],'.')


def coord_transform(dx, dy, dh, wd):
    coswd = np.cos(wd*np.pi/180.0)
    sinwd = np.sin(wd*np.pi/180.0)
    nx = sinwd * dx + coswd * dy
    nr = np.sqrt((coswd * dx - sinwd * dy)**2.0 + dh**2.0)
    return nx, nr
