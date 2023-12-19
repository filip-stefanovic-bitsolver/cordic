module cordic(
 input clk,
 input rst_n,
 input signed  [6:0] z_tgt,
 output signed [6:0] x_out,
 output signed [6:0] y_out
);
localparam signed[41:0] atan = {7'd1,7'd3,7'd5,7'd10,7'd19,7'd32};
reg signed[6:0][6:0] x;
reg signed[6:0][6:0] y;
reg signed[6:0][6:0] z;
wire signed[6:0] x1, y1, z1;
wire signed[6:0] x2, y2, z2;
wire signed[6:0] x3, y3, z3;
wire signed[6:0] x4, y4, z4;
wire signed[6:0] x5, y5, z5;
wire signed[6:0] x6, y6, z6;
 
always @(posedge clk, negedge rst_n) begin
  if (!rst_n) begin
    x <= '0;
    y <= '0;
    z <= '0;
  end else begin
    y[0] <= '0;
    z[0] <= z_tgt;
    x[0] <= 7'd38;
    x[1] <= (!z[0][6]) ? x[0] - (y[0]>>>0) : x[0] + (y[0]>>>0);
    y[1] <= (!z[0][6]) ? y[0] + (x[0]>>>0) : y[0] - (x[0]>>>0);
    z[1] <= (!z[0][6]) ? z[0] - atan[6:0] : z[0] + atan[6:0];
    x[2] <= (!z[1][6]) ? x[1] - (y[1]>>>1) : x[1] + (y[1]>>>1);
    y[2] <= (!z[1][6]) ? y[1] + (x[1]>>>1) : y[1] - (x[1]>>>1);
    z[2] <= (!z[1][6]) ? z[1] - atan[13:7] : z[1] + atan[13:7];
    x[3] <= (!z[2][6]) ? x[2] - (y[2]>>>2) : x[2] + (y[2]>>>2);
    y[3] <= (!z[2][6]) ? y[2] + (x[2]>>>2) : y[2] - (x[2]>>>2);
    z[3] <= (!z[2][6]) ? z[2] - atan[20:14] : z[2] + atan[20:14];
    x[4] <= (!z[3][6]) ? x[3] - (y[3]>>>3) : x[3] + (y[3]>>>3);
    y[4] <= (!z[3][6]) ? y[3] + (x[3]>>>3) : y[3] - (x[3]>>>3);
    z[4] <= (!z[3][6]) ? z[3] - atan[27:21] : z[3] + atan[27:21];
    x[5] <= (!z[4][6]) ? x[4] - (y[4]>>>4) : x[4] + (y[4]>>>4);
    y[5] <= (!z[4][6]) ? y[4] + (x[4]>>>4) : y[4] - (x[4]>>>4);
    z[5] <= (!z[4][6]) ? z[4] - atan[34:28] : z[4] + atan[34:28];
    x[6] <= (!z[5][6]) ? x[5] - (y[5]>>>5) : x[5] + (y[5]>>>5);
    y[6] <= (!z[5][6]) ? y[5] + (x[5]>>>5) : y[5] - (x[5]>>>5);
    z[6] <= (!z[5][6]) ? z[5] - atan[41:35] : z[5] + atan[41:35];
 end
end
assign x_out = x[6];
assign y_out = y[6];
assign x1 = x[1];
assign x2 = x[2];
assign x3 = x[3];
assign x4 = x[4];
assign x5 = x[5];
assign x6 = x[6];
assign y1 = y[1];
assign y2 = y[2];
assign y3 = y[3];
assign y4 = y[4];
assign y5 = y[5];
assign y6 = y[6];
assign z1 = z[1];
assign z2 = z[2];
assign z3 = z[3];
assign z4 = z[4];
assign z5 = z[5];
assign z6 = z[6];
 
endmodule