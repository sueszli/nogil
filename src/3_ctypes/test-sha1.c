/*
python -c "import hashlib; print(hashlib.sha1('wassup'.encode()).hexdigest())"

docker compose exec main gcc -fopenmp -o ./src/3_ctypes/test-sha1 ./src/3_ctypes/test-sha1.c ./src/3_ctypes/sha1.c
docker compose exec main ./src/3_ctypes/test-sha1
rm -rf ./src/3_ctypes/test-sha1
*/

#include "sha1.h"
#include <string.h>
#include <stdio.h>

void sha1_hash(const char* input, BYTE hash_output[SHA1_BLOCK_SIZE]) {
    SHA1_CTX ctx;
    sha1_init(&ctx);
    sha1_update(&ctx, (const BYTE*)input, strlen(input));
    sha1_final(&ctx, hash_output);
}

int main() {
    const char* message = "wassup";
    BYTE hash[SHA1_BLOCK_SIZE];
    sha1_hash(message, hash);
    
    for(int i = 0; i < SHA1_BLOCK_SIZE; i++) {
        printf("%02x", hash[i]);
    }
    printf("\n");
    
    return 0;
}
