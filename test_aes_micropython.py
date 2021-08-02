from os import urandom
import binascii
from ucryptolib import aes

# For Generating cipher text
secret_key = urandom(16)
iv = urandom(16)
crypto = aes(secret_key, 2, iv)

# Print hexstring of secret_key and iv
print('secret: ' + ''.join('%02x' % i for i in secret_key))
print('iv: ' + ''.join('%02x' % i for i in iv))

# Encrypt the message from text to bytes and hexstring
print('*** Encrypt original text')
message = 'Lorem Ipsum text'
encrypted_text_bytes = crypto.encrypt(message)
encrypted_text_hex = ''.join('%02x' % i for i in encrypted_text_bytes)
print('Original text       :', message)
print('Encrypted bytes     :', encrypted_text_bytes)
print('Encrypted hexstring :', encrypted_text_hex)

# Decrypt the message from bytes
print('*** Decrypt method #1 (bytes)')
decrypto = aes(secret_key, 2, iv)
decrypted_text_bytes = decrypto.decrypt(encrypted_text_bytes)
decrypted_text_hex = "".join("%02x" % i for i in decrypted_text_bytes)
print('The decrypted text  :', decrypted_text_bytes.decode())
print('The decrypted bytes :', decrypted_text_bytes)
print('The decrypted hex   :', decrypted_text_hex)

# Decrypt the message from hexstring
print('*** Decrypt method #2 (hexstring)')
decrypto = aes(secret_key, 2, iv)
decrypted_text_bytes = decrypto.decrypt(binascii.unhexlify(encrypted_text_hex))
decrypted_text_hex = "".join("%02x" % i for i in decrypted_text_bytes)
print('The decrypted text  :', decrypted_text_bytes.decode())
print('The decrypted bytes :', decrypted_text_bytes)
print('The decrypted hex   :', decrypted_text_hex)
