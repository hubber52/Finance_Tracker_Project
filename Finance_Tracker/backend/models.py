import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

class CustomUser(AbstractUser):
    id = models.BigAutoField(primary_key=True)
    uuid = models.UUIDField(default = uuid.uuid4, editable =False, null = True)
    phone = PhoneNumberField(blank = True, null = True)
    def __str__(self):
        return self.username
    
class CustomUserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    bio = models.CharField(blank = True, null = True)
    birth_date = models.DateField(blank = True, null = True)
    avatar = models.ImageField(blank = True, null = True)

    def __str__(self):
        return f'{self.user.username} Profile'