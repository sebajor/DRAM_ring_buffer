import corr, time, struct, sys, ctypes
import numpy as np
import matplotlib.pyplot as plt
import socket
from snapshot import plot_snap, plot_spectrums

lib = ctypes.CDLL('./parse_data2.so')

lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
lib.freeptr.argtype = ctypes.c_void_p
lib.freeptr.restype = None 


##initialize socket
pkt_sock = 36*220
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('10.0.0.29', 1234)
print('starting up on {} port {}'.format(*server_address))
sock.bind(server_address)
f = open('data', 'wb')


##gain
gain = 1


##gbe parameters
pkt_size = 36*220-2
idle =25000#20000
n_pkt = 10

dest_ip = 10*(2**24) + 0*(2**16) + 0*(2**8)+29 #192*(2**24) + 168*(2**16) + 1*(2**8)+29
fabric_port=1234
source_ip= 10*(2**24) + 0*(2**16) + 0*(2**8)+45 #192*(2**24) + 168*(2**16) + 1*(2**8)+45 #10.0.0.20

tx_core_name = 'one_GbE'
mac_base=(2<<40) + (2<<32)

##connect and upload model
fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'adc_3chann.fpg'

fpga.upload_program_bof(bof,3000)
time.sleep(1)
fpga.write_int('gain',gain)

plot_snap(fpga)
plot_spectrums(fpga)


##initialize parameters
## write_read: write, read, rst, rst_read, gbe_auto, rst_pkt
##

##configure ethernet 
fpga.tap_start('tx_tap',tx_core_name,mac_base+source_ip,source_ip,fabric_port)
time.sleep(1)
fpga.write_int('gbe_dest_ip', dest_ip)
fpga.write_int('gbe_dest_port', fabric_port)

fpga.write_int('control',2)
fpga.write_int('control',0)

#configure the ring buffer for reading
fpga.write_int('ring_configuration', 0b101100) #rst everything
fpga.write_int('ring_n_pkt', n_pkt)
fpga.write_int('ring_gbe_idle', idle)
#fpga.write_int('gbe_pkt_size', pkt_size)
fpga.write_int('ring_configuration',0)
fpga.write_int('ring_configuration', 1) #enable writing


## we have to enble the writing from outside
fpga.write_int('control',1)
time.sleep(1)
start = time.time()
#fpga.write_int('write_read', 0b10000)
#fpga.write_int('write_read', 0b10010) #read 1 burst of 220 
fpga.write_int('control',0)
#time.sleep(0.5)
#data = sock.recv(pkt_sock)


time.sleep(0.2)
fpga.write_int('ring_configuration', 0b110000)
fpga.write_int('ring_configuration', 0b010010) #read 1 burst of 220 
"""
for i in range(n_pkt+1):
    print(i)
    data = sock.recv(pkt_sock)
    f.write(data[:])
"""

#read whole dram
#takes 3 minutes!
for i in range(762*20):
    data = ""
    for j in range(n_pkt+1):
        data =data+sock.recv(pkt_sock)
    f.write(data[:])
    print(str(i)+"\t "+str(len(data)))
    if(i%50==1):
        time.sleep(0.2)
    fpga.write_int('ring_configuration', 0b110000)
    fpga.write_int('ring_configuration', 0b010010) #read 1 burst of 220 
    #if(i%30==1):
        #time.sleep(1)
end = time.time()
print("took %.4f secs read dram" %(end-start))


sock.close()
f.close()

"""ex
dat0_parse = lib.parse_data(data, len(data))
dat0_char = np.array(struct.unpack(str(len(data)*2)+'B', dat0_parse[0:len(data)*2]))
lib.freeptr(dat0_parse)
aux = dat0_char.reshape(len(dat0_char)/24,24) 
aux = aux[:,:8].flatten() #revisar los armonicos!!!!


"""



