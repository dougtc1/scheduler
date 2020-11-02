from django.contrib import admin
from django.urls import path
from .views import AppointmentView, AppointmentParametersView

urlpatterns = [
    path('', AppointmentView.as_view(), name='new_appointments'),
    path('<str:id>/', AppointmentParametersView.as_view(), name='existing_appointments'),
]
