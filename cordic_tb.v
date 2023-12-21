`timescale 1ns/1ps

module cordic_tb();

//constants//
localparam time  C_CLK_PERIOD    = 2ns;
localparam time C_RST_PERIOD    = 20ns;
localparam  D_WIDTH         = 7;
parameter   real PI         = 3.141592653589793;
parameter   ERROR_TOL       = 5;

reg clk;
reg rst_n;
integer max_z_tgt;
integer z_tgt_int;
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
    #C_RST_PERIOD;
    rst_n <= 1'b1;
    #10000ns;
    $finish;
end

initial begin
    $dumpfile("waves.vcd");
    $dumpvars;
end

always @(posedge clk or negedge rst_n) begin
    if (rst_n == 1'b0) begin
        max_z_tgt <= (2 ** (D_WIDTH-1));
        z_tgt_int <= 0;
    end
    else begin
    z_tgt_int <= z_tgt_int + 1;
    if (z_tgt_int == max_z_tgt - 1) 
        z_tgt_int <= '0;
    //for (integer i = 0; i < max_z_tgt; i = i + 1) 
    //    @(posedge clk);
    //    z_tgt_int <= z_tgt_int + 1;  
    end 
end

always @(*) begin
    if (error_x_r > ERROR_TOL && xv_out_int != 0)
        $display("Relativna greska x kordinate je veca od %0d%% i iznosi %0d%%.",ERROR_TOL,error_x_r);
    if (error_y_r > ERROR_TOL && yv_out_int !=0)
        $display("Relativna greska y kordinate je veca od %0d%% i iznosi %0d%%.",ERROR_TOL,error_y_r);
end

always @(*) begin
    xc_out_int = $itor(x_int) / (2 ** ((D_WIDTH)-1));
    yc_out_int = $itor(y_int) / (2 ** ((D_WIDTH)-1));
    if (z_tgt_int >= 6) begin
        xv_out_int = $cos(($itor(z_tgt_int-6) * PI) / (2 ** (D_WIDTH)));
        yv_out_int = $sin(($itor(z_tgt_int-6) * PI) / (2 ** (D_WIDTH)));
    end
    error_x_a  = xc_out_int - xv_out_int; //apsolute
    error_y_a  = yc_out_int - yv_out_int; //apsolute
    error_x_r  = (error_x_a/xv_out_int) * 100;  //realative
    error_y_r  = (error_y_a/yv_out_int) * 100;  //relative
end

cordic cordic_i (
    .clk(clk),
    .rst_n(rst_n),
    .z_tgt(z_tgt_int),
    .x_out(x_int),
    .y_out(y_int)
        ); 
endmodule