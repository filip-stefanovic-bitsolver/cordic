import math as m
from fxpmath import Fxp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def cordic (x_in, y_in, angle, artan):
  sin = np.zeros(len(angle))
  cos = np.zeros(len(angle))
  for i in range (len(angle)):
    #print(i, "ievi")
    z_tgt = angle[i]
    z = 0
    x = x_in
    y = y_in
    for j in range (len(artan)):
      if (j != 0):
        x = x_new   
      x_new = x - (y>>j) if (z < z_tgt) else x + (y>>j)
      #print(type(x_new))
      y = (x>>j) + y if (z < z_tgt) else y - (x>>j)
      z = z - artan[j] if (z >= z_tgt) else z + artan[j]
      #print(x, y, z)
    sin[i] = y
    cos[i] = x_new 
  print(sin[len(angle)-1])
  print(cos[len(angle)-1])
  print(angle[len(angle)-1])
  return(sin, cos)

def generate_inputs(input_width, step):
  max = 2**input_width - 1
  x_initial = round(0.607252935*max)
  print(x_initial, "x_initial")
  y_initial = 0
  z_initial = 0
  
  pi_half_int = 2**input_width         #pi/2 represented as corresponding integer
  
  #artan table generation
  artan = np.zeros(input_width)
  artan[0] = m.atan(1)*pi_half_int/np.pi*2
  if (m.ceil(artan[0]) - artan[0] > artan[0] - m.floor(artan[0])):
    artan[0] = int(m.floor(artan[0]))
  else:
    artan[0] = int(m.ceil(artan[0]))
  for i in range (input_width-1):
    artan[i+1] = m.atan(2**(-i-1))*pi_half_int/np.pi*2
    if (m.ceil(artan[i+1]) - artan[i+1] > artan[i+1] - m.floor(artan[i+1])):
      artan[i+1] = int(m.floor(artan[i+1]))
    else:
      artan[i+1] = int(m.ceil(artan[i+1]))
  print(artan,"artan values")


  return()