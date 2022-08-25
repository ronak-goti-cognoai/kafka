from time import sleep, time
from kafka import KafkaConsumer
from flask import Flask
from utils_livechat import LiveChatUtils

import json

app = Flask(__name__)

with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())

app.config.update(config)

livechat_report_testing_consumer = KafkaConsumer(app.config["TOPIC2"], 
                               bootstrap_servers=app.config["KAFKA_BOOTSTRAP_SERVERS"], 
                               value_deserializer=lambda x: json.loads(x.decode('utf-8')))

livechat_obj = LiveChatUtils(app.config)

def _generate_livechat_report_testing(data):
    livechat_obj.generate_livechat_report(data)

def _init_livechat_reports_testing_consumer():
    livechat_report_testing_consumer.poll()
    for msg in livechat_report_testing_consumer:
        _generate_livechat_report_testing(msg.value)
