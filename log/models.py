from django.db import models

class Old(models.Model):
    subject = models.CharField(max_length=60, primary_key=True)
    
class Terms(models.Model):
    term = models.CharField(max_length=100, primary_key=True)
    count = models.IntegerField()
    
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    
class State(models.Model):
    stateid = models.AutoField(primary_key=True)
    state = models.CharField(max_length=255)
    
class StateCategory(models.Model):
    statecategoryid = models.AutoField(primary_key=True)
    state = models.ForeignKey("State")
    statecategory = models.CharField(max_length=255)
    
class Current(models.Model):
    subject = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField()
    month = models.IntegerField()
    category = models.ForeignKey("Category", null=True, blank=True)
    state = models.ForeignKey("State", null=True, blank=True)
    processed = models.BooleanField(default=False)


