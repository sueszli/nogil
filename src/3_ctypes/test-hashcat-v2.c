/*
docker compose exec main gcc -fopenmp -o ./src/3_ctypes/test-hashcat-v2 ./src/3_ctypes/test-hashcat-v2.c -lcrypto -lssl
docker compose exec main ./src/3_ctypes/test-hashcat-v2 aaa
rm -rf ./src/3_ctypes/test-hashcat-v2
*/

#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>

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

#define MAX_LENGTH 8
#define ALPHABET_SIZE 62

bool try_password(char *current, int length, const char *target_hash) {
    const char alphabet[] = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    int position[MAX_LENGTH] = {0};

    while (true) {
        for (int i = 0; i < length; i++) {
            current[i] = alphabet[position[i]];
        }
        current[length] = '\0';

        char hashed[SHA_DIGEST_LENGTH * 2 + 1];
        sha1_hash(current, hashed);
        if (strcmp(hashed, target_hash) == 0) {
            return true;
        }

        int idx = 0;
        while (idx < length) {
            position[idx]++;
            if (position[idx] < ALPHABET_SIZE) {
                break;
            }
            position[idx] = 0;
            idx++;
        }

        if (idx == length) {
            break;
        }
    }

    return false;
}

char* hashcat(const char *target_hash) {
    char *current = malloc(MAX_LENGTH + 1);
    if (!current) return NULL;

    for (int length = 1; length <= MAX_LENGTH; length++) {
        if (try_password(current, length, target_hash)) {
            return current;
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
