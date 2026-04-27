from django.db import models
from apps.accounts.models import User
from apps.appointments.models import VaccinationCenter


class Staff(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Bác sĩ'),
        ('nurse', 'Y tá'),
        ('receptionist', 'Lễ tân'),
    ]
    staff_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_profile')
    center = models.ForeignKey(VaccinationCenter, on_delete=models.SET_NULL, null=True, related_name='staff')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    name = models.CharField(max_length=200, verbose_name='Họ và tên')

    class Meta:
        verbose_name = 'Nhân viên'
        verbose_name_plural = 'Nhân viên'

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"


class Doctor(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Chuyên môn')
    license_number = models.CharField(max_length=50, blank=True, verbose_name='Số chứng chỉ hành nghề')

    class Meta:
        verbose_name = 'Bác sĩ'

    def __str__(self):
        return self.staff.name


class Nurse(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='nurse_profile')
    certification = models.CharField(max_length=200, blank=True, verbose_name='Chứng chỉ')

    class Meta:
        verbose_name = 'Y tá'

    def __str__(self):
        return self.staff.name


class Receptionist(models.Model):
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE, related_name='receptionist_profile')

    class Meta:
        verbose_name = 'Lễ tân'

    def __str__(self):
        return self.staff.name
