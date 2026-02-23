from django.core.management.base import BaseCommand
from WEATHERAPP.models import City, WeatherData
from WEATHERAPP.views import get_weather_data


class Command(BaseCommand):
    help = 'Update weather data for all tracked cities'

    def add_arguments(self, parser):
        parser.add_argument(
            '--city',
            type=str,
            help='Update weather for specific city (by name)',
        )

    def handle(self, *args, **options):
        if options['city']:
            # Update specific city
            try:
                city = City.objects.get(name__iexact=options['city'])
                self.update_city_weather(city)
            except City.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f"City '{options['city']}' not found")
                )
        else:
            # Update all cities
            cities = City.objects.all()
            if not cities.exists():
                self.stdout.write(
                    self.style.WARNING('No cities in database. Add cities first!')
                )
                return

            for city in cities:
                self.update_city_weather(city)

            self.stdout.write(
                self.style.SUCCESS(f'Updated {cities.count()} cities')
            )

    def update_city_weather(self, city):
        """Update weather data for a single city"""
        data = get_weather_data(city.name)

        if data and 'main' in data:
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
            self.stdout.write(
                self.style.SUCCESS(f"✓ Updated {city.name}")
            )
        else:
            self.stdout.write(
                self.style.ERROR(f"✗ Failed to update {city.name}")
            )
