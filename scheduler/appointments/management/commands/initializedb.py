from django.core.management.base import BaseCommand, CommandError
from appointments.models import Appointment, MeetingRoom, Amenity, Appointment_Participant
from django.contrib.auth.models import User
from faker import Faker
from datetime import timezone

fake = Faker()
Faker.seed(4321)

class Command(BaseCommand):
    help = 'Initializes DB for the project'

    def print_user_information(self, user):
        output = 'First name: ' + user.first_name\
            + ' | Last name: ' + user.last_name\
            + ' | Email: ' + user.email\
            + ' | Username: ' + user.username

        return output

    def print_meeting_room_information(self, room):
        output = 'Name: ' + room.name\
            + ' | Maximum occupancy: ' + str(room.maximum_occupancy)\
            + ' | Cost per hour: ' + str(room.cost_per_hour)

        return output

    def print_appointment_information(
        self, appointment, participant_1, participant_2
        ):

        output = 'Subject: ' + str(appointment)\
            + ' | Start_time: ' + appointment.start_time.isoformat()\
            + ' | End_time: ' + appointment.end_time.isoformat()\
            + ' | Location: ' + self.print_meeting_room_information(
                appointment.location
                )\
            + ' | \n Participants: [' + self.print_user_information(participant_1)\
            + ',' + self.print_user_information(participant_2)\
            + ']'

        return output

    def handle(self, *args, **options):
        # Create 5 users
        users = {}
        for i in range(5):
            user = User.objects.create(
                username=fake.unique.user_name(),
                first_name=fake.unique.first_name(),
                last_name=fake.unique.last_name(),
                email=fake.unique.email(),
                )
            self.stdout.write(self.print_user_information(user))
            users[i] = user
        self.stdout.write('\n')

        # Create 5 Meeting Rooms
        meeting_rooms = {}
        for i in range(5):
            room = MeetingRoom.objects.create(
                name=fake.unique.city(),
                maximum_occupancy=fake.random_digit_not_null(),
                cost_per_hour=fake.random_int(),
            )
            self.stdout.write(self.print_meeting_room_information(room))
            meeting_rooms[i] = room
        self.stdout.write('\n')

        # Create appointments
        appointments = {}
        for i in range(4):
            appointment = Appointment.objects.create(
                subject=fake.sentence(),
                start_time=fake.unique.date_time_this_year(tzinfo=timezone.utc),
                end_time=fake.unique.date_time_this_year(tzinfo=timezone.utc),
                location=meeting_rooms[i],
            )
            # First participant
            participant_1 = Appointment_Participant.objects.create(
                appointment=appointment,
                user=users[i]
                )

            # Second participant
            participant_2 = Appointment_Participant.objects.create(
                appointment=appointment,
                user=users[i+1]
                )

            self.stdout.write(
                self.print_appointment_information(
                    appointment,
                    participant_1.user,
                    participant_2.user
                    )
                )
