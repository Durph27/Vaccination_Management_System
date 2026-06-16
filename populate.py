"""
Full database seeder for Trick or Chet.
Covers: VaccinationCenter, User, Staff, Doctor, Nurse, Receptionist,
        Candidate, MedicalRecord, Vaccine, VaccineStock,
        Appointment, VaccineAdministration, Sale
Run: python populate.py
"""
import os
import sys
import django
import random
from datetime import date, time, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.utils import timezone
from django.db import transaction

from apps.accounts.models import User
from apps.appointments.models import VaccinationCenter, Appointment
from apps.vaccines.models import Vaccine, VaccineStock, VaccineAdministration
from apps.staff.models import Staff, Doctor, Nurse, Receptionist
from apps.candidates.models import Candidate
from apps.records.models import MedicalRecord
from apps.sales.models import Sale


# ──────────────────────────────────────────────
# HELPER
# ──────────────────────────────────────────────
def make_user(username, first, last, email, role, password='123456'):
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': first,
            'last_name': last,
            'email': email,
            'role': role,
        }
    )
    # SQL (get): SELECT * FROM accounts_user WHERE username = %s LIMIT 1
    # SQL (create nếu chưa tồn tại):
    #      INSERT INTO accounts_user (username, first_name, last_name, email, role, is_active, date_joined)
    #      VALUES (%s, %s, %s, %s, %s, 1, NOW())

    if created:
        user.set_password(password)
        user.save()
        # SQL: UPDATE accounts_user SET password = %s WHERE id = %s
    return user, created


# ──────────────────────────────────────────────
# 1. VACCINATION CENTERS
# ──────────────────────────────────────────────
CENTERS_DATA = [
    ("VNVC Hoàng Văn Thụ",     "198 Hoàng Văn Thụ, Phú Nhuận, TP.HCM",          "1800 6595"),
    ("VNVC Lê Đại Hành",       "241 Lê Đại Hành, Quận 11, TP.HCM",              "1800 6595"),
    ("VNVC An Phú",            "Cantavil An Phú, Quận 2, TP.HCM",               "1800 6595"),
    ("VNVC Hà Nội – Trần Duy Hưng", "180 Trần Duy Hưng, Cầu Giấy, Hà Nội",    "1800 6595"),
    ("VNVC Đà Nẵng",           "122 Nguyễn Văn Linh, Thanh Khê, Đà Nẵng",      "1800 6595"),
]


def populate_centers():
    centers = []
    for name, address, hotline in CENTERS_DATA:
        c, _ = VaccinationCenter.objects.get_or_create(
            name=name,
            defaults={'address': address, 'hotline': hotline}
        )
        # SQL (get): SELECT * FROM appointments_vaccinationcenter WHERE name = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO appointments_vaccinationcenter (name, address, hotline, created_at)
        #      VALUES (%s, %s, %s, NOW())
        centers.append(c)
    print(f"  ✓ {len(centers)} trung tâm tiêm chủng")
    return centers


# ──────────────────────────────────────────────
# 2. STAFF
# ──────────────────────────────────────────────
DOCTORS = [
    ("Nguyễn Thị Lan",      "Nhi khoa",          "BS-HCM-0012"),
    ("Trần Văn Minh",       "Nội khoa",           "BS-HCM-0047"),
    ("Lê Thị Hoa",          "Sản phụ khoa",       "BS-HCM-0088"),
    ("Phạm Quốc Bảo",       "Truyền nhiễm",       "BS-HN-0033"),
    ("Đỗ Thị Mai",          "Nhi khoa",           "BS-DN-0021"),
]

NURSES = [
    ("Võ Thị Thanh",        "Điều dưỡng đa khoa"),
    ("Nguyễn Văn Hùng",     "Điều dưỡng nhi"),
    ("Bùi Thị Phương",      "Điều dưỡng đa khoa"),
    ("Trương Văn Nam",      "Điều dưỡng nội"),
    ("Lý Thị Kim",          "Điều dưỡng đa khoa"),
]

RECEPTIONISTS = [
    "Dương Thị Ngọc",
    "Hoàng Văn Toàn",
    "Phan Thị Bích",
]


