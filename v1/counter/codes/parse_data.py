import ctypes 
import numpy as np
import struct
import corr
import matplotlib.pyplot as plt

lib = ctypes.CDLL('./parse_data.so')

lib.parse_data.argtypes = [ctypes.c_char_p, ctypes.c_int]
lib.parse_data.restype = ctypes.POINTER(ctypes.c_char)
lib.freeptr.argtype = ctypes.c_void_p
lib.freeptr.restype = None        #the output of freeptr is void

"""Just a little example
asd = "\x23"
qwe = lib.parse_data(asd, 1)

print(qwe[0])
print(qwe[1])

lib.freeptr(qwe)
"""






