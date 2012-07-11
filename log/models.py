from django.db import models

class Old(models.Model):
    subject = models.CharField(max_length=60, primary_key=True)
    
class Terms(models.Model):
    term = models.CharField(max_length=100, primary_key=True)
    count = models.IntegerField()
    
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    
class SubjectCategory(models.Model):
    subjectcategoryid = models.AutoField(primary_key=True)
    subjectcategory = models.CharField(max_length=255)
    
class Current(models.Model):
    subject = models.CharField(max_length=255, primary_key=True)
    count = models.IntegerField(null=True)
    date = models.DateField(auto_now=True)
    category = models.ForeignKey("Category", null=True, blank=True)
    subjectcategory = models.ForeignKey("SubjectCategory", null=True, blank=True)
    acquisition = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    note = models.TextField()

