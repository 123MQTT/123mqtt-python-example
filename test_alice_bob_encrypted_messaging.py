from ecdsa import ECDH, SigningKey, VerifyingKey, SECP128r1
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom

# For quick testing purposes, Alice keypairs and Bob keypairs are generated
# within this file. In reality, both of them are on their own devices, hence
# none of them can see each other private key.

# Alice and Bob generate keypairs, ideally this is done once and kept
# in PEM files.
alice_sk = SigningKey.generate(curve=SECP128r1)
alice_vk = alice_sk.verifying_key
alice_ecdh = ECDH(curve=SECP128r1)
alice_ecdh.load_private_key(alice_sk)

bob_sk = SigningKey.generate(curve=SECP128r1)
bob_vk = bob_sk.verifying_key
bob_ecdh = ECDH(curve=SECP128r1)
bob_ecdh.load_private_key(bob_sk)

# Alice and Bob generate shared secret from public key exchanged
alice_received_public_key = bob_vk.to_string().hex()
alice_ecdh.load_received_public_key_bytes(bytearray.fromhex(alice_received_public_key))
alice_secret = alice_ecdh.generate_sharedsecret_bytes()

bob_received_public_key = alice_vk.to_string().hex()
bob_ecdh.load_received_public_key_bytes(bytearray.fromhex(bob_received_public_key))
bob_secret = bob_ecdh.generate_sharedsecret_bytes()

print('')
print('Alice private info:')
print('===================')
print('Private key  : ' + alice_sk.to_string().hex())
print("Shared secret: " + alice_secret.hex())
print('')
print('Bob private info:')
print('=================')
print('Private key  : ' + bob_sk.to_string().hex())
print("Shared secret: " + bob_secret.hex())
print('')
print('Public keys shared on truststore:')
print('=================================')
print('Alice key: ' + alice_vk.to_string().hex())
print('Bob key  : ' + bob_vk.to_string().hex())
print('')

# Alice wants to send a message and sign it
message = 'Lorem Ipsum text with padding'
signature = alice_sk.sign(pad(message.encode(), AES.block_size))

# Once the signature is created, she encrypts the message
secret_key = alice_secret
iv = urandom(16)
crypto = AES.new(secret_key, AES.MODE_CBC, iv)
encrypted_text_bytes = crypto.encrypt(pad(message.encode(), AES.block_size))
encrypted_text_hex = encrypted_text_bytes.hex()

print('Alice message:')
print('==============')
print('Content  : ' + message)
print('Signature: ' + signature.hex())
print('')
print('Alice message after AES-128 encryption:')
print('=======================================')
print('In bytes    :', encrypted_text_bytes)
print('In hexstring:', encrypted_text_hex)
print('')

print('Package sent by Alice, received by Bob:')
print('=======================================')
bob_received_msg = encrypted_text_hex
bob_received_signature = signature.hex()
bob_received_public_key = alice_vk.to_string().hex()
bob_received_iv = iv.hex()
print('Content    : ' + bob_received_msg)
print('Signature  : ' + bob_received_signature)
print('Session key: ' + bob_received_iv)
print('')

# Bob tries to decrypt the message
decrypto = AES.new(bob_secret, AES.MODE_CBC, bytes.fromhex(bob_received_iv))
decrypted_text_bytes = decrypto.decrypt(bytes.fromhex(bob_received_msg))
decrypted_text_hex = decrypted_text_bytes.hex()
print('Bob decrypts the content:')
print('=========================')
print('In text     :', decrypted_text_bytes.decode())
print('In bytes    :', decrypted_text_bytes)
print('In hexstring:', decrypted_text_hex)
print('')

# Bob tries to verify if public key is valid
vk_string = bytearray.fromhex(bob_received_public_key)
bob_received_vk = VerifyingKey.from_string(vk_string, SECP128r1)
# Bob tries to verify if Alice message is authentic
print('Bob verifies if the content is authentic:')
print('=========================================')
try:
    #authentic = bob_received_vk.verify(bytearray.fromhex(bob_received_signature), decrypted_text_bytes)
    authentic = bob_received_vk.verify(bytearray.fromhex(bob_received_signature), bytearray.fromhex(decrypted_text_hex))
except:
    authentic = False
print('Content is authentic: ' + str(authentic))
print('')