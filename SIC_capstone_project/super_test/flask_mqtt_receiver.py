from flask import Flask, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

# Thiết lập MQTT
broker = "5b3a886659fe4b0c9123bb34ac492b6b.s1.eu.hivemq.cloud"  # Thay thế bằng broker của bạn
port = 8883
topic = "traffic_light/status"

latest_message = "Unknown"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    global latest_message
    latest_message = msg.payload.decode()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker, port, 60)
client.loop_start()

@app.route('/flask_to_web')
def flask_to_web():
    return render_template("flask_to_web.html", result=latest_message)

@app.route('/<path:path>')
def catch_all(path):
    return "This page does not exist", 404

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