def populate_staff(centers):
    doctors, nurses = [], []

    for i, (name, spec, lic) in enumerate(DOCTORS):
        center = centers[i % len(centers)]
        user, _ = make_user(
            username=f"doctor_{i+1}",
            first=name.split()[-1],
            last=' '.join(name.split()[:-1]),
            email=f"doctor{i+1}@vnvc.vn",
            role=User.ROLE_DOCTOR
        )
        staff, _ = Staff.objects.get_or_create(
            user=user,
            defaults={'center': center, 'role': 'doctor', 'name': name}
        )
        # SQL (get): SELECT * FROM staff_staff WHERE user_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO staff_staff (user_id, center_id, role, name)
        #      VALUES (%s, %s, 'doctor', %s)

        doc, _ = Doctor.objects.get_or_create(
            staff=staff,
            defaults={'specialization': spec, 'license_number': lic}
        )
        # SQL (get): SELECT * FROM staff_doctor WHERE staff_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO staff_doctor (staff_id, specialization, license_number)
        #      VALUES (%s, %s, %s)
        doctors.append(doc)

    for i, (name, cert) in enumerate(NURSES):
        center = centers[i % len(centers)]
        user, _ = make_user(
            username=f"nurse_{i+1}",
            first=name.split()[-1],
            last=' '.join(name.split()[:-1]),
            email=f"nurse{i+1}@vnvc.vn",
            role=User.ROLE_NURSE
        )
        staff, _ = Staff.objects.get_or_create(
            user=user,
            defaults={'center': center, 'role': 'nurse', 'name': name}
        )
        # SQL (get): SELECT * FROM staff_staff WHERE user_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO staff_staff (user_id, center_id, role, name)
        #      VALUES (%s, %s, 'nurse', %s)

        nurse, _ = Nurse.objects.get_or_create(
            staff=staff,
            defaults={'certification': cert}
        )
        # SQL (get): SELECT * FROM staff_nurse WHERE staff_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO staff_nurse (staff_id, certification) VALUES (%s, %s)
        nurses.append(nurse)

    for i, name in enumerate(RECEPTIONISTS):
        center = centers[i % len(centers)]
        user, _ = make_user(
            username=f"receptionist_{i+1}",
            first=name.split()[-1],
            last=' '.join(name.split()[:-1]),
            email=f"receptionist{i+1}@vnvc.vn",
            role=User.ROLE_RECEPTIONIST
        )
        staff, _ = Staff.objects.get_or_create(
            user=user,
            defaults={'center': center, 'role': 'receptionist', 'name': name}
        )
        # SQL (get): SELECT * FROM staff_staff WHERE user_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO staff_staff (user_id, center_id, role, name)
        #      VALUES (%s, %s, 'receptionist', %s)

        Receptionist.objects.get_or_create(staff=staff)
        # SQL (get): SELECT * FROM staff_receptionist WHERE staff_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO staff_receptionist (staff_id) VALUES (%s)

    print(f"  ✓ {len(DOCTORS)} bác sĩ, {len(NURSES)} y tá, {len(RECEPTIONISTS)} lễ tân")
    return doctors, nurses


