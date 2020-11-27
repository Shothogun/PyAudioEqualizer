import numpy as np
import math as mt

class Filter():
  def __init__(self):
    
    PI = mt.pi
    # Filter order
    M=100

    omega_c1 = 63
    omega_c2 = 277
    omega_s = 314

    wc1 = omega_c1*2*PI / omega_s
    wc2 = omega_c2*2*PI / omega_s
    n = np.arange(1,M/2)
    print(n)



    # 32 Hz Filter
    
