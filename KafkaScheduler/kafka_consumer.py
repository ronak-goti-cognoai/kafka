from utils_livechat_reports_testing import _init_livechat_reports_testing_consumer
from kafka import KafkaConsumer
from flask import Flask
from utils_livechat import LiveChatUtils
from utils_livechat_reports import _init_livechat_reports_consumer

import json
import threading

app = Flask(__name__)

with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())

app.config.update(config)

kafka_consumer = KafkaConsumer(app.config["TOPIC"], 
                               bootstrap_servers=app.config["KAFKA_BOOTSTRAP_SERVERS"], 
                               value_deserializer=lambda x: json.loads(x.decode('utf-8')))

livechat_obj = LiveChatUtils(app.config)

def _assign_livechat_agent(data):
    livechat_obj.request_to_assign_livechat_customer_to_agent(data)

def _init_kafka_listener():
    kafka_consumer.poll()
    for msg in kafka_consumer:
        _assign_livechat_agent(msg.value)

def _start_kafka_flask_app():
    # thread = threading.Thread(target=_init_kafka_listener, daemon=True)
    # thread.start()
    thread = threading.Thread(target=_init_livechat_reports_consumer, daemon=True)
    thread.start()
    # thread = threading.Thread(target=_init_livechat_reports_testing_consumer, daemon=True)
    # thread.start()
    
    return app

if __name__ == "__main__":
    _start_kafka_flask_app()
    app.run(port=5004, use_reloader=False, debug=True)
