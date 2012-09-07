#coding: utf-8
from django import forms

from log.models import Current, Category, SubjectCategory

categories_list = ["-", "dílo", "osoba", "korporace", "předmět", "akce", "místo", "jiné"]
subject_categories_list = ["-","deskriptor", "nedeskriptor", "podrobné", "obecné", "vícevýznamové", "produkt", "slang", "málo užívané", "profesní skupina", "obsaženo v PSH"]

categories_list = Category.objects.all()
categories = [(c.categoryid, c.category) for c in categories_list]
categories.insert(0, (0, "-"))

subject_categories_list = SubjectCategory.objects.all()
subject_categories = [(c.subjectcategoryid, c.subjectcategory) for c in subject_categories_list]
subject_categories.insert(0, (0, "-"))

class EditForm(forms.Form):
    """Model of form for file upload"""
    # categories = tuple([(c, categories_list[c]) for c in range(len(categories_list))])
    # subject_categories = tuple([(s, subject_categories_list[s]) for s in range(len(subject_categories_list))])        
    
    category = forms.ChoiceField(categories)
    subject_category = forms.ChoiceField(subject_categories, widget=forms.Select(attrs={'disabled':'disabled'}))
    acquisition = forms.BooleanField()
    note = forms.CharField(widget=forms.Textarea)

class FilterForm(forms.Form):
    filter_subject_category = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple, choices=subject_categories[1:])
    filter_category = forms.MultipleChoiceField(required=False, widget=forms.SelectMultiple, choices=categories[1:])
    hide_processed = forms.BooleanField()
