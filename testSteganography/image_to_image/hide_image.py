#!/usr/bin/env python
import sys
import Image, ImageOps

def extract_image(from_image, s=4):
	data = Image.open(from_image)
	for x in range(data.size[0]):
		for y in range(data.size[1]):
			p = data.getpixel((x, y))
			red    = (p[0] % s) + (s * q[0] / 255)
			green  = (p[1] % s) + (s * q[2] / 255)
			blue   = (p[2] % s) + (s * q[2] / 255)
			data.putpixel((x,y), (red, green, blue))
		return data

def give_help():
	print "wrong, try:"
	print "%s show from.jpg" % sys.argv[0]
	print "%s hide public.jpg secret.jpg" % sys.argv[0]