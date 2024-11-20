def fac_multithread(num):
    import os
    import queue
    import threading

    def fac_partial(start, end):
        partial_factorial = 1
        for i in range(start, end):
            partial_factorial *= i
        return partial_factorial

    threads = []
    results = queue.Queue()
    num_threads = os.cpu_count() * 2
    chunk_size = num // num_threads
    for i in range(num_threads):
        start = i * chunk_size + 1
        end = num + 1 if i == num_threads - 1 else (i + 1) * chunk_size + 1
        thread = threading.Thread(target=lambda s, e: results.put(fac_partial(s, e)), args=(start, end))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    total_factorial = 1
    while not results.empty():
        total_factorial *= results.get()
    return total_factorial


if __name__ == "__main__":
    import sys

    assert len(sys.argv) == 2
    num = int(sys.argv[1])

    _ = fac_multithread(int(num))
