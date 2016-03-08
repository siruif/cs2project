from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^explore', views.explore, name='explore'),
    url(r'^comparisontool', views.comparisontool, name='comparisontool'),
    url(r'^recommendationtool', views.recommendationtool, name='recommendationtool'),
    url(r'^heatmaps', views.heatmaps, name='heatmaps'),
    url(r'^index', views.index, name = 'index')

]