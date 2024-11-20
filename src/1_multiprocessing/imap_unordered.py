def hash_password(password):
    from hashlib import sha1

    return password, sha1(password.encode()).hexdigest()


def hashcat(target_hash, max_length=8):
    import itertools
    import multiprocessing
    import string

    alphabet = string.ascii_letters + string.digits
    with multiprocessing.Pool(
        processes=multiprocessing.cpu_count(),
        maxtasksperchild=1000,  # good ratio based on benchmarks
    ) as pool:
        for length in range(1, max_length + 1):
            guesses = ("".join(guess) for guess in itertools.product(alphabet, repeat=length))
            for password, hashed in pool.imap_unordered(hash_password, guesses):
                if hashed == target_hash:
                    pool.terminate()
                    return password
    return None


if __name__ == "__main__":
    import hashlib
    import sys

    assert len(sys.argv) == 2
    password = sys.argv[1]

    hashed = hashlib.sha1(password.encode()).hexdigest()
    _ = hashcat(hashed)