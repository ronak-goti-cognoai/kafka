from django.conf import settings
from kafka import KafkaProducer
import logger_setup


import json

kafka_producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v: json.dumps(v).encode('utf-8')
)

def send_packet_into_kafka_producer(topic, value):
    logger = logger_setup.setup_logger(__name__,'app.log')
    logger.info("Inside send_packet_into_kafka_producer topic:")
    kafka_producer.send(topic, value = value)
    kafka_producer.flush()
    logger.info("Exit send_packet_into_kafka_producer")

# send_packet_into_kafka_producer('LiveChatCustomerTopic',{"type": "LiveChatLeadAssigment"})