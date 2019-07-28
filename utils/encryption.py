import hashlib

'''
Hash algorithms.
The available algorithms are : 'sha256', 'sha384', 'sha224', 'sha512', 'sha1', 'md5'
'''


def sha1(token):
    return hashlib.sha1(token.encode()).hexdigest()


def sha224(token):
    return hashlib.sha224(token.encode()).hexdigest()


def sha256(token):
    return hashlib.sha256(token.encode()).hexdigest()


def sha384(token):
    return hashlib.sha384(token.encode()).hexdigest()


def sha512(token):
    return hashlib.sha512(token.encode()).hexdigest()


def md5(token):
    return hashlib.md5(token.encode()).hexdigest()


