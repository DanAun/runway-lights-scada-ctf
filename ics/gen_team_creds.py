# Generates the team credentials to be used in CTF

import bcrypt
import secrets
import string

def generate_random_password(length=12):
    """Generate a random password of the given length."""
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def generate_team_credentials(num_teams):
    """Generate team credentials with hashed and clear passwords."""
    users_hashed = {}
    users_clear = {}

    for i in range(1, num_teams + 1):
        team_name = f'team{i}'
        password = generate_random_password()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        users_hashed[team_name] = hashed_password
        users_clear[team_name] = password

    return users_hashed, users_clear

num_teams = 40
users_hashed, users_clear = generate_team_credentials(num_teams)

print("Users with Hashed Passwords:")
print(users_hashed)

print("\nUsers with Clear Passwords:")
print(users_clear)
