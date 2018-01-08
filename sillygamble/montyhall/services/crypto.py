import random
import hashlib
import uuid

LEN = 32

def salt():
    # ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # chars=[]
    # for i in range(LEN):
    #     chars.append(random.choice(ALPHABET))

    # return "".join(chars)
    return str(uuid.uuid4()).replace('-','')

def password():
    salted_value = salt() + salt() + salt()

    return hashlib.sha256(salted_value.encode('utf-8')).hexdigest()

def checksum(game_data):
    checksum_str = hashlib.sha1(game_data.encode('utf-8')).hexdigest()
    return checksum_str.upper()