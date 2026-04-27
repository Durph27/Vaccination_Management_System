from django.contrib import admin
from .models import MedicalRecord

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'blood_type', 'allergies', 'chronic_diseases', 'updated_at']
    search_fields = ['candidate__full_name']
    list_filter = ['blood_type']
