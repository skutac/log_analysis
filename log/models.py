from django.db import models

class Current(models.Model):
    subject = models.CharField(max_length=60, primary_key=True)
    count = models.IntegerField()

class Old(models.Model):
    subject = models.CharField(max_length=60, primary_key=True)
    
class Terms(models.Model):
    term = models.CharField(max_length=100, primary_key=True)
    count = models.IntegerField()


