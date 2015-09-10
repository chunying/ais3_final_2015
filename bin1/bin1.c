#include <stdio.h>

unsigned char encrypted[] = {
	0xca, 0x70, 0x93, 0xc8, 0x06, 0x54, 0xd2, 0xd5, 0xda, 0x6a,
	0xd1, 0x59, 0xde, 0x45, 0xf9, 0xb5, 0xa6, 0x87, 0x19, 0xa5,
	0x56, 0x6e, 0x63, 0x00
};

int
decode() {
	int i;
	for(i = 0; i < 23; i++) {
		int shift = (i ^ 9) & 3;
		unsigned char ch = encrypted[i];
		ch -= 8;
		ch = (ch >> shift) | (ch << (8 - shift));
		ch ^= i;
		printf("%c", ch);
	}
	printf("\n");
	return 0;
}

int
main(int argc, char *argv[]) {
	decode();
	return 0;
}

