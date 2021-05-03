from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):

    '''Custom User model'''

    GENDER_MALE = "male"
    GENDER_FEMALE = "female"
    GENDER_OTHER = "other"

    GENDER_CHOICES = (
        (GENDER_MALE, "Male"),
        (GENDER_FEMALE,"Female"),
        (GENDER_OTHER,"Other")
    )

    avatar = models.ImageField(blank = True)
    gender = models.CharField(choices=GENDER_CHOICES,max_length=10,blank=True)
    bio = models.TextField(blank=True)
    superorganizer = models.BooleanField(default = False)
