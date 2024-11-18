from Crypto.Cipher import AES
from multiprocessing import Pool

def parallel_encrypt(data, key, num_processes=4):
    def encrypt_chunk(chunk):
        cipher = AES.new(key, AES.MODE_ECB)
        return cipher.encrypt(chunk)
    
    # Pad data to be multiple of 16 bytes
    padding = 16 - (len(data) % 16)
    data += bytes([padding]) * padding
    
    # Split into chunks
    chunk_size = len(data) // num_processes
    chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    
    with Pool(num_processes) as pool:
        encrypted_chunks = pool.map(encrypt_chunk, chunks)
    
    return b''.join(encrypted_chunks)
  
