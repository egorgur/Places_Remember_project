from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Memo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=300)
    text = models.TextField(max_length=1500, null=True, blank=True)
    position_x = models.FloatField()
    position_y = models.FloatField()

    def __str__(self):
        return "Memo " + self.name


class userInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vk_fio = models.TextField(max_length=300)
    icon_href =  models.TextField(max_length=300)
