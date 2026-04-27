from django import forms
from .models import Appointment, VaccinationCenter


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['center', 'appointment_date', 'appointment_time', 'notes']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ghi chú thêm (nếu có)...'}),
        }
        labels = {
            'center': 'Trung tâm tiêm chủng',
            'appointment_date': 'Ngày hẹn',
            'appointment_time': 'Giờ hẹn',
            'notes': 'Ghi chú',
        }
