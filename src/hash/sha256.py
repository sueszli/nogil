"""
incredibly slow:

- my implementation: ~7688.53it/s
- hashlib implementation: ~1907737.45it/s

in practice this is like 32.15s vs 0.14s and is too slow for any practical use.
"""


def sha256_old(message: bytearray) -> bytearray:
    if isinstance(message, str):
        message = bytearray(message, "ascii")
    elif isinstance(message, bytes):
        message = bytearray(message)
    elif not isinstance(message, bytearray):
        assert False

    # constants based on specification
    K = [0x428A2F98, 0x71374491, 0xB5C0FBCF, 0xE9B5DBA5, 0x3956C25B, 0x59F111F1, 0x923F82A4, 0xAB1C5ED5, 0xD807AA98, 0x12835B01, 0x243185BE, 0x550C7DC3, 0x72BE5D74, 0x80DEB1FE, 0x9BDC06A7, 0xC19BF174, 0xE49B69C1, 0xEFBE4786, 0x0FC19DC6, 0x240CA1CC, 0x2DE92C6F, 0x4A7484AA, 0x5CB0A9DC, 0x76F988DA, 0x983E5152, 0xA831C66D, 0xB00327C8, 0xBF597FC7, 0xC6E00BF3, 0xD5A79147, 0x06CA6351, 0x14292967, 0x27B70A85, 0x2E1B2138, 0x4D2C6DFC, 0x53380D13, 0x650A7354, 0x766A0ABB, 0x81C2C92E, 0x92722C85, 0xA2BFE8A1, 0xA81A664B, 0xC24B8B70, 0xC76C51A3, 0xD192E819, 0xD6990624, 0xF40E3585, 0x106AA070, 0x19A4C116, 0x1E376C08, 0x2748774C, 0x34B0BCB5, 0x391C0CB3, 0x4ED8AA4A, 0x5B9CCA4F, 0x682E6FF3, 0x748F82EE, 0x78A5636F, 0x84C87814, 0x8CC70208, 0x90BEFFFA, 0xA4506CEB, 0xBEF9A3F7, 0xC67178F2]

    # masking functions based on specification
    _rotate_right = lambda num, shift, size=32: (num >> shift) | (num << size - shift)
    _sigma0 = lambda num: _rotate_right(num, 7) ^ _rotate_right(num, 18) ^ (num >> 3)
    _sigma1 = lambda num: _rotate_right(num, 17) ^ _rotate_right(num, 19) ^ (num >> 10)
    _capsigma0 = lambda num: _rotate_right(num, 2) ^ _rotate_right(num, 13) ^ _rotate_right(num, 22)
    _capsigma1 = lambda num: _rotate_right(num, 6) ^ _rotate_right(num, 11) ^ _rotate_right(num, 25)
    _ch = lambda x, y, z: (x & y) ^ (~x & z)
    _maj = lambda x, y, z: (x & y) ^ (x & z) ^ (y & z)

    # padding and preprocessing
    length = len(message) * 8
    message.append(0x80)
    while (len(message) * 8 + 64) % 512 != 0:
        message.append(0x00)
    message += length.to_bytes(8, "big")
    assert (len(message) * 8) % 512 == 0
    blocks = []
    for i in range(0, len(message), 64):
        blocks.append(message[i : i + 64])

    h0 = 0x6A09E667
    h1 = 0xBB67AE85
    h2 = 0x3C6EF372
    h3 = 0xA54FF53A
    h5 = 0x9B05688C
    h4 = 0x510E527F
    h6 = 0x1F83D9AB
    h7 = 0x5BE0CD19

    for message_block in blocks:
        message_schedule = []
        for t in range(0, 64):
            if t <= 15:
                message_schedule.append(bytes(message_block[t * 4 : (t * 4) + 4]))
            else:
                term1 = _sigma1(int.from_bytes(message_schedule[t - 2], "big"))
                term2 = int.from_bytes(message_schedule[t - 7], "big")
                term3 = _sigma0(int.from_bytes(message_schedule[t - 15], "big"))
                term4 = int.from_bytes(message_schedule[t - 16], "big")
                schedule = ((term1 + term2 + term3 + term4) % 2**32).to_bytes(4, "big")
                message_schedule.append(schedule)
        assert len(message_schedule) == 64

        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        for t in range(64):
            t1 = (h + _capsigma1(e) + _ch(e, f, g) + K[t] + int.from_bytes(message_schedule[t], "big")) % 2**32
            t2 = (_capsigma0(a) + _maj(a, b, c)) % 2**32
            h = g
            g = f
            f = e
            e = (d + t1) % 2**32
            d = c
            c = b
            b = a
            a = (t1 + t2) % 2**32

        h0 = (h0 + a) % 2**32
        h1 = (h1 + b) % 2**32
        h2 = (h2 + c) % 2**32
        h3 = (h3 + d) % 2**32
        h4 = (h4 + e) % 2**32
        h5 = (h5 + f) % 2**32
        h6 = (h6 + g) % 2**32
        h7 = (h7 + h) % 2**32

    return (h0).to_bytes(4, "big") + (h1).to_bytes(4, "big") + (h2).to_bytes(4, "big") + (h3).to_bytes(4, "big") + (h4).to_bytes(4, "big") + (h5).to_bytes(4, "big") + (h6).to_bytes(4, "big") + (h7).to_bytes(4, "big")


