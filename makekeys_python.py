from ecdsa import SigningKey, SECP128r1

# generate keypairs, return value is the private key
sk = SigningKey.generate(curve=SECP128r1)
print(sk.to_string().hex())

# get the public key
vk = sk.verifying_key
print(vk.to_string().hex())

# generate signature from a message
message = b'hello'
signature = sk.sign(message)
print(signature.hex())

# verifying if message is authentic
print(vk.verify(signature, message))

# store keypairs into files
with open("private.pem", "wb") as f:
    f.write(sk.to_pem())
with open("public.pem", "wb") as f:
    f.write(vk.to_pem())