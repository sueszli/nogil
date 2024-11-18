import hashlib
from multiprocessing import Pool

def parallel_hash_passwords(passwords, num_processes=4):
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    with Pool(num_processes) as pool:
        return pool.map(hash_password, passwords)
