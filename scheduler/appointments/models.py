import uuid
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Amenity(models.Model):
    class Meta:
        verbose_name_plural = 'Amenities'

    def __str__(self):
        return str(self.name)

    NAMES = (
        ('projector', 'projector'),
        ('tv', 'tv'),
        ('whiteboard', 'whiteboard'),
        ('speakers', 'speakers'),
        ('phone', 'phone'),
        ('air_conditioning', 'air conditioning')
    )

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False
    )
    name = models.CharField(choices=NAMES, max_length=32, unique=True)
    description = models.CharField(max_length=128)

class MeetingRoom(models.Model):
    def __str__(self):
        return str(self.name)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False
    )
    name = models.CharField(max_length=64, unique=True)
    maximum_occupancy = models.PositiveIntegerField()
    cost_per_hour = models.PositiveIntegerField()
    #amenities = models.ManyToManyField(Amenity)

class Appointment(models.Model):
    class Meta:
        unique_together = ('subject', 'start_time','end_time')

    def __str__(self):
        return str(self.subject)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False
        )
    subject = models.CharField(max_length=128)
    start_time = models.DateTimeField('Start time')
    end_time = models.DateTimeField('End time')
    location = models.ForeignKey(
        MeetingRoom,
        on_delete=models.PROTECT
        )
    participants = models.ManyToManyField(
        User,
        through='Appointment_Participant',
        through_fields=('appointment','user'),
        blank=True
        )
    deleted_at = models.DateTimeField(
        'Time of deletion',
        default=None,
        null=True
        )

class Appointment_Participant(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['appointment', 'user'],
                name='unique appversion'
                )
            ]

    def __str__(self):
        return str(self.id)

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        db_index=True,
        editable=False
        )
    appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    deleted_at = models.DateTimeField(
        'Time of participant deletion',
        default=None,
        null=True
        )
