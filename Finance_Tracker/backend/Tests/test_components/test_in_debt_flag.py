from django.test import TestCase
from unittest.mock import patch, MagicMock
from backend.Components.in_debt_flag import InDebtCheck
from backend.Models.debt_information import InDebtModel
from backend.Tests.Factory.django_factories import UserFactory

class TestInDebtCheck(TestCase):
    @patch("backend.Components.kafka_messages.KafkaMessageService")
    def test_get_debt_flag_in_debt(self, MockKafkaMessageService):

        # Mock the debtor
        mock_user = UserFactory()
        # Mock the InDebtModel lookup and its instance (simulate in debt)
        mock_debtor = MagicMock(spec=InDebtModel)
        mock_debtor.save = MagicMock()
        mock_debtor.negative_debt = 1  # Simulate user being in debt
        total_debt = 0  # This should trigger the "out of debt" logic in the helper method
        response = InDebtCheck.get_debt_flag(mock_user, 
                                             total_debt, 
                                             producer=MockKafkaMessageService)
        self.assertEqual(response, True)

    @patch("backend.Components.kafka_messages.KafkaMessageService")
    def test_get_debt_flag_in_debt(self, MockKafkaMessageService):

        # Mock the debtor
        mock_user = UserFactory()
        mock_debtor = MagicMock(spec=InDebtModel)
        mock_debtor.save = MagicMock()
        mock_debtor.negative_debt = 0  # Simulate user not in debt
        mock_debtor.save = MagicMock()
        total_debt = 1  # This should trigger the "in debt" logic in the helper method
        response = InDebtCheck.get_debt_flag(mock_user, 
                                             total_debt, 
                                             producer=MockKafkaMessageService)
        
        self.assertEqual(response, True)

    @patch("backend.Components.kafka_messages.KafkaMessageService")
    def test_get_debt_flag_no_update(self, MockKafkaMessageService):

        # Mock the debtor
        mock_user = UserFactory()
        mock_debtor = MagicMock(spec=InDebtModel)
        mock_debtor.save = MagicMock()
        mock_debtor.negative_debt = 1  # Simulate user with no debt update
        mock_debtor.save = MagicMock()
        total_debt = 1  # This should trigger no call
        response = InDebtCheck.get_debt_flag(mock_user, 
                                             total_debt, 
                                             producer=MockKafkaMessageService)
        
        self.assertEqual(response, True)

    @patch("backend.Components.kafka_messages.KafkaMessageService")
    def test_get_debt_flag_no_user(self, MockKafkaMessageService):
        total_debt = 1
        response = InDebtCheck.get_debt_flag(None, 
                                            total_debt, 
                                            producer=MockKafkaMessageService)
        
        self.assertEqual(response.status_code, 404)