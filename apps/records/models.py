from django.db import models
from apps.candidates.models import Candidate


class MedicalRecord(models.Model):
    record_id = models.AutoField(primary_key=True)
    candidate = models.OneToOneField(Candidate, on_delete=models.CASCADE, related_name='medical_record')
    blood_type = models.CharField(max_length=5, blank=True, verbose_name='Nhóm máu',
                                   choices=[('A+','A+'),('A-','A-'),('B+','B+'),('B-','B-'),
                                            ('AB+','AB+'),('AB-','AB-'),('O+','O+'),('O-','O-')])
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Chiều cao (cm)')
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='Cân nặng (kg)')
    allergies = models.TextField(blank=True, verbose_name='Dị ứng')
    chronic_diseases = models.TextField(blank=True, verbose_name='Bệnh mãn tính')
    notes = models.TextField(blank=True, verbose_name='Ghi chú bác sĩ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hồ sơ y tế'
        verbose_name_plural = 'Hồ sơ y tế'

    def __str__(self):
        return f"Hồ sơ - {self.candidate.full_name}"
