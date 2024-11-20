from itertools import product
from string import ascii_letters, digits

from tqdm import tqdm

from hash.sha1 import sha1


def timeit(func) -> callable:
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.2f}s")
        return result

    return wrapper


@timeit
def crack_hash(target_hash, max_length=8):
    chars = ascii_letters + digits
    for length in range(1, max_length + 1):
        for guess in tqdm(product(chars, repeat=length)):
            password = "".join(guess)
            hashed = sha1(password.encode()).hex()
            # hashed = hashlib.sha1(password.encode()).hexdigest()
            if hashed == target_hash:
                return password
    return None


target = sha1("abc1".encode()).hex()
# target = hashlib.sha1("abc1".encode()).hexdigest()
result = crack_hash(target)
print(f"Hash: {target}")
print(f"Cracked password: {result}")
