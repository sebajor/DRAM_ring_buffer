`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    13:18:52 04/02/2020 
// Design Name: 
// Module Name:    read_control_v2 
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
module read_control_v2(
    clk,
    ce,
    dram_addr,
    bram_full,
    rd_val,
    en,
    en_read,
    write_bram,
    rst,
	 state
    );
	input clk;
   input ce;
   output [23:0] dram_addr;
   input bram_full;
   input rd_val;
   input en;
   output en_read;
   output write_bram;
   input rst;
	output [3:0] state;
	
	wire clk;
	wire ce;
	wire [23:0] dram_addr;
	wire bram_full;
	wire rd_val;
	wire en;
	wire en_read;
	wire write_bram;
	wire rst;
	wire [3:0] state;
	 
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
	
	reg [3:0] actual_state=a;
	reg [3:0] next_state;
	
	reg [23:0] addr_ = 24'd0;
	reg en_read_, write_bram_;
	reg [7:0]init_counter = 8'd0;
	
	always@(posedge clk or posedge rst)begin
		if(rst)
			actual_state <= a;
		else
			actual_state <= next_state;
	end
	
	always@(*)begin
		case(actual_state)
		a:
			begin
				addr_ = 0;
				en_read_ = 0;
				write_bram_ = 0;
				init_counter = 8'd0;
			end
		c:
			en_read_ = 1;
		d:
			en_read_ = 1;
		e:
			en_read_ = 0;
		f:
			write_bram_ = 1;
		g:
			write_bram_ = 0;
		i:
			addr_ = addr_+1;
		j:
			init_counter = init_counter +1;
		endcase
	end
	
	
	always@(posedge clk)begin
		case(actual_state)
			a:
				next_state = b;
			b:
				if(en)		next_state = j;
				else			next_state = b;
			c:
				next_state = d;
			d:
				next_state = e;
			e:
				if(rd_val)	next_state = f;
				else			next_state = e;
			f:
				next_state = g;
			g:
				if(bram_full)	next_state = h;
				else				next_state = i;
			h:
				if(bram_full)	next_state = h;
				else				next_state = i;
			i:
				next_state = c;
			j:
				if(init_counter>8'd128)	next_state = c;
				else 					next_state = j;
		endcase
	end
	
	
	assign addr = addr_;
	assign en_read = en_read_;
	assign write_bram = write_bram_;
	assign state = actual_state;
endmodule
