import numpy as np

arr = np.random.rand(40, 5000, 5000)
m = np.mean(arr, axis=0)
print(m)

