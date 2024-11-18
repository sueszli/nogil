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

# 
# torch
# 

import torch

A = torch.zeros(2, 3)
B = torch.zeros(2, 3)
result = torch.mm(A, B)
result = torch.matmul(A, B)
result = torch.bmm(A, B)

# 
# tensorflow
# 

import tensorflow as tf

A = tf.zeros([3, 4], tf.int32)
B = tf.zeros([3, 4], tf.int32)
result = tf.matmul(A, B)
