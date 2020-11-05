module read_controller(
    clk,
    ce,
    dram_addr,
    bram_full,
    rd_val,
    en,
    en_read,
    write_bram,
    rst,
	 state,
    counter,
	 dram_val
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
	input [23:0]dram_val;
	output [3:0] state;
    output [7:0]counter;
	
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
	wire [7:0] counter;
	wire [23:0] dram_val;
	 
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
	
	
	reg [3:0] actual_state=a;
	reg [3:0] next_state;
	
	reg [23:0] addr_ = 24'd0;
	reg en_read_=0, write_bram_=0;
	reg [7:0]counter_ = 8'd0;
	
	always@(posedge clk or posedge rst)begin
		if(rst)
			actual_state <= a;
		else
			actual_state <= next_state;
	end
	
	always@(posedge clk)begin
		case(actual_state)
				a:
					begin
						counter_ = 0;
						addr_ =0;
						en_read_ = 0;
						write_bram_ = 0;
					end

				j:
					counter_ = counter_ +1;
				c:
					counter_ = 0;
				d:
					en_read_ = 1;
				e:
					en_read_ = 1;
				f:
					en_read_ = 0;
				h:
					counter_ = counter_ +1;
				i:
					write_bram_ = 1;
				k:
					write_bram_ = 0;
				m:
					addr_ = addr_+1;
		endcase
	end
	
	
	always@(*)begin
		case(actual_state)
			a:
				next_state = b;
			b:
				begin
					if(en)	next_state = j;
					else		next_state = b;
				end
			j:
				if(counter>128)	next_state = c;
				else					next_state = j;
			c:
				next_state = d;
			d:
				next_state = e;
			e:
				next_state = f;
			f:
				if(rd_val)		next_state = g;
				else				next_state = f;
			g:
				begin
					if((addr_[23:0] == dram_val[23:0]) || (counter>30)) next_state = i;
					else next_state = h;
				end
			h:
				next_state = d;
			i:
				next_state = k;
			k:
				if(bram_full) 	next_state = l;
				else 				next_state = m;
			l:
				if(bram_full)	next_state = l;
				else 				next_state = m;
			m:
				next_state = c;
		endcase
	end
	
	
	assign dram_addr[23:0] = addr_[23:0];
	assign en_read = en_read_;
	assign write_bram = write_bram_;
	assign state[3:0] = actual_state[3:0];
   assign counter[7:0] = counter_[7:0];
endmodule
