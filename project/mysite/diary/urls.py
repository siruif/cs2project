from django.conf.urls import include, url
from django.contrib import admin

from django.http import HttpResponse

urlpatterns = [
    url(r'^admin/', admin.site.urls),
]