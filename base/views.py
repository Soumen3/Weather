from django.shortcuts import render,redirect
from datetime import datetime
import requests
import json
from geopy.geocoders import Nominatim
import os
from decouple import config
from .utilities import get_coordinates, get_current_location

# Create your views here.
def home(request):
    context={}

    #--------------------Get the coordinates of the enterd city-------------#
    if request.method =='POST':
        city_name = request.POST['city']
        context['city']=city_name

        #----------get the coordinates--------------#
        coordinates = get_coordinates(city_name)
        if coordinates:
            latitude, longitude = coordinates
            context['lat']=latitude
            context['lon']=longitude
            

    #------------------------get the current location's coordinates-----------------------#
    else:
        current_location = get_current_location()
        if current_location:
            latitude, longitude, city_name= current_location
        # else:
            # print("Location information not available.")
        context['lat']=latitude
        context['lon']=longitude
        context['city']=city_name  


    #-------------------get the weather--------------------------#  


    # Retrieve the API key from an environment variable
    api_key = config("OPENWEATHERMAP_API_KEY")

    if api_key is None:
        raise Exception("API key not found in environment variables.")  
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}"      # api url
    response = requests.get(url)
    data = response.json()      # get the data about weather
    # print(data)
    kelvinTemp = data['main']['temp']
    celsiusTemp = kelvinTemp-273.15
    context['celsi']=round(celsiusTemp)

    feelsLike=data['main']['feels_like']-273.15
    context['feelsLike']=round(feelsLike)

    maxTemp=data['main']['temp_max']-273.15
    context['maxTemp']=round(maxTemp)

    minTemp=data['main']['temp_min']-273.15
    context['minTemp']=round(minTemp)

    humidity=data["main"]["humidity"]
    context['humidity']=humidity

    windSpeed=data["wind"]["speed"]
    context['windSpeed']=windSpeed

    direction=data['wind']['deg']
    context['direction']=direction

    pressure=data["main"]["pressure"]
    context['pressure']=pressure

    visibility=data['visibility']
    context['visibility']=visibility/1000

    sunriseTime=datetime.fromtimestamp((int)(data["sys"]["sunrise"])).strftime('%H:%M')
    context['sunrise']=sunriseTime

    sunsetTime=datetime.fromtimestamp((int)(data["sys"]["sunset"])).strftime('%H:%M')
    context['sunset']=sunsetTime

    cloudiness = data["clouds"]["all"]
    context['cloud']=cloudiness

    forecast = get_weather_forecast(latitude, longitude, api_key)
    context['forecast'] = forecast
    print(forecast)

    return render(request,'home.html', context)




def get_weather_forecast(latitude, longitude, api_key):
    # Construct the URL for the API request
    url = f"http://api.openweathermap.org/data/2.5/forecast/daily?lat={latitude}&lon={longitude}&cnt=10&appid={api_key}"

    # Make the API request
    response = requests.get(url)

    # Parse the JSON response
    weather_data = json.loads(response.text)
    print(weather_data)
    # Get the weather forecast for the next 10 days
    # forecast = weather_data['list']

    return None

