from django.db import models
from apps.appointments.models import VaccinationCenter


class Vaccine(models.Model):
    vaccine_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200, verbose_name='Tên vaccine')
    manufacturer = models.CharField(max_length=200, verbose_name='Nhà sản xuất')
    description = models.TextField(blank=True, verbose_name='Mô tả')
    target_disease = models.CharField(max_length=200, blank=True, verbose_name='Bệnh phòng ngừa')
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Giá (VNĐ)')
    required_doses = models.IntegerField(default=1, verbose_name='Số liều cần thiết')
    image = models.ImageField(upload_to='vaccines/', blank=True, null=True, verbose_name='Hình ảnh')
    centers = models.ManyToManyField(VaccinationCenter, through='VaccineStock', related_name='vaccines')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Vaccine'
        verbose_name_plural = 'Vaccine'

    def __str__(self):
        return f"{self.name} ({self.manufacturer})"


class VaccineStock(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    center = models.ForeignKey(VaccinationCenter, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, verbose_name='Số lượng tại trung tâm')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='Hạn sử dụng')

    class Meta:
        unique_together = ['vaccine', 'center']
        verbose_name = 'Kho vaccine'


class VaccineAdministration(models.Model):
    vaccine_administration_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField('appointments.Appointment', on_delete=models.CASCADE, related_name='administration')
    vaccines = models.ManyToManyField(Vaccine, related_name='administrations')
    doctor = models.ForeignKey('staff.Doctor', on_delete=models.SET_NULL, null=True, blank=True, related_name='examinations')
    nurse = models.ForeignKey('staff.Nurse', on_delete=models.SET_NULL, null=True, blank=True, related_name='injections')
    immunization_hour = models.DateTimeField(verbose_name='Giờ tiêm', null=True, blank=True)
    dose_number = models.IntegerField(default=1, verbose_name='Liều thứ')
    notes = models.TextField(blank=True, verbose_name='Ghi chú bác sĩ')
    post_vaccination_status = models.TextField(blank=True, verbose_name='Tình trạng sau tiêm')

    class Meta:
        verbose_name = 'Lần tiêm'
        verbose_name_plural = 'Lịch sử tiêm'

    @property
    def total_price(self):
        return sum(v.price for v in self.vaccines.all())

    @property
    def vaccine(self):
        """Backward compatibility helper for single vaccine references."""
        return self.vaccines.first()

    def __str__(self):
        v_names = ", ".join([v.name for v in self.vaccines.all()])
        return f"{self.appointment.candidate.full_name} - {v_names} - {self.immunization_hour}"

