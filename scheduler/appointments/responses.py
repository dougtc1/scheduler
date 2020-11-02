"""
Response serializers used for Swagger documentation of Appointment app
"""
from rest_framework import serializers


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for error response body
    """

    error_message = serializers.CharField(max_length=256)

class UserResponseSerializer(serializers.Serializer):
    """
    Serializer for user related responses
    """
    first_name = serializers.CharField(max_length=150, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=150)

class MeetingRoomResponseSerializer(serializers.Serializer):
    """
    Serializer for meeting room related responses
    """

    id = serializers.UUIDField(required=False)
    name = serializers.CharField(max_length=64)
    maximum_occupancy = serializers.IntegerField(required=False)
    cost_per_hour = serializers.IntegerField(required=False)

class AppointmentResponseSerializer(serializers.Serializer):
    """
    Serializer for appointment response
    """

    id = serializers.UUIDField(required=False)
    subject = serializers.CharField(max_length=128)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    location = MeetingRoomResponseSerializer()
    participants = UserResponseSerializer(many=True)
    deleted_at = serializers.DateTimeField(required=False)


get_response = {
    200: AppointmentResponseSerializer,
    461: ErrorResponseSerializer
}

post_response = {
    200: AppointmentResponseSerializer,
    461: ErrorResponseSerializer
}

put_response = {}
delete_response = {}