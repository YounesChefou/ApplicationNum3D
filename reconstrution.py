import numpy as np

data = np.load("arr_0.npy")
np.set_printoptions(threshold=data)
print(data)
