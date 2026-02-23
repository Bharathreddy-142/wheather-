from django.contrib import admin
from .models import City, WeatherData, SearchHistory, Favorite


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'created_at')
    search_fields = ('name', 'country')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'temperature', 'weather_main', 'timestamp')
    search_fields = ('city__name', 'weather_main')
    list_filter = ('weather_main', 'timestamp')
    ordering = ('-timestamp',)
    readonly_fields = ('timestamp',)


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ('city', 'searched_at')
    search_fields = ('city__name',)
    list_filter = ('searched_at',)
    ordering = ('-searched_at',)
    readonly_fields = ('searched_at',)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('city', 'added_at')
    search_fields = ('city__name',)
    list_filter = ('added_at',)
    ordering = ('-added_at',)
    readonly_fields = ('added_at',)
