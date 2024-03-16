from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Appointment, Location, Doctor


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']


class LocationForm(forms.Form):
    location = forms.ModelChoiceField(queryset=Location.objects.all())


class DoctorForm(forms.Form):
    doctor = forms.ModelChoiceField(queryset=Doctor.objects.all())


class AppointmentForm(forms.ModelForm):
    Disease_choices = [
        ('disease1', 'Disease 1'),
        ('disease2', 'Disease 2'),
    ]

    disease = forms.ChoiceField(choices=Disease_choices)

    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'disease', 'additional_info', 'time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'})
        }