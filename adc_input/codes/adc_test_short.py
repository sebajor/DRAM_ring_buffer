import corr
import time
import struct
import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from matplotlib.animation import FuncAnimation
import ctypes
from snapshot import plot_snap, plot_spectrums



lib = ctypes.CDLL('./parse_data.so')

lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
lib.freeptr.argtype = ctypes.c_void_p
lib.freeptr.restype = None 
IP = '192.168.0.40'
#bof = 'sim_dram.bof' #has the old controller /SMA/mlib_dev/sim_dram3
bof = 'dram_adc.bof.gz'

fpga = corr.katcp_wrapper.FpgaClient(IP)
time.sleep(1)
fpga.upload_program_bof(bof,3000)
time.sleep(2)


fpga.write_int('gain',1)

plot_snap(fpga)


##get spectrum 
plot_spectrums(fpga)


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








snap_adc = struct.unpack('>16384B',fpga.snapshot_get('adc',man_trig=True, man_valid=True)['data'])
snap_red = struct.unpack('>16384B',fpga.snapshot_get('reduce',man_trig=True, man_valid=True)['data'])

spec_red = fft(snap_red)
spec_adc = fft(snap_adc)
vals_flat = vals.flat
spec_dram = fft(vals_flat[0:16384])

freq = np.linspace(0, 540, 8192, endpoint=False)

fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312, sharex=ax1)
ax3 = fig.add_subplot(313, sharex=ax1)
ax1.grid()
ax2.grid()
ax3.grid()


plt.setp(ax2.get_xticklabels(), visible=False)
plt.setp(ax1.get_xticklabels(), visible=False)


ax1.plot(freq, 20*np.log10(np.abs(spec_adc[:8192])))
ax2.plot(freq, 20*np.log10(np.abs(spec_red[:8192])))
ax3.plot(freq, 20*np.log10(np.abs(spec_dram[:8192])))


ax1.set_title('8bits snapshot', loc='left')
ax2.set_title('4bits snapshot', loc='left')
ax3.set_title('dram', loc='left')
ax3.set_xlabel('[MHz]')

ax1.set_ylim(0,120)
ax2.set_ylim(0,120)
ax3.set_ylim(0,120)

ax1.set_ylabel('[dB]')
ax2.set_ylabel('[dB]')
ax3.set_ylabel('[dB]')

fig.suptitle('200MHz input')
plt.show()



def plot_spectrogram(data):
    f,t,Sxx = spectrogram(data, fs=1080, nperseg=1024)
    plt.pcolormesh(t,f,20*np.log10(plot_data))
    plt.show() 




