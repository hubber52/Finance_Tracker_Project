from django.db import models
from django.conf import settings
from .custom_manager import CustomManager


class ExpenseModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(default = "", 
                                max_length=100, 
                                blank = True)
    expense_name = models.CharField(max_length=100, 
                                    default = "", 
                                    blank = True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='customUserModel', # Optional: A reverse relationship name
        null = True,
        blank = True,
    )
    expense_category = models.CharField(max_length=100, 
                                        default = "Essential", 
                                        blank = True)
    expense_amount = models.FloatField(max_length=10, 
                                       default = 0, 
                                       blank = True)
    expense_notes = models.CharField(max_length=200, 
                                     default = "", 
                                     blank = True)
    expense_rate = models.CharField(max_length=20, 
                                    default = 'Weekly', 
                                    blank = True)
    expense_datetime = models.DateTimeField(auto_now = True, 
                                            null = True, 
                                            blank = True)
    
    #Custom model managers
    objects = models.Manager()
    customObject = CustomManager()


    def __str__(self):
        return self.expense_name
    



