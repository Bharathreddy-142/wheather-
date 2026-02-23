import requests
from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView
from django.views import View
from django.utils.decorators import method_decorator

from .models import City, WeatherData, SearchHistory, Favorite
from .forms import CityForm, SearchWeatherForm

# OpenWeatherMap API key - get your free key from https://openweathermap.org/api
API_KEY = '05edc8fd06245d4b2c734037613e3877'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast'

# Additional OpenWeatherMap endpoints
AIRPOLLUTION_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'
UVI_URL = 'http://api.openweathermap.org/data/2.5/uvi'


def get_weather_data(city_name):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric'  # Use Celsius
        }
        response = requests.get(BASE_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


def get_forecast_data(city_name):
    """Fetch 5-day forecast data from OpenWeatherMap API"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
            'cnt': 40  # Get 5 days (8 forecasts per day for 3-hour intervals)
        }
        response = requests.get(FORECAST_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        # Process forecast data - get one forecast per day (at midday)
        daily_forecasts = {}
        for forecast in data['list']:
            from datetime import datetime
            dt = datetime.fromtimestamp(forecast['dt'])
            day_key = dt.strftime('%Y-%m-%d')
            
            # Use midday forecast (around 12:00)
            if day_key not in daily_forecasts or dt.hour == 12 or (dt.hour < 12 and daily_forecasts[day_key]['hour'] > 12):
                daily_forecasts[day_key] = {
                    'dt': forecast['dt'],
                    'date': dt,
                    'hour': dt.hour,
                    'temperature': forecast['main']['temp'],
                    'temp_min': forecast['main']['temp_min'],
                    'temp_max': forecast['main']['temp_max'],
                    'humidity': forecast['main']['humidity'],
                    'pressure': forecast['main']['pressure'],
                    'description': forecast['weather'][0]['description'].title(),
                    'main': forecast['weather'][0]['main'],
                    'wind_speed': forecast['wind']['speed'],
                    'cloudiness': forecast['clouds']['all'],
                    'rain': forecast.get('rain', {}).get('3h', 0),
                }
        
        # Sort by date and return first 10 days worth
        sorted_forecasts = sorted(daily_forecasts.items())[:10]
        return [forecast[1] for forecast in sorted_forecasts]
    except requests.exceptions.RequestException as e:
        return []


def get_hourly_forecast(city_name):
    """Fetch hourly forecast for next 24 hours"""
    try:
        params = {
            'q': city_name,
            'appid': API_KEY,
            'units': 'metric',
            'cnt': 8  # Get next 24 hours (8 forecasts)
        }
        response = requests.get(FORECAST_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        hourly_data = []
        for forecast in data['list'][:8]:  # First 8 = next 24 hours
            dt = datetime.fromtimestamp(forecast['dt'])
            hourly_data.append({
                'time': dt.strftime('%H:%M'),
                'hour': dt.hour,
                'temperature': forecast['main']['temp'],
                'feels_like': forecast['main'].get('feels_like'),
                'humidity': forecast['main']['humidity'],
                'description': forecast['weather'][0]['description'].title(),
                'main': forecast['weather'][0]['main'],
                'wind_speed': forecast['wind']['speed'],
                'rain_prob': forecast.get('pop', 0) * 100,  # Probability of precipitation
                'cloudiness': forecast['clouds']['all'],
            })
        return hourly_data
    except requests.exceptions.RequestException as e:
        return []


def get_aqi_data(lat, lon):
    """Fetch Air Quality Index data"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY
        }
        response = requests.get(AIRPOLLUTION_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data['list']:
            aqi = data['list'][0]['main']['aqi']  # 1-5 scale
            components = data['list'][0]['components']
            return {
                'aqi': aqi,
                'pm25': components.get('pm2_5'),
                'pm10': components.get('pm10'),
                'no2': components.get('no2'),
                'o3': components.get('o3'),
            }
    except requests.exceptions.RequestException as e:
        pass
    return None


def get_uvi_data(lat, lon):
    """Fetch UV Index data"""
    try:
        params = {
            'lat': lat,
            'lon': lon,
            'appid': API_KEY
        }
        response = requests.get(UVI_URL, params=params, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return None


class IndexView(View):
    """Home page showing all tracked cities and their weather"""
    
    def get(self, request):
        # Get recent searches instead of all cities
        recent_searches = SearchHistory.objects.all()[:10]
        weather_data = {}
        
        # Fetch current weather for recent searches
        for search_record in recent_searches:
            city = search_record.city
            data = get_weather_data(city.name)
            if data and 'main' in data:
                weather_data[city.id] = {
                    'temperature': data['main']['temp'],
                    'feels_like': data['main'].get('feels_like'),
                    'temp_min': data['main'].get('temp_min'),
                    'temp_max': data['main'].get('temp_max'),
                    'humidity': data['main']['humidity'],
                    'description': data['weather'][0]['description'].title(),
                    'main': data['weather'][0]['main'],
                    'wind_speed': data['wind']['speed'],
                    'wind_deg': data['wind'].get('deg'),
                    'wind_gust': data['wind'].get('gust'),
                    'pressure': data['main']['pressure'],
                    'cloudiness': data['clouds']['all'],
                    'visibility': data.get('visibility'),
                    'sunrise': data['sys'].get('sunrise'),
                    'sunset': data['sys'].get('sunset'),
                    'country': data['sys'].get('country'),
                    'coords': {
                        'lat': data['coord']['lat'],
                        'lon': data['coord']['lon']
                    }
                }
        
        search_form = SearchWeatherForm()
        
        context = {
            'recent_searches': recent_searches,
            'weather_data': weather_data,
            'search_form': search_form,
        }
        
        return render(request, 'WEATHERAPP/index.html', context)
    
    def post(self, request):
        """Handle city search and addition"""
        if 'search' in request.POST:
            search_form = SearchWeatherForm(request.POST)
            if search_form.is_valid():
                city_name = search_form.cleaned_data['city_name']
                data = get_weather_data(city_name)
                
                if data and 'main' in data:
                    # Get or create city
                    city, created = City.objects.get_or_create(
                        name=data['name'],
                        defaults={
                            'country': data['sys'].get('country', ''),
                            'latitude': data['coord']['lat'],
                            'longitude': data['coord']['lon'],
                        }
                    )
                    
                    # Create weather record with comprehensive data
                    WeatherData.objects.create(
                        city=city,
                        temperature=data['main']['temp'],
                        feels_like=data['main'].get('feels_like'),
                        humidity=data['main']['humidity'],
                        pressure=data['main']['pressure'],
                        weather_main=data['weather'][0]['main'],
                        weather_description=data['weather'][0]['description'],
                        wind_speed=data['wind']['speed'],
                        cloudiness=data['clouds']['all'],
                    )
                    
                    # Add to search history
                    SearchHistory.objects.create(city=city)
                    
                    messages.success(request, f"Weather data for {city.name} fetched successfully!")
                    # Redirect to the city detail page to show full report
                    return redirect('weather_city_detail', pk=city.id)
                else:
                    messages.error(request, f"City not found or API error. Check your API key!")
            
        elif 'add_city' in request.POST:
            city_form = CityForm(request.POST)
            if city_form.is_valid():
                city_form.save()
                messages.success(request, "City added successfully!")
        
        return redirect('weather_index')


class CityDetailView(DetailView):
    """Detailed weather view for a specific city"""
    model = City
    template_name = 'WEATHERAPP/city_detail.html'
    context_object_name = 'city'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        city = self.get_object()
        
        # Get latest weather data
        latest_weather = city.weather_records.first()
        context['latest_weather'] = latest_weather
        
        # Get weather history (last 10 records)
        context['weather_history'] = city.weather_records.all()[:10]
        
        # Check if city is favorite
        context['is_favorite'] = Favorite.objects.filter(city=city).exists()
        
        # Fetch current weather from API
        current_data = get_weather_data(city.name)
        if current_data and 'main' in current_data:
            context['current_api_data'] = {
                'temperature': current_data['main']['temp'],
                'feels_like': current_data['main'].get('feels_like'),
                'temp_min': current_data['main'].get('temp_min'),
                'temp_max': current_data['main'].get('temp_max'),
                'humidity': current_data['main']['humidity'],
                'description': current_data['weather'][0]['description'].title(),
                'main': current_data['weather'][0]['main'],
                'wind_speed': current_data['wind']['speed'],
                'wind_deg': current_data['wind'].get('deg'),
                'wind_gust': current_data['wind'].get('gust'),
                'pressure': current_data['main']['pressure'],
                'cloudiness': current_data['clouds']['all'],
                'visibility': current_data.get('visibility'),
                'sunrise': current_data['sys'].get('sunrise'),
                'sunset': current_data['sys'].get('sunset'),
                'country': current_data['sys'].get('country'),
            }
        
        # Fetch 10-day forecast
        forecast_data = get_forecast_data(city.name)
        context['forecast_data'] = forecast_data
        
        # Fetch hourly forecast (next 24 hours)
        hourly_data = get_hourly_forecast(city.name)
        context['hourly_forecast'] = hourly_data
        
        # Fetch AQI data
        if current_data:
            aqi_data = get_aqi_data(current_data['coord']['lat'], current_data['coord']['lon'])
            context['aqi_data'] = aqi_data
            
            # Fetch UV Index
            uvi_data = get_uvi_data(current_data['coord']['lat'], current_data['coord']['lon'])
            context['uvi_data'] = uvi_data
        
        # Calculate historical stats for trend analysis
        weather_records = city.weather_records.all()[:30]  # Last 30 records
        if weather_records.exists():
            temps = [r.temperature for r in weather_records]
            context['temp_trend'] = {
                'avg': sum(temps) / len(temps),
                'min': min(temps),
                'max': max(temps),
                'temperatures': list(reversed([t for t in temps])),
            }
        
        return context


class CityListView(ListView):
    """List all tracked cities"""
    model = City
    template_name = 'WEATHERAPP/city_list.html'
    context_object_name = 'cities'
    paginate_by = 10


class SearchHistoryView(ListView):
    """List all searched cities with their search timestamps"""
    model = SearchHistory
    template_name = 'WEATHERAPP/search_history.html'
    context_object_name = 'search_records'
    paginate_by = 20
    
    def get_queryset(self):
        """Get unique cities sorted by last search time"""
        # Group by city and get the most recent search for each
        return SearchHistory.objects.all().select_related('city')


@require_http_methods(["POST"])
def delete_city(request, pk):
    """Delete a city and its weather data"""
    city = get_object_or_404(City, pk=pk)
    city.delete()
    messages.success(request, f"City {city.name} deleted successfully!")
    return redirect('weather_index')


@require_http_methods(["GET"])
def refresh_weather(request, pk):
    """Refresh weather data for a city"""
    city = get_object_or_404(City, pk=pk)
    data = get_weather_data(city.name)
    
    if data and 'main' in data:
        # Update city info
        city.latitude = data['coord']['lat']
        city.longitude = data['coord']['lon']
        city.country = data['sys'].get('country', '')
        city.save()
        
        # Create new weather record
        WeatherData.objects.create(
            city=city,
            temperature=data['main']['temp'],
            feels_like=data['main'].get('feels_like'),
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            weather_main=data['weather'][0]['main'],
            weather_description=data['weather'][0]['description'],
            wind_speed=data['wind']['speed'],
            cloudiness=data['clouds']['all'],
        )
        
        messages.success(request, f"Weather data for {city.name} updated!")
    else:
        messages.error(request, "Failed to fetch weather data. Check your API key!")
    
    return redirect('weather_city_detail', pk=city.pk)


@require_http_methods(["POST"])
def toggle_favorite(request, city_id):
    """Toggle favorite status for a city"""
    try:
        city = City.objects.get(id=city_id)
        favorite, created = Favorite.objects.get_or_create(city=city)
        
        if not created:
            favorite.delete()
            return JsonResponse({'status': 'removed', 'is_favorite': False})
        
        return JsonResponse({'status': 'added', 'is_favorite': True})
    except City.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'City not found'}, status=404)


def get_hourly_data(request, city_id):
    """API endpoint to get hourly forecast for a city"""
    try:
        city = City.objects.get(id=city_id)
        hourly_data = get_hourly_forecast(city.name)
        return JsonResponse({'hourly_forecast': hourly_data})
    except City.DoesNotExist:
        return JsonResponse({'status': 'error'}, status=404)


def favorites_view(request):
    """View to show all favorite cities"""
    favorites = Favorite.objects.select_related('city').all()
    weather_data = {}
    
    for fav in favorites:
        data = get_weather_data(fav.city.name)
        if data and 'main' in data:
            weather_data[fav.city.id] = {
                'temperature': data['main']['temp'],
                'feels_like': data['main'].get('feels_like'),
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'].title(),
                'main': data['weather'][0]['main'],
                'wind_speed': data['wind']['speed'],
            }
    
    context = {
        'favorites': favorites,
        'weather_data': weather_data,
    }
    return render(request, 'WEATHERAPP/favorites.html', context)
