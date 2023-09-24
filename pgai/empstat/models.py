from django.db import models

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
class Fuelconsumption(models.Model):
    modelyear = models.IntegerField()
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    vehicleclass = models.CharField(max_length=25)
    enginesize = models.DecimalField(max_digits=10,decimal_places=1)
    cylinders = models.IntegerField()
    transmission = models.CharField(max_length=5)
    fueltype = models.CharField(max_length=1)
    fuelconsumption_city = models.DecimalField(max_digits=90,decimal_places=2)
    fuelconsumption_hwy = models.DecimalField(max_digits=90,decimal_places=2)
    fuelconsumption_comb = models.DecimalField(max_digits=90,decimal_places=2)
    fuelconsumption_comb_mpg = models.IntegerField()
    co2emissions = models.IntegerField()

    def __str__(self):
        return self.model
    

class WeatherData(models.Model):
    Precipitation = models.DecimalField(max_digits=5, decimal_places=2)
    Date_Full = models.DateField()
    Date_Month = models.IntegerField()
    Date_Week_of = models.IntegerField()
    Date_Year = models.IntegerField()
    Station_City = models.CharField(max_length=255)
    Station_Code = models.CharField(max_length=255)
    Station_Location = models.CharField(max_length=255)
    Station_State = models.CharField(max_length=255)
    Temperature_Avg = models.DecimalField(max_digits=5, decimal_places=2)
    Temperature_Max = models.DecimalField(max_digits=5, decimal_places=2)
    Temperature_Min = models.DecimalField(max_digits=5, decimal_places=2)
    Wind_Direction = models.CharField(max_length=255)
    Wind_Speed = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.Date_Full} - {self.Station_Location}"

    class Meta:
        verbose_name_plural = "Weather Data"

