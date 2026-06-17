from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CANDIDATE = 'candidate'
    ROLE_RECEPTIONIST = 'receptionist'
    ROLE_DOCTOR = 'doctor'
    ROLE_NURSE = 'nurse'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_CANDIDATE, 'Người tiêm'),
        (ROLE_RECEPTIONIST, 'Lễ tân'),
        (ROLE_DOCTOR, 'Bác sĩ'),
        (ROLE_NURSE, 'Y tá'),
        (ROLE_ADMIN, 'Quản trị viên'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_CANDIDATE)
    phone = models.CharField(max_length=15, blank=True)

    def is_staff_member(self):
        return self.role in [self.ROLE_RECEPTIONIST, self.ROLE_DOCTOR, self.ROLE_NURSE, self.ROLE_ADMIN]

    def is_candidate_user(self):
        return self.role == self.ROLE_CANDIDATE

    def is_receptionist(self):
        return self.role in [self.ROLE_RECEPTIONIST, self.ROLE_ADMIN]

    def is_doctor(self):
        return self.role in [self.ROLE_DOCTOR, self.ROLE_ADMIN]

    def is_nurse(self):
        return self.role in [self.ROLE_NURSE, self.ROLE_ADMIN]

    def is_admin(self):
        return self.role == self.ROLE_ADMIN

    def __str__(self):
        name = self.get_full_name() or self.username
        get_role = getattr(self, 'get_role_display', None)
        role = get_role() if get_role else self.role
        return f"{name} ({role})"
