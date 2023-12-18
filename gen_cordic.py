import numpy as np
def generate_cordic(atan, data_width):
  d_w = data_width - 1
  idx = np.zeros(d_w-1)
  for i in range (d_w-1):
    idx[i] = i
  cordic = f" module cordic(\n"
  cordic+= f" input clk,\n"
  cordic+= f" input rst_n,\n"
  cordic+=f" input   [{data_width-1}:0] x_in,\n"
  cordic+=f" input   [{data_width-1}:0] y_in,\n"
  cordic+=f" input   [{data_width-1}:0] z_in,\n"
  cordic+=f" input   [{data_width-1}:0] z_tgt,\n"
  cordic+=f" output  [{data_width-1}:0] x_out,\n"
  cordic+=f" output  [{data_width-1}:0] y_out\n"
  cordic+=f");\n"
  cordic+=f"localparam [{data_width*data_width}:0] atan = "
  cordic+= "{"
  for i in range (d_w,-1,-1):
    cordic+= f"{d_w}'d{atan[i]},"
  cordic = cordic[:-1]
  cordic+= "};"
  cordic+= f"\n"
  cordic+= f"reg [{d_w}:0][{d_w}:0] x;\n"
  cordic+= f"reg [{d_w}:0][{d_w}:0] y;\n"
  cordic+= f"reg [{d_w}:0][{d_w}:0] z;\n"
 
  cordic+= """ 
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n) begin
      x <= '0;
      y <= '0;
      z <= '0;
    end else begin
      x[0] <= x_in;
      y[0] <= y_in;
      z[0] <= z_in;
"""
  for i in range (d_w):
    cordic += f"x[{i+1}] <= (z[{i}] < z_tgt) ? x[{i}] - (y[{i}]>>{i}) : x[{i}] + (y[{i}]>>{i});\n"
    cordic += f"y[{i+1}] <= (z[{i}] < z_tgt) ? y[{i}] + (x[{i}]>>{i}) : y[{i}] - (x[{i}]>>{i});\n"
    cordic += f"z[{i+1}] <= (z[{i}] < z_tgt) ? x[{i}] + atan[{(i+1)*d_w-1}:{i*d_w}] : z[{i}] - atan[{(i+1)*d_w-1}:{i*d_w}];\n"

  cordic+= f"end\nend\n"
  cordic+= f"assign x_out = x[{d_w}];\n"
  cordic+= f"assign y_out = y[{d_w}];\n"
  cordic += "endmodule"
  return cordic





atan = [2, 4, 6, 8, 10, 12]
data_width = 6

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

x_in = 20
y_in = 0

s, c = cordic_py(20,0,16,atan[::-1])
cordic = generate_cordic(atan, data_width)
print(s,c,"sin i cos")
with open('cordic.v', 'w') as f:
    f.write(cordic)
