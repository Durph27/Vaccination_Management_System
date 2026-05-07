from django import forms
from .models import Candidate


class CandidateEditForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['full_name', 'dob', 'gender', 'phone', 'address']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        labels = {
            'full_name': 'Họ và tên',
            'dob': 'Ngày sinh',
            'gender': 'Giới tính',
            'phone': 'Số điện thoại',
            'address': 'Địa chỉ',
        }
