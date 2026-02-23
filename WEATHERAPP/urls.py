from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='weather_index'),
    path('cities/', views.CityListView.as_view(), name='weather_city_list'),
    path('search-history/', views.SearchHistoryView.as_view(), name='search_history'),
    path('favorites/', views.favorites_view, name='favorites'),
    path('city/<int:pk>/', views.CityDetailView.as_view(), name='weather_city_detail'),
    path('city/<int:pk>/delete/', views.delete_city, name='weather_city_delete'),
    path('city/<int:pk>/refresh/', views.refresh_weather, name='weather_refresh'),
    path('city/<int:city_id>/favorite/toggle/', views.toggle_favorite, name='toggle_favorite'),
    path('city/<int:city_id>/hourly/', views.get_hourly_data, name='get_hourly_data'),
]
