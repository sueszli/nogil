/*
python -c "import hashlib; print(hashlib.sha1('wassup'.encode()).hexdigest())"

docker compose exec main gcc -fopenmp -o ./src/3_cffi/test-openssl ./src/3_cffi/test-openssl.c -lcrypto -lssl
docker compose exec main ./src/3_cffi/test-openssl
rm -rf ./src/3_cffi/test-openssl
*/


#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>

int main(int argc, char *argv[]) {
    unsigned char temp[SHA_DIGEST_LENGTH];
    char buf[SHA_DIGEST_LENGTH*2 + 1];
    const char *string = "wassup";
    
    SHA1((unsigned char *)string, strlen(string), temp);
    
    for (int i = 0; i < SHA_DIGEST_LENGTH; i++) {
        sprintf((char*)&(buf[i*2]), "%02x", temp[i]);
    }
    
    printf("%s\n", buf);
    return 0;
}
