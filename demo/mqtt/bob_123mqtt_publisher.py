import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid):
    print('message published')

client = mqtt.Client()
client.on_publish = on_publish
client.username_pw_set(username='Silly-Headrest-2013', password='jTeMIfTy')
client.connect("123mqtt.com", 1883, 60)

# publish to public-chat/<username> (no sub-topic allowed)
# topic: public-chat/<username> 
client.publish("public-chat/Silly-Headrest-2013", "Hello 123MQTT!")

# publish to public-data/<username> (sub-topic allowed)
# topic: public-data/<username>/#
client.publish("public-data/Silly-Headrest-2013/temperature/balcony", "17C")

# publish to private channel (sub-topic allowed)
# topic: <username>/#
client.publish("Silly-Headrest-2013/temperature/bedroom", "16C")

# done sending, disconnect
client.disconnect()