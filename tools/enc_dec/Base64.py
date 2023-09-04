import base64


def base64_encrypt(text, encode='utf-8'):
    base64_encry = base64.b64encode(text.encode(encode))
    return (base64_encry)


def base64_decrypt(text, encode='utf-8'):
    base64_decry = (base64.b64decode(text)).decode(encode)
    return base64_decry
