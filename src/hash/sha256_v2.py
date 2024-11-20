"""
just slightly faster, but significantly simpler
"""

def sha256(message):
    # just slightly faster, but significantly simpler

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
    return b"".join([f.to_bytes(4, "big") for f in H]).hex()


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
        my_result = sha256(word.encode())
        my_time = time.time() - start

        diff = my_time - lib_time
        diffs.append(diff)
        assert lib_result == my_result

    print(f"average time difference: {sum(diffs) / len(diffs)}")
    print("all tests passed!")
