from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()
cipher = Fernet(key)

ctf_flag = "EACTL{euXnet_1s_0neutr3lized_g00d_7ob}"

# Encrypt the flag
encrypted_flag = cipher.encrypt(ctf_flag.encode())
print(f"key_b64 = {key}")
print(f"flag_enc = {encrypted_flag}")