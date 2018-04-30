import numpy as np
def reverseSigmoid(x):
    return (np.exp(-x))/(1 + np.exp(-x))
