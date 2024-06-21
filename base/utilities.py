import requests
from geopy.geocoders import Nominatim


def get_coordinates(city_name):
    try:
        # Initialize a geolocator using Nominatim (OpenStreetMap)
        geolocator = Nominatim(user_agent="city_geocoder")

        # Use geocode to get location information for the city
        location = geolocator.geocode(city_name)

        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None

    except Exception as e:
        return None






def get_current_location():
    try:
        # Make a GET request to the ip-api.com API
        response = requests.get('http://ip-api.com/json')

        if response.status_code == 200:
            data = response.json()
            latitude = data['lat']
            longitude = data['lon']
            city_name=data['city']
            return float(latitude), float(longitude), str(city_name)
        else:
            return None

    except Exception as e:
        return None

