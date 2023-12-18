import math as m
from fxpmath import Fxp
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt


#function to transform to Fxp


#def gen_angles (frac_width, num_width, stage_nbr):
  #frac_width = 16
  #num_width = 2
  #word_width = frac_width + num_width + 1 # +1 for sign

  #min_stage_nbr = 6       #min cordic stages
  #stage_nbr = 16          #cordic stages
  

      
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
  print(sin[len(angle)-1],"sin poslednji")
  print(cos[len(angle)-1],"cos poslednji")
  print(angle[len(angle)-1],"za ugao")
  return(sin, cos)

def gen_inputs (frac_width, num_width, step_order, stage_nbr, all_points):

  #word_width = frac_width + num_width + 1
  def fixed (xin):
    word_width = frac_width
            
    xout = Fxp (xin, False, word_width, frac_width)
    print(xin, word_width, xout, xout.bin(), "fixed")
    return(xout)

  x_initial = fixed (0.607252935)
  print(x_initial.bin(), "binary")
  y_initial = fixed (0)

  if (stage_nbr < 6):
    stage_nbr = 6       #min stage nbr


  pi_half_int = 2**frac_width         #pi/2 represented as corresponding integer

  #arctan lookup generation
  artan = np.zeros(stage_nbr)
  artan[0] = m.atan(1)*pi_half_int/np.pi*2
  if (m.ceil(artan[0]) - artan[0] > artan[0] - m.floor(artan[0])):
    artan[0] = int(m.floor(artan[0]))
  else:
    artan[0] = int(m.ceil(artan[0]))
  for i in range (stage_nbr-1):
    artan[i+1] = m.atan(2**(-i-1))*pi_half_int/np.pi*2
    if (m.ceil(artan[i+1]) - artan[i+1] > artan[i+1] - m.floor(artan[i+1])):
      artan[i+1] = int(m.floor(artan[i+1]))
    else:
      artan[i+1] = int(m.ceil(artan[i+1]))
  print(artan,"artan")
  
  angle = np.arange(2**frac_width) #possible angle array
  
  if (all_points):
    angle_in = angle
  else:
    step = 2**step_order
    angle_in = angle[::step]
    # step = 2**frac_width/num_of_points
    # if (m.ceil(step) - step > step - m.floor(step)):
    #   fractional_part = step%1
    #   step = m.floor(step)
    #   direction = 0
    # elif (m.ceil(step) - step < step - m.floor(step)):
    #   fractional_part = 1 - step%1
    #   step = m.ceil(step)
    #   direction = 1
    # else:
    #   fractional_part = 0
    #   step = int(step)
    #   direction = 0

    # print (step, fractional_part, " step")  
    # j = 0
    # frac_sum = 0
    # if (fractional_part != 0):
    #   while (frac_sum < 1):
    #     j+=1 
    #     frac_sum += fractional_part
    # max_idx = int(2**frac_width/step)

    # angle_in = np.zeros(max_idx)
    # for i in range (max_idx):
    #   if (fractional_part != 0):
    #     if (i%j==0 and i != 0):
    #       if (direction == 1):
    #         k = -1
    #       else:
    #         k = 0
    #     else:
    #       k = 0
    #   else:
    #     k = 0
    #   angle_in[i] = angle[i*step+k] #input angles sampled from possible angles
    # print(angle_in[max_idx-1],"max")

  return (x_initial, y_initial, angle_in, artan)

def run_cordic (x, y, z, a):
  sin = np.zeros((4,len(z)))
  cos = np.zeros((4,len(z)))
  #z_inv = np.zeros(len(z))
  z_inv = np.roll(z, -1)
  z_inv = z_inv[::-1]
  print(z_inv)
  for i in range (4):
    if (i == 1 or i == 3):
      sin[i], cos[i] = cordic (x, y, z_inv, a)
    else:
      sin[i], cos[i] = cordic (x, y, z, a)
    if (i == 1):
      tmp = cos[i][0]
      print(tmp)
      cos[i][0] = sin[i][0]
      sin[i][0] = tmp
      cos[i] = np.negative(cos[i])
    elif (i == 2):
      cos[i] = np.negative(cos[i])
      sin[i] = np.negative(sin[i])
    elif (i == 3):
      tmp = cos[i][0]
      print(tmp)
      cos[i][0] = sin[i][0]
      sin[i][0] = tmp
      sin[i] = np.negative(sin[i])

  sin_r = np.reshape(sin, 4*len(z))
  cos_r = np.reshape(cos, 4*len(z))
  print ("PLOT!!!")
  fig, axs = plt.subplots(2, 1, figsize=(8, 6))

  # Plot on each subplot
  axs[0].plot(sin_r)
  axs[0].set_title('Sin(x)')

  axs[1].plot(cos_r)
  axs[1].set_title('Cos(x)')
  plt.tight_layout()  # Adjust layout for better spacing
  plt.show()
  return(sin_r, cos_r)

def find_errors_point (sin, cos, z, frac_width):
  #err = np.arange (0, 2*np.pi, 2*np.pi/len(sin))
  pi_half_int = 2**frac_width
  max_err = 0
  err_sin_point = np.zeros(int(len(sin)/4))
  err_cos_point = np.zeros(int(len(sin)/4))
  for i in range (int(len(sin)/4)):
    err_sin_point[i] = abs(np.sin(z[i]*np.pi/(2*pi_half_int))) - abs(float(sin[i]))
    err_cos_point[i] = abs(np.cos(z[i]*np.pi/(2*pi_half_int))) - abs(float(cos[i]))

    if (max_err < err_sin_point[i]):
      max_err = err_sin_point[i]
      a = i
    elif(max_err < err_cos_point[i]):
      max_err = err_cos_point[i]
      a = i
  #print(err_sin_point, err_cos_point, "err")
  print(max_err,a, "MAX ERROR POINT")

def find_errors_real (sin, cos, frac_width):
  real_angles = np.arange(0, np.pi/2, np.pi/2/int(len(sin)/4))
  err_sin_real = np.zeros(int(len(sin)/4))
  err_cos_real = np.zeros(int(len(sin)/4))
  max_err = 0
  for i in range (len(real_angles)):
    err_sin_real[i] = abs(np.sin(real_angles[i])) - abs(float(sin[i]))
    err_cos_real[i] = abs(np.cos(real_angles[i])) - abs(float(cos[i]))
    if (max_err < err_sin_real[i]):
      max_err = err_sin_real[i]
    elif (max_err < err_cos_real[i]):
      max_err = err_sin_real[i]
  print (max_err, "MAX ERROR REAL")

x, y, z, a = gen_inputs(6,2,1,6, False) #arguments: frac width, num width, step order, number of stages, use all points[true/false]
sin, cos = run_cordic(x,y,z,a)
find_errors_point(sin, cos, z, 12)
find_errors_real(sin, cos, 12)



