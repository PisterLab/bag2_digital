//systemVerilog HDL for "bag2_digital", "pfd" "systemVerilog"


module pfd ( 
	input CLKA,
	input CLKB,
	output reg UP,
	output reg UPb,
	output reg DOWN,
	output reg DOWNb,
	inout VDD,
	inout VSS);

wire RSTb;
assign RSTb = ~(UP & DOWN);

always @(posedge CLKB or negedge RSTb) begin
	DOWN <= ~RSTb ? 1'b0 : 1'b1;
	DOWNb <= ~RSTb ? 1'b1 : 1'b0;
end

always @(posedge CLKA or negedge RSTb) begin
	UP <= ~RSTb ? 1'b0 : 1'b1;
	UPb <= ~RSTb ? 1'b1 : 1'b0;
end

endmodule
