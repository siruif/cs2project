from django import forms
from . import school_info

CHOICES = school_info.school_names()
#CHOICES = [1,2,3,4,5,6]

class AddressForm(forms.Form):
    address_form = forms.CharField(label='Enter Address', max_length=500, )

class ReccomendationForm(forms.Form):
    diversity = forms.FloatField(label='Diversity', max_value=100, min_value=0)
    diversity_ranking = forms.ChoiceField(label='Ranking',choices=[(x, x) for x in range(1, 10)])
    lunch = forms.FloatField(label='Free Reduced Lunch', max_value=100, min_value=0)
    lunch_ranking = forms.ChoiceField(label='Ranking',choices=[(x, x) for x in range(1, 10)])
    english_learners = forms.FloatField(label='English Learners', max_value=100, min_value=0)
    english_ranking = forms.ChoiceField(label='Ranking',choices=[(x, x) for x in range(1, 10)])
    special_ed = forms.FloatField(label='Special Education', max_value=100, min_value=0)
    specialed_ranking = forms.ChoiceField(label='Ranking',choices=[(x, x) for x in range(1, 10)])
    performance = forms.FloatField(label='Performance', max_value=100, min_value=0)
    performance_ranking = forms.ChoiceField(label='Ranking',choices=[(x, x) for x in range(1, 10)])

class ComparisonForm(forms.Form):
    school_1 = forms.ChoiceField ( label = 'School 1', choices = [(x,x) for x in CHOICES])
    school_2 = forms.ChoiceField ( label = 'School 2', choices = [(x,x) for x in CHOICES])
    school_3 = forms.ChoiceField ( label = 'School 3', choices = [(x,x) for x in CHOICES])
    school_4 = forms.ChoiceField ( label = 'School 4', choices = [(x,x) for x in CHOICES])
    school_5 = forms.ChoiceField ( label = 'School 5', choices = [(x,x) for x in CHOICES])

