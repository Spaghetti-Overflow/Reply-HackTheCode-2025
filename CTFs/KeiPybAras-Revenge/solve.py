from Crypto.Cipher import AES
from Crypto.Util import Counter
import os
import time
from datetime import datetime
import random
import hashlib

def generate_timestamp(date_str):
# Converte la stringa in un oggetto datetime
    dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S.%f")
# Calcola il timestamp (numero di secondi dal 1 gennaio 1970)
    timestamp = dt.timestamp()
    timestamp_ms = round(timestamp,3)   
    date = datetime.fromtimestamp(timestamp_ms)

    timestamp_int = int(timestamp_ms * 1000)
    ts = timestamp_int.to_bytes(16, byteorder='big') 
    return str(date),hashlib.md5(ts).digest()

def deobfuscation(ciphertext,date_str):
    ciphertext=bytes.fromhex(ciphertext.decode())
    date, ts = generate_timestamp(date_str)
    ciphertext_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    deobfuscated_cyphertext = b''

    for block in ciphertext_blocks:
        block_with_xor = bytes(a ^ b for a, b in zip(block, ts))
        deobfuscated_cyphertext += block_with_xor

    return deobfuscated_cyphertext

def xor_with_test(ciphertext, test_data):
    # Ensure both key_stream and test_data are of the same length
    min_length = min(len(ciphertext), len(test_data))
    result = bytes(a ^ b for a, b in zip(ciphertext[:min_length], test_data[:min_length]))
    return result

def decryption(ciphertext,date_str):
    ciphertext=bytes.fromhex(ciphertext)

    ciphertext_blocks = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    ciphertext_with_xor = b''

    for block in ciphertext_blocks:
        block_with_xor = bytes(a ^ b for a, b in zip(block, ts))
        ciphertext_with_xor += block_with_xor

    return key_stream

date_str_1 = "2025-03-10 09:50:07.974000"
date_str_2= "2025-03-10 09:50:10.975000"
ciphertext_1=b"ac0720038488a5f6f149cf0f3a41e31ffff996363fa6a0cf493c2a2998ad0bddfab0422efd4df201bf05ede07926ce3988015bb35a717504d03db4a0ac52d67c8f006b9e662f0db0a6644484d210eb33d3ce54d9565c10bb2fcc08d8db5e87d96d576418"
ciphertext_2=b"b571b8eb470f7c3b466618af91cb111184d73bfca56c3f1ddc44c5845f789f8584d7a6fe60d3328b386a0044b8e1164bb810f97398e8b98d280903220dc33452be73e90fefa9"
test = b"Capybara friends, mission accomplished! We've caused a blackout, let's meet at the bar to celebrate!"
deobfuscated_cyphertext_1=deobfuscation(ciphertext_1,date_str_1)
deobfuscated_cyphertext_2=deobfuscation(ciphertext_2,date_str_2)
key_stream=xor_with_test(deobfuscated_cyphertext_1,test)
print(xor_with_test(key_stream,deobfuscated_cyphertext_2))

