from django.db import models
from apps.accounts.models import User


class Candidate(models.Model):
    GENDER_CHOICES = [('M', 'Nam'), ('F', 'Nữ'), ('O', 'Khác')]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    candidate_id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200, verbose_name='Họ và tên')
    dob = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, verbose_name='Giới tính')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Người tiêm'
        verbose_name_plural = 'Người tiêm'

    def __str__(self):
        return self.full_name
