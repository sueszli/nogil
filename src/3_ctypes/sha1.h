// https://github.com/B-Con/crypto-algorithms/blob/master/sha1.h

#ifndef SHA1_H
#define SHA1_H

#include <stddef.h>
#define SHA1_BLOCK_SIZE 20   // SHA1 outputs a 20 byte digest
typedef unsigned char BYTE;  // 8-bit byte
typedef unsigned int  WORD;  // 32-bit word, change to "long" for 16-bit machines

typedef struct {
	BYTE data[64];
	WORD datalen;
	unsigned long long bitlen;
	WORD state[5];
	WORD k[4];
} SHA1_CTX;

void sha1_init(SHA1_CTX *ctx);
void sha1_update(SHA1_CTX *ctx, const BYTE data[], size_t len);
void sha1_final(SHA1_CTX *ctx, BYTE hash[]);

#endif // SHA1_H
