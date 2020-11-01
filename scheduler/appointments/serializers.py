from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Appointment, MeetingRoom, Amenity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    username = serializers.CharField(max_length=150)

class AmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['name', 'description']
    
    id = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField(max_length=128)

class MeetingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingRoom
        fields = '__all__'

    id = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=64)
    maximum_occupancy = serializers.IntegerField(required=False)
    cost_per_hour = serializers.IntegerField(required=False)

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

    id = serializers.UUIDField(required=False)
    subject = serializers.CharField(max_length=128)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = MeetingRoomSerializer()
    participants = UserSerializer(many=True)
    deleted_at = serializers.DateTimeField(required=False)
