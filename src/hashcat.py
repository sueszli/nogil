def timeit(func) -> callable:
    import functools
    import time

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} executed in {end - start:.5f}s")
        return result

    return wrapper


def sha1(msg):
    if isinstance(msg, str):
        msg = msg.encode()
    assert isinstance(msg, bytes)

    lrot = lambda value, n: ((value << n) & mask) | (value >> (width - n))
    bytes_to_word = lambda b: (b[0] << 24) | (b[1] << 16) | (b[2] << 8) | b[3]

    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    width = 32
    mask = 0xFFFFFFFF
    ml = len(msg) * 8

    msg += b"\x80"
    msg += b"\x00" * (-(len(msg) + 8) % 64)
    msg += bytes([(ml >> (56 - i * 8)) & 0xFF for i in range(8)])

    for chunk in [msg[i : i + 64] for i in range(0, len(msg), 64)]:
        w = [bytes_to_word(chunk[i : i + 4]) for i in range(0, 64, 4)]

        for i in range(16, 80):
            w.append(lrot(w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16], 1))

        a, b, c, d, e = h
        for i in range(len(w)):
            if i < 20:
                f, k = d ^ (b & (c ^ d)), 0x5A827999
            elif i < 40:
                f, k = b ^ c ^ d, 0x6ED9EBA1
            elif i < 60:
                f, k = (b & c) | (d & (b | c)), 0x8F1BBCDC
            else:
                f, k = b ^ c ^ d, 0xCA62C1D6
            temp = (lrot(a, 5) + f + e + k + w[i]) & mask
            e, d, c, b, a = d, c, lrot(b, 30), a, temp

        c_hash = [a, b, c, d, e]
        h = [((v + n) & mask) for v, n in zip(h, c_hash)]

    return b"".join([v.to_bytes(4, "big") for v in h])


@timeit
def crack_hash(target_hash, max_length=8):
    from string import ascii_letters, digits

    def product(*args, repeat=1):
        pools = [tuple(pool) for pool in args] * repeat
        result = [[]]
        for pool in pools:
            result = [x + [y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)

    chars = ascii_letters + digits
    for length in range(1, max_length + 1):
        for guess in product(chars, repeat=length):
            password = "".join(guess)
            hashed = sha1(password.encode()).hex()
            if hashed == target_hash:
                return password
    return None


target = sha1("ab".encode()).hex()
result = crack_hash(target)
print(f"Hash: {target}")
print(f"Cracked password: {result}")
