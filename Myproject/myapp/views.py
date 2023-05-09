from django.contrib import messages
from django.shortcuts import render
import requests
from .models import City
from .forms import CityForm
from datetime import datetime


def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=22ab249f8c200b37a50ba18255d07bd9'
    form = CityForm()

    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            new_city = form.cleaned_data['name']
            existing_city = City.objects.filter(name=new_city).first()
            if not existing_city:
                City.objects.create(name=new_city)
        else:
            messages.error(request, 'Invalid city name')

    city = request.POST.get('name')  # Get the city entered by the user
    weather_data = []
    current_time = datetime.now()
    formatted_time = current_time.strftime("%A, %B %d %Y, %H:%M:%S %p")

    if city:
        city_weather = requests.get(url.format(city)).json()
        if city_weather.get('cod') == '404':  # Check if the API response indicates an invalid city
            messages.error(request, 'Invalid city name')
        else:
            weather = {
                'city': city,
                'temperature': 'Temperature: ' + str((city_weather['main']['temp']-32)*5//9) + ' °C',
                'description': city_weather['weather'][0]['description'],
                'icon': city_weather['weather'][0]['icon'],
                'wind': 'Wind: ' + str(city_weather['wind']['speed']) + 'km/h',
                'humidity': 'Humidity: ' + str(city_weather['main']['humidity']) + '%',
                'time': formatted_time
            }

            weather_data.append(weather)


    context = {'weather_data': weather_data, 'form': form}

    return render(request, 'index.html', context)
