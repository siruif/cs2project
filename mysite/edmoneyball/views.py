import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AddressForm, ReccomendationForm, ComparisonForm
from . import getcontext, geocode, school_info, update_charts

def homepage(request):
    form = AddressForm()  

    context={'location':[], 'form':form}
    if request.method == 'POST':
        form = AddressForm(request.POST)
        print (form)
        if form.is_valid():
            data=form.cleaned_data
            print ('coming here')
            print (data)
            #address = urllib.parse.quote_plus(data['address_form'])
            school_name = data['address_form']
            url_list = update_charts.create_charts (school_name)
            print(url_list)
            #latlon = geocode.get_latlon(address)
            #school_list = school_info.find_neighbor_schools(latlon,1)
            #latlon.insert ( 0,'Home' ) 
            #school_list.insert( 0,latlon )
            #context['location'] = school_list
            #print(context['location']) 
        return render( request, 'address.html', context)
    else:
        context['location'] = getcontext.extract_location()
        return render( request, 'helloworld.html', context)

def recommendationtool(request):
    if request.method == 'POST':
        form = ReccomendationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print (data)
        form = ReccomendationForm()
        context = {'form':form}
        return render( request, 'recommendation.html', context)
    else:
        form = ReccomendationForm()
        context = {'form':form}
        return render( request, 'recommendation.html', context)

def comparisontool(request):
    if request.method == 'POST':
        form = ComparisonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            print (data)
        form = ComparisonForm()
        context = {'form':form}
        return render( request, 'comparison.html', context)
    else:
        form = ComparisonForm()
        context = {'form':form}
        return render( request, 'comparison.html', context)    

def heatmaps(request):
    return render( request, 'html.heatmap')