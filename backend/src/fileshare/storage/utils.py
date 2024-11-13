import uuid
from datetime import datetime

from cryptography.fernet import Fernet

def encrypt_content(content: bytes, key):
    fernet = Fernet(key)
    return fernet.encrypt(content)

def decrypt_content(content: bytes, key):
    fernet = Fernet(key)
    return fernet.encrypt(content)

def name_generator():
    unique_id = uuid.uuid4()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Adds timestamp for further uniqueness
    filename = f"{unique_id}_{timestamp}"
    return filename