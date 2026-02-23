# Weather App - Django Weather Application

A Django web application that fetches and displays weather data using the OpenWeatherMap API.

## Features

✨ **Core Features:**
- Search for cities and retrieve weather data from OpenWeatherMap API
- Track multiple cities with persistent weather history
- View detailed weather information for each city
- Beautiful responsive UI with Bootstrap 5
- Real-time weather updates
- Weather history tracking
- Admin interface for data management

## Project Structure

```
WEATHERAPP/
├── models.py              # Database models (City, WeatherData)
├── views.py               # View functions and classes
├── forms.py               # Django Forms for user input
├── urls.py                # URL routing configuration
├── admin.py               # Django admin configuration
├── apps.py                # App configuration
├── templatetags/
│   └── weather_filters.py # Custom template filters
└── templates/WEATHERAPP/
    ├── base.html          # Base template with navigation
    ├── index.html         # Home page with city search
    ├── city_detail.html   # Detailed weather view
    └── city_list.html     # List of all tracked cities
```

## Installation & Setup

### 1. Prerequisites
- Python 3.8+
- Django 3.2+
- pip

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Get OpenWeatherMap API Key

1. Visit [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Get your free API key from the dashboard

### 4. Configure the App

#### Add to Django Settings

In your Django project's `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'WEATHERAPP',
]
```

#### Update API Key

In `WEATHERAPP/views.py`, replace `YOUR_API_KEY_HERE` with your actual OpenWeatherMap API key:

```python
API_KEY = 'your_actual_api_key_here'
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (for admin access)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit `http://localhost:8000/` in your browser.

## URL Configuration

Add this to your main project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    # ... other patterns
    path('weather/', include('WEATHERAPP.urls')),
]
```

## Usage

### Home Page `/weather/`
- Search for cities by name
- View current weather for all tracked cities
- Quick access to city details, refresh, and delete options

### City Details `/weather/city/<id>/`
- View detailed current weather information
- See weather history (last 10 records)
- Refresh weather data
- View city coordinates

### All Cities `/weather/cities/`
- See all tracked cities in a table format
- Pagination support
- Quick actions for each city

### Admin `/admin/`
- Manage cities and weather records
- View historical data
- Filter and search capabilities

## API Endpoints

The app uses the following OpenWeatherMap API endpoint:

```
https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric
```

Parameters:
- `q`: City name (required)
- `appid`: Your API key (required)
- `units`: metric (Celsius) or imperial (Fahrenheit)

## Database Schema

### City Model
- name: CharField (Unique)
- country: CharField
- latitude: FloatField
- longitude: FloatField
- created_at: DateTimeField

### WeatherData Model
- city: ForeignKey to City
- temperature: FloatField
- feels_like: FloatField (optional)
- humidity: IntegerField
- pressure: IntegerField
- weather_main: CharField
- weather_description: CharField
- wind_speed: FloatField
- cloudiness: IntegerField
- timestamp: DateTimeField

## Features Explained

### 1. City Search
Users can search for any city, and the app will fetch weather data from the API and store it in the database.

### 2. Weather Display
Current weather is displayed with:
- Temperature in Celsius
- "Feels like" temperature
- Weather condition with emoji icons
- Humidity percentage
- Wind speed
- Pressure

### 3. Weather History
The app tracks all weather records, allowing users to see how weather has changed over time for each city.

### 4. Admin Interface
Full Django admin support for:
- Managing cities
- Viewing weather records
- Filtering by weather condition
- Searching by city name

## Common Issues & Troubleshooting

### "City not found" Error
- Make sure you've entered the correct city name
- Some cities may require country codes (e.g., "London, UK")

### "Failed to fetch weather data"
- Verify your API key is correct
- Check if your API key is active on OpenWeatherMap
- Ensure you have an internet connection

### Template not found
- Make sure `WEATHERAPP` is in `INSTALLED_APPS`
- Verify template directory structure is correct
- Check Django `TEMPLATES` setting includes app templates

### No migrations
- Run `python manage.py makemigrations WEATHERAPP`
- Run `python manage.py migrate`

## Customization Ideas

1. **Temperature Units**: Modify the `units` parameter in `get_weather_data()` to switch between Celsius/Fahrenheit
2. **More Details**: Add more fields like UV index, visibility, sunrise/sunset times
3. **Weather Alerts**: Implement email notifications for temperature changes
4. **Charts**: Add weather trend visualization using Chart.js or similar
5. **API Alternatives**: Use other weather APIs like WeatherAPI or Weather.gov
6. **Mobile App**: Build a mobile app using Django REST Framework

## Technologies Used

- **Backend**: Django 3.2+
- **Frontend**: Bootstrap 5, HTML5, CSS3
- **Database**: SQLite (default), PostgreSQL or MySQL compatible
- **API**: OpenWeatherMap API
- **HTTP**: Requests library

## Security Notes

- Never commit your API key to version control
- Use environment variables for sensitive data:
  ```python
  import os
  API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
  ```

## Performance Tips

1. Cache API responses to avoid excessive API calls
2. Implement rate limiting for search functionality
3. Use async tasks (Celery) for background weather updates
4. Add pagination to weather history

## Future Enhancements

- [ ] Real-time weather updates using WebSockets
- [ ] Weather forecast (5-day, 7-day predictions)
- [ ] Weather alerts and notifications
- [ ] User accounts with saved favorite cities
- [ ] Weather comparison between multiple cities
- [ ] Advanced filtering and search
- [ ] Data export (CSV, JSON)
- [ ] Mobile app
- [ ] API endpoint for third-party integrations
- [ ] Machine learning for weather predictions

## License

This project is open-source and available under the MIT License.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review the code comments
3. Check Django and OpenWeatherMap documentation

## Credits

- **Django**: https://www.djangoproject.com/
- **OpenWeatherMap**: https://openweathermap.org/
- **Bootstrap**: https://getbootstrap.com/

---

**Happy Weather Tracking!** 🌤️⛅🌦️