# ──────────────────────────────────────────────
# 3. VACCINES
# ──────────────────────────────────────────────
VACCINES_DATA = [
    {
        "name": "Infanrix Hexa",
        "manufacturer": "GSK",
        "price": 1015000,
        "required_doses": 3,
        "target_disease": "Bạch hầu, Ho gà, Uốn ván, Bại liệt, Hib, Viêm gan B",
        "description": "Vaccine 6-trong-1 bảo vệ trẻ khỏi 6 bệnh nguy hiểm trong giai đoạn đầu đời. Được khuyến nghị cho trẻ từ 2 tháng tuổi.",
    },
    {
        "name": "Hexaxim",
        "manufacturer": "Sanofi Pasteur",
        "price": 1050000,
        "required_doses": 3,
        "target_disease": "Bạch hầu, Ho gà, Uốn ván, Bại liệt, Hib, Viêm gan B",
        "description": "Vaccine 6-trong-1 thế hệ mới với công nghệ tế bào nguyên vẹn, đảm bảo hiệu quả bảo vệ cao và ít tác dụng phụ.",
    },
    {
        "name": "Prevenar 13",
        "manufacturer": "Pfizer",
        "price": 1290000,
        "required_doses": 4,
        "target_disease": "Phế cầu khuẩn (13 chủng)",
        "description": "Vaccine phòng viêm phổi, viêm màng não, nhiễm trùng huyết do phế cầu. Bảo vệ trẻ khỏi 13 chủng phế cầu khuẩn phổ biến nhất.",
    },
    {
        "name": "Rotarix",
        "manufacturer": "GSK",
        "price": 825000,
        "required_doses": 2,
        "target_disease": "Viêm dạ dày ruột do Rotavirus",
        "description": "Vaccine uống phòng tiêu chảy cấp do Rotavirus – nguyên nhân hàng đầu gây nhập viện ở trẻ nhỏ toàn cầu.",
    },
    {
        "name": "Rotateq",
        "manufacturer": "MSD",
        "price": 665000,
        "required_doses": 3,
        "target_disease": "Viêm dạ dày ruột do Rotavirus",
        "description": "Vaccine uống 5 chủng Rotavirus, bảo vệ trẻ khỏi các thể tiêu chảy nặng trong năm đầu đời.",
    },
    {
        "name": "Vaxigrip Tetra",
        "manufacturer": "Sanofi",
        "price": 356000,
        "required_doses": 1,
        "target_disease": "Cúm mùa (4 chủng A & B)",
        "description": "Vaccine cúm tứ giá bảo vệ khỏi 4 chủng cúm phổ biến nhất mỗi mùa. Được khuyến nghị tiêm hàng năm cho mọi lứa tuổi từ 6 tháng.",
    },
    {
        "name": "Gardasil 9",
        "manufacturer": "MSD",
        "price": 1750000,
        "required_doses": 3,
        "target_disease": "Ung thư cổ tử cung (HPV 9 chủng)",
        "description": "Vaccine phòng ung thư cổ tử cung và các bệnh do HPV, bảo vệ trước 9 chủng HPV nguy hiểm nhất. Hiệu quả lên đến 98%.",
    },
    {
        "name": "Varivax",
        "manufacturer": "MSD",
        "price": 730000,
        "required_doses": 2,
        "target_disease": "Thủy đậu",
        "description": "Vaccine phòng bệnh thủy đậu (chickenpox) rất hiệu quả, ngừa biến chứng nặng như viêm não, viêm phổi.",
    },
    {
        "name": "Twinrix",
        "manufacturer": "GSK",
        "price": 450000,
        "required_doses": 3,
        "target_disease": "Viêm gan A & B",
        "description": "Vaccine kết hợp phòng viêm gan A và B trong một mũi tiêm, tiện lợi và tiết kiệm thời gian cho người lớn.",
    },
    {
        "name": "Shingrix",
        "manufacturer": "GSK",
        "price": 3200000,
        "required_doses": 2,
        "target_disease": "Zona thần kinh (Herpes Zoster)",
        "description": "Vaccine thế hệ mới phòng zona thần kinh với hiệu quả bảo vệ hơn 90%, dành cho người từ 50 tuổi trở lên.",
    },
]


def populate_vaccines(centers):
    vaccines = []
    for vd in VACCINES_DATA:
        v, _ = Vaccine.objects.get_or_create(
            name=vd['name'],
            defaults={
                'manufacturer': vd['manufacturer'],
                'price': vd['price'],
                'required_doses': vd['required_doses'],
                'target_disease': vd['target_disease'],
                'description': vd['description'],
            }
        )
        # SQL (get): SELECT * FROM vaccines_vaccine WHERE name = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO vaccines_vaccine
        #      (name, manufacturer, price, required_doses, target_disease, description, created_at)
        #      VALUES (%s, %s, %s, %s, %s, %s, NOW())

        # Stock in every center
        for center in centers:
            VaccineStock.objects.get_or_create(
                vaccine=v, center=center,
                defaults={
                    'quantity': random.randint(30, 150),
                    'expiry_date': timezone.now().date() + timedelta(days=random.randint(180, 730)),
                }
            )
            # SQL (get): SELECT * FROM vaccines_vaccinestock
            #            WHERE vaccine_id = %s AND center_id = %s LIMIT 1
            # SQL (create nếu chưa tồn tại):
            #      INSERT INTO vaccines_vaccinestock (vaccine_id, center_id, quantity, expiry_date)
            #      VALUES (%s, %s, %s, %s)

        vaccines.append(v)
    print(f"  ✓ {len(vaccines)} loại vaccine, tồn kho tại {len(centers)} trung tâm")
    return vaccines


