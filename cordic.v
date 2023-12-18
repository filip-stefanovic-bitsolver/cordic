 module cordic(
 input clk,
 input rst_n,
 input   [5:0] x_in,
 input   [5:0] y_in,
 input   [5:0] z_in,
 input   [5:0] z_tgt,
 output  [5:0] x_out,
 output  [5:0] y_out
);
localparam [36:0] atan = {5'd12,5'd10,5'd8,5'd6,5'd4,5'd2};
reg [5:0][5:0] x;
reg [5:0][5:0] y;
reg [5:0][5:0] z;
 
  always @(posedge clk, negedge rst_n) begin
    if (!rst_n) begin
      x <= '0;
      y <= '0;
      z <= '0;
    end else begin
      x[0] <= x_in;
      y[0] <= y_in;
      z[0] <= z_in;
x[1] <= (z[0] < z_tgt) ? x[0] - (y[0]>>0) : x[0] + (y[0]>>0);
y[1] <= (z[0] < z_tgt) ? y[0] + (x[0]>>0) : y[0] - (x[0]>>0);
z[1] <= (z[0] < z_tgt) ? x[0] + atan[4:0] : z[0] - atan[4:0];
x[2] <= (z[1] < z_tgt) ? x[1] - (y[1]>>1) : x[1] + (y[1]>>1);
y[2] <= (z[1] < z_tgt) ? y[1] + (x[1]>>1) : y[1] - (x[1]>>1);
z[2] <= (z[1] < z_tgt) ? x[1] + atan[9:5] : z[1] - atan[9:5];
x[3] <= (z[2] < z_tgt) ? x[2] - (y[2]>>2) : x[2] + (y[2]>>2);
y[3] <= (z[2] < z_tgt) ? y[2] + (x[2]>>2) : y[2] - (x[2]>>2);
z[3] <= (z[2] < z_tgt) ? x[2] + atan[14:10] : z[2] - atan[14:10];
x[4] <= (z[3] < z_tgt) ? x[3] - (y[3]>>3) : x[3] + (y[3]>>3);
y[4] <= (z[3] < z_tgt) ? y[3] + (x[3]>>3) : y[3] - (x[3]>>3);
z[4] <= (z[3] < z_tgt) ? x[3] + atan[19:15] : z[3] - atan[19:15];
x[5] <= (z[4] < z_tgt) ? x[4] - (y[4]>>4) : x[4] + (y[4]>>4);
y[5] <= (z[4] < z_tgt) ? y[4] + (x[4]>>4) : y[4] - (x[4]>>4);
z[5] <= (z[4] < z_tgt) ? x[4] + atan[24:20] : z[4] - atan[24:20];
end
end
assign x_out = x[5];
assign y_out = y[5];
endmodule