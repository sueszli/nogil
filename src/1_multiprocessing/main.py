def timeit(func) -> callable:
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__}: {end - start:.5f}s")
        return result

    return wrapper


def hash_password(password):
    from hashlib import sha1

    return password, sha1(password.encode()).hexdigest()


@timeit
def hashcat_imap_unordered(target_hash, max_length=8):
    import itertools
    import multiprocessing
    import string

    alphabet = string.ascii_letters + string.digits
    with multiprocessing.Pool(
        processes=multiprocessing.cpu_count(),
        maxtasksperchild=max(100_000, 10_000 * len(alphabet) ** max_length),
    ) as pool:
        for length in range(1, max_length + 1):
            guesses = ("".join(guess) for guess in itertools.product(alphabet, repeat=length))
            for password, hashed in pool.imap_unordered(hash_password, guesses):
                if hashed == target_hash:
                    pool.terminate()
                    return password
    return None


@timeit
def hashcat_imap(target_hash, max_length=8):
    import itertools
    import multiprocessing
    import string

    alphabet = string.ascii_letters + string.digits
    with multiprocessing.Pool(
        processes=multiprocessing.cpu_count(),
        maxtasksperchild=max(100_000, 10_000 * len(alphabet) ** max_length),
    ) as pool:
        for length in range(1, max_length + 1):
            guesses = ("".join(guess) for guess in itertools.product(alphabet, repeat=length))
            for password, hashed in pool.imap(hash_password, guesses):
                if hashed == target_hash:
                    pool.terminate()
                    return password
    return None


@timeit
def hashcat_map(target_hash, max_length=8):
    import itertools
    import multiprocessing
    import string

    alphabet = string.ascii_letters + string.digits
    with multiprocessing.Pool(
        processes=multiprocessing.cpu_count(),
        maxtasksperchild=max(100_000, 10_000 * len(alphabet) ** max_length),
    ) as pool:
        for length in range(1, max_length + 1):
            guesses = ("".join(guess) for guess in itertools.product(alphabet, repeat=length))
            for password, hashed in pool.map(hash_password, guesses):
                if hashed == target_hash:
                    pool.terminate()
                    return password
    return None


if __name__ == "__main__":
    import hashlib

    password = "abc"
    hashed = hashlib.sha1(password.encode()).hexdigest()

    out = hashcat_imap_unordered(hashed)
    out = hashcat_imap(hashed)
    out = hashcat_map(hashed)
