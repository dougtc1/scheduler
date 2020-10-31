from django.contrib import admin
from django.urls import path
from .views import Appointment, AppointmentParameters

urlpatterns = [
    path('', Appointment.as_view(), name='new_appointments'),
    path('<slug:id>', AppointmentParameters.as_view(), name='existing_appointments'),
]
