from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

ctf_flag = "ECTL{f7e55121293ff83dae7e882587f47734}"

# Encrypt the flag
encrypted_flag = cipher.encrypt(ctf_flag.encode())
print(f"key_b64 = {key}")
print(f"flag_enc = {encrypted_flag}")