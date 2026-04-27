from django.contrib import admin
from .models import Candidate

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'dob', 'gender', 'phone']
    search_fields = ['full_name', 'phone']
