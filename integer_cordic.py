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

  angle = np.arange(2**input_width)
  angle = angle[::step]
  return(x_initial, y_initial, angle, artan)

def find_errors_point (sin, cos, z, frac_width):
  #err = np.arange (0, 2*np.pi, 2*np.pi/len(sin))
  pi_half_int = 2**frac_width
  max_err = 0
  err_sin_point = np.zeros(len(sin))
  err_cos_point = np.zeros(len(cos))
  for i in range (len(sin)):
    err_sin_point[i] = abs(np.sin(z[i]*np.pi/(2*pi_half_int))) - abs((sin[i])/(pi_half_int-1))
    err_cos_point[i] = abs(np.cos(z[i]*np.pi/(2*pi_half_int))) - abs((cos[i])/(pi_half_int-1))

    if (max_err < err_sin_point[i]):
      max_err = err_sin_point[i]
      a = i
    elif(max_err < err_cos_point[i]):
      max_err = err_cos_point[i]
      a = i
  #print(err_sin_point, err_cos_point, "err")
  print(max_err,a, "MAX ERROR POINT")

x, y, z, a = generate_inputs(6, 1**2**4)
print(x,"initial")
sin, cos = cordic (x, y, z, a) 
find_errors_point (sin, cos, z, 6)
fig, axs = plt.subplots(2, 1, figsize=(6, 6))

# Plot on each subplot
axs[0].plot(sin)
axs[0].set_title('Sin(x)')

axs[1].plot(cos)
axs[1].set_title('Cos(x)')
plt.tight_layout()  # Adjust layout for better spacing
plt.show()


