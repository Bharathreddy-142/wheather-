# Weather App - Quick Start Guide

## 5-Minute Setup

### Step 1: Install Requirements
```bash
pip install -r requirements.txt
```

### Step 2: Get API Key
1. Go to https://openweathermap.org/api
2. Sign up for FREE
3. Copy your API key

### Step 3: Update views.py
Edit `WEATHERAPP/views.py` and replace:
```python
API_KEY = 'YOUR_API_KEY_HERE'
```
with your actual API key.

### Step 4: Add to Django Settings
In your Django project's `settings.py`, add:
```python
INSTALLED_APPS = [
    # ... other apps
    'WEATHERAPP',
]
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Add URLs
In your main `urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    # ... other patterns
    path('weather/', include('WEATHERAPP.urls')),
]
```

### Step 7: Run Server
```bash
python manage.py runserver
```

Visit: http://localhost:8000/weather/

---

## Features You Can Now Use

✅ Search for cities
✅ View weather data
✅ Track weather history
✅ See city details
✅ Refresh data
✅ Admin panel for management

---

## Next Steps

- [ ] Customize temperature units (Celsius/Fahrenheit)
- [ ] Add more weather details
- [ ] Set up automatic weather updates
- [ ] Create user accounts
- [ ] Add notifications

---

## Troubleshooting

**Issue**: "City not found"
- Solution: Check spelling and try full name (e.g., "London, UK")

**Issue**: "API error"
- Solution: Verify API key is correct and active

**Issue**: Templates not showing
- Solution: Make sure `APP_DIRS: True` in TEMPLATES setting

For more help, see README.md
