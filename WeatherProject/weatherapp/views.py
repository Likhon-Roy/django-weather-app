from django.shortcuts import get_object_or_404, redirect, render, redirect
import requests
from .models import City
from .form import CityForm

# Create your views here.

def CityWeatherView(request):
    errmsg=""
    msgclass=""
    msg=""

    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=a88e26ca3a41428e630a426e5953a366"

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            count = City.objects.filter(name = new_city).count()
            if count==0:
                r = requests.get(url.format(new_city)).json()
                if r['cod']==200:
                    form.save()
                else:
                    errmsg='The city is not in the world'
            else:
                errmsg="Already city is added to the database"
        if errmsg:
            msg=errmsg
            msgclass='is-danger'
        else:
            msg='added'
            msgclass='is-success'
    else:
        form = CityForm()

        

    city = City.objects.all()

    weather = []

    for i in city:

        r= requests.get(url.format(i)).json()

        fahrenheit = r['main']['temp']
        Celsius = (fahrenheit - 32) * 5 / 9

        city_weather = {
            'city':i,
            'temperature':'%.2f'% Celsius,
            'desc': r['weather'][0]['description'],
            'icon':r['weather'][0]['icon']
        }
        weather.append(city_weather)

    #print(r)

    context = {
        'weather':weather,
        'form':form,
        'msg':msg,
        'msgclass':msgclass
    }
    return render(request, 'weather.html',context)



def city_delete(request,city_name):
    city = get_object_or_404(City,name=city_name)
    city.delete()
    return redirect('Weatherapp:city_weather')