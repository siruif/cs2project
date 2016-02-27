import urllib.parse
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AddressForm
from . import getcontext, geocode, school_info



def index(request):
    form = AddressForm()  

    context={'location':[], 'form':form}
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            address = urllib.parse.quote_plus(data['address_form'])
            latlon = geocode.get_latlon(address)
            school_list = school_info.find_neighbor_schools(latlon,1)
            latlon.insert ( 0,'Home' ) 
            school_list.insert( 0,latlon )
            context['location'] = school_list
            print(context['location']) 
        return render( request, 'address.html', context)
    else:
        context['location'] = getcontext.extract_location()
        return render( request, 'helloworld.html', context)

