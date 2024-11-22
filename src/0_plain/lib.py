def hashcat(target_hash, max_length=8):
    import hashlib
    import string
    from itertools import product

    for length in range(1, max_length + 1):
        for password in ("".join(guess) for guess in product(string.ascii_letters + string.digits, repeat=length)):
            if target_hash == hashlib.sha1(password.encode()).hexdigest():
                return password
    return None


if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2
    target_hash = sys.argv[1]
    password = hashcat(target_hash)
