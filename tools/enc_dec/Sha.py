import hashlib


def sha1_encrypt(text, encode='utf-8'):
    sha1_ = hashlib.sha1()
    sha1_.update(text.encode(encoding=encode))
    encrypt_str = sha1_.hexdigest()
    return encrypt_str


def sha256_encrypt(text, encode='utf-8'):
    sha256_ = hashlib.sha256()
    sha256_.update(text.encode(encoding=encode))
    encrypt_str = sha256_.hexdigest()
    return encrypt_str


def sha512_encrypt(text, encode='utf-8'):
    sha512_ = hashlib.sha512()
    sha512_.update(text.encode(encoding=encode))
    encrypt_str = sha512_.hexdigest()
    return encrypt_str
