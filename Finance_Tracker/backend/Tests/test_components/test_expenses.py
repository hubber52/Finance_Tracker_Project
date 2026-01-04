from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from backend.Models.expense_information import ExpenseModel
from ..Factory.django_factories import UserFactory, ExpenseFactory

#Unit Tests for backend.Components.expense_information
class ExpenseGetViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.expense = ExpenseFactory(user=self.user)

    def test_get_expenses_success(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('expenseGetView')
        response = self.client.get(url)

        # Check that the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_expenses_no_authentication(self):
        # Test without authentication
        url = reverse('expenseGetView')
        response = self.client.get(url)

        # Ensure it returns unauthorized error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ExpenseCreateViewTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_create_expense_success(self):
        # Valid data
        url = reverse('expenseCreateView')
        data = {"expense_amount": 100, "expense_name": "Test Expense"}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        # Check if the response is successful and the data is correct
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['expense_amount'], 100)
        self.assertEqual(response.data['expense_name'], "Test Expense")

    def test_create_expense_no_authentication(self):
        # Test without authentication
        url = reverse('expenseCreateView')  # Adjust to your URL name
        data = {"expense_amount": 100, "expense_name": "Test Expense"}
        response = self.client.post(url, data, format='json')

        # Ensure it returns unauthorized error
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_expense_invalid_data(self):
        # Invalid data (incorrect field type)
        url = reverse('expenseCreateView')
        data = {"expense_name": [100]}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')

        # Check for validation errors
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("expense_name", response.data)


class ExpenseUpdateDeleteViewTestCase(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        self.expense = ExpenseModel.objects.create(user=self.user, 
                                                   expense_amount=50, 
                                                   expense_name="Test Expense")

    def test_get_expense(self):
        # Get the expense by ID
        url = reverse('expenseGetView')
        response = self.client.get(url)

        # Ensure the expense is returned correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['expense_name'], "Test Expense")

    def test_update_expense_success(self):
        # Update the expense
        url = reverse('expenseUpdateDeleteView', args=[self.expense.id])
        data = {"expense_amount": 200, "expense_name": "Updated Expense"}
        response = self.client.put(url, data, format='json')

        # Check that the update was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.expense.refresh_from_db()  # Reload from database
        self.assertEqual(self.expense.expense_amount, 200)
        self.assertEqual(self.expense.expense_name, "Updated Expense")

    def test_update_expense_forbidden(self):
        # Simulate a different user trying to update the expense
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)

        url = reverse('expenseUpdateDeleteView', args=[self.expense.id])
        data = {"expense_amount": 200, "expense_name": "Updated Expense"}
        response = self.client.put(url, data, format='json')

        # Should be forbidden since the user doesn't own the expense
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_expense_success(self):
        # Delete the expense
        url = reverse('expenseUpdateDeleteView', args=[self.expense.id])
        response = self.client.delete(url)

        # Ensure the expense is deleted
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ExpenseModel.objects.filter(id=self.expense.id).exists())

    def test_delete_expense_forbidden(self):
        # Simulate a different user trying to delete the expense
        new_user = UserFactory()
        self.client.force_authenticate(user=new_user)

        url = reverse('expenseUpdateDeleteView', args=[self.expense.id])
        response = self.client.delete(url)

        # Should be forbidden since the user doesn't own the expense
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class ExpenseTotalViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client.force_authenticate(user=self.user)
        # Create some expenses for this user
        ExpenseModel.objects.create(user=self.user, 
                                    expense_amount=50, 
                                    expense_name="Expense 1")
        ExpenseModel.objects.create(user=self.user, 
                                    expense_amount=100, 
                                    expense_name="Expense 2")

    def test_get_expenses_total(self):
        # Get the total expenses for the user
        url = reverse('expenseTotalView')
        response = self.client.get(url)

        # Check that the total is calculated correctly
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("expense_amount", response.data)
        self.assertEqual(response.data["expense_amount"], 150)

    def test_get_expenses_total_no_expenses(self):
        # Test when the user has no expenses
        self.user2 = UserFactory()
        self.client.force_authenticate(user=self.user2)

        url = reverse('expenseTotalView')
        response = self.client.get(url)

        # Ensure a zero total is returned for users without expenses
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("expense_amount", response.data)
        self.assertEqual(response.data["expense_amount"], 0)
