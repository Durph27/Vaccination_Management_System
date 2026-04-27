from django import forms
from .models import MedicalRecord


class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['blood_type', 'allergies', 'chronic_diseases', 'notes']
        widgets = {
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'chronic_diseases': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 4}),
        }
        labels = {
            'blood_type': 'Nhóm máu',
            'allergies': 'Dị ứng',
            'chronic_diseases': 'Bệnh mãn tính',
            'notes': 'Ghi chú',
        }
