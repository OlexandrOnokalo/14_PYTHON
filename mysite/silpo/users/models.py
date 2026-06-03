from django.db import models
from django.contrib.auth.models import AbstractUser
 

# Create your models here.
class CustomUser(AbstractUser):
    image_small = models.CharField(max_length=100, blank=True, null=True)
    image_medium = models.CharField(max_length=100, blank=True, null=True)
    image_large = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.email