import numpy as np
from multiprocessing import Pool

def parallel_matrix_mult(A, B, num_processes=4):
    def chunk_multiply(args):
        start, end = args
        return np.dot(A[start:end], B)
        
    chunks = [(i * len(A)//num_processes, (i+1) * len(A)//num_processes) 
              for i in range(num_processes)]
    
    with Pool(num_processes) as pool:
        results = pool.map(chunk_multiply, chunks)
    
    return np.vstack(results)
