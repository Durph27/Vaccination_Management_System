# Trick or Chet — Hệ thống quản lý tiêm chủng

## Công nghệ sử dụng
- **Backend**: Python 3.10+, Django 4.2
- **Database**: MySQL 8+
- **Frontend**: Bootstrap 5, CSS tùy chỉnh, Google Fonts

---

## Cài đặt

### 1. Clone và tạo môi trường ảo
```bash
git clone <repo>
cd vaccinems
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. Cài dependencies
```bash
pip install -r requirements.txt
```

### 3. Tạo database MySQL
```sql
CREATE DATABASE vaccinems_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'vaccineuser'@'localhost' IDENTIFIED BY 'yourpassword';
GRANT ALL PRIVILEGES ON vaccinems_db.* TO 'vaccineuser'@'localhost';
FLUSH PRIVILEGES;
```

### 4. Cấu hình `.env` hoặc chỉnh sửa `config/settings.py`
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vaccinems_db',
        'USER': 'vaccineuser',
        'PASSWORD': 'yourpassword',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 5. Migrate và tạo superuser
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Chạy server
```bash
python manage.py runserver
```

Truy cập: http://localhost:8000

---

## Phân quyền

| Role | Quyền |
|------|-------|
| `candidate` | Đặt lịch, xem lịch sử, xem hồ sơ (chỉ đọc) |
| `receptionist` | Xem + chỉnh sửa hồ sơ người tiêm, quản lý lịch hẹn |
| `doctor` | Xem + chỉnh sửa + ghi nhận lần tiêm |
| `nurse` | Ghi nhận lần tiêm |
| `admin` | Toàn quyền |

---

## Cấu trúc thư mục

```
vaccinems/
├── config/               # Cấu hình Django
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── accounts/         # Xác thực, User model
│   ├── candidates/       # Hồ sơ người tiêm
│   ├── appointments/     # Lịch hẹn + Trung tâm tiêm
│   ├── vaccines/         # Vaccine + Lịch sử tiêm
│   ├── staff/            # Doctor, Nurse, Receptionist
│   ├── records/          # Hồ sơ y tế
│   └── sales/            # Hóa đơn thanh toán
├── templates/            # HTML templates
│   ├── base/
│   ├── accounts/
│   ├── dashboard/
│   ├── candidates/
│   ├── appointments/
│   ├── vaccines/
│   └── records/
├── static/
│   ├── css/main.css      # Stylesheet chính
│   └── js/main.js
├── manage.py
└── requirements.txt
```

---

## ERD — Tóm tắt quan hệ

- **User** (1) ↔ (1) **Candidate** hoặc **Staff**
- **Candidate** (1) → (N) **Appointment**
- **Appointment** (N) → (1) **VaccinationCenter**
- **VaccinationCenter** (1) → (N) **Staff**
- **Staff** → **Doctor** / **Nurse** / **Receptionist** (kế thừa)
- **Appointment** (1) → (N) **VaccineAdministration**
- **VaccineAdministration** → **Vaccine**, **Doctor**, **Nurse**
- **VaccineAdministration** (1) ↔ (1) **Sale**
- **Candidate** (1) ↔ (1) **MedicalRecord**
- **Vaccine** (N) ↔ (N) **VaccinationCenter** (qua VaccineStock)
