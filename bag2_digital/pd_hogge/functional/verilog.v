//Verilog HDL for "bag2_digital", "pd_hogge" "functional"


module pd_hogge (
	input 	data,
	input 	clk,
	output signed [1:0] 	error,
	output reg 			data_retimed);

reg 		A;
wire 	B, C;

always @(posedge clk) begin
	A <= data;
	data_retimed <= A;
end

assign B = dat ^ A;
assign C = A ^ data_retimed;
assign error = B - C;

endmodule
