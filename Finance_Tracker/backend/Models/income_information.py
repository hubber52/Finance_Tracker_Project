from django.db import models
from django.conf import settings
from .custom_manager import CustomManager

class IncomeModel(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=100, 
                                default="", 
                                blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, 
                             on_delete=models.CASCADE, 
                             related_name='UserIncome', 
                             blank=True, 
                             null=True
                             )
    income_amount = models.FloatField(default=0)
    income_name = models.CharField(default="", blank=True)
    income_type = models.CharField(default="", blank=True)
    income_rate = models.CharField(default="Weekly", blank=True)
    income_notes = models.CharField(default="", blank=True)
    income_datetime = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    customObject = CustomManager()

    def __str__(self):
        return self.income_name