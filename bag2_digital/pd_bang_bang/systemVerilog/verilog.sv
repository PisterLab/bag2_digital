//systemVerilog HDL for "bag2_digital", "pd_bang_bang" "systemVerilog"


module pd_bang_bang ( D_RETIME, T, E, VDD, VSS, CLK, CLKb, D, UPb, DOWN);

  input CLK;
  input CLKb;
  input D;

  output wire T;
  output wire E;
  output wire D_RETIME;
  output wire UPb;
  output wire DOWN;

  inout VDD;
  inout VSS;

reg q1;
reg q2;
reg q3;
reg q4;

assign D_RETIME = q4;
assign T = ~(q1 | q2);
assign E = ~(q2 | q4);

assign UPb = ~T | E;
assign DOWN = T & E;

always @(posedge CLK) begin
	q1 <= D;
	q2 <= q1;
	q4 <= q3;
end

always @(negedge CLKb) begin
	q3 <= D;
end

endmodule