# ──────────────────────────────────────────────
# 4. CANDIDATES & MEDICAL RECORDS
# ──────────────────────────────────────────────
CANDIDATES_DATA = [
    ("Nguyễn Văn An",       "1990-05-12", "M", "0901234561", "12 Lê Lợi, Q.1, TP.HCM",       170.0, 68.0, "A+", "Không", "Không"),
    ("Trần Thị Bình",       "1985-09-23", "F", "0912345672", "45 Nguyễn Huệ, Q.1, TP.HCM",   158.0, 52.0, "B+", "Không", "Không"),
    ("Lê Hoàng Cường",      "2000-01-15", "M", "0923456783", "78 Đinh Tiên Hoàng, Q.1, TP.HCM", 175.0, 72.0, "O+", "Không", "Không"),
    ("Phạm Thị Dung",       "1978-11-30", "F", "0934567894", "99 Hai Bà Trưng, Q.3, TP.HCM",  155.0, 48.0, "AB+", "Phấn hoa", "Tiểu đường type 2"),
    ("Đỗ Văn Em",           "1995-03-08", "M", "0945678905", "321 Nguyễn Thị Minh Khai, Q.3", 168.0, 75.0, "A-", "Không", "Không"),
    ("Võ Thị Phương",       "1988-07-22", "F", "0956789016", "55 CMT8, Q.10, TP.HCM",         162.0, 56.0, "B-", "Penicillin", "Không"),
    ("Ngô Minh Quân",       "1972-12-01", "M", "0967890127", "200 Lạc Long Quân, Q.11",       172.0, 80.0, "O-", "Không", "Huyết áp cao"),
    ("Hồ Thị Hoa",          "2005-06-18", "F", "0978901238", "15 Tô Hiến Thành, Q.10",        155.0, 43.0, "AB-", "Không", "Không"),
    ("Đinh Văn Khoa",       "1993-02-14", "M", "0989012349", "88 Bà Huyện Thanh Quan, Q.3",   178.0, 82.0, "A+", "Tôm cua", "Không"),
    ("Bùi Thị Lan",         "1982-08-05", "F", "0990123450", "33 Phan Đình Phùng, Phú Nhuận", 160.0, 55.0, "B+", "Không", "Viêm khớp"),
    ("Trương Văn Mạnh",     "1999-10-27", "M", "0901234562", "77 Nguyễn Đình Chiểu, Q.3",     173.0, 70.0, "O+", "Không", "Không"),
    ("Lý Thị Ngân",         "1991-04-16", "F", "0912345673", "102 Võ Thị Sáu, Q.3, TP.HCM",  157.0, 50.0, "A+", "Không", "Không"),
    ("Mai Công Oanh",        "1986-01-09", "M", "0923456784", "250 Điện Biên Phủ, Q. Bình Thạnh", 169.0, 73.0, "B+", "Aspirin", "Tiểu đường"),
    ("Dương Thị Phúc",      "2003-09-11", "F", "0934567895", "19 Xô Viết Nghệ Tĩnh, Bình Thạnh", 164.0, 52.0, "O+", "Không", "Không"),
    ("Vũ Hoàng Quân",       "1975-05-25", "M", "0945678906", "66 Ung Văn Khiêm, Bình Thạnh", 176.0, 85.0, "AB+", "Không", "Tim mạch"),
]


