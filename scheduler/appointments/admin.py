from django.contrib import admin
from .models import Appointment, MeetingRoom, Appointment_Participant
from django.contrib.auth.models import User

# Register your models here.

# Needed for inline capability in Sensor model
class Appointment_ParticipantInline(admin.TabularInline):
    model = Appointment_Participant
    can_delete = False
    verbose_name_plural = 'Participants'

class AppointmentAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = (
        'id',
        'subject',
        'start_time',
        'end_time',
        'location',
        'deleted_at',
        )
    inlines = [Appointment_ParticipantInline]

class MeetingRoomAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = (
        'id',
        'name',
        'maximum_occupancy',
        'cost_per_hour',
        )

class Appointment_ParticipantAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'appointment',
        'user',
        'deleted_at'
    )

admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(MeetingRoom, MeetingRoomAdmin)
admin.site.register(Appointment_Participant, Appointment_ParticipantAdmin)
