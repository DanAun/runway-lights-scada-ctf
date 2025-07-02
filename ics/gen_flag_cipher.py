from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

ctf_flag = "ECTL{7f42e5bb63791059998fd800dcf5eb0d}"

# Encrypt the flag
encrypted_flag = cipher.encrypt(ctf_flag.encode())
print(f"key_b64 = {key}")
print(f"flag_enc = {encrypted_flag}")