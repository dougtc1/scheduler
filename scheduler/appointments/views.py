from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from drf_yasg.utils import swagger_auto_schema
from .serializers import AppointmentSerializer
from .responses import *
from django.http import JsonResponse

# Create your views here.

class Appointment(GenericAPIView):
    serializer_class = AppointmentSerializer

    @swagger_auto_schema(
        operation_description='Endpoint to fetch appointments',
        responses=get_response
        )
    def get(self, request):
        pass
    
    @swagger_auto_schema(
        operation_description='Endpoint to create a new appointment',
        request_body=AppointmentSerializer,
        responses=post_response
        )
    def post(self, request):
        pass


class AppointmentParameters(GenericAPIView):
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
