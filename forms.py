#coding: utf-8
from django import forms

from log.models import Category, SubjectCategory

def get_categories():
    categories = Category.objects.all()
    categories = [(c.categoryid, c.category) for c in categories]
    categories.insert(0, (0, "-"))
    return categories

def get_subject_categories():
    subject_categories = SubjectCategory.objects.all()
    subject_categories = [(c.subjectcategoryid, c.subjectcategory) for c in subject_categories]
    subject_categories.insert(0, (0, "-"))
    return subject_categories

class EditForm(forms.Form):
    """Model of form for file upload"""

    category = forms.ChoiceField(get_categories())
    subject_category = forms.ChoiceField(get_subject_categories(), widget=forms.Select(attrs={'disabled':'disabled'}))
    acquisition = forms.BooleanField()
    note = forms.CharField(widget=forms.Textarea)

class FilterForm(forms.Form):
    filter_subject_category = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple, choices=get_subject_categories()[1:])
    filter_category = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple, choices=get_categories()[1:])
    graph = forms.MultipleChoiceField(required=False, widget=forms.Select(), choices=[(0, "-"), (1, "kategorie"), (2, "podkategorie"), (3, "akvizice")])
    hide_processed = forms.BooleanField()

class LoginForm(forms.Form):
    """Model of form for user login"""
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    
