import sys
import csv
from django.shortcuts import render

from django.http import HttpResponse

#import getcontext


def index(request):
   
       
    context={'location':[]}
    with open('edmoneyball/cps.csv', newline='') as csvfile:
            locationreader = csv.reader(csvfile, delimiter=',')
            next(locationreader) #skipping first line
            for row in locationreader:
                context['location'].append( [float(row[4]),float(row[5])] )
                

    
    #context={'location':[[41.75734007, -87.63277352]]}
    return render( request, 'helloworld.html', context)
# Create your views here.
