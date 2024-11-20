def hashcat(target_hash, max_length=8):
    import hashlib
    import string
    from itertools import product

    alphabet = string.ascii_letters + string.digits
    for length in range(1, max_length + 1):
        guesses = ("".join(guess) for guess in product(alphabet, repeat=length))
        for password in guesses:
            hashed = hashlib.sha1(password.encode()).hexdigest()
            if hashed == target_hash:
                return password
    return None


if __name__ == "__main__":
    import hashlib
    import sys

    assert len(sys.argv) == 2
    password = sys.argv[1]

    hashed = hashlib.sha1(password.encode()).hexdigest()
    _ = hashcat(hashed)
