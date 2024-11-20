/*
docker compose exec main gcc -fopenmp -o ./src/3_cffi/test-hashcat ./src/3_cffi/test-hashcat.c -lcrypto -lssl
docker compose exec main ./src/3_cffi/test-hashcat aaa
rm -rf ./src/3_cffi/test-hashcat
*/

#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>

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

bool try_password(char *current, int position, int length, const char *target_hash) {
    if (position == length) {
        char hashed[SHA_DIGEST_LENGTH * 2 + 1];
        sha1_hash(current, hashed);
        return strcmp(hashed, target_hash) == 0;
    }

    for (int i = 0; i < ALPHABET_SIZE; i++) {
        current[position] = alphabet[i];
        if (try_password(current, position + 1, length, target_hash)) {
            return true;
        }
    }
    return false;
}

char* hashcat(const char *target_hash) {
    char *current = malloc(MAX_LENGTH + 1);
    if (!current) return NULL;

    for (int length = 1; length <= MAX_LENGTH; length++) {
        current[length] = '\0';
        if (try_password(current, 0, length, target_hash)) {
            return current;
        }
    }
    
    free(current);
    return NULL;
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <password>\n", argv[0]);
        return 1;
    }

    char hashed[SHA_DIGEST_LENGTH * 2 + 1];
    sha1_hash(argv[1], hashed);
    
    char *result = hashcat(hashed);
    if (result) {
        // assert that result is the same as argv[1]
        assert(strcmp(result, argv[1]) == 0);
        printf("success\n");
        free(result);
        return strcmp(result, argv[1]) == 0 ? 0 : 1;
    }
    
    printf("failure\n");
    return 1;
}
