def worker(queue, target_hash, found_event, result_queue):
    import hashlib
    from queue import Queue

    while not found_event.is_set():
        try:
            chunk = queue.get(timeout=1)
            if chunk is None:
                break

            for password in chunk:
                if found_event.is_set():
                    break

                hashed = hashlib.sha1(password.encode()).hexdigest()
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
    import hashlib
    import sys

    assert len(sys.argv) == 2
    password = sys.argv[1]

    hashed = hashlib.sha1(password.encode()).hexdigest()
    assert hashcat(hashed) == password