def sha256(message):
    # just slightly faster, but significantly simpler
    message = bytearray(message, "ascii") if isinstance(message, str) else bytearray(message)

    K = bytearray.fromhex("428a2f9871374491b5c0fbcfe9b5dba53956c25b59f111f1923f82a4ab1c5ed5d807aa9812835b01243185be550c7dc372be5d7480deb1fe9bdc06a7c19bf174e49b69c1efbe47860fc19dc6240ca1cc2de92c6f4a7484aa5cb0a9dc76f988da983e5152a831c66db00327c8bf597fc7c6e00bf3d5a7914706ca63511429296727b70a852e1b21384d2c6dfc53380d13650a7354766a0abb81c2c92e92722c85a2bfe8a1a81a664bc24b8b70c76c51a3d192e819d6990624f40e3585106aa07019a4c1161e376c082748774c34b0bcb5391c0cb34ed8aa4a5b9cca4f682e6ff3748f82ee78a5636f84c878148cc7020890befffaa4506cebbef9a3f7c67178f2")
    K_blocks = [int.from_bytes(K[x : x + 4], "big") for x in range(0, len(K), 4)]
    H = [0x6A09E667, 0xBB67AE85, 0x3C6EF372, 0xA54FF53A, 0x510E527F, 0x9B05688C, 0x1F83D9AB, 0x5BE0CD19]

    Right_Shift = lambda x, y: x >> y
    Rotate_Right = lambda x, y: (x >> y) | (x << (32 - y)) & 0xFFFFFFFF
    sigma0 = lambda x: Rotate_Right(x, 7) ^ Rotate_Right(x, 18) ^ Right_Shift(x, 3)
    sigma1 = lambda x: Rotate_Right(x, 17) ^ Rotate_Right(x, 19) ^ Right_Shift(x, 10)
    Ch = lambda x, y, z: (x & y) ^ (~x & z)
    Maj = lambda x, y, z: (x & y) ^ (x & z) ^ (y & z)
    Sigma0 = lambda x: Rotate_Right(x, 2) ^ Rotate_Right(x, 13) ^ Rotate_Right(x, 22)
    Sigma1 = lambda x: Rotate_Right(x, 6) ^ Rotate_Right(x, 11) ^ Rotate_Right(x, 25)

    padded_message = []
    l = len(message)
    p = message + b"\x80" + b"\x00" * ((64 - l - 1 - 8) % 64) + (l * 8).to_bytes(8, byteorder="big")
    blocks = [p[x : x + 64] for x in range(0, len(p), 64)]
    for b in blocks:
        padded_message.append([int.from_bytes(b[x : x + 4], "big") for x in range(0, len(b), 4)])

    for i in range(0, len(padded_message)):
        rounds = [padded_message[i][v] for v in range(0, 16)]
        for w in range(16, 64):
            rounds.append((sigma1(rounds[w - 2]) + rounds[w - 7] + sigma0(rounds[w - 15]) + rounds[w - 16]) & 0xFFFFFFFF)
        a, b, c, d, e, f, g, h = H[0], H[1], H[2], H[3], H[4], H[5], H[6], H[7]
        for t in range(64):
            T1 = (h + Sigma1(e) + Ch(e, f, g) + K_blocks[t] + rounds[t]) & 0xFFFFFFFF
            T2 = (Sigma0(a) + Maj(a, b, c)) & 0xFFFFFFFF
            h = g
            g = f
            f = e
            e = (d + T1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (T1 + T2) & 0xFFFFFFFF
        H[0] += a
        H[1] += b
        H[2] += c
        H[3] += d
        H[4] += e
        H[5] += f
        H[6] += g
        H[7] += h
        H = [h & 0xFFFFFFFF for h in H]
    return b"".join([f.to_bytes(4, "big") for f in H])


#
# test
#


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
        lib_result = hashlib.sha256(word.encode()).hexdigest()
        lib_time = time.time() - start

        start = time.time()
        my_result = sha256(word).hex()
        my_time = time.time() - start

        diff = my_time - lib_time
        diffs.append(diff)
        assert lib_result == my_result

    print(f"average time difference: {sum(diffs) / len(diffs)}")
    print("all tests passed!")
