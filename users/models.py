from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'


class Location(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    name = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    speciality = models.TextField(max_length=100, null=True)
    qualification = models.TextField(max_length=100, null=True)
    address = models.TextField(null=True, max_length=255)
    phone = models.IntegerField(null=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, default=1)
    date = models.DateField(null=True)
    additional_info = models.TextField(blank=True)
    disease = models.TextField(null=True)
    time = models.TimeField(null=True)

    def __str__(self):
        return f"{self.user.username} - {self.doctor.name} - {self.date}"