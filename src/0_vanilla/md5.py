"""
9847.03it/s
"""

import struct
from enum import Enum
from math import floor, sin


def md5(string):
    class MD5Buffer(Enum):
        A = 0x67452301
        B = 0xEFCDAB89
        C = 0x98BADCFE
        D = 0x10325476

    buffers = {
        MD5Buffer.A: None,
        MD5Buffer.B: None,
        MD5Buffer.C: None,
        MD5Buffer.D: None,
    }

    # step 1
    message_bytes = string.encode("utf-8")
    original_bit_len = len(message_bytes) * 8
    padding_len = (448 - (original_bit_len + 1) % 512) % 512
    padded = bytearray(message_bytes)
    padded.append(0x80)
    padded.extend([0] * ((padding_len - 7) // 8))

    # step 2
    original_bit_len = len(string) * 8
    length_bytes = struct.pack("<Q", original_bit_len % (2**64))
    preprocessed_bytes = bytearray(padded)
    preprocessed_bytes.extend(length_bytes)

    # step 3
    for buffer_type in buffers.keys():
        buffers[buffer_type] = buffer_type.value

    # step 4
    F = lambda x, y, z: (x & y) | (~x & z)
    G = lambda x, y, z: (x & z) | (y & ~z)
    H = lambda x, y, z: x ^ y ^ z
    I = lambda x, y, z: y ^ (x | ~z)
    rotate_left = lambda x, n: (x << n) | (x >> (32 - n))
    modular_add = lambda a, b: (a + b) % pow(2, 32)

    T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]
    chunks = [preprocessed_bytes[i : i + 64] for i in range(0, len(preprocessed_bytes), 64)]

    for chunk in chunks:
        X = list(struct.unpack("<16I", chunk))
        A = buffers[MD5Buffer.A]
        B = buffers[MD5Buffer.B]
        C = buffers[MD5Buffer.C]
        D = buffers[MD5Buffer.D]

        for i in range(64):
            if 0 <= i <= 15:
                k = i
                s = [7, 12, 17, 22]
                temp = F(B, C, D)
            elif 16 <= i <= 31:
                k = ((5 * i) + 1) % 16
                s = [5, 9, 14, 20]
                temp = G(B, C, D)
            elif 32 <= i <= 47:
                k = ((3 * i) + 5) % 16
                s = [4, 11, 16, 23]
                temp = H(B, C, D)
            else:
                k = (7 * i) % 16
                s = [6, 10, 15, 21]
                temp = I(B, C, D)

            temp = modular_add(temp, X[k])
            temp = modular_add(temp, T[i])
            temp = modular_add(temp, A)
            temp = rotate_left(temp, s[i % 4])
            temp = modular_add(temp, B)

            A = D
            D = C
            C = B
            B = temp

        buffers[MD5Buffer.A] = modular_add(buffers[MD5Buffer.A], A)
        buffers[MD5Buffer.B] = modular_add(buffers[MD5Buffer.B], B)
        buffers[MD5Buffer.C] = modular_add(buffers[MD5Buffer.C], C)
        buffers[MD5Buffer.D] = modular_add(buffers[MD5Buffer.D], D)

    # step 5
    A = struct.unpack("<I", struct.pack(">I", buffers[MD5Buffer.A]))[0]
    B = struct.unpack("<I", struct.pack(">I", buffers[MD5Buffer.B]))[0]
    C = struct.unpack("<I", struct.pack(">I", buffers[MD5Buffer.C]))[0]
    D = struct.unpack("<I", struct.pack(">I", buffers[MD5Buffer.D]))[0]
    return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"


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
        lib_result = hashlib.md5(word.encode()).hexdigest()
        lib_time = time.time() - start

        start = time.time()
        my_result = md5(word)
        my_time = time.time() - start

        diff = my_time - lib_time
        diffs.append(diff)
        assert lib_result == my_result

    print(f"average time difference: {sum(diffs) / len(diffs)}")
    print("all tests passed!")
