from django.contrib import admin
from .models import Employee,Fuelconsumption,WeatherData

# Register your models here.
admin.site.register(Employee)
admin.site.register(Fuelconsumption)
admin.site.register(WeatherData)
