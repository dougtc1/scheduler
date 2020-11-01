from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import AppointmentSerializer
from .responses import *
from django.http import JsonResponse
from .models import Appointment
import json

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
    def get(self):
        qs_appointments = (
            Appointment.objects.filter(deleted_at=None).order_by('start_time')
            )
        serialized_appointments = AppointmentSerializer(
            qs_appointments,
            many=True
            )
        response = self.build_response(serialized_appointments.data, 200)

        return JsonResponse(response)

    @swagger_auto_schema(
        operation_description='Endpoint to create a new appointment',
        request_body=AppointmentSerializer,
        responses=post_response
        )
    def post(self, request):
        json_request = json.loads(request.body.decode('utf-8'))
        serializer = AppointmentSerializer(data=json_request)

        response = self.build_response('No errors', 200)
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
