def sha1(msg):
    if isinstance(msg, str):
        msg = msg.encode()
    assert isinstance(msg, bytes)

    ml = len(msg) * 8
    msg += b"\x80"
    msg += b"\x00" * (-(len(msg) + 8) % 64)
    msg += bytes([(ml >> (56 - i * 8)) & 0xFF for i in range(8)])

    h = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    K = [0x5A827999, 0x6ED9EBA1, 0x8F1BBCDC, 0xCA62C1D6]

    for i in range(0, len(msg), 64):
        chunk = msg[i:i + 64]
        w = [
            (chunk[j] << 24) | (chunk[j + 1] << 16) | (chunk[j + 2] << 8) | chunk[j + 3]
            for j in range(0, 64, 4)
        ]

        for j in range(16, 80):
            value = w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16]
            w.append(((value << 1) & 0xFFFFFFFF) | (value >> 31))

        a, b, c, d, e = h
        for j in range(20):
            f = d ^ (b & (c ^ d))
            tmp = (((a << 5) & 0xFFFFFFFF) | (a >> 27)) + f + e + K[0] + w[j]
            e, d, c, b, a = d, c, ((b << 30) & 0xFFFFFFFF) | (b >> 2), a, tmp & 0xFFFFFFFF
        for j in range(20, 40):
            f = b ^ c ^ d
            tmp = (((a << 5) & 0xFFFFFFFF) | (a >> 27)) + f + e + K[1] + w[j]
            e, d, c, b, a = d, c, ((b << 30) & 0xFFFFFFFF) | (b >> 2), a, tmp & 0xFFFFFFFF
        for j in range(40, 60):
            f = (b & c) | (d & (b | c))
            tmp = (((a << 5) & 0xFFFFFFFF) | (a >> 27)) + f + e + K[2] + w[j]
            e, d, c, b, a = d, c, ((b << 30) & 0xFFFFFFFF) | (b >> 2), a, tmp & 0xFFFFFFFF
        for j in range(60, 80):
            f = b ^ c ^ d
            tmp = (((a << 5) & 0xFFFFFFFF) | (a >> 27)) + f + e + K[3] + w[j]
            e, d, c, b, a = d, c, ((b << 30) & 0xFFFFFFFF) | (b >> 2), a, tmp & 0xFFFFFFFF

        h[0] = (h[0] + a) & 0xFFFFFFFF
        h[1] = (h[1] + b) & 0xFFFFFFFF
        h[2] = (h[2] + c) & 0xFFFFFFFF
        h[3] = (h[3] + d) & 0xFFFFFFFF
        h[4] = (h[4] + e) & 0xFFFFFFFF

    return b"".join(v.to_bytes(4, "big") for v in h)


def worker(queue, target_hash, found_event, result_queue):
    from queue import Queue

    while not found_event.is_set():
        try:
            chunk = queue.get(timeout=1)
            if chunk is None:
                break

            for password in chunk:
                if found_event.is_set():
                    break

                hashed = sha1(password.encode()).hex()
                if hashed == target_hash:
                    result_queue.put(password)
                    found_event.set()
                    break

            queue.task_done()
        except Queue.Empty:
            continue


def hashcat(target_hash, max_length=8):
    import os
    import string
    from itertools import product
    from queue import Queue
    from threading import Event, Thread

    alphabet = string.ascii_letters + string.digits
    work_queue = Queue()
    result_queue = Queue()
    found_event = Event()
    num_threads = os.cpu_count() * 2

    threads = []
    for _ in range(num_threads):
        t = Thread(target=worker, args=(work_queue, target_hash, found_event, result_queue))
        t.daemon = True
        t.start()
        threads.append(t)

    for length in range(1, max_length + 1):
        if found_event.is_set():
            break

        def chunk_generator(iterable, chunk_size=1000):
            chunk = []
            for item in iterable:
                chunk.append(item)
                if len(chunk) == chunk_size:
                    yield chunk
                    chunk = []
            if chunk:
                yield chunk

        guesses = ("".join(guess) for guess in product(alphabet, repeat=length))
        for chunk in chunk_generator(guesses):
            work_queue.put(chunk)
            if found_event.is_set():
                break

    # barrier
    for _ in threads:
        work_queue.put(None)
    for t in threads:
        t.join()

    # check if any success
    if not result_queue.empty():
        return result_queue.get()
    return None


if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2
    target_hash = sys.argv[1]
    password = hashcat(target_hash)
