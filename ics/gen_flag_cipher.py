# encrypt_flag.py
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
import base64

flag = b'CTF{super_secret_flag}'  # must be bytes
key = os.urandom(32)  # 256-bit AES key
iv = os.urandom(16)   # 128-bit IV for CBC

# Pad the flag
padder = padding.PKCS7(128).padder()
padded_flag = padder.update(flag) + padder.finalize()

# Encrypt
cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
encryptor = cipher.encryptor()
encrypted_flag = encryptor.update(padded_flag) + encryptor.finalize()

# Output encoded data to embed in your Python challenge file
print("Key:", base64.b64encode(key).decode())
print("IV:", base64.b64encode(iv).decode())
print("Encrypted flag:", base64.b64encode(encrypted_flag).decode())
