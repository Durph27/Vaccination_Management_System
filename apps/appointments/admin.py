from django.contrib import admin
from .models import Appointment, VaccinationCenter

admin.site.register(VaccinationCenter)

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'appointment_date', 'center', 'status']
    list_filter = ['status', 'center']
