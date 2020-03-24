from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import ast

class Encryptor:
    privKeyPath = "msgKey.key"
    pubKeyPath = "msgKey.pub"

    def encrypt(self, message):
        publicKey = self.getPublicKey()
        key = RSA.importKey(publicKey)

        encryptor = PKCS1_OAEP.new(key)
        encrypted = encryptor.encrypt(message.encode())
        return encrypted

    def decrypt(self, encrypted):
        privKey = self.getPrivateKey()

        key = RSA.importKey(privKey)

        decryptor = PKCS1_OAEP.new(key)
        message = decryptor.decrypt(ast.literal_eval(str(encrypted)))
        return message.decode()

    def getPublicKey(self):
        with open(self.pubKeyPath, 'r') as file:
            return file.read()

    def getPrivateKey(self):
        with open(self.privKeyPath, 'r') as file:
            return file.read()

