def hashcat(target_hash, shared_lib):
    import ctypes

    lib = ctypes.CDLL(shared_lib)

    # `char* hashcat(const char *target_hash)`
    lib.hashcat.argtypes = [ctypes.c_char_p]
    lib.hashcat.restype = ctypes.c_char_p

    hash_bytes = target_hash.encode("utf-8")
    result = lib.hashcat(hash_bytes)
    return result.decode("utf-8")


if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 3
    shared_lib = sys.argv[1]
    target_hash = sys.argv[2]
    password = hashcat(target_hash, shared_lib)
