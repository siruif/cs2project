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
        return render( request, 'edmoneyball/plot_individual_school.html', context)
    else:
        context['location'] = getcontext.extract_location()
        print(context)
        return render( request, 'edmoneyball/helloworld.html', context)

def recommendationtool(request):
    if request.method == 'POST':
        form = ReccomendationForm(request.POST)
        print('post request')
        #print(form)
        if form.is_valid():
            data = form.cleaned_data
            if data['location'] != '':
                address = urllib.parse.quote_plus ( data['location'] )
                latlon = geocode.get_latlon(address)
                data['location'] = latlon
            data ['ethnicity'] = data['ethnicity'].lower()
            context = update_charts.compare_recommend(True, pref_crit_from_ui = data)
            school_list = context['school']
            i = 0
            for each_scool in school_list:
                if each_scool != 'District Average*':
                    key = "school" + str(i)
                    context[key] = each_scool
                    i += 1

            print (data)
            print (context)

        return render( request, 'edmoneyball/plot_school_recommendations.html', context)
    else:
        form = ReccomendationForm() 
        context = {'form':form}
        return render( request, 'edmoneyball/recommendation.html', context)

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
        return render( request, 'edmoneyball/plot_school_comparisons.html', context)
    else:
        form = ComparisonForm ( )
        context = {'form':form}
        return render( request, 'edmoneyball/comparison.html', context)    

def heatmaps(request):
    return render( request, 'edmoneyball/heatmap.html')

def index(request):
    return render ( request, 'edmoneyball/index.html')