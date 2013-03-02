from django.db import models
    
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    category = models.CharField(max_length=255)
    
class SubjectCategory(models.Model):
    subjectcategoryid = models.AutoField(primary_key=True)
    subjectcategory = models.CharField(max_length=255)

class Subjects(models.Model):
    subject = models.CharField(max_length=255, primary_key=True)
    category = models.ForeignKey("Category", null=True, blank=True)
    subjectcategory = models.ForeignKey("SubjectCategory", null=True, blank=True)
    acquisition = models.BooleanField(default=False)
    processed = models.BooleanField(default=False)
    note = models.TextField()

class SubjectCount(models.Model):
    subject = models.ForeignKey('Subjects', db_column="subject")
    date = models.DateField()
    count = models.IntegerField(null=True)

