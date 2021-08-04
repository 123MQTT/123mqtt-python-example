import paho.mqtt.client as mqtt

def on_publish(client, userdata, mid):
    print('message published')

client = mqtt.Client()
client.on_publish = on_publish
client.username_pw_set(username='Old-Engine-6372', password='0CewA5a1')
client.connect("123mqtt.com", 1883, 60)

# publish to public-chat/<username> (no sub-topic allowed)
# topic: public-chat/<username> 
client.publish("public-chat/Old-Engine-6372", "Hello 123MQTT!")

# publish to public-data/<username> (sub-topic allowed)
# topic: public-data/<username>/#
client.publish("public-data/Old-Engine-6372/temperature/balcony", "27C")

# publish to private channel (sub-topic allowed)
# topic: <username>/#
client.publish("Old-Engine-6372/temperature/bedroom", "28C")

# done sending, disconnect
client.disconnect()