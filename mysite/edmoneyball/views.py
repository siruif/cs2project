import csv
import urllib.parse
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import AddressForm
#import getcontext


def index(request):
    form = AddressForm()   
    context={'location':[], 'form':form}
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            address = urllib.parse.quote_plus(data['address_form'])
            maps_api_url = "?".join(["https://maps.googleapis.com/maps/api/geocode/json",urllib.parse.urlencode({"address":address, "sensor":False, 'key':'AIzaSyD3MgwYmLVdZ6FUuftS3d-Yf85HbniwypY'})])
            response = urllib.request.urlopen(maps_api_url)
            data = json.loads(response.read().decode('utf8'))
            if data['status'] == 'OK':
                lat = data['results'][0]['geometry']['location']['lat']
                lng = data['results'][0]['geometry']['location']['lng']
                context['location'].append([lat,lng])
        return render( request, 'address.html', context)
    else:
        with open('edmoneyball/cps.csv', newline='') as csvfile:
            locationreader = csv.reader(csvfile, delimiter=',')
            next(locationreader) #skipping first line
            for row in locationreader:
                context['location'].append( [float(row[4]),float(row[5])] )
        return render( request, 'helloworld.html', context)

