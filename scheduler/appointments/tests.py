from django.test import TestCase, RequestFactory
from .models import Appointment, MeetingRoom, Appointment_Participant
from django.contrib.auth.models import User
from datetime import datetime, timedelta, timezone
from faker import Faker
from .views import BaseClass, AppointmentView, AppointmentParametersView

fake = Faker()

# Create your tests here.
user_1 = None
user_2 = None
meeting_room = None
appointment = None
appointment_participants = []
time = datetime.now().replace(tzinfo=timezone.utc)

class AppointmentTestCase(TestCase):

    def setUp(self):
        global user_1, user_2, meeting_room, appointment, appointment_participants, time

        user_1 = User.objects.create(
            username=fake.unique.user_name(),
            first_name=fake.unique.first_name(),
            last_name=fake.unique.last_name(),
            email=fake.unique.email()
        )

        user_2 = User.objects.create(
            username=fake.unique.user_name(),
            first_name=fake.unique.first_name(),
            last_name=fake.unique.last_name(),
            email=fake.unique.email()
        )

        meeting_room = MeetingRoom.objects.create(
            name=fake.unique.city(),
            maximum_occupancy=fake.random_digit_not_null(),
            cost_per_hour=fake.random_int()
        )

        appointment = Appointment.objects.create(
            subject=fake.unique.sentence(),
            start_time=time + timedelta(hours=1),
            end_time=time + timedelta(hours=2),
            location=meeting_room,
            )

        appointment.participants.set([user_1, user_2])

    def test_is_appointment_unique(self):

        test = Appointment.objects.get(subject=appointment.subject)

        self.assertEqual(test, appointment)

    def test_is_max_occupancy_bigger_than_participants(self):
        test_room = MeetingRoom.objects.create(
            name='Test room',
            maximum_occupancy=1,
            cost_per_hour=100
        )
        validator = BaseClass()
        result = validator.validate_number_of_participants(
            {'name': test_room.name},
            [user_1, user_2]
            )

        self.assertIs(result, False)
    
    def test_is_user_in_appointment(self):

        participants = appointment.participants.all()
        self.assertIn(user_1, participants)
        self.assertIn(user_2, participants)

    def test_get_all_appointments(self):
        request = RequestFactory().get('/')
        view = AppointmentView()
        response = view.get(request)
        response = response.content.decode('utf-8')

        self.assertIn(appointment.subject, response)

    def test_create_appointment_post(self):
        POST_REQUEST = {
            "subject": "test appointment",
            "start_time": "2020-11-05 01:00:00",
            "end_time": "2020-11-05 03:00:00",
            "location": {
                "name": meeting_room.name
            },
            "participants": [
                {
                    "username":"rickbrown"
                },
                {
                    "username": "kiddcourtney"
                }
            ]
        }

        request = RequestFactory().post('/', data=POST_REQUEST, content_type='application/json')
        view = AppointmentView()
        response = view.post(request)

        appointment = (Appointment.objects
            .filter(subject=POST_REQUEST['subject'])
            .first()
            )

        self.assertIsNotNone(appointment)

    def test_get_specific_appointment(self):
        request = RequestFactory().get('/' + str(appointment.id) + '/')
        view = AppointmentParametersView()
        response = view.get(request, appointment.id)
        response = response.content.decode('utf-8')

        self.assertIn(appointment.subject, response)

    def test_put_specific_appointment(self):
        PUT_REQUEST = {
            "subject": "updated appointment",
            "start_time": "2020-11-05 01:00:00",
            "end_time": "2020-11-05 03:00:00",
            "location": {
                "name": meeting_room.name
            },
            "participants": [
                {
                    "username":"rickbrown"
                },
                {
                    "username": "kiddcourtney"
                }
            ]
        }

        request = RequestFactory().put(
            '/' + str(appointment.id) + '/',
            data=PUT_REQUEST,
            content_type='application/json'
            )

        view = AppointmentParametersView()
        response = view.put(request, appointment.id)

        updated_appointment = (Appointment.objects
            .filter(subject=PUT_REQUEST['subject'])
            .first()
            )

        self.assertIsNotNone(updated_appointment)
        self.assertEqual(updated_appointment.subject, PUT_REQUEST['subject'])
    
    def test_delete_specific_appointment(self):
        request = RequestFactory().delete('/' + str(appointment.id) + '/')
        view = AppointmentParametersView()
        response = view.delete(request, appointment.id)
        response = response.content.decode('utf-8')
        
        self.assertIn('Succesfully deleted appointment with id: ', response)
        self.assertIn('200', response)
