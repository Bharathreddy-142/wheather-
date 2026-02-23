import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import City, WeatherData
from datetime import datetime


class CityModelTest(TestCase):
    """Test Case for City Model"""

    def setUp(self):
        self.city = City.objects.create(
            name="London",
            country="UK",
            latitude=51.5074,
            longitude=-0.1278
        )

    def test_city_creation(self):
        """Test that a city can be created"""
        self.assertEqual(self.city.name, "London")
        self.assertEqual(self.city.country, "UK")
        self.assertIsNotNone(self.city.created_at)

    def test_city_string_representation(self):
        """Test city __str__ method"""
        self.assertEqual(str(self.city), "London, UK")

    def test_city_uniqueness(self):
        """Test that city names are unique"""
        with self.assertRaises(Exception):
            City.objects.create(
                name="London",
                country="UK"
            )


class WeatherDataModelTest(TestCase):
    """Test Case for WeatherData Model"""

    def setUp(self):
        self.city = City.objects.create(
            name="Paris",
            country="France",
            latitude=48.8566,
            longitude=2.3522
        )
        self.weather = WeatherData.objects.create(
            city=self.city,
            temperature=15.5,
            feels_like=14.2,
            humidity=65,
            pressure=1013,
            weather_main="Clouds",
            weather_description="overcast clouds",
            wind_speed=3.5,
            cloudiness=90
        )

    def test_weather_data_creation(self):
        """Test that weather data can be created"""
        self.assertEqual(self.weather.city, self.city)
        self.assertEqual(self.weather.temperature, 15.5)
        self.assertEqual(self.weather.weather_main, "Clouds")

    def test_weather_data_string_representation(self):
        """Test weather data __str__ method"""
        expected = f"Paris - {self.weather.timestamp}"
        self.assertIn("Paris", str(self.weather))

    def test_weather_data_ordering(self):
        """Test that weather data is ordered by timestamp descending"""
        # Create another weather record
        WeatherData.objects.create(
            city=self.city,
            temperature=16.0,
            feels_like=15.0,
            humidity=70,
            pressure=1014,
            weather_main="Rain",
            weather_description="light rain",
            wind_speed=4.0,
            cloudiness=100
        )

        # Get all weather records for the city
        records = self.city.weather_records.all()
        self.assertEqual(records.count(), 2)
        # Latest should be first
        self.assertEqual(records.first().temperature, 16.0)


class ViewsTest(TestCase):
    """Test Case for Views"""

    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(
            name="Tokyo",
            country="Japan",
            latitude=35.6762,
            longitude=139.6503
        )

    def test_index_page_loads(self):
        """Test that index page loads successfully"""
        response = self.client.get(reverse('weather:weather_index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'WEATHERAPP/index.html')

    def test_city_list_page_loads(self):
        """Test that city list page loads successfully"""
        response = self.client.get(reverse('weather:weather_city_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'WEATHERAPP/city_list.html')

    def test_city_detail_page_loads(self):
        """Test that city detail page loads successfully"""
        response = self.client.get(
            reverse('weather:weather_city_detail', args=[self.city.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'WEATHERAPP/city_detail.html')
        self.assertEqual(response.context['city'], self.city)

    def test_city_detail_404(self):
        """Test that city detail returns 404 for nonexistent city"""
        response = self.client.get(
            reverse('weather:weather_city_detail', args=[999])
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_city(self):
        """Test that city can be deleted"""
        initial_count = City.objects.count()
        response = self.client.post(
            reverse('weather:weather_city_delete', args=[self.city.id]),
            follow=True
        )
        self.assertEqual(City.objects.count(), initial_count - 1)
        self.assertEqual(response.status_code, 200)


class FormsTest(TestCase):
    """Test Case for Forms"""

    def test_city_form_valid(self):
        """Test that CityForm works with valid data"""
        from .forms import CityForm
        form = CityForm(data={'name': 'Berlin'})
        self.assertTrue(form.is_valid())

    def test_city_form_invalid(self):
        """Test that CityForm fails with invalid data"""
        from .forms import CityForm
        form = CityForm(data={'name': ''})
        self.assertFalse(form.is_valid())

    def test_search_weather_form_valid(self):
        """Test that SearchWeatherForm works with valid data"""
        from .forms import SearchWeatherForm
        form = SearchWeatherForm(data={'city_name': 'New York'})
        self.assertTrue(form.is_valid())

    def test_search_weather_form_invalid(self):
        """Test that SearchWeatherForm fails with invalid data"""
        from .forms import SearchWeatherForm
        form = SearchWeatherForm(data={'city_name': ''})
        self.assertFalse(form.is_valid())


class TemplateTest(TestCase):
    """Test Case for Templates"""

    def setUp(self):
        self.client = Client()
        self.city = City.objects.create(
            name="Sydney",
            country="Australia"
        )

    def test_index_template_context(self):
        """Test that index template receives proper context"""
        response = self.client.get(reverse('weather:weather_index'))
        self.assertIn('cities', response.context)
        self.assertIn('search_form', response.context)
        self.assertIn('city_form', response.context)

    def test_city_detail_template_context(self):
        """Test that city detail template receives proper context"""
        response = self.client.get(
            reverse('weather:weather_city_detail', args=[self.city.id])
        )
        self.assertIn('city', response.context)
        self.assertIn('latest_weather', response.context)
        self.assertIn('weather_history', response.context)


# Run tests with: python manage.py test WEATHERAPP
# Run specific test: python manage.py test WEATHERAPP.tests.CityModelTest
# Run with coverage: coverage run --source='.' manage.py test WEATHERAPP
#                    coverage report
