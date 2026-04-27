from django.db import models
from apps.candidates.models import Candidate


class VaccinationCenter(models.Model):
    center_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Tên trung tâm')
    address = models.TextField(verbose_name='Địa chỉ')
    hotline = models.CharField(max_length=20, verbose_name='Đường dây nóng')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Trung tâm tiêm chủng'
        verbose_name_plural = 'Trung tâm tiêm chủng'

    def __str__(self):
        return self.name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ xác nhận'),
        ('confirmed', 'Đã xác nhận'),
        ('completed', 'Hoàn thành'),
        ('cancelled', 'Đã hủy'),
    ]

    appointment_id = models.AutoField(primary_key=True)
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='appointments')
    center = models.ForeignKey(VaccinationCenter, on_delete=models.SET_NULL, null=True, related_name='appointments')
    appointment_date = models.DateField(verbose_name='Ngày hẹn')
    appointment_time = models.TimeField(verbose_name='Giờ hẹn')
    notes = models.TextField(blank=True, verbose_name='Ghi chú')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Lịch hẹn'
        verbose_name_plural = 'Lịch hẹn'
        ordering = ['-appointment_date']

    def __str__(self):
        return f"{self.candidate.full_name} - {self.appointment_date}"
