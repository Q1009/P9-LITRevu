from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    super_user = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.username