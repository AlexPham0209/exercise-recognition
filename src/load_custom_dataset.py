import os
import numpy as np 

PATH = os.path.join('data', 'custom', 'punch.txt')
res = np.loadtxt(PATH).reshape((-1, 119, 6))
print(res.shape)