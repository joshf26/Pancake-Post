import hashlib

from uuid import uuid4


def generate_hash(password):
    salt = uuid4().hex
    pw_hash = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    return pw_hash, salt


def check_password(password, pw_hash, salt):
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest() == pw_hash
