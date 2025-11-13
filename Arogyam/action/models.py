from django.db import models

class Admin(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=500, null=True)
    pwd = models.CharField(max_length=50)