# docker compose exec main gcc -shared -o ./src/4_cpython/fibmodule.so -fPIC -I/usr/local/include/python3.13t ./src/4_cpython/test_fib.c
# docker compose exec main python3 ./src/4_cpython/test_fib.py

import fibmodule

print(fibmodule.__doc__)
print(dir(fibmodule))
print(fibmodule.fib.__doc__)

print(fibmodule.fib(35))
