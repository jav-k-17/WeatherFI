import requests
from django.shortcuts import redirect, render
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=520f061ea01422af15ef6a7a6c7c2837'
   
    error_message = ""
    message = ""
    class_message = ""

    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()

            if city_count == 0:
                city_weather = requests.get(url.format(new_city)).json()

                if city_weather['cod'] == 200:
                    form.save()
                else:
                    error_message = "City Not Found"
            else:
                error_message = "City already added"

        if error_message:
            message = error_message
            class_message = "Could not add City"
        else:
            message = 'City added'
            class_message = "City added"

    form = CityForm()

    cities = City.objects.all()

    weather_data = []

    for city in cities:

        city_weather = requests.get(url.format(city)).json()

        weather = {
            'city' : city.name,
            'temperature' : city_weather['main']['temp'],
            'description' : city_weather['weather'][0]['description'],
            'icon' : city_weather['weather'][0]['icon'],
        }

        weather_data.append(weather)

    context = {'weather_data' : weather_data, 
                'form' : form, 
                'message': message, 
                'class_message' : class_message,
                }
    return render(request, 'weather/index.html', context)

def delete(request,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('home')