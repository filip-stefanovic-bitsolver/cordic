import numpy as np
import math as m
import sys
import subprocess
import time

#function for generating cordic (arguments: table of arc tan, signal width in bits, initial value of x coordinate)
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
  cordic+= f"reg signed[{data_width}:0] z_tmp;\n"
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
  cordic+= f"assign x_out = (x[{d_w+1}][{data_width}] != 1'b1) ? x[{d_w+1}] : {data_width+1}'d{2**data_width-1};\n"
  cordic+= f"assign y_out = (y[{d_w+1}][{data_width}] != 1'b1) ? y[{d_w+1}] : {data_width+1}'d{2**data_width-1};\n"
  #cordic+= f"assign x_out = x[{d_w+1}];\n"
  #cordic+= f"assign y_out = y[{d_w+1}];\n"
  cordic += "endmodule"
  return cordic

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python generate_cordic_tb.py <input_data>")
        sys.exit(1)

    input_width = int(sys.argv[1])
    error_tol = int(sys.argv[2])
    step = int(sys.argv[3])
    wave_req = int(sys.argv[4])

    print(f"Selected input_width: {input_width}")
    print(f"Selected error tolerance : {error_tol}")
    print(f"Selected step : {step}")
pi_half_int = 2**input_width
artan = np.zeros(input_width)
artan[0] = m.atan(1)*pi_half_int/np.pi*2
artan[0] = round(artan[0])
for i in range (input_width-1):
  artan[i+1] = m.atan(2**(-i-1))*pi_half_int/np.pi*2
  artan[i+1] = round(artan[i+1])

data_width = input_width

x_const = 0.607252935

x_in = round(x_const*(2**input_width-1))
print(x_in, "x_in")
y_in = 0

artan = artan[::-1]
atan = list(range(input_width))
for i in range(len(artan)):
  atan[i] = (int(artan[i]))
print(atan,"artan values")

atan = atan[::-1]
cordic = generate_cordic(atan, data_width,x_in)
with open('cordic.v', 'w') as f:
    f.write(cordic)

