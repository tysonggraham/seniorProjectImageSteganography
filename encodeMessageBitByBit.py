userInput = input('Please enter a string to encode: ')
for x in userInput:
	x = ord(x)
	# print(bin(x))
	for i in range(8):
		print (x & 1)
		x = x >> 1
