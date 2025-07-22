from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

ctf_flag = "ECTL{46a84653657acbc31fa89d464a18b2bc}"

# Encrypt the flag
encrypted_flag = cipher.encrypt(ctf_flag.encode())
print(f"key_b64 = {key}")
print(f"flag_enc = {encrypted_flag}")