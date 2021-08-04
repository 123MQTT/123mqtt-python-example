from ecdsa import SigningKey, VerifyingKey, SECP128r1

# For quick testing purposes, Alice keypairs and Bob keypairs are generated
# within this file. In reality, both of them are on their own devices, hence
# none of them can see each other private key.

# generate Alice keypairs, return value is the private key
alice_sk = SigningKey.generate(curve=SECP128r1)
print('Alice private: ' + alice_sk.to_string().hex())

# get Alice public key
alice_vk = alice_sk.verifying_key
print('Alice public : ' + alice_vk.to_string().hex())

# Alice creates signature for the message she is about to send
message = 'hello Bob!'
signature = alice_sk.sign(message.encode())
print('Alice message: ' + message)
print('Message signature: ' + signature.hex())

# Man in the middle attack, trying to alter the reply
# Uncomment the line below and Bob can detect that the reply has been altered
#message = 'hello Dirtbag!'

# After this point the message and signature are sent to Bob
# Bob receives both message and signature from Alice and verify it againt
# Alice's public key
bob_received_msg = message
bob_received_signature = signature.hex()
bob_received_public_key = alice_vk.to_string().hex()
print('Message exchange, content: ' + bob_received_msg)
print('Message exchange, signature: ' + bob_received_signature)
print('Message exchange, public key: ' + bob_received_public_key)

# Bob verifies if public key is valid
vk_string = bytearray.fromhex(bob_received_public_key)
bob_received_vk = VerifyingKey.from_string(vk_string, SECP128r1)
print('Received public key: ' + bob_received_vk.to_string().hex())

# Bob is verifying if message is authentic
try:
    authentic = bob_received_vk.verify(bytearray.fromhex(bob_received_signature), bob_received_msg.encode())
except:
    authentic = False
print('Alice message is authentic: ' + str(authentic))

# generate Bob keypairs, return value is the private key
bob_sk = SigningKey.generate(curve=SECP128r1)
print('Bob private: ' + bob_sk.to_string().hex())

# get the public key
bob_vk = bob_sk.verifying_key
print('Bob public : ' + bob_vk.to_string().hex())

# Alice creates signature for the message she is about to send
message = 'hello Alice, good to hear from the real you!'
signature = bob_sk.sign(message.encode())
print('Bob reply: ' + message)
print('Reply signature: ' + signature.hex())

# Man in the middle attack, trying to alter the reply
# Uncomment the line below and Alice can detect that the reply has been altered
#message = 'hello Alice, go to hell!'

# After this point the reply and signature are sent to Alice
# Alice receives both reply and signature from Bob and verify it againt
# Bob's public key
alice_received_msg = message
alice_received_signature = signature.hex()
alice_received_public_key = bob_vk.to_string().hex()
print('Message exchange, content: ' + alice_received_msg)
print('Message exchange, signature: ' + alice_received_signature)
print('Message exchange, public key: ' + alice_received_public_key)

# Alice verifies if public key is valid
vk_string = bytearray.fromhex(alice_received_public_key)
alice_received_vk = VerifyingKey.from_string(vk_string, SECP128r1)
print('Received public key: ' + alice_received_vk.to_string().hex())

# Bob is verifying if message is authentic
try:
    authentic = alice_received_vk.verify(bytearray.fromhex(alice_received_signature), alice_received_msg.encode())
except:
    authentic = False
print('Bob reply is authentic: ' + str(authentic))