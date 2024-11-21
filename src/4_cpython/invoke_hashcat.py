import hashcatmodule

if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 3
    shared_lib = sys.argv[1]
    target_hash = sys.argv[2]
    password = hashcatmodule.hashcat(target_hash)
