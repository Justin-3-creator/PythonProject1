import numpy as np

A = np.array([[2,4],
              [3,6]])

B = np.array([[5,7],
              [8,10]])

C = A + B    #Elementwise addition

D = A * B    #Elementwise multiplication

print(f"{C}: Elementwise addition")
print(f"{D}: Elementwise multiplication")
print(f"{A @ B}: Matrix product")  #The Matrix product