import sys
import struct
import numpy
import matplotlib.pyplot as plt

from PIL import Image

# Decompose a binary file into an array of bits
def decompose(data):
	#the array of bits we will fill
	v = []
	
	#Length of the file. Will be used in the nex loop
	fSize = len(data)

	#add the header onto the string. This will tell us when to stop reading.
	bytes = [ord(b) for b in struct.pack("i", fSize)]
	
	#now add the rest of the data onto the string.
	bytes += [ord(b) for b in data]

	#append each byte in the string to the array. Bitwise and each one to turn them into pure 1's and 0's
	for b in bytes:
		#append each bit to the array starting from the LSB to the MSB. Bitwise and it with a 1 to grab the original value
		for i in range(7, -1, -1):
			v.append((b >> i) & 0x1)

	return v

# Assemble an array of bits into a binary file
def assemble(v):    
	bytes = ""

	length = len(v)
	for idx in range(0, len(v)//8):
		byte = 0
		for i in range(0, 8):
			if (idx*8+i < length):
				byte = (byte<<1) + v[idx*8+i]                
		bytes = bytes + chr(byte)

	size_of_file_to_hide = struct.unpack("i", bytes[:4])[0]

	# size_of_file_to_hide = struct.unpack("i", bytes[:4])[0]

	return bytes[4: size_of_file_to_hide + 4]

# Set the i-th bit of v to x
def set_bit(n, i, x):
	mask = 1 << i
	n &= ~mask
	if x:
		n |= mask
	return n

# Embed payload file into LSB bits of an image
def embed(hide_stuff_in_file, file_we_want_to_hide):
	# Process source image
	img = Image.open(hide_stuff_in_file)
	(width, height) = img.size
	conv = img.convert("RGBA").getdata()
	print("[*] Input image size: %dx%d pixels." % (width, height))
	max_size = width*height*3.0/8/1024		# max file_we_want_to_hide size
	print("[*] Usable file_we_want_to_hide size: %.2f KB." % (max_size))

	f = open(file_we_want_to_hide, "rb")
	data = f.read()
	f.close()
	print ("[+] file_we_want_to_hide size: %.3f KB " % (len(data)/1024.0))
		
	# Encypt
	# cipher = AESCipher(password)
	# data_enc = cipher.encrypt(data)

	# Process data from file_we_want_to_hide file
	v = decompose(data)
	#v = decompose(data_enc)
	
	#add until divisible by 3 so we can divide the bits into rgb values
	while(len(v)%3):
		v.append(0)

	#turn the filesize into kb's
	size_of_file_to_hide = len(v)/8/1024.0
	print("[+] Encrypted file_we_want_to_hide size: %.3f KB " % (size_of_file_to_hide))
	#if the file we want to hide is larger than the max size plus stop reader header
	if (size_of_file_to_hide > max_size - 4):
		print("[-] Cannot embed. File too large")
		sys.exit()
		
	# Create output image
	file_with_hidden_image = Image.new('RGBA',(width, height))
	data_of_file_with_hidden_image = file_with_hidden_image.getdata()

	idx = 0

	for h in range(height):
		for w in range(width):
			(r, g, b, a) = conv.getpixel((w, h))
			if idx < len(v):
				r = set_bit(r, 0, v[idx])
				g = set_bit(g, 0, v[idx+1])
				b = set_bit(b, 0, v[idx+2])
			data_of_file_with_hidden_image.putpixel((w,h), (r, g, b, a))
			idx = idx + 3
    
	file_with_hidden_image.save("stego.png", "PNG")
	
	print("[+] %s embedded successfully!" % file_we_want_to_hide)

# Extract data embedded into LSB of the input file
def extract(stuff_is_hidden_in_this_file, revealed_image_file):
	# Process source image
	img = Image.open(stuff_is_hidden_in_this_file)
	(width, height) = img.size
	conv = img.convert("RGBA").getdata()
	print("[+] Image size: %dx%d pixels." % (width, height))

	# Extract LSBs
	v = []
	for h in range(height):
		for w in range(width):
			(r, g, b, a) = conv.getpixel((w, h))
			v.append(r & 1)
			v.append(g & 1)
			v.append(b & 1)
			
	data_out = assemble(v)

	# set up a file to write output to.
	out_f = open(revealed_image_file, "wb")
	# Write inserted hidden bits to output file.
	out_f.write(data_out)

	out_f.close()
	
	print("[+] Written extracted data to %s." % revealed_image_file)

def usage(progName):
	print("LSB steganogprahy. Hide files within least significant bits of image.\n")
	print("Usage:")
	print("  %s hide <file_we_want_to_hide_stuff_in> <file_we_want_to_hide>" % progName)
	print("  %s extract <file_with_hidden_image> <file_with_revealed_image>" % progName)
	sys.exit()
	
if __name__ == "__main__":
	if len(sys.argv) < 3:
		usage(sys.argv[0])
		
	if sys.argv[1] == "hide":		
		embed(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == "extract":
		extract(sys.argv[2], sys.argv[3])
	else:
		print("[-] Invalid operation specified")