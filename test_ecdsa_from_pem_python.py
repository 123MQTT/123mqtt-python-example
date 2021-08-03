from ecdsa import SigningKey, SECP128r1

# Before you execute this python script, you need to make the keypair with makekeys_python.py

# load private key from PEM
with open("private.pem") as f:
    sk = SigningKey.from_pem(f.read())
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