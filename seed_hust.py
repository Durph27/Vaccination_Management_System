"""
Seed script: Xóa toàn bộ dữ liệu và tạo mới 2 trung tâm HUST với đầy đủ nhân viên.

Cú pháp tài khoản: role_diachi
Mật khẩu: 123456

Chạy: python seed_hust.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.accounts.models import User
from apps.appointments.models import VaccinationCenter, Appointment
from apps.candidates.models import Candidate
from apps.staff.models import Staff, Doctor, Nurse, Receptionist
from apps.records.models import MedicalRecord
from apps.vaccines.models import Vaccine, VaccineStock, VaccineAdministration
from apps.sales.models import Sale

PASSWORD = '123456'

# ──────────────────────────────────────────
# 1. XÓA TOÀN BỘ DỮ LIỆU
# ──────────────────────────────────────────
print("🗑️  Đang xóa toàn bộ dữ liệu cũ...")

Sale.objects.all().delete()
# SQL: DELETE FROM sales_sale
print("   ✓ Sale")

VaccineAdministration.objects.all().delete()
# SQL: DELETE FROM vaccines_vaccineadministration
print("   ✓ VaccineAdministration")

Appointment.objects.all().delete()
# SQL: DELETE FROM appointments_appointment
print("   ✓ Appointment")

VaccineStock.objects.all().delete()
# SQL: DELETE FROM vaccines_vaccinestock
print("   ✓ VaccineStock")

Vaccine.objects.all().delete()
# SQL: DELETE FROM vaccines_vaccine
print("   ✓ Vaccine")

MedicalRecord.objects.all().delete()
# SQL: DELETE FROM records_medicalrecord
print("   ✓ MedicalRecord")

# Delete staff sub-profiles first (due to OneToOne constraints)
Doctor.objects.all().delete()
# SQL: DELETE FROM staff_doctor
Nurse.objects.all().delete()
# SQL: DELETE FROM staff_nurse
Receptionist.objects.all().delete()
# SQL: DELETE FROM staff_receptionist
Staff.objects.all().delete()
# SQL: DELETE FROM staff_staff
print("   ✓ Staff / Doctor / Nurse / Receptionist")

Candidate.objects.all().delete()
# SQL: DELETE FROM candidates_candidate
print("   ✓ Candidate")

VaccinationCenter.objects.all().delete()
# SQL: DELETE FROM appointments_vaccinationcenter
print("   ✓ VaccinationCenter")

# Delete all non-superuser accounts
User.objects.filter(is_superuser=False).delete()
# SQL: DELETE FROM accounts_user WHERE is_superuser = 0
print("   ✓ User (non-superuser)")

print()

# ──────────────────────────────────────────
# 2. TẠO 2 TRUNG TÂM
# ──────────────────────────────────────────
print("🏥 Tạo trung tâm tiêm chủng...")

center1 = VaccinationCenter.objects.create(
    name='HUST – Số 1 Đại Cồ Việt',
    address='Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội',
    hotline='024 3869 2152',
)
# SQL: INSERT INTO appointments_vaccinationcenter (name, address, hotline, created_at)
#      VALUES ('HUST – Số 1 Đại Cồ Việt', 'Số 1 Đại Cồ Việt, Hai Bà Trưng, Hà Nội', '024 3869 2152', NOW())
print(f"   ✓ {center1.name}")

center2 = VaccinationCenter.objects.create(
    name='HUST – 36 Thanh Xuân',
    address='36 Thanh Xuân, Thanh Xuân, Hà Nội',
    hotline='024 3858 3660',
)
# SQL: INSERT INTO appointments_vaccinationcenter (name, address, hotline, created_at)
#      VALUES ('HUST – 36 Thanh Xuân', '36 Thanh Xuân, Thanh Xuân, Hà Nội', '024 3858 3660', NOW())
print(f"   ✓ {center2.name}")

print()

# ──────────────────────────────────────────
# 3. HÀM HELPER TẠO NHÂN VIÊN
# ──────────────────────────────────────────
def create_staff_user(username, first_name, last_name, role_str, center):
    """Tạo User + Staff + sub-profile tương ứng."""
    user = User.objects.create_user(
        username=username,
        password=PASSWORD,
        first_name=first_name,
        last_name=last_name,
        email=f"{username}@hust.edu.vn",
        role=role_str,
    )
    # SQL: INSERT INTO accounts_user
    #      (username, password, first_name, last_name, email, role, is_active, date_joined)
    #      VALUES (%s, <hashed_password>, %s, %s, %s, %s, 1, NOW())

    role_map = {
        'doctor': 'doctor',
        'nurse': 'nurse',
        'receptionist': 'receptionist',
    }

    staff = Staff.objects.create(
        user=user,
        center=center,
        role=role_map[role_str],
        name=f"{last_name} {first_name}",
    )
    # SQL: INSERT INTO staff_staff (user_id, center_id, role, name)
    #      VALUES (%s, %s, %s, %s)

    if role_str == 'doctor':
        Doctor.objects.create(
            staff=staff,
            specialization='Y học dự phòng',
            license_number=f'BS-{username.upper()}',
        )
        # SQL: INSERT INTO staff_doctor (staff_id, specialization, license_number)
        #      VALUES (%s, 'Y học dự phòng', %s)
    elif role_str == 'nurse':
        Nurse.objects.create(
            staff=staff,
            certification='Điều dưỡng đại học',
        )
        # SQL: INSERT INTO staff_nurse (staff_id, certification)
        #      VALUES (%s, 'Điều dưỡng đại học')
    elif role_str == 'receptionist':
        Receptionist.objects.create(staff=staff)
        # SQL: INSERT INTO staff_receptionist (staff_id) VALUES (%s)

    return user, staff


# ──────────────────────────────────────────
# 4. TẠO NHÂN VIÊN TRUNG TÂM 1 (Đại Cồ Việt)
# ──────────────────────────────────────────
print("👨‍⚕️  Tạo nhân viên Trung tâm 1 (Đại Cồ Việt)...")

u, s = create_staff_user(
    username='doctor_daicoviet',
    first_name='Minh',
    last_name='Nguyễn Văn',
    role_str='doctor',
    center=center1,
)
print(f"   ✓ Bác sĩ: {u.username}  |  Mật khẩu: {PASSWORD}")

u, s = create_staff_user(
    username='nurse_daicoviet',
    first_name='Hoa',
    last_name='Trần Thị',
    role_str='nurse',
    center=center1,
)
print(f"   ✓ Y tá: {u.username}  |  Mật khẩu: {PASSWORD}")

u, s = create_staff_user(
    username='receptionist_daicoviet',
    first_name='Lan',
    last_name='Lê Thị',
    role_str='receptionist',
    center=center1,
)
print(f"   ✓ Lễ tân: {u.username}  |  Mật khẩu: {PASSWORD}")

print()

# ──────────────────────────────────────────
# 5. TẠO NHÂN VIÊN TRUNG TÂM 2 (Thanh Xuân)
# ──────────────────────────────────────────
print("👨‍⚕️  Tạo nhân viên Trung tâm 2 (Thanh Xuân)...")

u, s = create_staff_user(
    username='doctor_thanhhoa',
    first_name='Hùng',
    last_name='Phạm Văn',
    role_str='doctor',
    center=center2,
)
print(f"   ✓ Bác sĩ: {u.username}  |  Mật khẩu: {PASSWORD}")

u, s = create_staff_user(
    username='nurse_thanhhoa',
    first_name='Nga',
    last_name='Hoàng Thị',
    role_str='nurse',
    center=center2,
)
print(f"   ✓ Y tá: {u.username}  |  Mật khẩu: {PASSWORD}")

u, s = create_staff_user(
    username='receptionist_thanhhoa',
    first_name='Mai',
    last_name='Vũ Thị',
    role_str='receptionist',
    center=center2,
)
print(f"   ✓ Lễ tân: {u.username}  |  Mật khẩu: {PASSWORD}")

print()

# ──────────────────────────────────────────
# 6. TẠO ADMIN (nếu chưa có)
# ──────────────────────────────────────────
print("🔑 Kiểm tra tài khoản admin...")
if not User.objects.filter(username='admin').exists():
    # SQL: SELECT 1 FROM accounts_user WHERE username = 'admin' LIMIT 1
    User.objects.create_superuser(
        username='admin',
        password=PASSWORD,
        email='admin@hust.edu.vn',
        first_name='Quản trị',
        last_name='Viên',
        role='admin',
    )
    # SQL: INSERT INTO accounts_user
    #      (username, password, email, first_name, last_name, role,
    #       is_active, is_staff, is_superuser, date_joined)
    #      VALUES ('admin', <hashed_password>, 'admin@hust.edu.vn',
    #              'Quản trị', 'Viên', 'admin', 1, 1, 1, NOW())
    print(f"   ✓ Tạo admin: admin  |  Mật khẩu: {PASSWORD}")
else:
    print("   ℹ️  Tài khoản admin đã tồn tại, bỏ qua.")

print()
print("=" * 55)
print("✅ HOÀN TẤT! Tóm tắt tài khoản:")
print("=" * 55)
print(f"{'Tài khoản':<30} {'Vai trò':<15} {'Trung tâm'}")
print("-" * 55)
accounts = [
    ('admin',                    'Quản trị viên', 'Toàn hệ thống'),
    ('doctor_daicoviet',         'Bác sĩ',        'Đại Cồ Việt'),
    ('nurse_daicoviet',          'Y tá',           'Đại Cồ Việt'),
    ('receptionist_daicoviet',   'Lễ tân',         'Đại Cồ Việt'),
    ('doctor_thanhhoa',          'Bác sĩ',         'Thanh Xuân'),
    ('nurse_thanhhoa',           'Y tá',            'Thanh Xuân'),
    ('receptionist_thanhhoa',    'Lễ tân',          'Thanh Xuân'),
]
for uname, role, center in accounts:
    print(f"{uname:<30} {role:<15} {center}")
print("-" * 55)
print(f"Tất cả mật khẩu: {PASSWORD}")
print()
