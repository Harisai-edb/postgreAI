# Generated by Django 4.2.5 on 2023-09-24 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("empstat", "0003_alter_fuelconsumption_fuelconsumption_city_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="WeatherData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Precipitation", models.DecimalField(decimal_places=2, max_digits=5)),
                ("Date_Full", models.DateField()),
                ("Date_Month", models.IntegerField()),
                ("Date_Week_of", models.IntegerField()),
                ("Date_Year", models.IntegerField()),
                ("Station_City", models.CharField(max_length=255)),
                ("Station_Code", models.CharField(max_length=255)),
                ("Station_Location", models.CharField(max_length=255)),
                ("Station_State", models.CharField(max_length=255)),
                (
                    "Temperature_Avg",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "Temperature_Max",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                (
                    "Temperature_Min",
                    models.DecimalField(decimal_places=2, max_digits=5),
                ),
                ("Wind_Direction", models.CharField(max_length=255)),
                ("Wind_Speed", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                "verbose_name_plural": "Weather Data",
            },
        ),
    ]
