from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

app_name = 'Weatherapp'

urlpatterns = [
    path('',views.CityWeatherView,name='city_weather'),
    path('remove/<city_name>/',views.city_delete,name='city_remove')
]