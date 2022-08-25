from kafka import KafkaConsumer
from flask import Flask
from utils_livechat import LiveChatUtils
import logger_setup
import json

app = Flask(__name__)

with open("config.json", "r") as config_file:
    config = json.loads(config_file.read())

app.config.update(config)

livechat_report_consumer = KafkaConsumer(app.config["TOPIC1"], 
                               bootstrap_servers=app.config["KAFKA_BOOTSTRAP_SERVERS"], 
                               value_deserializer=lambda x: json.loads(x.decode('utf-8')))

livechat_obj = LiveChatUtils(app.config)

def _generate_livechat_report(data):
    logger = logger_setup.setup_logger(__name__,'app.log')
    logger.info("inside generate report")
    livechat_obj.generate_livechat_report(data)

def _init_livechat_reports_consumer():
    livechat_report_consumer.poll()
    for msg in livechat_report_consumer:
        _generate_livechat_report(msg.value)
