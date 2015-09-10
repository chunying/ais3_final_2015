#!/usr/bin/env python

from PIL import Image

im = Image.open("maze.png");
print "Dimension:", im.size

size = 385
print im.getpixel((size-2, 0))
print "Start: [s-1, 0] ", map(hex, im.getpixel((size-2, 0)))
print "Step1: [s-1, 1] ", map(hex, im.getpixel((size-2, 1)))
print "Step2: [s-1, 2] ", map(hex, im.getpixel((size-2, 2)))
print "Step3: [s-1, 3] ", map(hex, im.getpixel((size-2, 3)))

def inrange(m, pt):
	# check range
	w, h = m.size
	if pt[0] < 0 or pt[0] >= w: return False
	if pt[1] < 0 or pt[1] >= h: return False
	return True

def validway(m, pt):
	pix = m.getpixel(pt)
	if pix[0] == 0 and pix[1] == 0: return True	# check blue
	return False

def notvisited(m, matrix, pt):
	if inrange(m, pt) == False: return False
	pix = m.getpixel(pt)
	if pix[0] != 0 or pix[1] != 0: return False	# check blue
	if matrix[pt[1]][pt[0]] != 0: return False
	return True

def walkmaze(m, start, end):
	dirs = [(0, -1), (0, +1), (-1, 0), (+1, 0)]
	w, h = im.size
	# this one does not work
	#matrix = [[0] * w, ] * h
	matrix = [[0 for x in range(w)] for x in range(h)]
	path = []
	queue = [start]
	matrix[start[1]][start[0]] = 1
	# walk the maze
	while len(queue) > 0:
		curr = queue.pop(0)
		if curr == end:
			break;
		if validway(m, curr) == False:
			print "Invalid point", curr
			break
		for d in dirs:
			testp = (curr[0] + d[0], curr[1] + d[1])
			if notvisited(m, matrix, testp):
				matrix[testp[1]][testp[0]] = matrix[curr[1]][curr[0]] + 1
				queue.append(testp)
	# backtrack stps
	curr = end
	while curr != start:
		for d in dirs:
			testp = (curr[0] + d[0], curr[1] + d[1])
			if inrange(m, testp) == False: continue
			if matrix[testp[1]][testp[0]] == matrix[curr[1]][curr[0]] -1:
				path = [ testp ] + path
				curr = testp
				break
	return path

#path = walkmaze(im, (639, 0), (1, 640));
path = walkmaze(im, (383, 0), (1, 384));

dat = []
for p in path:
	c = im.getpixel(p)
	dat.append(chr(c[2]))	# fetch blue
dat = ''.join(dat)
fp = file('path.bin', 'wb')
fp.write(dat[0::2])
fp.close()

for p in path:
	im.putpixel(p, (0, 255, 0, 255))
im.save('output.png')
print "Steps:", len(path)

