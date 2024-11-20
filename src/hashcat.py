import hashlib
from itertools import product
from string import ascii_letters, digits

def crack_hash(target_hash, max_length=8):
    chars = ascii_letters + digits
    
    for length in range(1, max_length + 1):
        for guess in product(chars, repeat=length):
            password = ''.join(guess)
            hashed = hashlib.md5(password.encode()).hexdigest()
            if hashed == target_hash:
                return password
    
    return None


target = hashlib.md5("abc1".encode()).hexdigest()
result = crack_hash(target)
print(f"Hash: {target}")
print(f"Cracked password: {result}")
