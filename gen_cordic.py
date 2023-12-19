import numpy as np
import math as m
def generate_cordic(atan, data_width, x_init):
  d_w = data_width - 1
  idx = np.zeros(d_w-1)
  for i in range (d_w-1):
    idx[i] = i
  cordic = f"module cordic(\n"
  cordic+= f" input clk,\n"
  cordic+= f" input rst_n,\n"
  cordic+=f" input signed  [{data_width}:0] z_tgt,\n"
  cordic+=f" output signed [{data_width}:0] x_out,\n"
  cordic+=f" output signed [{data_width}:0] y_out\n"
  cordic+=f");\n"
  cordic+=f"localparam signed[{(data_width+1)*data_width-1}:0] atan = "
  cordic+= "{"
  for i in range (d_w,-1,-1):
    cordic+= f"{data_width+1}'d{atan[i]},"
  cordic = cordic[:-1]
  cordic+= "};"
  cordic+= f"\n"
  cordic+= f"reg signed[{data_width}:0][{data_width}:0] x;\n"
  cordic+= f"reg signed[{data_width}:0][{data_width}:0] y;\n"
  cordic+= f"reg signed[{data_width}:0][{data_width}:0] z;\n"
  cordic+= """ 
always @(posedge clk, negedge rst_n) begin
  if (!rst_n) begin
    x <= '0;
    y <= '0;
    z <= '0;
  end else begin
    y[0] <= '0;
    z[0] <= z_tgt;
"""
  cordic+= f"    x[0] <= {data_width+1}'d{x_init};\n"
  for i in range (d_w+1):
    cordic += f"    x[{i+1}] <= (!z[{i}][{data_width}]) ? x[{i}] - (y[{i}]>>>{i}) : x[{i}] + (y[{i}]>>>{i});\n"
    cordic += f"    y[{i+1}] <= (!z[{i}][{data_width}]) ? y[{i}] + (x[{i}]>>>{i}) : y[{i}] - (x[{i}]>>>{i});\n"
    cordic += f"    z[{i+1}] <= (!z[{i}][{data_width}]) ? z[{i}] - atan[{(i+1)*(data_width+1)-1}:{i*(data_width+1)}] : z[{i}] + atan[{(i+1)*(data_width+1)-1}:{i*(data_width+1)}];\n"

  cordic+= f" end\nend\n"
  cordic+= f"assign x_out = x[{d_w+1}];\n"
  cordic+= f"assign y_out = y[{d_w+1}];\n"
  cordic += "endmodule"
  return cordic


input_width = 6
pi_half_int = 2**input_width
artan = np.zeros(input_width)
artan[0] = m.atan(1)*pi_half_int/np.pi*2
artan[0] = round(artan[0])
for i in range (input_width-1):
  artan[i+1] = m.atan(2**(-i-1))*pi_half_int/np.pi*2
  artan[i+1] = round(artan[i+1])
print(artan,"artan values")

data_width = input_width

def cordic_py (x_in, y_in, angle, artan):
  z_tgt = angle
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
  sin = y
  cos = z
  return(sin, cos)

x_in = 38
y_in = 0

s, c = cordic_py(x_in,y_in,0,artan)

print(s,c,"sin i cos")
s, c = cordic_py(x_in,y_in,10,artan)
print(s,c,"sin i cos")
artan = artan[::-1]
atan = [1,2,3,4,5,6]
for i in range(len(artan)):
  atan[i] = (int(artan[i]))
print(atan,"artan values")
# test = float(1)
# print(test)
# test = int(test)
# print(test)
atan = atan[::-1]
cordic = generate_cordic(atan, data_width,x_in)
with open('cordic.v', 'w') as f:
    f.write(cordic)

