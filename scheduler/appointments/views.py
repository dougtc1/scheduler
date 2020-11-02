from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import AppointmentSerializer, MeetingRoomSerializer
from .responses import *
from django.http import JsonResponse
from .models import Appointment, MeetingRoom, Appointment_Participant
import json
from sentry_sdk import capture_exception
from datetime import datetime, timezone
import structlog

logger = structlog.get_logger(__name__)

# Create your views here.

class BaseClass(GenericAPIView):
    def build_response(self, data, status_code, error_message=None):
        response = {
            'data': data,
            'status_code': status_code
            }

        if error_message:
            response.pop('data', None)
            response['error_message'] = error_message

        return response
    
    def validate_number_of_participants(self, location, participants):
        room = MeetingRoom.objects.get(name=location['name'])
        return  room.maximum_occupancy >= len(participants)
    
    def convert_request(self, request):
        json_request = json.loads(request.body.decode('utf-8'))
        serializer = AppointmentSerializer(data=json_request)

        return serializer


class AppointmentView(BaseClass):
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(
        operation_description='Endpoint to fetch appointments',
        responses=get_response
        )
    def get(self, request):
        try:
            qs_appointments = (
                Appointment.objects.filter(deleted_at=None)
                .order_by('start_time')
                )
            serialized_appointments = AppointmentSerializer(
                qs_appointments,
                many=True
                )
            response = self.build_response(serialized_appointments.data, 200)
            logger.info(
                'Response in list appointments',
                data=serialized_appointments.data
                )
        except Exception as exc:
            capture_exception(exc)
            response = self.build_response(
                [],
                500,
                'There was an error fetching the data.'
                )
            logger.error(
                'Error in list appointments',
                error=exc
                )
        else:
            return JsonResponse(response, status=response['status_code'])

    @swagger_auto_schema(
        operation_description='Endpoint to create a new appointment',
        request_body=AppointmentSerializer,
        responses=post_response
        )
    def post(self, request):
        serializer = self.convert_request(request)

        if serializer.is_valid():
            location = serializer.validated_data.get('location')
            participants = serializer.validated_data.get('participants')
            if self.validate_number_of_participants(location, participants):
                serializer.save()
                response = self.build_response(serializer.data, 200)
                logger.info(
                    'Response in create appointment',
                    data=serializer.data
                    )
            else:
                response = self.build_response(
                    [],
                    461,
                    post_response[461]['error_message']
                    )
                logger.error(
                    'Error in create appointments',
                    error=post_response[461]['error_message']
                    )
                
        else:
            response = self.build_response([], 400, serializer.errors)
        return JsonResponse(response, status=response['status_code'])


class AppointmentParametersView(BaseClass):
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(
        operation_description='Endpoint to fetch appointments',
        responses=get_response
        )
    def get(self, request, id):
        appointment = get_object_or_404(Appointment, pk=id, deleted_at=None)
        deserialized_appointment = AppointmentSerializer(appointment)
        response = self.build_response(deserialized_appointment.data, 200)

        logger.info(
            'Response in get specific appointment',
            data=deserialized_appointment.data
            )

        return JsonResponse(response, status=response['status_code'])

    @swagger_auto_schema(
        operation_description='Endpoint to update an existing appointment',
        request_body=AppointmentSerializer,
        responses=put_response
        )
    def put(self, request, id):
        appointment = get_object_or_404(Appointment, pk=id, deleted_at=None)
        serializer = self.convert_request(request)
        if serializer.is_valid():
            serializer.save()
            response = self.build_response(serializer.data, 200)
            logger.info(
                'Response in update specific appointment',
                data=serializer.data
                )
        else:
            response = self.build_response([], 400, serializer.errors)

            logger.error(
                'Error in update specific appointment',
                errors=serializer.errors
                )

        return JsonResponse(response, status=response['status_code'])
    
    @swagger_auto_schema(
        operation_description='Endpoint to delete an appointment',
        responses=delete_response
        )
    def delete(self, request, id):
        appointment = get_object_or_404(Appointment, pk=id, deleted_at=None)
        try:
            deletion_time = datetime.now(tz=timezone.utc)
            appointment.deleted_at = deletion_time
            appointment.save()
            qs_appointment_participants = (Appointment_Participant
                .objects.filter(appointment=appointment)
                )

            for appointment_participant in qs_appointment_participants:
                appointment_participant.deleted_at = deletion_time
                appointment_participant.save()

            response = {
                'message': 'Succesfully deleted appointment with id: ' + str(id),
                'status_code': 200
                }
            logger.info(
                'Response in delete appointment'
                )
        except Exception as exc:
            capture_exception(exc)
            response = self.build_response(
                [],
                500,
                'There was an error deleting the specified object'
                )
            logger.error(
                'Error in delete appointment',
                error=exc
                )

        return JsonResponse(response, status=response['status_code'])
