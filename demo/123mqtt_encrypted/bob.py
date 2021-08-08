import paho.mqtt.client as mqtt
from ecdsa import ECDH, SigningKey, VerifyingKey, SECP128r1
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from os import urandom
import time
import threading
import json

PRIVATEKEY = 'bb3f488769037d24358f8060111b76fd'
shared_secret = ''

def unpack_topic(pattern, topic):
    """
    returns one string for each "+", followed by a list of strings when a trailing "#" is present
    """
    pattern_parts = iter(pattern.split("/"))
    topic_parts = iter(topic.split("/"))
    while True:
        try:
            cur_pattern = next(pattern_parts)
        except StopIteration:
            try:
                cur_topic = next(topic_parts)
                raise Exception("The topic to be matched is longer than the pattern without an # suffix. "
                                "The first unmatched part is {!r}".format(cur_topic))
            except StopIteration:
                # no more elements in both sequences.
                return
        if cur_pattern == "#":
            yield list(topic_parts)
            try:
                cur_pattern = next(pattern_parts)
                raise Exception("The pattern has a component after a #: {!r}".format(cur_pattern))
            except StopIteration:
                # topic has been exhausted by list() enumeration, and pattern is empty, too.
                return
        else:
            try:
                cur_topic = next(topic_parts)
            except StopIteration:
                raise Exception("The topic lacks a component to match a non-#-component in the pattern.")
            else:
                if cur_pattern == "+":
                    yield cur_topic
                elif "+" in cur_pattern:
                    raise Exception(
                        "The single-level wildcard can be used at any level in the Topic Filter, including first and last levels. Where it is used, it MUST occupy an entire level of the filter.")
                elif "#" in cur_pattern:
                    raise Exception(
                        "The multi-level wildcard character MUST be specified either on its own or following a topic level separator. In either case it MUST be the last character specified in the Topic Filter.")
                elif cur_pattern != cur_topic:
                    raise Exception(
                        "The pattern {!r} is no wildcard, and the topic {!r} differs.".format(cur_pattern, cur_topic))
                else:  # pattern == topic and neither contain a # or +
                    # we do not yield return constant non-wildcards.
                    continue

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # subscribe to public-chat (sub-topic-allowed)
    client.subscribe("public-chat/#")

    # subscribe to public-data (sub-topic allowed)
    client.subscribe("public-data/+/Silly-Headrest-2013/request")
    client.subscribe("public-data/+/Silly-Headrest-2013/publickey")
    client.subscribe("public-data/+/Silly-Headrest-2013/message")

    # subscribe to private channel (sub-topic allowed)
    # topic: <username>/#
    client.subscribe("Silly-Headrest-2013/#")

def on_message(client, userdata, msg):
    global shared_secret
    print(msg.topic + ': ' + msg.payload.decode())
    received = list(unpack_topic('public-data/+/Silly-Headrest-2013/#', msg.topic))
    print(received)
    sender = received[0]
    message_type = received[1][0]
    if (message_type == 'request' and msg.payload == b'publickey'):
        # got a request for a public key
        print('sending public key')
        client.publish('public-data/Silly-Headrest-2013/' + received[0] + '/publickey', vk.to_string().hex(), 2)
    elif (message_type == 'publickey'):
        # received public key from the other end
        received_public_key = msg.payload
        ecdh.load_received_public_key_bytes(bytearray.fromhex(received_public_key.decode()))
        shared_secret = ecdh.generate_sharedsecret_bytes()
        print('Shared secret: ' + shared_secret.hex())
    elif (message_type == 'message'):
        # got a message
        received = json.loads(msg.payload)
        # decrypting message when shared secret is obtained
        if (shared_secret != '' and received['encryption'] != 'none'):
            decrypto = AES.new(shared_secret, AES.MODE_CBC, bytes.fromhex(received['iv']))
            decrypted_text_bytes = decrypto.decrypt(bytes.fromhex(received['message']))
            print('*** Decrypted message: ', decrypted_text_bytes.decode())
    else:
        pass

def on_publish(client, userdata, mid):
    print('message published')

def update_public_shared_secret():
    # request Alice's public key
    print(time.ctime())
    client.publish("public-data/Silly-Headrest-2013/Old-Engine-6372/request", "publickey", 2)
    threading.Timer(30, update_public_shared_secret).start()

def send_periodic_message():
    global shared_secret
    print(time.ctime())
    if (shared_secret == ''):
        #send unencrypted message
        message = {"message" : "hello Alice!", "encryption" : "none", "iv" : "none"}
        client.publish("public-data/Silly-Headrest-2013/Old-Engine-6372/message", json.dumps(message), 2)
    else:
        #send encrypted message
        message = 'hello Alice!'
        signature = sk.sign(pad(message.encode(), AES.block_size))
        iv = urandom(16)
        crypto = AES.new(shared_secret, AES.MODE_CBC, iv)
        encrypted_text_bytes = crypto.encrypt(pad(message.encode(), AES.block_size))
        encrypted_text_hex = encrypted_text_bytes.hex()
        message = {"message" : encrypted_text_hex, "encryption" : "AES-128-CBC", "iv" : iv.hex()}
        client.publish("public-data/Silly-Headrest-2013/Old-Engine-6372/message", json.dumps(message), 2)
    threading.Timer(5, send_periodic_message).start()

# get private key and public keys, and load private key for ECDH
sk_string = bytearray.fromhex(PRIVATEKEY)
sk = SigningKey.from_string(sk_string, SECP128r1)
vk = sk.verifying_key
ecdh = ECDH(curve=SECP128r1)
ecdh.load_private_key(sk)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.username_pw_set(username='Silly-Headrest-2013', password='jTeMIfTy')
client.connect("123mqtt.com", 1883, 60)

threading.Timer(30, update_public_shared_secret).start()
send_periodic_message()

# do not exit
client.loop_forever()