# CS 122 Project: EdMoneyBall
# Creates the Plotly charts
# Vi Nguyen, Sirui Feng, Turab Hassan
# Modified, looked up from https://docs.djangoproject.com/en/1.9/intro/tutorial01/


from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^explore', views.explore, name = 'explore'),
    url(r'^comparisontool', views.comparisontool, name = 'comparisontool'),
    url(r'^recommendationtool', views.recommendationtool, name = 'recommendationtool'),
    url(r'^methodology', views.methodology, name = 'methodology'),
    url(r'^index', views.index, name = 'index')

]