import sys
import struct
import numpy
import matplotlib.pyplot as plt

from PIL import Image

from crypt import AESCipher


# Decompose a bin]ary file into an array of bits
def decompose(data):
	#array of bits
	v = []
	
	# Pack file len in 4 bytes
	fSize = len(data);
	#take b and turn it into its ascii value.
	print('data')
	# print(data)
	# print('fSize')
	# print(fSize)
	
	bytes = [ord(b) for b in struct.pack("i", fSize)]
	
	#sum all of the ascii values together
	bytes += [ord(b) for b in data]

	#This is where we iterate through the bytes and append to the array v
	for b in bytes:
		for i in range(7, -1, -1):
			#Shift b over i bits. Then and with 0001
			v.append((b >> i) & 0x1)

	return v
decompose(['1000'])
