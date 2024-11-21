usage:

```bash
# 
# prepare environment
# 

# compile cpython
make docker-up # takes 20min
docker compose exec main python3 -c 'import sys; assert sys.version_info >= (3, 13); assert not sys._is_gil_enabled(); print("it works!")'

# get dependencies for hyperfine, openssl
docker compose exec main apt update
docker compose exec main apt install -y build-essential apt-utils curl libssl-dev openssl
docker compose exec main sh -c 'curl --proto "=https" --tlsv1.2 -sSf https://sh.rustup.rs | sh'
docker compose exec main /root/.cargo/bin/cargo --version
docker compose exec main /root/.cargo/bin/cargo install --locked hyperfine
docker compose exec main /root/.cargo/bin/hyperfine --version

# get target hash to crack
python -c "import hashlib; print(hashlib.sha1('aaa'.encode()).hexdigest())"

# 
# benchmark
# 

# plain
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/0_plain/itertools.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +1 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/0_plain/lib.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/0_plain/plain.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv

# multiprocessing
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/1_multiprocessing/imap_unordered.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/1_multiprocessing/imap.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/1_multiprocessing/map_async.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/1_multiprocessing/map.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv

# multithreading
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "PYTHON_GIL=1 python ./src/2_multithreading/executor.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "PYTHON_GIL=0 python ./src/2_multithreading/executor.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "PYTHON_GIL=1 python ./src/2_multithreading/workers.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "PYTHON_GIL=0 python ./src/2_multithreading/workers.py 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv

# ctypes
docker compose exec main gcc -fopenmp -fPIC -shared -o ./src/3_ctypes/libhashcat.so ./src/3_ctypes/hashcat.c -lcrypto -lssl
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/3_ctypes/invoke_hashcat.py ./src/3_ctypes/libhashcat.so 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv

docker compose exec main gcc -fopenmp -fPIC -shared -o ./src/3_ctypes/libhashcat_openmp.so ./src/3_ctypes/hashcat_openmp.c -lcrypto -lssl
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/3_ctypes/invoke_hashcat.py ./src/3_ctypes/libhashcat_openmp.so 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv

# cpython
docker compose exec main gcc -shared -fopenmp -o ./src/4_cpython/hashcatmodule.so -fPIC -I/usr/local/include/python3.13t ./src/4_cpython/hashcat.c -lcrypto -lssl
docker compose exec main /root/.cargo/bin/hyperfine --warmup 3 --export-csv tmp.csv "python ./src/4_cpython/invoke_hashcat.py ./src/3_ctypes/libhashcat_openmp.so 7e240de74fb1ed08fa08d38063f6a6a91462a815" && tail -n +2 tmp.csv >> results.csv
```
