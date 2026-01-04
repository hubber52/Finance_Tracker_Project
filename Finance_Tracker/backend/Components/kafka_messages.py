from confluent_kafka import Producer
import json

topic = "Ruby_Message_Service"

class KafkaMessageService:
    def __init__(self, producer=None):
        conf = {'bootstrap.servers': "localhost:9092", 'retries': 3}
        self.producer = producer or Producer(conf)
    
    def send_message(self, body):
        self.producer.produce(topic, value=json.dumps(body))
        self.producer.flush()
    