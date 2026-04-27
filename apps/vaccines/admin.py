from django.contrib import admin
from .models import Vaccine, VaccineAdministration, VaccineStock

@admin.register(Vaccine)
class VaccineAdmin(admin.ModelAdmin):
    list_display = ['name', 'manufacturer', 'price', 'required_doses', 'quantity_available', 'expiry_date']
    search_fields = ['name', 'manufacturer', 'target_disease']
    list_filter = ['manufacturer', 'required_doses']

@admin.register(VaccineStock)
class VaccineStockAdmin(admin.ModelAdmin):
    list_display = ['vaccine', 'center', 'quantity']
    list_filter = ['center']
    search_fields = ['vaccine__name', 'center__name']

@admin.register(VaccineAdministration)
class VaccineAdministrationAdmin(admin.ModelAdmin):
    list_display = ['get_candidate', 'vaccine', 'dose_number', 'immunization_hour', 'doctor', 'nurse']
    list_filter = ['vaccine', 'dose_number']
    search_fields = ['appointment__candidate__full_name', 'vaccine__name']

    def get_candidate(self, obj):
        return obj.appointment.candidate.full_name
    get_candidate.short_description = 'Người tiêm'
