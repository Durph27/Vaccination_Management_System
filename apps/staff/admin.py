from django.contrib import admin
from .models import Staff, Doctor, Nurse, Receptionist

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'center', 'user']
    list_filter = ['role', 'center']
    search_fields = ['name', 'user__email']

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['staff', 'specialization', 'license_number']
    search_fields = ['staff__name']

@admin.register(Nurse)
class NurseAdmin(admin.ModelAdmin):
    list_display = ['staff', 'certification']
    search_fields = ['staff__name']

@admin.register(Receptionist)
class ReceptionistAdmin(admin.ModelAdmin):
    list_display = ['staff']
    search_fields = ['staff__name']
