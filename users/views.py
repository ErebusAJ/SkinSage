from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AppointmentForm, DoctorForm, LocationForm
from .models import Appointment, Doctor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required()
def profile(request):
    user_appointments = Appointment.objects.filter(user=request.user)
    return render(request,'users/profile.html', {'appointments': user_appointments})


@login_required()
def update(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/update.html', context)


@login_required
def select_doctor(request):
    doctors = Doctor.objects.all()

    if request.method == 'POST':
        location_form = LocationForm(request.POST)
        doctor_form = DoctorForm(request.POST)

        if location_form.is_valid():
            selected_location = location_form.cleaned_data['location']
            if selected_location:
                doctors = Doctor.objects.filter(location=selected_location)

        if doctor_form.is_valid():
            selected_doctor = doctor_form.cleaned_data['doctor']
            request.session['doctor'] = selected_doctor.id
            return render(request, 'users/booking.html', {'doctor': selected_doctor, 'location_form': LocationForm()})
    else:
        location_form = LocationForm()
        doctor_form = DoctorForm()

    return render(request, 'users/doctor.html', {'doctors': doctors, 'location_form': location_form, 'doctor_form': doctor_form})


def book_appointment(request):
    doctor_id = request.GET.get('doctor_id')
    if doctor_id:
        doctor = get_object_or_404(Doctor, id=doctor_id)
    else:
        doctor = None
    time_slots = [
        '11:00', '12:00', '3:00', '4:00', '5:00'
    ]
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            if doctor:
                appointment.doctor = doctor  # Assign the selected doctor to the appointment
            try:
                appointment.save()
                messages.success(request, f'Your appointment has been booked')
                return redirect('profile')
            except IntegrityError as e:
                messages.error(request, f'Error: {e}')
    else:
        form = AppointmentForm(initial={'doctor': doctor})  # Pass the doctor as initial data to the form

    return render(request, 'users/booking.html', {'form': form, 'available_time_slots': time_slots, 'doctor': doctor})


@login_required
def display_appointments(request):
    user_appointments = Appointment.objects.filter(user=request.user)
    return render(request, 'users/appointments.html', {'appointments': user_appointments})
