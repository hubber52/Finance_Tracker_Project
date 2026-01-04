from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class incomeTest(APITestCase):

    def setUp(self):
        print("Running test_income")
        self.CustomUser =  get_user_model()
        self.data = {
            "username": "john",
            "income_amount" : 10,
            "income_name": "IncomeTest1",
            "income_type": "Job",
            "income_rate": "Weekly",
            "income_notes": "Misc cat",
        }
        self.data2 = {
            "username": "johndad",
            "income_amount" : 101,
            "income_name": "IncomeTest2",
            "income_type": "Royalty",
            "income_rate": "Weekly",
            "income_notes": "Misc cat",
        }

        self.cred = {"username":"test1", "password":"test1"}
        self.unAuthorizedCreds = {"username":"test2", "password":"test2"}

    def test_unAuth_income_post(self):
        post_url = reverse('incomeCreateView')
        response = self.client.post(post_url, self.data2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_income_CRUD(self):
        register_url=reverse('registrationView')
        register_response = self.client.post(register_url, self.cred, format = 'json')
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)

        login_url = reverse('loginView')
        login_response = self.client.post(login_url, self.cred, format = 'json')
        self.assertEqual(login_response.status_code, status.HTTP_202_ACCEPTED)
        login_refresh_token = login_response.data['refresh']
        login_access_token = login_response.data['access']
        header = {'HTTP_AUTHORIZATION' : f'Bearer {login_access_token}'}

        create_url = reverse('incomeCreateView')
        success_create_response = self.client.post(create_url, self.data, **header, format = 'json')
        self.assertEqual(success_create_response.status_code, status.HTTP_201_CREATED)
        
        get_url = reverse('incomeGetView')
        success_get_response = self.client.get(get_url, **header, format = 'json')
        primaryKey = success_get_response.data[0]['id']

        success_get_data = success_get_response.data[0]
        success_get_data.pop('id')
        success_get_data.pop('user')
        success_get_data.pop('income_datetime')
        self.assertEqual(success_get_data, self.data)

        get_total_url = reverse('incomeTotalView')
        total_response = self.client.get(get_total_url, **header)
        self.assertEqual(total_response.status_code, status.HTTP_200_OK)

        failed_get_response = self.client.get(get_url, format = 'json')
        self.assertEqual(failed_get_response.status_code, status.HTTP_401_UNAUTHORIZED)

        update_url = reverse('incomeUpdateDeleteView', kwargs={'pk': primaryKey})
        update_response = self.client.put(update_url, self.data2, **header, format = 'json')
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        update_response.data.pop('id')
        update_response.data.pop('user')
        update_response.data.pop('income_datetime')
        self.assertEqual(update_response.data, self.data2)

        delete_url = reverse('incomeUpdateDeleteView', kwargs={'pk' : primaryKey})
        delete_response = self.client.delete(delete_url, **header, format = 'json')
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)