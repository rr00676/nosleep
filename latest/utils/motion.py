import numpy as np
from itertools import repeat

def random_walk(start:np.ndarray,
                mu: np.ndarray, 
                sigma: np.ndarray, 
                dt:float, 
                steps:int,
                trials:int) -> np.ndarray:
    """Generate random walk paths based on multivariate normal distributions."""
    path = np.zeros((len(mu),trials, steps+1, len(mu[0])))
    path[:,:,0] = start[:,None,:]
    path[:,:,1:] = dt*np.array([*map(np.random.multivariate_normal, mu, sigma, repeat((trials, steps)))])
    return path.cumsum(axis=2)
    

def elliptical(center:np.ndarray,
            periods: np.ndarray,
            a:np.ndarray,
            b:np.ndarray,
            phi:np.ndarray,
            steps:int) -> np.ndarray:
    """Generate elliptical paths with specified parameters."""
    t = np.linspace(0, 2*np.pi*periods, steps+1)
    X = lambda t: a*np.cos(t)*np.cos(phi) - b*np.sin(t)*np.sin(phi)
    Y = lambda t: a*np.cos(t)*np.sin(phi) + b*np.sin(t)*np.cos(phi)
    return np.array([X(t),Y(t)]).T + center[:,None,:]

def linear(start:np.ndarray,
           velocity:np.ndarray,
           angle:float,
           dt:float,
           steps:int) -> np.ndarray:
     """Generate linear paths with constant velocity and direction."""
     v = (velocity*np.array([np.cos(angle), np.sin(angle)])*dt).T
     return v[:,None,:]*np.arange(steps+1)[None,:,None] + start[:,None,:]

def stationary(start:np.ndarray,
               steps:int) -> np.ndarray:
    """Generate stationary paths."""
    return np.repeat(start[:,None,:], steps+1, axis=1)
