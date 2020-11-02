import json
from django.core.management.base import BaseCommand
from appointments.views import AppointmentView
from django.test import RequestFactory

class Command(BaseCommand):
    help = 'Command to list all registered appointments'

    def handle(self, *args, **options):
        request = RequestFactory().get('/')
        view = AppointmentView()
        response = view.get(request)
        response = json.loads(response.content.decode('utf-8'))

        self.stdout.write(json.dumps(response, indent=2, sort_keys=True))
