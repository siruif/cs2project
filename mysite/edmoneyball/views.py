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
        
        if form.is_valid():
            data=form.cleaned_data
            #print ('coming here')
            #print (data)
            #address = urllib.parse.quote_plus(data['address_form'])
            school_name = data['address_form']
            context = update_charts.create_charts (school_name)
            #print(context)

            print(context)
            #latlon = geocode.get_latlon(address)
            #school_list = school_info.find_neighbor_schools(latlon,1)
            #latlon.insert ( 0,'Home' ) 
            #school_list.insert( 0,latlon )
            #context['location'] = school_list
            #print(context['location']) 
        return render( request, 'plot_individual_school.html', context)
    else:
        context['location'] = getcontext.extract_location()
        print(context)
        return render( request, 'helloworld.html', context)

def recommendationtool(request):
    if request.method == 'POST':
        form = ReccomendationForm(request.POST)
        print('post request')
        #print(form)
        if form.is_valid():
            data = form.cleaned_data
            if data['location'] != '':
                address = urllib.parse.quote_plus ( data['location'] )
                print('this should not show')
                latlon = geocode.get_latlon(address)
                data['location'] = latlon
            data ['ethnicity'] = data['ethnicity'].lower()
            context = update_charts.compare_recommend(True, pref_crit_from_ui = data)

            print (data)
            print (context)

        return render( request, 'plot_school_comparisons.html', context)
    else:
        form = ReccomendationForm() 
        context = {'form':form}
        return render( request, 'recommendation.html', context)

def comparisontool(request):
    if request.method == 'POST':
        form = ComparisonForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            school_list = []
            for key in data.keys():
                if data[key] != '':
                    school_list.append(data[key]) 
            context = update_charts.compare_recommend(False, list_of_schools = school_list )            
        return render( request, 'plot_school_comparisons.html', context)
    else:
        form = ComparisonForm ( )
        context = {'form':form}
        return render( request, 'comparison.html', context)    

def heatmaps(request):
    return render( request, 'html.heatmap')