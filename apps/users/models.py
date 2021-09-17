from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField('メールアドレス', unique=True)


class Connection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followee = models.ManyToManyField(User, related_name='follower', blank=True)

    def __str__(self):
       return self.user.username
