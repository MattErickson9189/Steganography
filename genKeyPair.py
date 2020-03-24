from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii


keyPair = RSA.generate(4096)

pubKey = keyPair.publickey()
f = open('msgKey.pub','wb')
f.write(pubKey.exportKey('PEM'))
f.close()

f2 = open('msgKey.key','wb')
f2.write(keyPair.exportKey())
f2.close()

