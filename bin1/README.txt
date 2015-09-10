
note: binary evaluation32_a and evaluation64_a are from tyler

Here is my sample solution

## strategy #1

Reverse it and you can see
- main() passes argv[1] to verify()
- verify() does some computations for each character in argv[1] and compare
  the obtained byte against a buffer @ 0x804a014
- The buffer length is 23 bytes, and so does the flag
- See bin1.c for the codes to decode the buffer @ 0x804a014

## strategy #2

Use pin tools
A sample command to count instructions:

pin -injection child -t /source/tools/ManualExamples/obj-intel64/inscount0.so \
	-- /path/to/evaluation64_a a

Given the same length of input strings, a correct input string should have a
higher instructions count. Based on this observation, you can implement a
simple brute-force attack to reveal the correct flag.

