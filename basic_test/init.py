import numpy as np
import corr
import struct
import time

IP = '192.168.0.40'
#bof = 'sim_dram.bof' #has the old controller /SMA/mlib_dev/sim_dram3
bof = 'basic_test.bof'

fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(2)

fpga.write_int('rst',1)
fpga.write_int('read',0)

fpga.write_int('write',1)
fpga.write_int('addr', 10)
fpga.write_int('input', 1023)


fpga.write_int('addr',11)
fpga.write_int('input', 100)

fpga.write_int('write',0)
fpga.write_int('addr',10)
print(fpga.read_int('output'))

fpga.write_int('rst',0)
fpga.write_int('read',1)

print(fpga.read_int('output'))

fpga.write_int('addr',11)
fpga.write_int('read',0)
fpga.write_int('read',1)




data = struct.unpack('>1024I', fpga.read('vals', 1024*4))
