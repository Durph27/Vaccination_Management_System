# 💉 Trick or Chet — Hệ Thống Quản Lý Tiêm Chủng

Hệ thống quản lý tiêm chủng thông minh **Trick or Chet** được xây dựng trên nền tảng **Django (Python)** và **MySQL**, triển khai đầy đủ quy trình từ đăng ký, khám sàng lọc, tiêm chủng cho đến theo dõi phản ứng sau tiêm và thanh toán hóa đơn.

---

## 🛠️ Công Nghệ Sử Dụng

* **Backend**: Python 3.10 – 3.14+, [Django 4.2](https://www.djangoproject.com/) (Kiến trúc MTV).
* **Database**: [MySQL 8.0+](https://www.mysql.com/) (CSDL quan hệ).
* **Frontend**: HTML5, CSS3 (Vanilla CSS, custom layout Flexbox/Grid), Bootstrap 5 (tích hợp qua `crispy-forms`), Bootstrap Icons, Google Fonts (Outfit & Cormorant Garamond).
* **Tiện ích**: `python-docx` (Xuất báo cáo CSDL dạng Word), `Mermaid` (Vẽ sơ đồ quan hệ trực quan).

---

## 🗂️ Cấu Trúc Thư Mục Dự Án

```
vaccinems/
├── config/                   # Cấu hình dự án Django
│   ├── settings.py           # Cấu hình Database, Apps, Middleware
│   └── urls.py               # Định tuyến URL toàn hệ thống
├── apps/                     # Các ứng dụng thành phần (Apps)
│   ├── accounts/             # Xác thực, phân quyền & Custom User Model
│   ├── candidates/           # Quản lý hồ sơ người tiêm
│   ├── appointments/         # Lịch hẹn tiêm chủng & Trung tâm tiêm
│   ├── vaccines/             # Danh mục vaccine, kho hàng, lượt tiêm thực tế
│   ├── staff/                # Phân hệ nhân sự (Bác sĩ, Y tá, Lễ tân)
│   ├── records/              # Quản lý hồ sơ y tế của bệnh nhân
│   └── sales/                # Quản lý hóa đơn & thanh toán
├── templates/                # Chứa giao diện HTML mẫu
├── static/                   # CSS, JS, hình ảnh tĩnh của hệ thống
├── requirements.txt          # Danh sách các thư viện Python cần thiết
└── manage.py                 # Công cụ dòng lệnh quản trị Django
```

---

## ⚙️ Hướng Dẫn Cài Đặt & Chạy Dự Án

Khi clone hoặc pull dự án về máy, hãy thực hiện tuần tự các bước sau để thiết lập môi trường và chạy chương trình:

### Bước 1: Tạo môi trường ảo (Virtual Environment)
Mở terminal tại thư mục gốc của dự án và chạy các lệnh sau:
```bash
# Tạo môi trường ảo
python -m venv .venv

# Kích hoạt môi trường ảo
# Trên Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Trên Windows (CMD):
.venv\Scripts\activate.bat
# Trên Linux/macOS:
source .venv/bin/activate
```

### Bước 2: Cài đặt các thư viện cần thiết
```bash
pip install -r requirements.txt
```

### Bước 3: Cấu hình Cơ sở dữ liệu MySQL
1. Đăng nhập vào MySQL Server của bạn (qua MySQL CLI hoặc các công cụ giao diện như DBeaver, phpMyAdmin, MySQL Workbench) và chạy lệnh SQL sau để tạo cơ sở dữ liệu mới:
   ```sql
   CREATE DATABASE vaccinems_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
2. Mở tệp tin [config/settings.py](file:///d:/TrickorChet/vaccinems/config/settings.py) và cập nhật thông tin kết nối CSDL tại cấu hình `DATABASES` cho khớp với tài khoản MySQL cục bộ của bạn:
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.mysql',
           'NAME': 'vaccinems_db',
           'USER': 'root',              # User đăng nhập MySQL của bạn
           'PASSWORD': 'your_password',  # Mật khẩu MySQL của bạn
           'HOST': 'localhost',
           'PORT': '3306',
       }
   }
   ```

### Bước 4: Chạy Migrations tạo cấu trúc bảng CSDL
Chạy lệnh sau để Django sinh toàn bộ cấu trúc bảng dữ liệu trong cơ sở dữ liệu MySQL của bạn:
```bash
python manage.py migrate
```

### Bước 5: Tạo tài khoản quản trị tối cao (Django Superuser)
Để có tài khoản đăng nhập vào trang quản trị Django Admin mặc định (`/admin`), hãy tạo một tài khoản Superuser bằng lệnh:
```bash
python manage.py createsuperuser
```
Hệ thống sẽ yêu cầu bạn nhập:
* **Username** (Tên đăng nhập)
* **Email address** (Email liên hệ)
* **Password** và **Password (again)** (Mật khẩu - lưu ý mật khẩu nhập vào sẽ không hiện ký tự trên terminal, chỉ cần nhập chính xác và nhấn Enter)

### Bước 6: Khởi tạo dữ liệu mẫu (Database Seeding)
Dự án được xây dựng kèm một tệp kịch bản `populate.py` giúp tự động tạo sẵn các cơ sở dữ liệu chạy thử (trung tâm tiêm chủng, danh sách vaccine, nhân viên y tế, hồ sơ người tiêm mẫu, lịch hẹn tiêm, lịch sử lần tiêm, hóa đơn bán hàng, v.v.). **Bạn bắt buộc phải chạy lệnh này để hệ thống hoạt động bình thường:**
```bash
python populate.py
```
*Lưu ý:* Kịch bản seeding này cũng tự động tạo một tài khoản quản trị viên tối cao mặc định là: **admin / mật khẩu: admin** (nếu tài khoản này chưa tồn tại trong hệ thống).

### Bước 7: Khởi chạy Máy chủ Thử nghiệm (Development Server)
Khởi động server phát triển bằng lệnh:
```bash
python manage.py runserver
```
Sau đó truy cập ứng dụng thông qua trình duyệt web tại địa chỉ: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 👥 Danh Sách Tài Khoản Thử Nghiệm

Sau khi chạy xong kịch bản dữ liệu mẫu `populate.py`, các tài khoản dưới đây sẽ sẵn sàng để bạn đăng nhập thử nghiệm theo từng phân hệ chức năng:

| Phân hệ (Role) | Tên đăng nhập | Mật khẩu | Chức năng thử nghiệm chính |
| :--- | :--- | :--- | :--- |
| **Quản trị viên (Admin)** | `admin` | `admin` | Xem báo cáo doanh thu, thống kê, quản lý toàn bộ hệ thống |
| **Lễ tân (Receptionist)** | `le_tan_1` | `123456` | Tiếp đón, xác nhận lịch hẹn, chuyển trạng thái "Đang chờ khám" |
| **Bác sĩ (Doctor)** | `bac_si_1` | `123456` | Khám sàng lọc, chỉ định vaccine, chuyển trạng thái "Đang chờ tiêm" |
| **Y tá (Nurse)** | `y_ta_1` | `123456` | Thực hiện tiêm, theo dõi phản ứng sau tiêm, chuyển trạng thái "Chờ thanh toán" |
| **Người tiêm (Candidate)** | `candidate_1` | `123456` | Xem dashboard cá nhân, đặt lịch hẹn, xem lịch sử tiêm, xem hóa đơn |

---