def generate_cordic_tb(input_width,error_tol,step):
    C_CLK_PERIOD = 2
    C_RST_PERIOD = 20
    D_WIDTH = input_width + 1
    PI = 3.141592653589793
    ERROR_TOL_R = error_tol
    ERROR_TOL_A = ERROR_TOL_R/100
    MAX_Z_TGT = 2 ** (D_WIDTH-1)

    with open("cordic_tb_generated.v", "w") as file:
        file.write("`timescale 1ns/1ps\n\n")
        file.write("module cordic_tb_generated();\n\n")
        file.write("//constants//\n")
        file.write(f"localparam time  C_CLK_PERIOD   = 2ns;\n")
        file.write(f"localparam time C_RST_PERIOD    = 20ns;\n")
        file.write(f"localparam D_WIDTH             = {D_WIDTH};\n")
        file.write(f"localparam real PI             = 3.141592653589793;\n")
        file.write(f"localparam real ERROR_TOL_R     = {ERROR_TOL_R};\n")
        file.write(f"localparam real ERROR_TOL_A     = {ERROR_TOL_A};\n")
        file.write(f"localparam integer MAX_Z_TGT   = {MAX_Z_TGT};\n\n")
        file.write(f"localparam integer STEP_INT   = {step};\n\n")
        # Declare signals
        file.write("reg clk;\n")
        file.write("reg rst_n;\n")
        file.write("integer max_z_tgt;\n")
        file.write("integer z_tgt_int;\n")
        file.write("integer z_tgt_int_delay;\n")
        file.write("integer x_int;\n")
        file.write("integer y_int;\n")
        file.write("real xc_out_int;\n")
        file.write("real yc_out_int;\n")
        file.write("real xv_out_int;\n")
        file.write("real yv_out_int;\n")
        file.write("real error_x_a;\n")
        file.write("real error_y_a;\n")
        file.write("real error_x_r;\n")
        file.write("real error_y_r;\n\n")

        # Always block for clock generation
        file.write("always begin\n")
        file.write("    #(0.5*C_CLK_PERIOD);\n")
        file.write("    clk <= ~clk;\n")
        file.write("end\n\n")

        # Initial block for reset and finish
        file.write("initial begin\n")
        file.write("    clk   <= 1'b0;\n")
        file.write("    rst_n <= 1'b0;\n")
        file.write("    yv_out_int <= '0;\n")
        file.write("    xv_out_int <= '0;\n")
        file.write(f"    #{C_RST_PERIOD};\n")
        file.write("    rst_n <= 1'b1;\n")
        file.write(f"    #{30000*C_RST_PERIOD};\n")
        file.write("    $finish;\n")
        file.write("end\n\n")

        # Initial block for waveform dumping
        file.write("initial begin\n")
        file.write("    $dumpfile(\"waves.vcd\");\n")
        file.write("    $dumpvars;\n")
        file.write("end\n\n")

        # Always block for z_tgt_int increment
        file.write("always @(negedge clk or negedge rst_n) begin\n")
        file.write("    if (rst_n == 1'b0) begin\n")
        file.write("        z_tgt_int <= -STEP_INT;\n")
        file.write("    end\n")
        file.write("    else begin\n")
        file.write("        z_tgt_int <= z_tgt_int + STEP_INT;\n")
        file.write("        z_tgt_int_delay <= #((D_WIDTH-1)*C_CLK_PERIOD) z_tgt_int;\n")
        file.write(f"        if (z_tgt_int >= (MAX_Z_TGT - STEP_INT))\n")
        file.write("            z_tgt_int <= '0;\n")
        file.write("    end\n")
        file.write("end\n\n")

        # Always block for z_tgt_int increment
        file.write("always @(negedge clk or negedge rst_n) begin\n")
        file.write("    if (rst_n == 1'b0) begin\n")
        file.write("        error_x_a <= 0;\n")
        file.write("        error_y_a <= 0;\n")
        file.write("        error_x_r <= 0;\n")
        file.write("        error_x_r <= 0;\n")
        file.write("    end\n")
        file.write(f"    if ((xc_out_int < 0 || xc_out_int > 1)  && z_tgt_int_delay >= 0) begin\n")
        file.write(f"        $display(\"Values of x coordinate is not within the range of values corresponding to angles in the first quadrant.\");\n")
        file.write("         $finish;\n")
        file.write("    end\n")
        file.write(f"    if ((yc_out_int < 0 || yc_out_int > 1) && z_tgt_int_delay >= 0) begin\n")
        file.write(f"        $display(\"Values of y coordinate is not within the range of values corresponding to angles in the first quadrant.\");\n")
        file.write("         $finish;\n")
        file.write("    end\n")
        file.write("    if (z_tgt_int_delay >= 0) begin\n")
        file.write("        error_x_a  <= xc_out_int - xv_out_int; //apsolute\n")
        file.write("        error_y_a  <= yc_out_int - yv_out_int; //apsolute\n")
        file.write("        error_x_r  <= (error_x_a/xv_out_int) * 100;  //realative\n")
        file.write("        error_y_r  <= (error_y_a/yv_out_int) * 100;  //relative\n")
        file.write("    end\n")
        file.write("end\n\n")


        # Always block for error display
        file.write("always @(*) begin\n")
        file.write(f"    if (error_x_a > ERROR_TOL_A) begin\n")
        file.write(f"        $display(\"Apsolutna greska x kordinate je veca od %0f%% i iznosi %0f%% za vrednost ugla %0d.\", ERROR_TOL_A*100, error_x_a*100,z_tgt_int);\n")
        file.write("         $finish;\n")
        file.write("    end\n")
        file.write(f"    if (error_y_a > ERROR_TOL_A) begin\n")
        file.write(f"        $display(\"Apsolutna greska y kordinate je veca od %0f%% i iznosi %0f%% za vrednost ugla %0d.\", ERROR_TOL_A*100, error_y_a*100,z_tgt_int);\n")
        file.write("         $finish;\n")
        file.write("    end\n")
        file.write("end\n\n")

        # Always block for coordinate calculations
        file.write("always @(*) begin\n")
        file.write("    xc_out_int = $itor(x_int) / (2 ** ((D_WIDTH)-1));\n")
        file.write("    yc_out_int = $itor(y_int) / (2 ** ((D_WIDTH)-1));\n")
        file.write("    if (z_tgt_int >= (D_WIDTH-1)*(STEP_INT)) begin\n")
        file.write(f"        xv_out_int = $cos(($itor(z_tgt_int_delay) * PI) / (2 ** (D_WIDTH)));\n")
        file.write(f"        yv_out_int = $sin(($itor(z_tgt_int_delay) * PI) / (2 ** (D_WIDTH)));\n")
        file.write("    end\n")
        file.write(f"   if (z_tgt_int >= (MAX_Z_TGT - STEP_INT))\n")
        file.write("         $finish;\n")
        file.write("end\n\n")

      

        # Module instantiation
        file.write("cordic cordic_i (\n")
        file.write("    .clk(clk),\n")
        file.write("    .rst_n(rst_n),\n")
        file.write("    .z_tgt(z_tgt_int),\n")
        file.write("    .x_out(x_int),\n")
        file.write("    .y_out(y_int)\n")
        file.write(");\n\n")
        
        file.write("endmodule\n")

generate_cordic_tb(input_width,error_tol, step)

time.sleep(0.5)
subprocess.run (["iverilog", "-g2012", "cordic.v", "cordic_tb_generated.v"])
subprocess.run (["vvp", "a.out"])
if (wave_req >= 1):
  subprocess.run (["gtkwave", "waves.vcd"])