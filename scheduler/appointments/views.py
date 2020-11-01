from django.shortcuts import render, get_object_or_404
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import AppointmentSerializer, MeetingRoomSerializer
from .responses import *
from django.http import JsonResponse
from .models import Appointment, MeetingRoom
import json
from sentry_sdk import capture_exception

# Create your views here.

class BaseClass(GenericAPIView):
    def build_response(self, data, status_code, error_message=None):
        response = {
            'data': data,
            'status_code': status_code
            }
        print('response',data)
        if error_message:
            response.pop('data', None)
            response['error_message'] = error_message

        return response


class AppointmentView(BaseClass):
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(
        operation_description='Endpoint to fetch appointments',
        responses=get_response
        )
    def get(self, request):
        try:
            qs_appointments = (
                Appointment.objects.filter(deleted_at=None).order_by('start_time')
                )
            serialized_appointments = AppointmentSerializer(
                qs_appointments,
                many=True
                )
            response = self.build_response(serialized_appointments.data, 200)
        except Exception as exc:
            capture_exception(exc)
            response = self.build_response([], 500, serialized_appointments.errors)
        else:
            return JsonResponse(response)

    @swagger_auto_schema(
        operation_description='Endpoint to create a new appointment',
        request_body=AppointmentSerializer,
        responses=post_response
        )
    def post(self, request):
        json_request = json.loads(request.body.decode('utf-8'))
        serializer = AppointmentSerializer(data=json_request)
        if serializer.is_valid():
            serializer.save()
            response = self.build_response(serializer.data, 200)
        else:
            response = self.build_response([], 400, serializer.errors)
        return JsonResponse(response)


class AppointmentParametersView(BaseClass):
    serializer_class = AppointmentSerializer
       
    @swagger_auto_schema(
        operation_description='Endpoint to fetch appointments',
        responses=get_response
        )
    def get(self, request, id):
        pass

    @swagger_auto_schema(
        operation_description='Endpoint to update an existing appointment',
        request_body=AppointmentSerializer,
        responses=put_response
        )
    def put(self, request, id):
        pass
    
    @swagger_auto_schema(operation_description='Endpoint to delete an appointment', responses=delete_response)
    def delete(self, request, id):
        pass
