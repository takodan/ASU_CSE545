# part 0 aes
import base64
from Crypto.Cipher import AES

def decrypt_base64_aes256(base64_string, key):
    # Decode the Base64 string.
    cipher_text = base64.b64decode(base64_string)
    print(cipher_text)

    # Create an AES cipher object. MODE_ECB.
    cipher = AES.new(key, AES.MODE_ECB)

    # Decrypt the cipher_text.
    plaintext = cipher.decrypt(cipher_text)

    # Return the plaintext string.
    return plaintext




def aes():
    base64_string = "bBEUGZApdn9AWs3qKeG+iQ=="
    key = "crime"
    padded_key = (key + "\x00"*(32-len(key))).encode("utf-8")
    print(len(padded_key))
    print(padded_key)

    plaintext = decrypt_base64_aes256(base64_string, padded_key)

    print(plaintext)
    print(plaintext.decode())


# part 1 rsa

from decimal import *
from Crypto.Util.number import *
import math
# N = 84692954109552769374106613978990493265631425360379150170786955314741169348953
# 用yafu得出p*q = 264515818482660146971535304176490802643*320181056072095218868339092717483179171
# e = 65537

def rsa():
    n = 84692954109552769374106613978990493265631425360379150170786955314741169348953
    print(len(str(n)))
    getcontext().prec = 100
    e = 65537
    pq = 264515818482660146971535304176490802643*320181056072095218868339092717483179171 # 用yafu得出
    print(pq) # 84692954109552769374106613978990493265631425360379150170786955314741169348953
    r = (264515818482660146971535304176490802643-1)*(320181056072095218868339092717483179171-1)
    print(r) # 84692954109552769374106613978990493265046728485824394804947080917847195367140
    t = 1

    while t < 1000000:
        if((r*t+1)%e == 0 ):
            print(f"found t = {t}")
            break
        t = t+1
    d = int(Decimal(r*t+1)/Decimal(e))
    print(d)
    c = 21698323120385586424573862118808098555103084743518277473544693629498197679429

    print(long_to_bytes(pow(c , d , n)))



def main():
    # aes()
    rsa()
    


if __name__ == "__main__":
    main()


# part 2 hash
# https://hashes.com/en/decrypt/hash