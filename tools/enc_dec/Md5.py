import hashlib


def md5_encrypt(text, encode='utf-8'):
    md5_ = hashlib.md5()
    md5_.update(text.encode(encoding=encode))
    encrypt_str = md5_.hexdigest()
    return encrypt_str
