# CS 122 Project: EdMoneyBall
# Creates the Plotly charts
# Vi Nguyen, Sirui Feng, Turab Hassan
# All Original Code

from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AddressForm, RecommendationForm, ComparisonForm
from . import getcontext, geocode, school_info, update_charts
import urllib.parse

def explore(request):
    '''
    This function builds the explore page from a Http request. Within the 
    explore page we have 3 possibilites which can occur. The user has come 
    to the page for the first time than we render the page with all the school
    data, the user has clicked on an individual school and we render the page 
    with individual school data. The user has entered the his address and 
    we want to show the show the open schools associated with the address
    
    Input: Http request
    Output: Http Request with the html page and the context we want the html
    page to render
    '''
    form = AddressForm()  
    context={'info':[], 'form':form}


    if request.method == 'POST':
        form = AddressForm(request.POST)
        
        if form.is_valid():
            
            data=form.cleaned_data
            address = urllib.parse.quote_plus(data['address_form'])
            school_name = data['school_name']

            # When user clicks on a school and we want to display individual
            #School Information
            if school_name != '':
                context = update_charts.create_charts (school_name)
                return render( request, 'edmoneyball/individual.html', \
                        context)

            # When user enters his address and we want to show schools in his zone
            else:
                ulat,ulon = geocode.get_latlon(address)                
                context = getcontext.build_context_from_address(ulat, ulon)
                return render( request, 'edmoneyball/address.html', context)
    
    #Populating the Initial Page by displaying all the shcools
    else:
        context['info'] = school_info.build_context_explore()
        return render( request, 'edmoneyball/explore.html', context)

def recommendationtool(request):
    '''
    Based on the Http Request, return the recommendations page. There are two
    possibilites, we can either find atleast once school which meets the 
    recommendation or we cannot find any shcool that meets the recommendation.
    Based on this we render either the recommendation met page or the
    recommendation not met page
    Input: Http request
    Output: Http Request with the html page and the context we want the html
    page to render
    '''
    if request.method == 'POST':
        form = RecommendationForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            indicator, context = getcontext.\
            build_context_from_recommendation(data)

            #Criteria met show this page
            if indicator:
                return render( request, \
                    'edmoneyball/plot_school_recommendations.html', context)
            
            #Criteria not met Show this page
            else:
                return render( request, \
                    'edmoneyball/plot_school_recommendations_notmet.html', context)         
    
    #User coming in for the first time, load the base page
    else:
        form = RecommendationForm() 
        context = {'form':form}
        return render( request, 'edmoneyball/recommendation.html', context)

def comparisontool(request):
    '''
    This function builds the school comparison page from a HTTP request
    Once the user has entered the data, we check the data validity and 
    pass the data to the charting function which returns a list of URLs which
    this function than renders.
    Input: Http Request
    Output: Http Request with and html page and a context to render the html
    page 
    '''

    if request.method == 'POST':
        form = ComparisonForm(request.POST)
        
        if form.is_valid():
            data = form.cleaned_data
            context = getcontext.build_context_from_recommendation(data)
        return render( request, 'edmoneyball/plot_school_comparisons.html', context)
    
    else:
        form = ComparisonForm ( )
        context = {'form':form}
        return render( request, 'edmoneyball/comparison.html', context)    

def index(request):
    '''
    Based on a Http Request, return the index page
    '''
    return render ( request, 'edmoneyball/index.html')

def methodology(request):
    '''
    Based on a Http Request, return the methodology page
    '''
    return render ( request, 'edmoneyball/methodology.html')