def populate_candidates():
    blood_choices = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    candidates = []

    for i, (name, dob_str, gender, phone, address, height, weight, blood, allergies, chronic) in enumerate(CANDIDATES_DATA):
        dob = date.fromisoformat(dob_str)
        user, _ = make_user(
            username=f"candidate_{i+1}",
            first=name.split()[-1],
            last=' '.join(name.split()[:-1]),
            email=f"candidate{i+1}@gmail.com",
            role=User.ROLE_CANDIDATE
        )
        candidate, _ = Candidate.objects.get_or_create(
            user=user,
            defaults={
                'full_name': name,
                'dob': dob,
                'gender': gender,
                'phone': phone,
                'address': address,
            }
        )
        # SQL (get): SELECT * FROM candidates_candidate WHERE user_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO candidates_candidate
        #      (user_id, full_name, dob, gender, phone, address, created_at, updated_at)
        #      VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())

        MedicalRecord.objects.get_or_create(
            candidate=candidate,
            defaults={
                'blood_type': blood,
                'height': height,
                'weight': weight,
                'allergies': allergies,
                'chronic_diseases': chronic,
                'notes': 'Không có ghi chú đặc biệt' if chronic == 'Không' else f'Theo dõi định kỳ: {chronic}',
            }
        )
        # SQL (get): SELECT * FROM records_medicalrecord WHERE candidate_id = %s LIMIT 1
        # SQL (create nếu chưa tồn tại):
        #      INSERT INTO records_medicalrecord
        #      (candidate_id, blood_type, height, weight, allergies, chronic_diseases, notes, created_at, updated_at)
        #      VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())

        candidates.append(candidate)

    print(f"  ✓ {len(candidates)} người tiêm & hồ sơ y tế")
    return candidates


# ──────────────────────────────────────────────
# 5. APPOINTMENTS, ADMINISTRATIONS, SALES
# ──────────────────────────────────────────────
STATUSES = ['completed', 'completed', 'completed', 'confirmed', 'pending', 'cancelled']
PAYMENT_METHODS = ['cash', 'bank_transfer', 'cash', 'insurance']


def random_past_date(days_back=120):
    return timezone.now().date() - timedelta(days=random.randint(1, days_back))


def random_future_date(days_ahead=30):
    return timezone.now().date() + timedelta(days=random.randint(1, days_ahead))


def populate_appointments(candidates, centers, doctors, nurses, vaccines):
    created_appts = 0
    created_adms  = 0
    created_sales = 0

    for candidate in candidates:
        # 2-4 appointments per candidate
        n_appts = random.randint(2, 4)
        for j in range(n_appts):
            center = random.choice(centers)
            status = random.choice(STATUSES)

            if status == 'completed':
                appt_date = random_past_date(120)
            elif status == 'pending':
                appt_date = random_future_date(14)
            elif status == 'confirmed':
                appt_date = random_future_date(30)
            else:  # cancelled
                appt_date = random_past_date(60)

            # Avoid duplicate same-day same-center appointments
            if Appointment.objects.filter(candidate=candidate, appointment_date=appt_date, center=center).exists():
                # SQL: SELECT 1 FROM appointments_appointment
                #      WHERE candidate_id = %s AND appointment_date = %s AND center_id = %s
                #      LIMIT 1
                continue

            appointment = Appointment.objects.create(
                candidate=candidate,
                center=center,
                appointment_date=appt_date,
                appointment_time=time(random.randint(7, 16), random.choice([0, 30])),
                status=status,
                notes='Khách hàng không có tiền sử dị ứng với vaccine.' if j == 0 else '',
            )
            # SQL: INSERT INTO appointments_appointment
            #      (candidate_id, center_id, appointment_date, appointment_time, status, notes, created_at)
            #      VALUES (%s, %s, %s, %s, %s, %s, NOW())
            created_appts += 1

            # Only create administration+sale for completed appointments
            if status == 'completed':
                vaccine = random.choice(vaccines)
                doctor = next(
                    (d for d in doctors if d.staff.center == center),
                    random.choice(doctors)
                )
                nurse = next(
                    (n for n in nurses if n.staff.center == center),
                    random.choice(nurses)
                )

                imm_hour = timezone.make_aware(
                    timezone.datetime(
                        appt_date.year, appt_date.month, appt_date.day,
                        appointment.appointment_time.hour,
                        appointment.appointment_time.minute
                    )
                )

                adm = VaccineAdministration.objects.create(
                    appointment=appointment,
                    vaccine=vaccine,
                    doctor=doctor,
                    nurse=nurse,
                    immunization_hour=imm_hour,
                    dose_number=1,
                    notes='Tiêm bình thường, không có phản ứng bất thường.',
                )
                # SQL: INSERT INTO vaccines_vaccineadministration
                #      (appointment_id, vaccine_id, doctor_id, nurse_id,
                #       immunization_hour, dose_number, notes, post_vaccination_status)
                #      VALUES (%s, %s, %s, %s, %s, 1, %s, '')
                created_adms += 1

                Sale.objects.create(
                    vaccine_administration=adm,
                    total_amount=vaccine.price,
                    payment_method=random.choice(PAYMENT_METHODS),
                    status='paid',
                    paid_at=imm_hour + timedelta(minutes=30),
                )
                # SQL: INSERT INTO sales_sale
                #      (vaccine_administration_id, total_amount, payment_method, status, paid_at, created_at)
                #      VALUES (%s, %s, %s, 'paid', %s, NOW())
                created_sales += 1

    print(f"  ✓ {created_appts} lịch hẹn, {created_adms} lần tiêm, {created_sales} hóa đơn")


