import base64
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto import Random


def rsa_encrypt(text, rsa_public_key, encode='utf-8', padding='PKCS1_v1_5'):
    if '-----BEGIN RSA PUBLIC KEY-----' in rsa_public_key:
        pass
    else:
        rsa_public_key = '-----BEGIN RSA PUBLIC KEY-----\n' + rsa_public_key
    if '-----END RSA PUBLIC KEY-----' in rsa_public_key:
        pass
    else:
        rsa_public_key = rsa_public_key + '\n-----END RSA PUBLIC KEY-----'
    pub_key = RSA.importKey(rsa_public_key)
    if padding == 'PKCS1_v1_5':
        cipher = PKCS1_v1_5.new(pub_key)
    else:
        cipher = PKCS1_OAEP.new(pub_key)
    msg = text.encode(encode)
    default_encrypt_length = 245
    length = default_encrypt_length
    msg_list = [msg[i:i + length] for i in list(range(0, len(msg), length))]
    encrypt_msg_list = []
    for msg_str in msg_list:
        cipher_text = base64.b64encode(cipher.encrypt(message=msg_str))
        encrypt_msg_list.append(cipher_text)
    return encrypt_msg_list


def rsa_decrypt(text, rsa_private_key, encode='utf-8', padding='PKCS1_v1_5'):
    random_generator = Random.new().read
    pri_key = RSA.importKey(rsa_private_key)
    if padding == 'PKCS1_v1_5':
        cipher = PKCS1_v1_5.new(pri_key)
    else:
        cipher = PKCS1_OAEP.new(pri_key)
    msg_list = []
    for msg_str in text:
        msg_str = base64.decodebytes(msg_str)
        de_str = cipher.decrypt(msg_str, random_generator)
        msg_list.append(de_str.decode(encode))
    return ''.join(msg_list)
