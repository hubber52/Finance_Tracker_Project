import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from backend.Models.income_information import IncomeModel
from backend.Models.expense_information import ExpenseModel
from backend.Models.debt_information import DebtModel

class UserFactory(DjangoModelFactory):
    class Meta:
        model = get_user_model()
    username = factory.Sequence(lambda n: f'user_{n}')
    email = factory.Sequence(lambda n: f'user_{n}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'testpassword123')
    phone = '+12345678901'

class ExpenseFactory(DjangoModelFactory):
    class Meta:
        model = ExpenseModel
    username = ''
    user = ''
    expense_amount = factory.Sequence(lambda n: f'{n}')
    expense_name = factory.Sequence(lambda n: f'name_{n}')
    expense_category = factory.Sequence(lambda n: f'type_{n}')
    expense_rate = 'Weekly'
    expense_notes = ''

class IncomeFactory(DjangoModelFactory):
    class Meta:
        model = IncomeModel
    username = ''
    user = ''
    income_amount = factory.Sequence(lambda n: f'{n}')
    income_name = factory.Sequence(lambda n: f'name_{n}')
    income_type = factory.Sequence(lambda n: f'type_{n}')
    income_rate = 'Weekly'
    income_notes = ''

class DebtFactory(DjangoModelFactory):
    class Meta:
        model = DebtModel
    username = ''
    user = ''
    debt_amount = factory.Sequence(lambda n: f'{n}')
    debt_name = factory.Sequence(lambda n: f'name_{n}')
    debt_payment = factory.Sequence(lambda n: n)
    debt_rate = 'Weekly'
    debt_interest = factory.Sequence(lambda n: n)
    debt_notes = ''

'''
    debt_amount = models.FloatField(default=0.0, blank=True)
    debt_name = models.CharField(default="", blank=True)
    debt_payment = models.FloatField(default=0, blank=True)
    debt_rate = models.CharField(default="Weekly", blank=True)
    debt_interest = models.FloatField(default=0, blank=True)
    debt_notes = models.CharField(default="", blank=True)
    debt_datetime = models.DateTimeField(auto_now=True, 
                                         blank=True, 
                '''