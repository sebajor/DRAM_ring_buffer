import dram_class
import corr, ctypes, time
from snapshot import plot_snap, plot_spectrums


lib = ctypes.CDLL('./parse_data2.so')

lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
lib.freeptr.argtype = ctypes.c_void_p
lib.freeptr.restype = None

fpga = corr.katcp_wrapper.FpgaClient('192.168.0.40')
time.sleep(1)
bof = 'adc_3chann.fpg'

gain=1
fpga.upload_program_bof(bof,3000)
time.sleep(1)
fpga.write_int('gain',gain)

plot_snap(fpga)
plot_spectrums(fpga)

dram_ring = dram_class.dram_ring(fpga)
time.sleep(1)
dram_ring.init_ring()
time.sleep(1)
fpga.write_int('control',0) ##this should be done in hardware! jus add an or at 
                            ##at the input
dram_ring.reading_dram()

