import struct
from enum import Enum
from math import floor, sin


class MD5Buffer(Enum):
    A = 0x67452301
    B = 0xEFCDAB89
    C = 0x98BADCFE
    D = 0x10325476


class MD5(object):
    _string = None
    _buffers = {
        MD5Buffer.A: None,
        MD5Buffer.B: None,
        MD5Buffer.C: None,
        MD5Buffer.D: None,
    }

    @staticmethod
    def hash(string):
        MD5._string = string
        preprocessed_bytes = MD5._step_2(MD5._step_1())
        MD5._step_3()
        MD5._step_4(preprocessed_bytes)
        return MD5._step_5()

    @staticmethod
    def _step_1():
        message_bytes = MD5._string.encode("utf-8")
        original_bit_len = len(message_bytes) * 8
        padding_len = (448 - (original_bit_len + 1) % 512) % 512
        padded = bytearray(message_bytes)
        padded.append(0x80)
        padded.extend([0] * ((padding_len - 7) // 8))
        return padded

    @staticmethod
    def _step_2(step_1_result):
        original_bit_len = len(MD5._string) * 8
        length_bytes = struct.pack("<Q", original_bit_len % (2**64))
        result = bytearray(step_1_result)
        result.extend(length_bytes)
        return result

    @staticmethod
    def _step_3():
        for buffer_type in MD5._buffers.keys():
            MD5._buffers[buffer_type] = buffer_type.value

    @staticmethod
    def _step_4(step_2_result):
        F = lambda x, y, z: (x & y) | (~x & z)
        G = lambda x, y, z: (x & z) | (y & ~z)
        H = lambda x, y, z: x ^ y ^ z
        I = lambda x, y, z: y ^ (x | ~z)
        rotate_left = lambda x, n: (x << n) | (x >> (32 - n))
        modular_add = lambda a, b: (a + b) % pow(2, 32)

        T = [floor(pow(2, 32) * abs(sin(i + 1))) for i in range(64)]
        chunks = [step_2_result[i : i + 64] for i in range(0, len(step_2_result), 64)]

        for chunk in chunks:
            X = list(struct.unpack("<16I", chunk))
            A = MD5._buffers[MD5Buffer.A]
            B = MD5._buffers[MD5Buffer.B]
            C = MD5._buffers[MD5Buffer.C]
            D = MD5._buffers[MD5Buffer.D]

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

            MD5._buffers[MD5Buffer.A] = modular_add(MD5._buffers[MD5Buffer.A], A)
            MD5._buffers[MD5Buffer.B] = modular_add(MD5._buffers[MD5Buffer.B], B)
            MD5._buffers[MD5Buffer.C] = modular_add(MD5._buffers[MD5Buffer.C], C)
            MD5._buffers[MD5Buffer.D] = modular_add(MD5._buffers[MD5Buffer.D], D)

    @staticmethod
    def _step_5():
        A = struct.unpack("<I", struct.pack(">I", MD5._buffers[MD5Buffer.A]))[0]
        B = struct.unpack("<I", struct.pack(">I", MD5._buffers[MD5Buffer.B]))[0]
        C = struct.unpack("<I", struct.pack(">I", MD5._buffers[MD5Buffer.C]))[0]
        D = struct.unpack("<I", struct.pack(">I", MD5._buffers[MD5Buffer.D]))[0]
        return f"{format(A, '08x')}{format(B, '08x')}{format(C, '08x')}{format(D, '08x')}"


#
# test
#


if __name__ == "__main__":
    import hashlib
    import random
    import string

    words = [""]
    generate_random_string = lambda length=8: "".join(random.choices(string.ascii_letters + string.digits, k=length))
    words.extend([generate_random_string() for _ in range(100)])

    for word in words:
        lib_result = hashlib.md5(word.encode()).hexdigest()
        my_result = MD5.hash(word)
        assert lib_result == my_result

    print("all tests passed!")
