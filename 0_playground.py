import hashlib
import random
import string

def md5_generator(data):
    # Create an MD5 hash object
    md5_hash = hashlib.md5()
    # Update the hash object with the bytes-like object (string in this case)
    md5_hash.update(data.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    digest = md5_hash.digest()
    return digest

# Example usage
while True:
    curr_random = ''.join(random.choices(string.printable, k=6))    
    md5_result = md5_generator(curr_random)
    if md5_result[0:1] == b"\x00":
        print("Found it", md5_result, "for:", curr_random, ".")
        print(curr_random)
        break

    print("Original Data:", curr_random)
    print("MD5 Hash:", md5_result[0:1])