# ──────────────────────────────────────────────
# 6. ADMIN USER
# ──────────────────────────────────────────────
def ensure_superuser():
    if not User.objects.filter(username='admin').exists():
        # SQL: SELECT 1 FROM accounts_user WHERE username = 'admin' LIMIT 1
        User.objects.create_superuser(
            username='admin',
            email='admin@vnvc.vn',
            password='admin',
            role=User.ROLE_ADMIN,
            first_name='Admin',
            last_name='VNVC',
        )
        # SQL: INSERT INTO accounts_user
        #      (username, password, email, first_name, last_name, role,
        #       is_active, is_staff, is_superuser, date_joined)
        #      VALUES ('admin', <hashed_password>, 'admin@vnvc.vn',
        #              'Admin', 'VNVC', 'admin', 1, 1, 1, NOW())
        print("  ✓ Superuser: username=admin / password=admin")
    else:
        print("  ✓ Superuser đã tồn tại")


# ──────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────
@transaction.atomic
def populate():
    print("\n>>> Bat dau dien du lieu mau...\n")
    print("[1] Trung tam tiem chung")
    centers = populate_centers()

    print("[2] Nhan vien")
    doctors, nurses = populate_staff(centers)

    print("[3] Vaccine")
    vaccines = populate_vaccines(centers)

    print("[4] Nguoi tiem & ho so y te")
    candidates = populate_candidates()

    print("[5] Lich hen, lan tiem & hoa don")
    populate_appointments(candidates, centers, doctors, nurses, vaccines)

    print("[6] Tai khoan quan tri")
    ensure_superuser()

    print("\n=== HOAN THANH! Tong ket: ===")
    print(f"   Trung tam:  {VaccinationCenter.objects.count()}")
    # SQL: SELECT COUNT(*) FROM appointments_vaccinationcenter
    print(f"   Nhan vien:  {Staff.objects.count()}")
    # SQL: SELECT COUNT(*) FROM staff_staff
    print(f"   Vaccine:    {Vaccine.objects.count()}")
    # SQL: SELECT COUNT(*) FROM vaccines_vaccine
    print(f"   Nguoi tiem: {Candidate.objects.count()}")
    # SQL: SELECT COUNT(*) FROM candidates_candidate
    print(f"   Ho so YT:   {MedicalRecord.objects.count()}")
    # SQL: SELECT COUNT(*) FROM records_medicalrecord
    print(f"   Lich hen:   {Appointment.objects.count()}")
    # SQL: SELECT COUNT(*) FROM appointments_appointment
    print(f"   Lan tiem:   {VaccineAdministration.objects.count()}")
    # SQL: SELECT COUNT(*) FROM vaccines_vaccineadministration
    print(f"   Hoa don:    {Sale.objects.count()}")
    # SQL: SELECT COUNT(*) FROM sales_sale
    print()


if __name__ == '__main__':
    populate()
