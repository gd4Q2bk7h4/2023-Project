import numpy as np
import random


result_array = np.zeros(10)

for i in range(10):
    data_tmp = random.random() 
    result_array[i] = data_tmp
    print(result_array[i])

print(result_array)
print(result_array[5])