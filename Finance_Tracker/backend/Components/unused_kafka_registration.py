from confluent_kafka import Producer
import json
from django.conf import settings
import logging

topic = "User_Registration"
logger = logging.getLogger(__name__)

class KafkaUserRegistration:

    def user_register(self, topic, body, producer = None):

        def delivery_report(err, msg):
            # Called once for each message produced to indicate delivery result
            if err is not None:
                logger.error(f'Message delivery failed: {err}')
            else:
                logger.info(f'Message delivered to {msg.topic()} [{msg.partition()}]')

        conf = {'bootstrap.servers': settings.KAFKA_BROKER_URL, 'retries': 3 }
        userProducer = producer or Producer(conf)
        userProducer.produce(topic, value=json.dumps(body), callback=delivery_report)
        userProducer.flush()
    


