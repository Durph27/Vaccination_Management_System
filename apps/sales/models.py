from django.db import models
from apps.vaccines.models import VaccineAdministration


class Sale(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Chờ thanh toán'),
        ('paid', 'Đã thanh toán'),
        ('cancelled', 'Đã hủy'),
    ]
    PAYMENT_CHOICES = [
        ('cash', 'Tiền mặt'),
        ('bank_transfer', 'Chuyển khoản'),
        ('insurance', 'Bảo hiểm y tế'),
    ]

    sale_id = models.AutoField(primary_key=True)
    vaccine_administration = models.OneToOneField(
        VaccineAdministration, on_delete=models.CASCADE, related_name='sale'
    )
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Tổng tiền')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, verbose_name='Phương thức thanh toán')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Trạng thái')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Hóa đơn'
        verbose_name_plural = 'Hóa đơn'

    def __str__(self):
        return f"HD#{self.sale_id} - {self.vaccine_administration.appointment.candidate.full_name}"
