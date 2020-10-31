from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Appointment, MeetingRoom, Amenity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            'id',
            'subject',
            'start_time',
            'end_time',
            'location',
            'participants',
            'deleted_at'
            ]

class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = ['name', 'maximum_occupancy', 'cost_per_hour']

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description']
