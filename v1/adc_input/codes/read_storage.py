import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import spectrogram

dram_size = 2**30     #1Gb of data
addr_size = 64
bram_size = 2**13*addr_size

dirs = dram_size/bram_size

fft_size = 1024

plot_data = np.zeros([fft_size/2+1,dirs])

for i in range(dirs):
    data = np.memmap('dram_data2', mode='r',shape=(1,bram_size), offset=bram_size*i)
    f,t,Sxx = spectrogram(data[0], fs=1080, nperseg=1024)
    plot_data[:,i] = Sxx[:,40] #40 is in the middle... check how to obtain this number
    del data





plt.pcolormesh(np.arange(dirs),f,20*np.log10(plot_data))
plt.show() 




