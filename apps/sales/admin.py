from django.contrib import admin
from .models import Sale

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['sale_id', 'get_candidate', 'get_vaccines', 'total_amount', 'payment_method', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['vaccine_administration__appointment__candidate__full_name']

    def get_candidate(self, obj):
        return obj.vaccine_administration.appointment.candidate.full_name
    get_candidate.short_description = 'Người tiêm'

    def get_vaccines(self, obj):
        return ", ".join([v.name for v in obj.vaccine_administration.vaccines.all()])
    get_vaccines.short_description = 'Vaccines'
