skip all previous layers of abstraction, do all the work in C right in the CPython interpreter

the goal is to outperform `hashlib.sha1`

https://github.com/sueszli/fast-snek/blob/main/c-interop/fibmodule.c
https://peps.python.org/pep-0703/#overview-of-cpython-changes
