from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class DebtTest(APITestCase):

    def setUp(self):
        print("Running test_debt")
        self.CustomUser =  get_user_model()
        self.data = {
            "username": "john",
            "debt_amount" : 10,
            "debt_name": "DebtTest1",
            "debt_payment": 1,
            "debt_rate" : "Monthly",
            "debt_interest": 1,
            "debt_amount": 10.0,
            "debt_notes": "Misc cat",
        }
        self.data2 = {
            "username": "johndad",
            "debt_amount" : 10,
            "debt_name": "DebtTest2",
            "debt_payment": 2,
            "debt_rate" : "Annually",
            "debt_interest": 1,
            "debt_amount": 10.0,
            "debt_notes": "Misc cat",
        }

        self.cred = {"username":"test1", "password":"test1"}
        self.unAuthorizedCreds = {"username":"test2", "password":"test2"}

    def test_CRUD(self):
        register_url = reverse('registrationView')
        response = self.client.post(register_url, self.cred, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        login_url = reverse('loginView')
        response = self.client.post(login_url, self.unAuthorizedCreds)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(login_url, self.cred)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        login_access_token = response.data['access']
        login_refresh_token = response.data['refresh']
        header = {'HTTP_AUTHORIZATION': f'Bearer {login_access_token}'}

        post_url = reverse('debtCreateView')
        response = self.client.post(post_url, self.data, **header)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        get_url = reverse('debtGetView')
        response = self.client.get(get_url, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['debt_name'], 'DebtTest1')
        primaryKey = response.data[0]['id']

        get_total_url = reverse('debtTotalView')
        total_response = self.client.get(get_total_url, **header)
        self.assertEqual(total_response.status_code, status.HTTP_200_OK)

        #Update first item that belongs to authorized user.
        put_url = reverse('debtUpdateView', kwargs={'pk':primaryKey})
        response = self.client.put(put_url, self.data2, **header)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['debt_name'], 'DebtTest2')

        #Attempt to get data as a new user
        self.client.post(register_url, self.unAuthorizedCreds)
        response = self.client.post(login_url, self.unAuthorizedCreds)
        uaccess_token = response.data['access']
        uheader = {'HTTP_AUTHORIZATION' : f'Bearer {uaccess_token}'}
        response = self.client.get(get_url, **uheader)
        self.assertEqual(response.data, [])

        response = self.client.post(login_url, self.cred)
        login_access_token = response.data['access']
        login_refresh_token = response.data['refresh']
        header = {'HTTP_AUTHORIZATION' : f'Bearer {login_access_token}'}

        #Delete first item that belongs to authorized user
        response = self.client.get(get_url, **header)
        primaryKey = response.data[0]['id']
        delete_url = reverse('debtDeleteView', kwargs = {'pk':primaryKey})
        response = self.client.delete(delete_url, **header)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(get_url, **header)
        self.assertEqual(response.data, [])

        logout_url = reverse('logoutView')
        response = self.client.post(logout_url, {'refresh': login_refresh_token}, **header)
        self.assertEqual(response.status_code, 205)

    

        


