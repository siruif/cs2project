# CS 122 Project: EdMoneyBall
# Creates the Plotly charts
# Vi Nguyen, Sirui Feng, Turab Hassan
# Substantially Modified, made reading the documentation at 
# https://docs.djangoproject.com/en/1.9/ref/forms/fields/

from django import forms
from . import school_info

DEFAULT_CHOICE  = [""]

SCHOOL_CHOICES = school_info.school_names()

RACE_CHOICES = ['Asian','Black', 'White', 'Hispanic', 'Multiracial']

SCHOOL_TYPES = ['Charter', 'Regular']

class AddressForm(forms.Form):
    '''
    Address form to capture the address of the user in the explore page
    The school name field captures the school clicked by the user
    '''
    
    address_form = forms.CharField \
    (label = 'Enter Address to Find Schools Available to You',\
    max_length = 500, required = False )

    school_name = forms.CharField\
    (widget = forms.HiddenInput(), required = False)

class RecommendationForm(forms.Form):
    '''
    RecommendationForm to capture the user info entered on the Recommendation
    Tool
    '''
    
    performance = forms.ChoiceField\
    ( label = 'Minimum Threshold of Performance Percentile',\
    choices = [(x, x) for x in range ( 0, 105, 5 ) ], required = False )
    
    free_red_lunch = forms.ChoiceField\
    ( label = 'Minimum Percentage Free and Reduced Lunch',\
    choices = [ ( x, x ) for x in range ( 0, 105, 5 ) ], required = False )
    
    ethnicity = forms.ChoiceField\
    ( label = 'Ethnicity', choices = \
    [ ( x, x ) for x in DEFAULT_CHOICE + RACE_CHOICES ], required = False )

    ethnicity_threshold = forms.ChoiceField \
    ( label = 'Minimum Threshold for Specified Ethnicity',\
    choices = [ ( x, x ) for x in range ( 0, 105, 5 ) ], required = False )
    
    school_type = forms.ChoiceField \
    ( label = 'Type of School',choices = \
    [ ( x, x ) for x in DEFAULT_CHOICE + SCHOOL_TYPES ], required = False )

    location = forms.CharField\
    ( label = 'Enter Address to Find Schools Within a Certain Distance',\
    required = False )

    distance_threshold = forms.FloatField\
    ( label = 'Maximum Distance From Address (Miles)', required = False  )

class ComparisonForm(forms.Form):
    '''
    ComparisonForm to capture the Comparison Information that the user enters
    '''
    school_1 = forms.ChoiceField \
    ( label = 'School 1', choices = \
    [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_2 = forms.ChoiceField \
    ( label = 'School 2', choices = \
    [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_3 = forms.ChoiceField \
    ( label = 'School 3', choices = \
    [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_4 = forms.ChoiceField \
    ( label = 'School 4', choices =\
    [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )
    
    school_5 = forms.ChoiceField \
    ( label = 'School 5', choices = \
    [ (x,x) for x in DEFAULT_CHOICE + SCHOOL_CHOICES ], required = False )

