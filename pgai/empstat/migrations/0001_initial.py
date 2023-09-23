# Generated by Django 4.2.5 on 2023-09-23 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
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
                ("name", models.CharField(max_length=100)),
                ("department", models.CharField(max_length=50)),
                ("salary", models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name="Fuelconsumption",
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
                ("modelyear", models.IntegerField()),
                ("make", models.CharField(max_length=20)),
                ("model", models.CharField(max_length=50)),
                ("vehicleclass", models.CharField(max_length=25)),
                ("enginesize", models.DecimalField(decimal_places=1, max_digits=1)),
                ("cylinders", models.IntegerField()),
                ("transmission", models.CharField(max_length=5)),
                ("fueltype", models.CharField(max_length=1)),
                (
                    "fuelconsumption_city",
                    models.DecimalField(decimal_places=2, max_digits=2),
                ),
                (
                    "fuelconsumption_hwy",
                    models.DecimalField(decimal_places=2, max_digits=2),
                ),
                (
                    "fuelconsumption_comb",
                    models.DecimalField(decimal_places=2, max_digits=2),
                ),
                ("fuelconsumption_comb_mpg", models.IntegerField()),
                ("co2emissions", models.IntegerField()),
            ],
        ),
    ]