"""
too slow, each run takes multiple seconds
"""


def hash_password(password):
    from hashlib import sha1

    return password, sha1(password.encode()).hexdigest()


def hashcat(target_hash, max_length=8):
    import concurrent.futures
    import itertools
    import multiprocessing
    import string

    alphabet = string.ascii_letters + string.digits
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count(), mp_context=multiprocessing.get_context("fork")) as executor:
        for length in range(1, max_length + 1):
            guesses = ("".join(guess) for guess in itertools.product(alphabet, repeat=length))
            for password, hashed in executor.map(hash_password, guesses):
                if hashed == target_hash:
                    return password
    executor.shutdown(wait=False)
    return None


if __name__ == "__main__":
    import hashlib
    import sys

    assert len(sys.argv) == 2
    password = sys.argv[1]

    hashed = hashlib.sha1(password.encode()).hexdigest()
    _ = hashcat(hashed)
