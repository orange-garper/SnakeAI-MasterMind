import numpy as np

_obs = np.zeros((2, 3), dtype=np.float64)
_obs[1, 2] = 1
print(_obs)