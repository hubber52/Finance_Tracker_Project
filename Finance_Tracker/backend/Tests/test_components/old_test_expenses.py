from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model


class ExpenseTest(APITestCase):

    def setUp(self):
        print("Running test_expenses")
        self.CustomUser =  get_user_model()
        self.data = {
            "username": "john",
            "expense_name": "ExpenseTest1",
            "expense_category": "Essential",
            "expense_amount": 10.0,
            "notes": "Misc cat",
            "expense_rate": "Weekly",
        }
        self.data2 = {
            "username": "johndad",
            "expense_name": "ExpenseTest2",
            "expense_category": "Discretionary",
            "expense_amount": 50.0,
            "notes": "Misc cat",
            "expense_rate": "Monthly",
        }
        self.data3 = {
            "username": "john",
            "expense_name": "ExpenseTest3",
            "expense_category": "Essential",
            "expense_amount": 100.0,
            "notes": "Misc cat",
            "expense_rate": "Monthly",
        }

        self.data4 = {
            "username": "john",
            "expense_name": "ExpenseTest4",
            "expense_category": "Discretionary",
            "expense_amount": 110.0,
            "notes": "Misc cat",
            "expense_rate": "Annually",
        }
        self.user = self.CustomUser.objects.create_user(username="john", password="johnpassword")
        self.credentials = {"username":"test1", "password":"test1"}
        self.unAuthorizedCreds = {"username":"test2", "password":"test2"}
        self.client = APIClient()

    def test_unAuth_expense_post(self):
        post_url = reverse('expenseCreateView')
        response = self.client.post(post_url, self.data2, format = 'json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_CRUD_expense(self):
        register_url = reverse('registrationView')

        #Create a user using the registration api
        registerResponse = self.client.post(register_url, self.credentials, format='json') #Create authorized User
        self.assertEqual(registerResponse.status_code, 201)

        #Log in with the user created using the registration api
        login_url = reverse('loginView')
        loginResponse = self.client.post(login_url, self.credentials)
        login_access_token = loginResponse.data['access']
        refresh_access_tokens = loginResponse.data['refresh']
        login_headers_primary = {'HTTP_AUTHORIZATION': f'Bearer {login_access_token}'}
        #token_headers_primary = {'HTTP_AUTHORIZATION': f'Bearer {refresh_access_tokens}'}

        #Get a list of expenses which are owned by the logged in user
        get_url = reverse('expenseGetView')
        getEmptyResponse = self.client.get(get_url, **login_headers_primary)
        self.assertEqual(getEmptyResponse.status_code, 200)


        current_username = loginResponse.wsgi_request.user.username
        post_url = reverse('expenseCreateView')
        postResponse = self.client.post(post_url, self.data, **login_headers_primary, format='json')
        self.assertEqual(postResponse.status_code, 201)

        #Create extra data
        self.client.post(post_url, self.data3, **login_headers_primary, format='json')
        self.assertEqual(postResponse.status_code, 201)
        self.client.post(post_url, self.data4, **login_headers_primary, format='json')
        self.assertEqual(postResponse.status_code, 201)

        getTotal_url = reverse('expenseTotalView')
        getTotalResponse = self.client.get(getTotal_url, **login_headers_primary)
        self.assertEqual(getTotalResponse.status_code, status.HTTP_200_OK)

        getTotalDiscretionary_url = reverse('expenseTotalDiscretionaryView')
        discretionary_response = self.client.get(getTotalDiscretionary_url, **login_headers_primary)
        self.assertEqual(discretionary_response.status_code, status.HTTP_200_OK)
        
        getTotalEssential_url = reverse('expenseTotalEssentialView')
        essential_response = self.client.get(getTotalEssential_url, **login_headers_primary)
        self.assertEqual(essential_response.status_code, status.HTTP_200_OK)
        
        #Get the line item called "waste"
        getOneResponse = self.client.get(get_url, **login_headers_primary)
        self.assertEqual(getOneResponse.status_code, 200)

        #Log in as a second user
        self.client.post(register_url, self.unAuthorizedCreds, format='json')
        loginResponseUAuth = self.client.post(login_url, self.unAuthorizedCreds, format = 'json')
        login_access_token_UAuth = loginResponseUAuth.data['access']
        login_headers_UAuth = {'HTTP_AUTHORIZATION': f'Bearer {login_access_token_UAuth}'}
        
        #Get all expense data associated with the new user, should return nothing.
        getResponseUAuth = self.client.get(get_url, **login_headers_UAuth)
        self.assertEqual(getResponseUAuth.data, [])

        #Update line item "waste" to "treasure"
        put_url = reverse('expenseUpdateDeleteView', kwargs={'pk':1})
        new_data = {"username":current_username, "expense_name": "treasure"}
        putResponse = self.client.put(put_url, new_data, **login_headers_primary)
        self.assertEqual(putResponse.data['expense_name'], 'treasure')

        #Delete line item "treasure"
        delete_url = put_url
        deleteResponse = self.client.delete(delete_url, **login_headers_primary)
        self.assertEqual(deleteResponse.status_code, 204)

        getResponse_second = self.client.get(get_url, **login_headers_primary)
        #self.assertEqual(getResponse_second.data,)

        #Log out of the current user
        logout_url = reverse('logoutView')
        logoutResponse = self.client.post(logout_url, {'refresh': refresh_access_tokens}, **login_headers_primary)
        self.assertEqual(logoutResponse.status_code, 205)
