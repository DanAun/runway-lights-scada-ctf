from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

ctf_flag = "ECTL{c31d3ec493ff7b5a40d13dd3376f3894}"

# Encrypt the flag
encrypted_flag = cipher.encrypt(ctf_flag.encode())
print(f"key_b64 = {key}")
print(f"flag_enc = {encrypted_flag}")