from django.contrib import admin
from .models import Measurement, Sensor 

admin.site.register(Sensor)
admin.site.register(Measurement)
