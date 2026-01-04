from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.Models.income_information import IncomeModel
from ..Factory.django_factories import UserFactory, IncomeFactory

#Unit tests for backend.Components.income_information
class TestIncome(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.income = IncomeFactory(user=self.user)

    def test_get_income_successful(self):
        get_url = reverse('incomeGetView')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(get_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_get_income_no_authentication(self):
        get_url = reverse('incomeGetView')
        response = self.client.get(get_url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
class IncomeCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
    
    def test_create_income_success(self):
        data = {'income_name':'name'}
        self.client.force_authenticate(user=self.user)
        create_url = reverse('incomeCreateView')
        response = self.client.post(create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['income_name'], 'name')
    
    def test_create_income_no_authentication(self):
        data = {'income_name':'name'}
        create_url = reverse('incomeCreateView')
        response = self.client.post(create_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_income_invalid_data(self):
        # Invalid data (incorrect field type)
        url = reverse('incomeCreateView')
        data = {'income_name': [100]}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('income_name', response.data)

class IncomeUpdateDeleteViewTest(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.income = IncomeFactory(user=self.user)


    def test_get_income(self):
        url = reverse('incomeGetView')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['income_name'], self.income.income_name)

    def test_update_income_success(self):
        url = reverse('incomeUpdateDeleteView', args=[self.income.id])
        data = {"income_amount": 200, "income_name": "Updated Income"}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.income.refresh_from_db()  # Reload from database
        self.assertEqual(self.income.income_amount, 200)
        self.assertEqual(self.income.income_name, "Updated Income")


    def test_update_income_forbidden(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        url = reverse('incomeUpdateDeleteView', args=[self.income.id])
        data = {"income_amount": 200, "income_name": "Updated Income"}
        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_delete_income_success(self):
        url = reverse('incomeUpdateDeleteView', args=[self.income.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(IncomeModel.objects.filter(id=self.income.id).exists())

    def test_delete_income_forbidden(self):
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)
        url = reverse('incomeUpdateDeleteView', args=[self.income.id])
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class IncomeTotalViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.income1 = IncomeFactory(user=self.user)
        self.income2 = IncomeFactory(user=self.user)

    def test_get_incomes_total(self):
        url = reverse('incomeTotalView')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("income_amount", response.data)
        self.assertEqual(response.data["income_amount"], 
                         float(self.income1.income_amount) 
                         + float(self.income2.income_amount))

    def test_get_incomes_total_no_incomes(self):
        self.user2 = UserFactory()
        self.client.force_authenticate(user=self.user2)
        url = reverse('incomeTotalView')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("income_amount", response.data)
        self.assertEqual(response.data["income_amount"], 0)
