import numpy as np

a = np.array([
    [3, 3, 3], 
    [3, 3, 3], 
    [3, 3, 3]
])

print(a)
a[1: , 0:] = 1
print(a)