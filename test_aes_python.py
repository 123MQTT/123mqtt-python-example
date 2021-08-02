from os import urandom
from Crypto.Cipher import AES

# For Generating cipher text
secret_key = urandom(16)
iv = urandom(16)
crypto = AES.new(secret_key, AES.MODE_CBC, iv)

# Print hexstring of secret_key and iv
print('secret: ' + secret_key.hex())
print('iv: ' + iv.hex())

# Encrypt the message from text to bytes and hexstring
print('*** Encrypt original text')
message = 'Lorem Ipsum text'
encrypted_text_bytes = crypto.encrypt(message)
encrypted_text_hex = encrypted_text_bytes.hex()
print('Original text       :', message)
print('Encrypted bytes     :', encrypted_text_bytes)
print('Encrypted hexstring :', encrypted_text_hex)

# Decrypt the message from bytes
print('*** Decrypt method #1 (bytes)')
decrypto = AES.new(secret_key, AES.MODE_CBC, iv)
decrypted_text_bytes = decrypto.decrypt(encrypted_text_bytes)
print('The decrypted text  :', decrypted_text_bytes.decode())
print('The decrypted bytes :', decrypted_text_bytes)
print('The decrypted hex   :', decrypted_text_bytes.hex())

# Decrypt the message from hexstring
print('*** Decrypt method #2 (hexstring)')
decrypto = AES.new(secret_key, AES.MODE_CBC, iv)
decrypted_text_bytes = decrypto.decrypt(bytes.fromhex(encrypted_text_hex))
decrypted_text_hex = decrypted_text_bytes.hex()
print('The decrypted text  :', decrypted_text_bytes.decode())
print('The decrypted bytes :', decrypted_text_bytes)
print('The decrypted hex   :', decrypted_text_hex)