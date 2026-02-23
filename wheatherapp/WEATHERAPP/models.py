from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Cities"
    
    def __str__(self):
        return f"{self.name}, {self.country}"


class WeatherData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_records')
    temperature = models.FloatField()
    feels_like = models.FloatField(blank=True, null=True)
    temp_min = models.FloatField(blank=True, null=True)
    temp_max = models.FloatField(blank=True, null=True)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    weather_main = models.CharField(max_length=100)  # e.g., "Clouds", "Rain", "Clear"
    weather_description = models.CharField(max_length=255)  # e.g., "overcast clouds"
    wind_speed = models.FloatField()
    wind_deg = models.FloatField(blank=True, null=True)
    wind_gust = models.FloatField(blank=True, null=True)
    cloudiness = models.IntegerField()
    visibility = models.IntegerField(blank=True, null=True)
    sunrise = models.IntegerField(blank=True, null=True)
    sunset = models.IntegerField(blank=True, null=True)
    uvi = models.FloatField(blank=True, null=True)  # UV Index
    aqi = models.IntegerField(blank=True, null=True)  # Air Quality Index (1-5 scale)
    rain_probability = models.IntegerField(blank=True, null=True)  # 0-100
    timestamp = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.city.name} - {self.timestamp}"


class SearchHistory(models.Model):
    """Model to track searched cities"""
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='search_records')
    searched_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-searched_at']
        verbose_name_plural = "Search Histories"
    
    def __str__(self):
        return f"{self.city.name} - {self.searched_at}"


class Favorite(models.Model):
    """Model for user favorite cities"""
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='favorites')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-added_at']
    
    def __str__(self):
        return f"Favorite: {self.city.name}"
