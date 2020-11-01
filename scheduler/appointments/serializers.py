from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Appointment, MeetingRoom, Amenity
from django.shortcuts import get_object_or_404

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

    def create(self, validated_data):
        validated_location = validated_data.pop('location')
        validated_participants = validated_data.pop('participants')

        location_name = validated_location.get('name')
        location = get_object_or_404(MeetingRoom, name=location_name)
        appointment = Appointment.objects.create(location=location, **validated_data)
        
        username_list = [i.get('username') for i in validated_participants]
        print('usernames', username_list)

        participants = User.objects.filter(username__in=username_list)
        print('participants', participants)
        appointment.participants.set(participants)
        print('id',appointment.id)
        return appointment

    def update(self, instance, validated_data):
        instance.subject = validated_data.get('subject', instance.subject)
        instance.start_time = validated_data.get('start_time', instance.start_time)
        instance.end_time = validated_data.get('end_time', instance.end_time)
        instance.location = validated_data.get('location', instance.location)
        instance.participants = validated_data.get('participants', instance.participants)
        instance.save()
        return instance
