# import paho.mqtt.client as mqtt

# # Cấu hình HiveMQ broker
# broker_address = "85334ea20e91412da2bcf2c26bf7e321.s1.eu.hivemq.cloud"
# port = 8883
# topic = "your/topic"

# # Hàm callback khi kết nối thành công với broker
# def on_connect(client, userdata, flags, rc):
#     if rc == 0:
#         print("Kết nối thành công!")
#         # Bạn có thể publish dữ liệu tại đây nếu muốn
#         client.publish(topic, "Hello from Raspberry Pi!")
#     else:
#         print("Kết nối thất bại với mã lỗi ", rc)

# # Hàm callback khi có tin nhắn mới từ broker
# def on_message(client, userdata, message):
#     print("Nhận tin nhắn: ", str(message.payload.decode("utf-8")))

# # Tạo MQTT client và thiết lập hàm callback
# client = mqtt.Client()
# client.on_connect = on_connect
# client.on_message = on_message

# # Kết nối tới HiveMQ broker
# client.connect(broker_address, port=port)

# # Đăng ký (subscribe) vào một topic nếu cần
# client.subscribe(topic)

# # Bắt đầu vòng lặp để giữ kết nối và lắng nghe tin nhắn
# client.loop_forever()


#
# Copyright 2021 HiveMQ GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import ssl
from paho import mqtt
import paho.mqtt.client as paho
import paho.mqtt.publish as publish

# create a set of 2 test messages that will be published at the same time
msgs = [{'topic': "paho/test/multiple", 'payload': "hi truong!"}, ("paho/test/multiple", "test 2", 0, False)]

# use TLS for secure connection with HiveMQ Cloud
sslSettings = ssl.SSLContext(mqtt.client.ssl.PROTOCOL_TLS)

# put in your cluster credentials and hostname
auth = {'username': "hivemq.webclient.1723605366923", 'password': "34HAZOGayun68,<Nl%d#"}
publish.multiple(msgs, hostname="85334ea20e91412da2bcf2c26bf7e321.s1.eu.hivemq.cloud", port=8883, auth=auth,
                 tls=sslSettings, protocol=paho.MQTTv31)