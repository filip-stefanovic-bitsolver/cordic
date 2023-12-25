`timescale 1ns/1ps

module cordic_tb_generated();

//constants//
localparam time  C_CLK_PERIOD   = 2ns;
localparam time C_RST_PERIOD    = 20ns;
localparam D_WIDTH             = 16;
localparam real PI             = 3.141592653589793;
localparam real ERROR_TOL_R     = 50;
localparam real ERROR_TOL_A     = 0.5;
localparam integer MAX_Z_TGT   = 32768;

localparam integer STEP_INT   = 1000;

reg clk;
reg rst_n;
integer max_z_tgt;
integer z_tgt_int;
integer z_tgt_int_delay;
integer x_int;
integer y_int;
real xc_out_int;
real yc_out_int;
real xv_out_int;
real yv_out_int;
real error_x_a;
real error_y_a;
real error_x_r;
real error_y_r;

always begin
    #(0.5*C_CLK_PERIOD);
    clk <= ~clk;
end

initial begin
    clk   <= 1'b0;
    rst_n <= 1'b0;
    yv_out_int <= '0;
    xv_out_int <= '0;
    #20;
    rst_n <= 1'b1;
    #600000;
    $finish;
end

initial begin
    $dumpfile("waves.vcd");
    $dumpvars;
end

always @(negedge clk or negedge rst_n) begin
    if (rst_n == 1'b0) begin
        z_tgt_int <= -STEP_INT;
    end
    else begin
        z_tgt_int <= z_tgt_int + STEP_INT;
        z_tgt_int_delay <= #((D_WIDTH-1)*C_CLK_PERIOD) z_tgt_int;
        if (z_tgt_int >= (MAX_Z_TGT - STEP_INT))
            z_tgt_int <= '0;
    end
end

always @(negedge clk or negedge rst_n) begin
    if (rst_n == 1'b0) begin
        error_x_a <= 0;
        error_y_a <= 0;
        error_x_r <= 0;
        error_x_r <= 0;
    end
    if ((xc_out_int < 0 || xc_out_int > 1)  && z_tgt_int_delay >= 0) begin
        $display("Values of x coordinate is not within the range of values corresponding to angles in the first quadrant.");
         $finish;
    end
    if ((yc_out_int < 0 || yc_out_int > 1) && z_tgt_int_delay >= 0) begin
        $display("Values of y coordinate is not within the range of values corresponding to angles in the first quadrant.");
         $finish;
    end
    if (z_tgt_int_delay >= 0) begin
        error_x_a  <= xc_out_int - xv_out_int; //apsolute
        error_y_a  <= yc_out_int - yv_out_int; //apsolute
        error_x_r  <= (error_x_a/xv_out_int) * 100;  //realative
        error_y_r  <= (error_y_a/yv_out_int) * 100;  //relative
    end
end

always @(*) begin
    if (error_x_a > ERROR_TOL_A || -error_x_a > ERROR_TOL_A) begin
        $display("Apsolutna greska x kordinate je veca od %0f%% i iznosi %0f%% za vrednost ugla %0d.", ERROR_TOL_A*100, error_x_a*100,z_tgt_int);
         $finish;
    end
    if (error_y_a > ERROR_TOL_A || -error_y_a > ERROR_TOL_A) begin
        $display("Apsolutna greska y kordinate je veca od %0f%% i iznosi %0f%% za vrednost ugla %0d.", ERROR_TOL_A*100, error_y_a*100,z_tgt_int);
         $finish;
    end
end

always @(*) begin
    xc_out_int = $itor(x_int) / (2 ** ((D_WIDTH)-1));
    yc_out_int = $itor(y_int) / (2 ** ((D_WIDTH)-1));
    if (z_tgt_int >= (D_WIDTH-1)*(STEP_INT)) begin
        xv_out_int = $cos(($itor(z_tgt_int_delay) * PI) / (2 ** (D_WIDTH)));
        yv_out_int = $sin(($itor(z_tgt_int_delay) * PI) / (2 ** (D_WIDTH)));
    end
   if (z_tgt_int_delay >= (MAX_Z_TGT - STEP_INT))
         $finish;
end

cordic cordic_i (
    .clk(clk),
    .rst_n(rst_n),
    .z_tgt(z_tgt_int),
    .x_out(x_int),
    .y_out(y_int)
);

endmodule
