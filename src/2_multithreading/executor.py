def check_password_chunk(args):
    import hashlib

    chunk, target_hash = args
    for password in chunk:
        hashed = hashlib.sha1(password.encode()).hexdigest()
        if hashed == target_hash:
            return password
    return None


def hashcat(target_hash, max_length=8, num_threads=8):
    import string
    from itertools import product
    from concurrent.futures import ThreadPoolExecutor

    alphabet = string.ascii_letters + string.digits

    def chunk_generator(passwords, chunk_size=1000):
        chunk = []
        for password in passwords:
            chunk.append(password)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        for length in range(1, max_length + 1):
            passwords = ("".join(guess) for guess in product(alphabet, repeat=length))
            chunks = chunk_generator(passwords, chunk_size=1000)

            futures = []
            for chunk in chunks:
                future = executor.submit(check_password_chunk, (chunk, target_hash))
                futures.append(future)

            for future in futures:
                result = future.result()
                if result:
                    return result

    return None


if __name__ == "__main__":
    import hashlib
    import sys

    assert len(sys.argv) == 2
    password = sys.argv[1]

    hashed = hashlib.sha1(password.encode()).hexdigest()
    _ = hashcat(hashed)
