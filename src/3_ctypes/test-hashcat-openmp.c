/*
docker compose exec main gcc -fopenmp -o ./src/3_ctypes/test-hashcat-openmp ./src/3_ctypes/test-hashcat-openmp.c -lcrypto -lssl
docker compose exec main ./src/3_ctypes/test-hashcat-openmp aa
rm -rf ./src/3_ctypes/test-hashcat-openmp
*/

#include <stdio.h>
#include <string.h>
#include <openssl/sha.h>
#include <stdbool.h>
#include <stdlib.h>
#include <assert.h>
#include <omp.h>

// i have no idae how to openmp this
