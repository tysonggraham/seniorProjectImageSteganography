from PIL import Image
import binascii
import optparse

def rgb2hex(r, g, b):
	return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def hex2rgb(hexcode):
	return tuple(map(ord, hexcode[1:].decode('hex')))

def str2bin(message):
	binary = bin(int(binascii.hexlify(message), 16))
	# Adds a 0b at the front
	return binary[2:]

def bin2str(binary):
	message = binascii.unhexlify('%x' % (int('0b' + binary, 2)))
	return message

# Digit is 0 or 1 to encode into hexcode
def encode(hexcode, digit):
	if hexcode[-1] in ('0', '1', '2', '3', '4', '5'):
		hexcode = hexcode[:-1] + digit
		return hexcode
	else:
		return None

def decode(hexcode):
	if hexcode[-1] in ('0', '1'):
		return hexcode[-1]
	else:
		return None

def hide(filename, message):
	img = Image.open(filename)
	binary = str2bin(message) + '1111111111111110'
	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		image_data = img.getdata()

		newData = []
		digit = 0
		temp = ''

		for pixel_data in image_data:
			if (digit < len(binary)):
				newpix = encode(rgb2hex(pixel_data[0], pixel_data[1], pixel_data[2]), binary[digit])
				if(newpix == None):
					newData.append(pixel_data)
				else: 
					r, g, b = hex2rgb(newpix)
					newData.append((r,g,b,255))
					digit += 1
			else:
				newData.append(pixel_data)
		img.putdata(newData)
		img.save("newfile.png", "PNG")
		return "Completed!"
	return "Incorrect Image Mode Detected: Couldn't hide message!"

def retr(filename):
	img = Image.open(filename)
	binary = ''

	if img.mode in ('RGBA'):
		img = img.convert('RGBA')
		image_data = img.getdata()

		for pixel_data in image_data:
			digit = decode(rgb2hex(pixel_data[0], pixel_data[1], pixel_data[2]))
			if digit == None:
				pass
			else:
				binary += digit
				if (binary[-16:] == '1111111111111110'):
						print "Success"
						return bin2str(binary[:-16])
		# Message was too big
		return bin2str(binary)
	return "Incorrect Image Mode: Could Not Retrieve!"

def Main():
	parser = optparse.OptionParser("usage %prog " + \
		'-e/-d <target file>')
	parser.add_option('-e', dest='hide', type='string', \
		help='target Picture Path To Hide Text')
	parser.add_option('-d', dest='retr', type='string', \
		help='target picture path to retrieve the text from')

	(options, args) = parser.parse_args()
	if (options.hide != None):
		text = raw_input('Enter the message to hide: ')
		print hide(options.hide, text)
	elif (options.retr != None):
		print retr(options.retr)
	else:
			print parser.usage
			exit(0)

if __name__ == '__main__':
	Main()
