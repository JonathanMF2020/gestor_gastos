import hashlib

def encrypt(text:str):
    return hashlib.sha256(text.encode('UTF-8')).hexdigest()