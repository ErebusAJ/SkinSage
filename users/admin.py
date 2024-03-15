from django.contrib import admin
from .models import Profile, Location, Doctor, Appointment


admin.site.register(Profile)
admin.site.register(Location)
admin.site.register(Doctor)
admin.site.register(Appointment)
