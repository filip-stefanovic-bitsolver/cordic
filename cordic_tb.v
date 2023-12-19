`timescale 1ns/1ps
module cordic_tb();

localparam dw = 7;
localparam step = 4;
localparam max = (2**(dw-1))/step; 


integer i = 0;
reg clk;
reg rst_n;

reg   [dw-1:0] z_tgt;



always begin
  #2ns;
  clk = ~clk;
end

initial begin
  $dumpfile("waves.vcd");
  $display(max);
  //$display(haha, "ahah");
  $dumpvars;
end

initial begin
  clk = 0;
  rst_n = 0;
  z_tgt = 0;
  #10ns;
  @(posedge clk);
  rst_n <= 1'b1;
  @(posedge clk);
  z_tgt = '0;
  for (i = 0; i < max; i=i+1 ) begin
    @(posedge clk);
    z_tgt = z_tgt + step;
    $display(i);
  end
  #60ns;
  $finish;
end




cordic cordic(
  .clk(clk),
  .rst_n(rst_n),
  .z_tgt(z_tgt),
  .x_out(),
  .y_out()
);

endmodule