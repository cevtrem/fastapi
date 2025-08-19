import bcrypt


def hash_password(password: str) -> str:
    password = password.encode()
    password_hashed = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hashed.decode()


def check_password(password: str, password_hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hashed.encode())
