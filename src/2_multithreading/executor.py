import hashlib
import itertools
import string
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

assert sys.version_info >= (3, 13), "python 3.13+ is required"
assert not sys._is_gil_enabled(), "disable GIL first"


class HashWorker:
    def __init__(self, target_hash: str, max_length: int = 8):
        self.target_hash = target_hash
        self.max_length = max_length
        self.result: Optional[str] = None
        self.found = threading.Event()
        self.alphabet = string.ascii_letters + string.digits

    def hash_password(self, password: str) -> tuple[str, str]:
        return password, hashlib.sha1(password.encode()).hexdigest()

    def process_chunk(self, chunk: list[str]) -> Optional[str]:
        for password in chunk:
            if self.found.is_set():
                return None

            _, hashed = self.hash_password(password)
            if hashed == self.target_hash:
                self.found.set()
                return password
        return None

    def generate_passwords(self, length: int, chunk_size: int = 1000) -> list[str]:
        chunk = []
        for guess in itertools.product(self.alphabet, repeat=length):
            password = "".join(guess)
            chunk.append(password)
            if len(chunk) == chunk_size:
                yield chunk
                chunk = []
        if chunk:
            yield chunk

    def find_password(self) -> Optional[str]:
        num_threads = threading.active_count() * 2  # Adjust based on CPU cores

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for length in range(1, self.max_length + 1):
                if self.found.is_set():
                    break

                futures = []
                for chunk in self.generate_passwords(length):
                    if self.found.is_set():
                        break
                    future = executor.submit(self.process_chunk, chunk)
                    futures.append(future)

                for future in futures:
                    result = future.result()
                    if result:
                        self.result = result
                        return result

        return None


def hashcat(target_hash: str, max_length: int = 8) -> Optional[str]:
    worker = HashWorker(target_hash, max_length)
    return worker.find_password()


if __name__ == "__main__":
    import hashlib
    import sys

    assert len(sys.argv) == 2
    password = sys.argv[1]

    hashed = hashlib.sha1(password.encode()).hexdigest()
    _ = hashcat(hashed)
