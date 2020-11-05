import corr
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from matplotlib.animation import FuncAnimation

IP = '192.168.0.40'
#bof = 'sim_dram.bof' #has the old controller /SMA/mlib_dev/sim_dram3
bof = 'dram_fsm2.bof'

fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(2)

fpga.write_int('gain',1)
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
time.sleep(12)

fpga.write_int('en_write', 0)
print('dram escrita')

iterations = 2**11
par = np.zeros([8192, iterations])

fpga.write_int('read',1)
time.sleep(2)
fpga.read_int('bram_full1')
par = struct.unpack('>8192I',fpga.read('brams_parity', 2**13*4,0))



##todavia se salta algunas direcciones.. revisar 
##que wea las ultimas direcciones
##tmb revisar por que se escriben dir que estan iguales

"""
par = struct.unpack('>8192I',fpga.read('brams_parity', 2**13*4,0))
diff = np.diff(par)
ind = np.where(diff!=1)[0]
fpga.write_int('user_addressing',1)
"""
