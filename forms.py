from django import forms

from log.models import Current, Category, State, StateCategory

class EditForm(forms.Form):
    """Model of form for file upload"""
    categories = Category.objects.all()
    categories = tuple([(c.categoryid, c.category) for c in categories])
    
    states = State.objects.all()
    states = tuple([(s.stateid, s.state) for s in states])
    
    statecategories = StateCategory.objects.all()
    statecategories = tuple([(s.statecategoryid, s.statecategory) for s in statecategories])        
    
    category = forms.ChoiceField(categories)
    state = forms.ChoiceField(states)
    statecategory = forms.ChoiceField(statecategories)
    acquisition = forms.BooleanField()
    note = forms.CharField(widget=forms.Textarea)