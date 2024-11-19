# matmul

```python
from itertools import starmap, product
from functools import reduce

# 
# vanilla
# 

def matmul(A, B):
    assert len(A[0]) == len(B)
    result = [[0 for _ in range(len(B[0]))] for _ in range(len(A))]
    for i in range(len(A)):
        for j in range(len(B[0])):
            for k in range(len(B)):
                result[i][j] += A[i][k] * B[k][j]
    return result

def matmul_functional(A, B):
    assert len(A[0]) == len(B)
    return [[reduce(lambda x, y: x + y, starmap(lambda a, b: a * b, zip(row, col))) for col in zip(*B)] for row in A]

def matmul_comprehension(A, B):
    assert len(A[0]) == len(B)
    return [[sum(a*b for a,b in zip(X_row,Y_col)) for Y_col in zip(*B)] for X_row in A]

def matmul_infix(A, B):
    # https://peps.python.org/pep-0465/
    assert len(A[0]) == len(B)
    return A @ B

# 
# multiprocess
# 

from multiprocessing import Pool

def matmul_multiprocess(A, B, num_processes=4):
    assert len(A[0]) == len(B)

    def chunk_multiply(args):
        start, end = args
        return np.dot(A[start:end], B)
    
    chunks = [(i * len(A)//num_processes, (i+1) * len(A)//num_processes) for i in range(num_processes)]
    
    with Pool(num_processes) as pool:
        results = pool.map(chunk_multiply, chunks)

    return np.vstack(results)

# 
# numpy
# 

import numpy as np

A = np.zeros((2, 1))
B = np.zeros((2, 1))
result = np.dot(A, B)
result = np.matmul(A, B)

# 
# torch
# 

import torch

A = torch.zeros(2, 3)
B = torch.zeros(2, 3)
result = torch.matmul(A, B)

# 
# tensorflow
# 

import tensorflow as tf

A = tf.zeros([3, 4], tf.int32)
B = tf.zeros([3, 4], tf.int32)
result = tf.matmul(A, B)
```

# kmeans

```python
import numpy as np
from multiprocessing import Pool, cpu_count

def kmeans(data, k, max_iters=100):
    # Initialize centroids using first k points instead of random
    centroids = [data[i] for i in range(k)]
    
    for _ in range(max_iters):
        # Assign points to nearest centroid
        clusters = [[] for _ in range(k)]
        for point in data:
            distances = [sum((a-b)**2 for a, b in zip(point, c)) for c in centroids]
            closest = distances.index(min(distances))
            clusters[closest].append(point)
        
        # Update centroids
        new_centroids = []
        for cluster in clusters:
            if cluster:
                centroid = [sum(dim)/len(cluster) for dim in zip(*cluster)]
                new_centroids.append(centroid)
            else:
                # Handle empty clusters by keeping the previous centroid
                new_centroids.append(centroids[len(new_centroids)])
        
        if new_centroids == centroids:
            break
        centroids = new_centroids
    
    return centroids

def kmeans_parallel(data, k, max_iters=100):
    def euclidean_distance(point, centroid):
        return np.sum((point - centroid) ** 2)

    def assign_points(args):
        point, centroids = args
        distances = [euclidean_distance(point, centroid) for centroid in centroids]
        return np.argmin(distances)

    def update_centroid(cluster):
        return np.mean(cluster, axis=0) if len(cluster) > 0 else cluster[0]

    # Initialize centroids using first k points
    centroids = data[:k]
    
    num_cores = cpu_count()
    pool = Pool(processes=num_cores)
    
    for _ in range(max_iters):
        # Assign points to nearest centroid in parallel
        assignments = pool.map(assign_points, [(point, centroids) for point in data])
        
        # Group points by cluster
        clusters = [[] for _ in range(k)]
        for i, cluster_id in enumerate(assignments):
            clusters[cluster_id].append(data[i])
        
        # Update centroids in parallel
        new_centroids = pool.map(update_centroid, clusters)
        
        if np.all(new_centroids == centroids):
            break
        
        centroids = new_centroids
    
    pool.close()
    pool.join()
    
    return centroids
```

# aes

```python
from Crypto.Cipher import AES # hard to benchmark with C because it needs all the weights
from multiprocessing import Pool

def aes_parallel(data, key, num_processes=4):
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
```

# block encryption

```python
def block_encrypt(plaintext, key):
    # Constants
    block_size = 16
    
    # Pad plaintext if needed
    padding_length = block_size - (len(plaintext) % block_size)
    if padding_length < block_size:
        plaintext += chr(padding_length) * padding_length
    
    # Encrypt each block sequentially
    result = ''
    for i in range(0, len(plaintext), block_size):
        # Get current block
        block = plaintext[i:i+block_size]
        
        # Encrypt block using XOR with key
        encrypted_block = ''
        for char in block:
            # Convert key to integer if it's not already
            key_int = key if isinstance(key, int) else ord(str(key)[0])
            # XOR operation between character and key
            encrypted_char = chr(ord(char) ^ key_int)
            encrypted_block += encrypted_char
            
            # Rotate key for better diffusion
            key_int = ((key_int << 1) | (key_int >> 7)) & 0xFF
        
        result += encrypted_block
    
    return result

def block_encrypt_parallel(plaintext, key):
    block_size = 16
    blocks = [plaintext[i:i+block_size] for i in range(0, len(plaintext), block_size)]
    
    def encrypt_block(block):
        # Simplified AES-like encryption
        result = ''
        for char in block:
            result += chr(ord(char) ^ key)  # Simple XOR for demonstration
        return result
    
    # Simulate parallel processing
    encrypted_blocks = [encrypt_block(block) for block in blocks]
    return ''.join(encrypted_blocks)
```

# hashcat

```python
def hashcat(hash_to_crack, charset="abcdefghijklmnopqrstuvwxyz", max_length=8):
    def generate_passwords(start, end):
        from itertools import product
        candidates = []
        for length in range(1, max_length + 1):
            for guess in product(charset, repeat=length):
                password = ''.join(guess)
                if hash(password) == hash_to_crack:  # simplified hash function
                    return password
        return None
    
    # Simulate parallel processing (in real implementation, use multiprocessing)
    chunk_size = len(charset) // 4  # Split into 4 parallel tasks
    chunks = [charset[i:i + chunk_size] for i in range(0, len(charset), chunk_size)]
    return [generate_passwords(chunk, chunk + chunk_size) for chunk in chunks]
```
