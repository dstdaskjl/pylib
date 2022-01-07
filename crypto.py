import hashlib

import Crypto.Random
from Crypto.Cipher import AES


class Encryption:
    def AES_CDC(self, key: bytes, data: bytes):
        iv = Crypto.Random.get_random_bytes(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.encrypt(data).hex().encode()
        return ciphertext, iv

    def AES_EAX(self, key: bytes, data: bytes):
        cipher = AES.new(key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)
        print(ciphertext, nonce, tag)
        ciphertext = ciphertext.hex().encode()
        nonce = nonce.hex().encode()
        tag = tag.hex().encode()
        return ciphertext, nonce, tag


class Decryption:
    def AES_CDC(self, key: bytes, data: bytes, iv: bytes):
        cipher = AES.new(key, AES.MODE_CBC, iv)
        ciphertext = cipher.decrypt(data)
        return ciphertext

    def AES_EAX(self, key: bytes, nonce: bytes, data: bytes, tag: bytes = None):
        cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(data)

        if tag:
            try:
                cipher.verify(tag)
            except ValueError as e:
                print(e)

        return plaintext


class Hashing:
    def MD5(self, data: bytes):
        return hashlib.md5(data).hexdigest().encode()

    def SHA1(self, data: bytes):
        return hashlib.sha1(data).hexdigest().encode()

    def SHA224(self, data: bytes):
        return hashlib.sha224(data).hexdigest().encode()

    def SHA256(self, data: bytes):
        return hashlib.sha256(data).hexdigest().encode()

    def SHA384(self, data: bytes):
        return hashlib.sha384(data).hexdigest().encode()

    def SHA512(self, data: bytes):
        return hashlib.sha512(data).hexdigest().encode()


s = 'hello world 1234'
encrypted, nonce, tag = Encryption().AES_EAX(key='0123456789abcdef'.encode(), data=s.encode())
print(encrypted, nonce, tag)
decrypted = Decryption().AES_EAX(key='0123456789abcdef'.encode(), data=encrypted, nonce=nonce, tag=tag)
# print(decrypted)
