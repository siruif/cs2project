from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^homepage', views.homepage, name='homepage'),
    url(r'^comparisontool', views.comparisontool, name='comparisontool'),
    url(r'^recommendationtool', views.recommendationtool, name='recommendationtool'),
    url(r'^heatmaps', views.heatmaps, name='heatmaps')

]