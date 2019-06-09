from django.urls import path
from . import views

urlpatterns = [
    path('home', views.index, name='home'),
    path('analytics', views.analytics, name='analytics'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('data', views.data, name='data'),
    path('', views.index, name='index'),
]

