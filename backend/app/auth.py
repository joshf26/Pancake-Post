import hashlib

from uuid import uuid4


def generate_hash(password):
    salt = uuid4().hex
    hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return hash, salt


def check_password(password, hash, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest() == hash
