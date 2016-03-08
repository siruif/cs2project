from django import forms
from . import school_info

DEFAULT_CHOICE  = [""]

SCHOOL_CHOICES = school_info.school_names()

RACE_CHOICES = ['Asian','Black', 'White', 'Hispanic', 'Multiracial']

SCHOOL_TYPES = ['Charter', 'Neighborhood']

class AddressForm(forms.Form):
    
    address_form = forms.CharField(label='Enter Address', max_length=500, )

class ReccomendationForm(forms.Form):
    
    performance = forms.ChoiceField ( label = 'Performance \n',choices = [(x, x) for x in range ( 0, 105, 5 ) ] )
    
    free_red_lunch = forms.ChoiceField( label = 'Free and Reduced Lunch \n',choices = [ ( x, x ) for x in range ( 0, 105, 5 ) ] )
    
    ethnicity = forms.ChoiceField ( label = 'Ethnicity \n', choices = [ ( x, x ) for x in DEFAULT_CHOICE + RACE_CHOICES ]  )

    ethnicity_threshold = forms.ChoiceField ( label = 'Ethnicity Threshold \n',choices = [ ( x, x ) for x in range ( 0, 105, 5 ) ] )
    
    school_type = forms.ChoiceField ( label = 'Type of School \n',choices = [ ( x, x ) for x in DEFAULT_CHOICE + SCHOOL_TYPES ], required = False )

    location = forms.CharField( label = 'Please Enter Your Address\n', required = False )

    distance_threshold = forms.FloatField ( label = 'Maximum Distance From Address (Miles) \n', required = False  )

class ComparisonForm(forms.Form):
    
    school_1 = forms.ChoiceField ( label = 'School 1', choices = [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_2 = forms.ChoiceField ( label = 'School 2', choices = [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_3 = forms.ChoiceField ( label = 'School 3', choices = [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_4 = forms.ChoiceField ( label = 'School 4', choices = [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_5 = forms.ChoiceField ( label = 'School 5', choices = [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )

