import json
from unittest.mock import MagicMock
from django.test import TestCase
from backend.Components.kafka_messages import KafkaMessageService, topic

#Unit tests for backend.Components.kafka_messages
class KafkaMessageServiceTestCase(TestCase):
    def test_send_message_produces_and_flushes(self):
        mock_producer = MagicMock()
        service = KafkaMessageService(producer=mock_producer)
        body = {"event": "created", "id": 123}
        service.send_message(body)
        mock_producer.produce.assert_called_once_with(
            topic,
            value=json.dumps(body),
        )
        mock_producer.flush.assert_called_once()

