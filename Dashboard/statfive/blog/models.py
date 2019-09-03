import datetime
from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=42)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now, verbose_name="Date de parution")

    class Meta:
        ordering = ['date']
    
    def __str__(self):
        return self.name

#Article.objects.create(titre="Bonjour", auteur="Maxime", contenu="Salut")
#Article.objects.all()