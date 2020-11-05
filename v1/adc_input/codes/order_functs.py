import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import struct
import ipdb


def order_data(filename, point_index):
    """
    """
    #the dram has 2**24 addrs, we read this in
    #blocks of 2**13, we have 2**11 of those blocks
    #each block has 2**13*64 bytes


    dram_addrs = 2**24
    addr_size = 64
    block_size = 2**13
    block_bitesize = block_size*addr_size
    
    beg_block = point_index/block_size  #begining block
    offset_beg = point_index%block_size
    
    f = file('order_data', 'a')

    #1 read to complete the first blocksize

    if (offset_beg>0):
        data = np.memmap(filename, mode='r', shape=(1, (8192-offset_beg)*addr_size), offset=beg_block*block_bitesize+offset_beg*addr_size)
        raw_data = struct.pack('>'+str(len(data[0]))+'B', *data[0])
        f.write(raw_data)
        del data
    
    #2 read from the beg_block to the end of the file
    
    n_iter = 2**11-(beg_block+1)

    for i in range(n_iter):
        data = np.memmap(filename, mode='r', shape=(1, block_bitesize), offset=(beg_block+1)*block_bitesize+block_bitesize*i)
        raw_data = struct.pack('>'+str(len(data[0]))+'B', *data[0])
        f.write(raw_data)
        del data

    #3 read from to the beg_block

    for i in range(beg_block):
        data = np.memmap(filename, mode='r', shape=(1, block_bitesize), offset=block_bitesize*i)
        raw_data = struct.pack('>'+str(len(data[0]))+'B', *data[0])
        f.write(raw_data)
        del data

    #4 read from block_size to the beginig at miss offset

    data = np.memmap(filename, mode='r',shape=(1,(offset_beg)*addr_size), offset=beg_block*block_bitesize)
    raw_data = struct.pack('>'+str(len(data[0]))+'B', *data[0])
    f.write(raw_data)
    del data
    f.close()

        

def plot_spectrogram(filename):
    dram_size = 2**30     #1Gb of data
    addr_size = 64
    bram_size = 2**13*addr_size

    dirs = dram_size/bram_size

    fft_size = 1024

    plot_data = np.zeros([fft_size/2+1,dirs])

    for i in range(dirs):
        data = np.memmap(filename, mode='r',shape=(1,bram_size), offset=bram_size*i)
        f,t,Sxx = spectrogram(data[0], fs=1080, nperseg=1024)
        plot_data[:,i] = Sxx[:,40] #40 is in the middle... check how to obtain this number
        del data

    fpga_clk = 67.5*10**6
    total_time = 2**24*4/(fpga_clk)
    t = np.linspace(0,total_time, dirs)
    plt.xlabel('Time[s]')
    plt.ylabel('Frequency[MHz]')
    plt.pcolormesh(t,f,20*np.log10(plot_data))
    plt.show()



