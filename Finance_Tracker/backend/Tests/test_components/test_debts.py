from unittest.mock import patch
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.Models.debt_information import DebtModel
from ..Factory.django_factories import UserFactory, DebtFactory

#Unit tests for backend.Components.debt_information
class TestDebt(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.debt = DebtFactory(user=self.user)

    def test_get_debt_successful(self):
        get_url = reverse('debtGetView')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(get_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_debt_no_authentication(self):
        get_url = reverse('debtGetView')
        response = self.client.get(get_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class DebtCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
    
    def test_create_debt_success(self):
        data = {'debt_name':'name'}
        self.client.force_authenticate(user=self.user)
        create_url = reverse('debtCreateView')
        response = self.client.post(create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['debt_name'], 'name')
    
    def test_create_debt_no_authentication(self):
        data = {'debt_name':'name'}
        create_url = reverse('debtCreateView')
        response = self.client.post(create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_debt_invalid_data(self):
        # Invalid data (incorrect field type)
        url = reverse('debtCreateView')
        data = {'debt_name': [100]}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('debt_name', response.data)

class DebtUpdateViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.debt = DebtFactory(user=self.user)

    def test_get_debt(self):
        url = reverse('debtGetView')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['debt_name'], self.debt.debt_name)

    def test_update_debt_success(self):
        url = reverse('debtUpdateView', args=[self.debt.id])
        data = {"debt_amount": 200, "debt_name": "Updated Debt"}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.debt.refresh_from_db()  # Reload from database
        self.assertEqual(self.debt.debt_amount, 200)
        self.assertEqual(self.debt.debt_name, "Updated Debt")

    def test_update_debt_forbidden(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        url = reverse('debtUpdateView', args=[self.debt.id])
        data = {"debt_amount": 200, "debt_name": "Updated Debt"}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

class DebtDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.debt = DebtFactory(user=self.user)

    def test_delete_debt_success(self):
        url = reverse('debtDeleteView', args=[self.debt.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(DebtModel.objects.filter(id=self.debt.id).exists())

    def test_delete_debt_forbidden(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        url = reverse('debtDeleteView', args=[self.debt.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DebtTotalViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.debt1 = DebtFactory(user=self.user)
        self.debt2 = DebtFactory(user=self.user)

    def test_get_debts_total(self):
        url = reverse('debtTotalView')
        with patch("backend.Models.debt_information.DebtModel.customObject.get_total") \
            as mock_get_total, patch("backend.Components.in_debt_flag.InDebtCheck.get_debt_flag") \
            as mock_kafka:

            mock_get_total.return_value = {"debt_amount": float(self.debt1.debt_amount) 
                                                            + float(self.debt2.debt_amount)}
            mock_kafka.return_value = None  # Kafka producer does nothing
            response = self.client.get(url)
            assert response.status_code == 200
            mock_kafka.assert_called_once_with(user=self.user, total=float(self.debt1.debt_amount) 
                                                    + float(self.debt2.debt_amount))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("debt_amount", response.data)
        self.assertEqual(response.data["debt_amount"], float(self.debt1.debt_amount) 
                                                        + float(self.debt2.debt_amount))

    def test_get_debts_total_no_debts(self):
        self.user2 = UserFactory()
        self.client.force_authenticate(user=self.user2)
        url = reverse('debtTotalView')
        response = self.client.get(url)

        with patch("backend.Models.debt_information.DebtModel.customObject.get_total") as mock_get_total, \
            patch("backend.Components.in_debt_flag.InDebtCheck.get_debt_flag") as mock_kafka:

            mock_get_total.return_value = {"debt_amount": 0}
            mock_kafka.return_value = None  # Kafka producer does nothing

            response = self.client.get(url)
            assert response.status_code == 200
            mock_kafka.assert_called_once_with(user=self.user2, total=0)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("debt_amount", response.data)
        self.assertEqual(response.data["debt_amount"], 0)

class DebtPaymentViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.debt1 = DebtFactory(user=self.user)
        self.debt2 = DebtFactory(user=self.user)

    def test_get_debt_payment_total(self):
        payment_url = reverse('debtPaymentView')
        response = self.client.get(payment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['debt_payment'], 
                         self.debt1.debt_payment 
                         + self.debt2.debt_payment)
