import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid):
    print('message published')

client = mqtt.Client()
client.on_publish = on_publish
client.username_pw_set(username='Dopey-Speech-7536', password='2KtufXTC')
client.connect("123mqtt.com", 1883, 60)

# publish to public-chat/<username> (no sub-topic allowed)
# topic: public-chat/<username> 
client.publish("public-chat/Dopey-Speech-7536", "Hello 123MQTT!")

# publish to public-data/<username> (sub-topic allowed)
# topic: public-data/<username>/#
client.publish("public-data/Dopey-Speech-7536/temperature/balcony", "31C")

# publish to private channel (sub-topic allowed)
# topic: <username>/#
client.publish("Dopey-Speech-7536/temperature/bedroom", "32C")

# done sending, disconnect
client.disconnect()