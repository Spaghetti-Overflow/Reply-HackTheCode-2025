import base64

# Base64-encoded string
encoded_string = "PHE6Y2JRGGMQHjJwJmUpZjkCZmJFPFxtBFYGFQc0S1QkIgYTZko="
decoded_string = base64.b64decode(encoded_string).decode()

# XOR function
def xor_decrypt(enc, key):
    return "".join(chr(ord(enc[i]) ^ ord(key[i % len(key)])) for i in range(len(enc)))

# XOR decrypt with key
key = "G7v$Xp9!qLm2"
flag = xor_decrypt(decoded_string, key)

print("FLAG:", flag)
