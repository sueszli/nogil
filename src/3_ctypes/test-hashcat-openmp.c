/*
docker compose exec main gcc -fopenmp -o ./src/3_ctypes/test-hashcat-openmp ./src/3_ctypes/test-hashcat-openmp.c -lcrypto -lssl
docker compose exec main ./src/3_ctypes/test-hashcat-openmp a
rm -rf ./src/3_ctypes/test-hashcat-openmp
*/

#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>
#include <omp.h>

#define MAX_LENGTH 8
#define ALPHABET_SIZE 62

const char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";

void sha1_hash(const char *input, char *output) {
    unsigned char hash[SHA_DIGEST_LENGTH];
    SHA_CTX ctx;
    SHA1_Init(&ctx);
    SHA1_Update(&ctx, input, strlen(input));
    SHA1_Final(hash, &ctx);
    
    for(int i = 0; i < SHA_DIGEST_LENGTH; i++) {
        sprintf(output + (i * 2), "%02x", hash[i]);
    }
    output[SHA_DIGEST_LENGTH * 2] = '\0';
}

char* hashcat(const char *target_hash) {
    char *current = malloc(MAX_LENGTH + 1);
    if (!current) return NULL;

    current[MAX_LENGTH] = '\0'; // Null-terminate the string

    for (int length = 1; length <= MAX_LENGTH; length++) {
        for (int position = 0; position < length; position++) {
            for (int i = 0; i < ALPHABET_SIZE; i++) {
                current[position] = alphabet[i];

                if (position == length - 1) { // If we reached the end of the current combination
                    char hashed[SHA_DIGEST_LENGTH * 2 + 1];
                    sha1_hash(current, hashed);
                    if (strcmp(hashed, target_hash) == 0) {
                        return current; // Found matching hash
                    }
                }
            }
        }
    }

    free(current);
    return NULL;
}

int main(int argc, char *argv[]) {
    assert(argc == 2);
    char hashed[SHA_DIGEST_LENGTH * 2 + 1];
    sha1_hash(argv[1], hashed);
    
    char *result = hashcat(hashed);
    if (result) {
        char success = strcmp(result, argv[1]) == 0;
        free(result);
        if (success) {
            printf("success\n");
            return 0;
        }
    }
    
    printf("failure\n");
    return 1;
}
