from django.shortcuts import render

# Create your views here.

def abc(request):
    #return HttpResponse('Test')


    return reader(request, 'diary/start.html')