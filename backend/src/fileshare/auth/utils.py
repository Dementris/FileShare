import re
from passlib.context import CryptContext

passwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Generates a hashed version of the provided password."""
    return passwd_context.hash(password)


def is_hash(password: str) -> bool:
    """Checks if the password is a valid bcrypt hash."""
    bcrypt_regex = r"^\$2b\$(12)\$[A-Za-z0-9./]{22}[A-Za-z0-9./]{31}$"
    return bool(re.match(bcrypt_regex, password))


def verify_password(passw: str, hashed_passw: str) -> bool:
    return passwd_context.verify(passw, hashed_passw)
