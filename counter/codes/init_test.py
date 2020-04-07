import corr
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from matplotlib.animation import FuncAnimation
import ctypes


lib = ctypes.CDLL('./parse_data.so')

lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
lib.freeptr.argtype = ctypes.c_void_p
lib.freeptr.restype = None 

"""In this model the counters are 1 sample ahead each one
so in one address we should get a upper ladder of values
Except I made a mistake so one value is repeated in two counter
per cycles...but is good to look if the data read is fine

"""

IP = '192.168.0.40'
#bof = 'sim_dram.bof' #has the old controller /SMA/mlib_dev/sim_dram3
bof = 'dram_fsm.bof.gz'

fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(2)

fpga.write_int('gain',2**4-1)
#fpga.write_int('thresh_read', 4096)
fpga.write_int('user_addressing',0)



fpga.write_int('read',0)
fpga.write_int('rst_brams',1)
fpga.write_int('rst_brams',0)
#fpga.write_int('test_mode',1) #nose xq esta al reves :(
#fpga.write_int('thresh_read',8192)
fpga.write_int('rst',1)
#fpga.write_int('test_missing',2**24-2)
#fpga.write_int('last_dir_miss_read',9)
time.sleep(0.5)
fpga.write_int('en_write',1)
fpga.write_int('rst',0)




print('escribiendo dram')
time.sleep(5)

fpga.write_int('en_write', 0)
print('dram escrita')

iterations = 2**11
par = np.zeros([8192, iterations])

fpga.write_int('read',1)
time.sleep(3)

while(1):
    if (fpga.read_int('bram_full1')):
        break


len_data = 8192*16

par = struct.unpack('>8192I',fpga.read('brams_parity', 2**13*4,0))
dat0 = fpga.read('brams_dat0', len_data)
dat1 = fpga.read('brams_dat1', len_data)


dat0_parse = lib.parse_data(dat0[:len_data],len_data)
dat0_char = np.array(struct.unpack('>'+str(len_data*2)+'B', dat0_parse[0:len_data*2]))
lib.freeptr(dat0_parse)

dat1_parse = lib.parse_data(dat1[:len_data],len_data)
dat1_char = np.array(struct.unpack('>'+str(len_data*2)+'B', dat1_parse[0:len_data*2]))
lib.freeptr(dat1_parse)


##order the data, the first 16 correspond to the n+1 bits
##ie the odd data is first than the even

dat0_ = dat0_char.reshape([len_data*2/16, 16])
dat1_ = dat1_char.reshape([len_data*2/16, 16])


dat0_even = dat0_[::2,:]
dat0_odd  = dat0_[1::2,:]
dat1_even = dat1_[::2,:]
dat1_odd  = dat1_[1::2,:]


vals = np.hstack([dat0_odd, dat0_even, dat1_odd, dat1_even])





