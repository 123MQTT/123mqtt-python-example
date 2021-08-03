from ecdsa import SigningKey, SECP128r1

# replace this with your private key
private_key = '630ba2a8637139a1ba6eb4cdb723d448'

# load the private key
sk_string = bytearray.fromhex(private_key)
sk = SigningKey.from_string(sk_string, SECP128r1)
print(sk.to_string().hex())

# get the public key
vk = sk.verifying_key
print(vk.to_string().hex())

# generate signature from message
message = b'hello'
signature = sk.sign(message)
print(signature.hex())

# verifying if message is authentic
print(vk.verify(signature, message))