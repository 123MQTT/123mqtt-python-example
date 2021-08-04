import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # subscribe to public-chat (sub-topic-allowed)
    client.subscribe("public-chat/#")

    # subscribe to public-data (sub-topic allowed)
    client.subscribe("public-data/#")

    # subscribe to private channel (sub-topic allowed)
    # topic: <username>/#
    client.subscribe("Dopey-Speech-7536/#")

def on_message(client, userdata, msg):
    print(msg.topic + ': ' + msg.payload.decode())

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username='Dopey-Speech-7536', password='2KtufXTC')
client.connect("123mqtt.com", 1883, 60)

# do not exit
client.loop_forever()