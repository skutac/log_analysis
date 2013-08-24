from django.db import models
from django.contrib.auth.models import User
    
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    
class SubjectCategory(models.Model):
    subjectcategoryid = models.AutoField(primary_key=True)
    subjectcategory = models.CharField(max_length=255)

class Subjects(models.Model):
    subjectid = models.AutoField(primary_key=True)
    subject = models.CharField(max_length=255)
    category = models.ForeignKey("Category", null=True, blank=True)
    subjectcategory = models.ForeignKey("SubjectCategory", null=True, blank=True)
    acquisition = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    note = models.TextField()

class SubjectCount(models.Model):
    subjectcountid = models.AutoField(primary_key=True)
    subject = models.ForeignKey('Subjects')
    date = models.DateField()
    count = models.IntegerField(null=True)
    user = models.ForeignKey(User, null=True, blank=True)
