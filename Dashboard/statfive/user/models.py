from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


# Create your models here.
class users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user = users.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


