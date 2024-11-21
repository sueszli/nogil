#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>

#define MAX_LENGTH 8

char* hashcat(const char *target_hash) {
    const char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    const int alphabet_size = 62;

    char *current = malloc(MAX_LENGTH + 1);
    if (!current) {
        return NULL;
    }

    int position[MAX_LENGTH] = {0};
    for (int length = 1; length <= MAX_LENGTH; length++) {
        while (true) {
            for (int i = 0; i < length; i++) {
                current[i] = alphabet[position[i]];
            }
            current[length] = '\0';

            char hashed[SHA_DIGEST_LENGTH * 2 + 1];
            unsigned char hash[SHA_DIGEST_LENGTH];
            SHA_CTX ctx;
            SHA1_Init(&ctx);
            SHA1_Update(&ctx, current, strlen(current));
            SHA1_Final(hash, &ctx);
            
            for(int i = 0; i < SHA_DIGEST_LENGTH; i++) {
                sprintf(hashed + (i * 2), "%02x", hash[i]);
            }
            hashed[SHA_DIGEST_LENGTH * 2] = '\0';
            if (strcmp(hashed, target_hash) == 0) {
                return current;
            }

            int idx = 0;
            while (idx < length) {
                position[idx]++;
                if (position[idx] < alphabet_size) {
                    break;
                }
                position[idx] = 0;
                idx++;
            }

            if (idx == length) {
                break;
            }
        }
    }

    free(current);
    return NULL;
}
