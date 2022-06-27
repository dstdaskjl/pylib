import hashlib
import Cryptodome.Random
import traceback
import whirlpool
from Cryptodome.Cipher import AES, DES


# AES requires a key with 128, 192, or 256 bits.
# DES requires a key with 56 bits.
# ECB does not take IV.

class Encryption:
    def AES_CBC(self, key: bytes, plaintext: bytes) -> tuple:
        iv = Cryptodome.Random.get_random_bytes(AES.block_size)
        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        ciphertext = cipher.encrypt(plaintext=plaintext)
        return iv, ciphertext

    def AES_CFB(self, key: bytes, plaintext: bytes) -> tuple:
        iv = Cryptodome.Random.get_random_bytes(AES.block_size)
        cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
        ciphertext = cipher.encrypt(plaintext=plaintext)
        return iv, ciphertext

    def AES_EAX(self, key: bytes, plaintext: bytes) -> tuple:
        cipher = AES.new(key=key, mode=AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext=plaintext)
        nonce = cipher.nonce
        return ciphertext, tag, nonce

    def AES_ECB(self, key: bytes, plaintext: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext=plaintext)
        return ciphertext

    def AES_GCM(self, key: bytes, plaintext: bytes) -> tuple:
        cipher = AES.new(key=key, mode=AES.MODE_GCM)
        ciphertext, tag = cipher.encrypt_and_digest(plaintext=plaintext)
        nonce = cipher.nonce
        return ciphertext, tag, nonce

    def DES_ECB(self, key: bytes, plaintext: bytes) -> bytes:
        cipher = DES.new(key=key, mode=DES.MODE_ECB)
        ciphertext = cipher.encrypt(plaintext=plaintext)
        return ciphertext

    def DES_OFB(self, key: bytes, plaintext: bytes) -> tuple:
        iv = Cryptodome.Random.get_random_bytes(DES.block_size)
        cipher = DES.new(key=key, mode=DES.MODE_OFB, iv=iv)
        ciphertext = cipher.encrypt(plaintext=plaintext)
        return iv, ciphertext


class Decryption:
    def AES_CBC(self, key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_CBC, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def AES_CFB(self, key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_CFB, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def AES_EAX(self, key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext=ciphertext, received_mac_tag=tag)

        try:
            cipher.verify(tag)
        except ValueError:
            print(traceback.format_exc())

        return plaintext

    def AES_ECB(self, key: bytes, ciphertext: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def AES_GCM(self, key: bytes, nonce: bytes, ciphertext: bytes, tag: bytes) -> bytes:
        cipher = AES.new(key=key, mode=AES.MODE_GCM, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext=ciphertext, received_mac_tag=tag)

        try:
            cipher.verify(tag)
        except ValueError:
            print(traceback.format_exc())

        return plaintext

    def DES_ECB(self, key: bytes, ciphertext: bytes) -> bytes:
        cipher = DES.new(key=key, mode=DES.MODE_ECB)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext

    def DES_OFB(self, key: bytes, ciphertext: bytes, iv: bytes) -> bytes:
        cipher = DES.new(key=key, mode=DES.MODE_OFB, iv=iv)
        plaintext = cipher.decrypt(ciphertext)
        return plaintext


class Hashing:
    def MD5(self, plaintext: bytes):
        return hashlib.md5(plaintext).hexdigest().encode()

    def SHA1(self, plaintext: bytes):
        return hashlib.sha1(plaintext).hexdigest().encode()

    def SHA224(self, plaintext: bytes):
        return hashlib.sha224(plaintext).hexdigest().encode()

    def SHA256(self, plaintext: bytes):
        return hashlib.sha256(plaintext).hexdigest().encode()

    def SHA384(self, plaintext: bytes):
        return hashlib.sha384(plaintext).hexdigest().encode()

    def SHA512(self, plaintext: bytes):
        return hashlib.sha512(plaintext).hexdigest().encode()

    def whirlpool(self, plaintext: bytes):
        return whirlpool.new(plaintext).hexdigest()
