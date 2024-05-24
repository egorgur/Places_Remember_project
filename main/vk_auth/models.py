from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserVkData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vk_id = models.IntegerField()
    access_token = models.TextField(max_length=500)
