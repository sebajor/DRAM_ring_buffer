`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    11:16:05 04/01/2020 
// Design Name: 
// Module Name:    read_controller 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module read_controller(
	clk, ce, en, rst, dram_addr, bram_full, we, addr, max_count, state
	);

	/*carefull must be take, when you read severeal times
	the same address could be variation	on the values 
	of some bits...
	*/
	input clk;
   input ce;
   input en;
   input rst;
   input [24:0] dram_addr;
   input bram_full;
   output we;
   output [24:0] addr;
	output [3:0] state;
	input [7:0] max_count;
	
	wire clk;
   wire ce;
   wire en;
   wire rst;
   wire [24:0] dram_addr;
   wire bram_full;
   wire we;
	wire [3:0] state;
   wire [24:0] addr;
	wire [7:0] max_count;
	
	
	parameter a = 4'd0;
	parameter b = 4'd1;
	parameter c = 4'd2;
	parameter d = 4'd3;
	parameter e = 4'd4;
	parameter f = 4'd5;
	parameter g = 4'd6;
	parameter h = 4'd7;
	parameter i = 4'd8;
	parameter j = 4'd9;
	parameter k = 4'd10;
	parameter l = 4'd11;
	parameter m = 4'd12;
	
	
	reg [24:0] addr_ =24'd0;  //address counter
	reg [7:0] counter=7'd0;		// timeout counter
	reg [24:0] com =  24'd0;		//comparator register
	
	reg [3:0] next_state;
	reg [3:0] actual_state = a;
	
	
	//output registers
	reg we_ = 0;
	
	
	
	
	
	always@(posedge clk or posedge rst) begin
		if(rst)
			actual_state <= a;
		else
			actual_state <= next_state;
	end
	
	
	always@(*) begin
		case(actual_state)
			a:
				next_state = b;
			b:
				if(~en)	next_state = b;
				else		next_state = c;
			c:
				if(counter>max_count)	next_state = e;
				else if(dram_addr==addr_)	next_state = d;
				else			next_state = c;
			d:
				next_state = f;
			e:
				next_state = k;
			f:
				if(bram_full)		next_state = i;
				else			next_state = g;
			g:
				if(counter>max_count)	next_state = e;
				else if(dram_addr==com)	next_state = h;
				else 			next_state = g;
			h:
				next_state = f;
			i:
				if(bram_full)		next_state = i;
				else 			next_state = g;
			j:
				if(bram_full)		next_state = j;
				else			next_state = l;
			k:
				if(bram_full) next_state = j;
				else		next_state = l;
			l:
				if(counter>max_count)		next_state = m;
				else				next_state = l;
			m:
				next_state = f;
			default:
				next_state = a;
		endcase
	end
	
	
	always@(posedge clk)begin 
		case(actual_state)
			a:
				begin
					counter = 0;
					addr_ = 0;
					we_ = 0;
					com=0;
				end
			c:
				counter = counter + 1;
			d:
				begin
					we_ = 1;
					com = addr_;
				end
			e:
				begin
					we_ = 1;
					counter = 0;
				end
			f:
				begin
					we_ = 0;
					addr_ = addr_ +1;
					com = com + 1;
					counter = 0;
				end
			e:
				begin
					we_ = 1;
					counter = 0;
				end
			g:
				counter = counter +1;
			h:
				we_ = 1;
			k:
				begin
					we_ = 0;
					addr_ = addr_ +1;
				end
			l:
				counter = counter+1;
			m:
				begin
					we_ =1;
					com = dram_addr;
				end
		endcase
	end
	
	
	assign we = we_;
	assign addr = addr_;
	assign state = actual_state;

	


endmodule
