import sys
import hashlib
import itertools
import string
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from typing import Optional

assert not sys._is_gil_enabled(), "disable GIL first"
# assert sys.version_info >= (3, 13), "python 3.13+ is required"

class HashWorker:
    def __init__(self, target_hash: str, max_length: int = 8):
        self.target_hash = target_hash
        self.max_length = max_length
        self.result: Optional[str] = None
        self.found = threading.Event()
        self.alphabet = string.ascii_letters + string.digits
        
    def hash_password(self, password: str) -> tuple[str, str]:
        """Thread-safe password hashing function"""
        return password, hashlib.sha1(password.encode()).hexdigest()
    
    def process_chunk(self, chunk: list[str]) -> Optional[str]:
        """Process a chunk of password candidates"""
        for password in chunk:
            if self.found.is_set():
                return None
                
            _, hashed = self.hash_password(password)
            if hashed == self.target_hash:
                self.found.set()
                return password
        return None

    def generate_passwords(self, length: int, chunk_size: int = 1000) -> list[str]:
        """Generate chunks of password candidates of given length"""
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
        """Find password using thread pool"""
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
    """Main entry point for password cracking"""
    worker = HashWorker(target_hash, max_length)
    return worker.find_password()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python script.py <password>")
        sys.exit(1)
        
    password = sys.argv[1]
    target_hash = hashlib.sha1(password.encode()).hexdigest()
    
    found = hashcat(target_hash)
    if found:
        print(f"Password found: {found}")
    else:
        print("Password not found")