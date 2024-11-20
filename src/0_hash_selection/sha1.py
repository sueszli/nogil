"""
twice as fast as sha256

good tradeoff between security and speed

18578.26it/s
"""


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


if __name__ == "__main__":
    import hashlib
    import random
    import string
    import time

    import tqdm

    words = [""]
    generate_random_string = lambda length=8: "".join(random.choices(string.ascii_letters + string.digits, k=length))
    words.extend([generate_random_string() for _ in range(100_000)])

    diffs = []
    for word in tqdm.tqdm(words):
        start = time.time()
        lib_result = hashlib.sha1(word.encode()).hexdigest()
        lib_time = time.time() - start

        start = time.time()
        my_result = sha1(word).hex()
        my_time = time.time() - start

        diff = my_time - lib_time
        diffs.append(diff)
        assert lib_result == my_result

    print(f"average time difference: {sum(diffs) / len(diffs)}")
    print("all tests passed!")
