/*
TODO:
- add openmp stuff
- compare our sha1 vs. openssl sha1

docker compose exec main gcc -fopenmp -o ./src/3_ctypes/test_hashcat-v3 ./src/3_ctypes/test_hashcat-v3.c -lcrypto -lssl
docker compose exec main ./src/3_ctypes/test_hashcat-v3 aaa
rm -rf ./src/3_ctypes/test_hashcat-v3
*/

