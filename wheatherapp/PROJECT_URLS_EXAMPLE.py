# Example main project URLs configuration

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Weather App URLs - Add this line
    path('weather/', include('WEATHERAPP.urls')),
    
    # You can also use a different path:
    # path('', include('WEATHERAPP.urls')),  # For root domain
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
