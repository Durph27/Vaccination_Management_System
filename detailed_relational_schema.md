# 🗄️ Chi Tiết Sơ Đồ Quan Hệ Cơ Sở Dữ Liệu

Tài liệu này miêu tả chi tiết thiết kế cơ sở dữ liệu vật lý (Relational Schema) dựa trên các Django Models hiện tại của hệ thống **Trick or Chet** (Vaccination Management System), dưới dạng các bảng đặc tả chi tiết.

---

## 1. Đặc Tả Chi Tiết Các Bảng (Relational Tables)

### 1.1 Bảng `accounts_user` (Người dùng hệ thống)
*Bảng này kế thừa `AbstractUser` của Django để quản lý tài khoản và phân quyền cho người tiêm và nhân viên.*

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Số nguyên dương tự tăng, định danh duy nhất tài khoản |
| **username** | `VARCHAR(150)` | `UNIQUE`, `NOT NULL` | Tên đăng nhập (1 - 150 ký tự) |
| **password** | `VARCHAR(128)` | `NOT NULL` | Chuỗi ký tự băm mật khẩu |
| **first_name** | `VARCHAR(150)` | `NULL` | Tên (tối đa 150 ký tự) |
| **last_name** | `VARCHAR(150)` | `NULL` | Họ (tối đa 150 ký tự) |
| **email** | `VARCHAR(254)` | `NULL` | Địa chỉ email hợp lệ |
| **role** | `VARCHAR(20)` | `NOT NULL`, `DEFAULT 'candidate'` | Vai trò: `'candidate'`, `'receptionist'`, `'doctor'`, `'nurse'`, `'admin'` |
| **phone** | `VARCHAR(15)` | `NULL` | Số điện thoại liên hệ (10 - 15 ký tự số) |
| **is_staff** | `TINYINT(1)` | `NOT NULL`, `DEFAULT 0` | Trạng thái truy cập admin panel (0: Sai, 1: Đúng) |
| **is_active** | `TINYINT(1)` | `NOT NULL`, `DEFAULT 1` | Trạng thái kích hoạt tài khoản (0: Khóa, 1: Kích hoạt) |
| **is_superuser** | `TINYINT(1)` | `NOT NULL`, `DEFAULT 0` | Quyền tối cao (0: Sai, 1: Đúng) |
| **date_joined** | `DATETIME` | `NOT NULL` | Thời điểm tạo tài khoản |

---

### 1.2 Bảng `candidates_candidate` (Người tiêm / Bệnh nhân)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **candidate_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Số nguyên dương tự tăng, định danh người tiêm |
| **user_id** | `INT` | `FOREIGN KEY` -> `accounts_user(id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với tài khoản đăng nhập |
| **full_name** | `VARCHAR(200)` | `NOT NULL` | Họ và tên người tiêm (tối đa 200 ký tự) |
| **dob** | `DATE` | `NULL` | Ngày sinh (Phải là ngày trong quá khứ) |
| **gender** | `VARCHAR(1)` | `NULL` | Giới tính: `'M'` (Nam), `'F'` (Nữ), `'O'` (Khác) |
| **phone** | `VARCHAR(15)` | `NULL` | Số điện thoại riêng của người tiêm |
| **address** | `TEXT` | `NULL` | Địa chỉ cư trú |
| **created_at** | `DATETIME` | `NOT NULL` | Thời điểm tạo hồ sơ người tiêm |
| **updated_at** | `DATETIME` | `NOT NULL` | Thời điểm cập nhật hồ sơ người tiêm lần cuối |

---

### 1.3 Bảng `records_medicalrecord` (Hồ sơ y tế)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **record_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Số nguyên dương tự tăng, định danh hồ sơ y tế |
| **candidate_id** | `INT` | `FOREIGN KEY` -> `candidates_candidate(candidate_id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với Người tiêm |
| **blood_type** | `VARCHAR(5)` | `NULL` | Nhóm máu: `'A+'`, `'A-'`, `'B+'`, `'B-'`, `'AB+'`, `'AB-'`, `'O+'`, `'O-'` |
| **height** | `DECIMAL(5,2)` | `NULL` | Chiều cao tính bằng cm (Ví dụ: `175.50`, miền giá trị: > 0) |
| **weight** | `DECIMAL(5,2)` | `NULL` | Cân nặng tính bằng kg (Ví dụ: `65.40`, miền giá trị: > 0) |
| **allergies** | `TEXT` | `NULL` | Thông tin dị ứng của bệnh nhân |
| **chronic_diseases** | `TEXT` | `NULL` | Bệnh mãn tính (ví dụ: tiểu đường, huyết áp...) |
| **notes** | `TEXT` | `NULL` | Ghi chú chuẩn đoán chung của bác sĩ |
| **created_at** | `DATETIME` | `NOT NULL` | Thời điểm tạo hồ sơ |
| **updated_at** | `DATETIME` | `NOT NULL` | Thời điểm cập nhật hồ sơ lần cuối |

---

### 1.4 Bảng `appointments_vaccinationcenter` (Trung tâm tiêm chủng)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **center_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất trung tâm tiêm chủng |
| **name** | `VARCHAR(200)` | `NOT NULL` | Tên trung tâm tiêm chủng (Ví dụ: VNVC Hà Đông) |
| **address** | `TEXT` | `NOT NULL` | Địa chỉ chi nhánh |
| **hotline** | `VARCHAR(20)` | `NOT NULL` | Đường dây nóng hỗ trợ (tối đa 20 ký tự số) |
| **created_at** | `DATETIME` | `NOT NULL` | Thời điểm khởi tạo trung tâm trên hệ thống |

---

### 1.5 Bảng `staff_staff` (Nhân viên trung tâm)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **staff_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất nhân viên |
| **user_id** | `INT` | `FOREIGN KEY` -> `accounts_user(id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với tài khoản đăng nhập của nhân viên |
| **center_id** | `INT` | `FOREIGN KEY` -> `appointments_vaccinationcenter(center_id)`, `NULL` | Trung tâm nơi nhân viên đang làm việc |
| **role** | `VARCHAR(20)` | `NOT NULL` | Vai trò công việc: `'doctor'` (Bác sĩ), `'nurse'` (Y tá), `'receptionist'` (Lễ tân) |
| **name** | `VARCHAR(200)` | `NOT NULL` | Họ tên nhân viên |

---

### 1.6 Bảng `staff_doctor` (Bác sĩ - Phân hệ chuyên biệt của Staff)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất của bảng bác sĩ |
| **staff_id** | `INT` | `FOREIGN KEY` -> `staff_staff(staff_id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với thông tin nhân viên chung |
| **specialization** | `VARCHAR(200)` | `NULL` | Lĩnh vực chuyên môn khoa (Ví dụ: Nhi, Nội tổng quát) |
| **license_number** | `VARCHAR(50)` | `NULL` | Số chứng chỉ hành nghề y tế |

---

### 1.7 Bảng `staff_nurse` (Y tá - Phân hệ chuyên biệt của Staff)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất của bảng y tá |
| **staff_id** | `INT` | `FOREIGN KEY` -> `staff_staff(staff_id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với thông tin nhân viên chung |
| **certification** | `VARCHAR(200)` | `NULL` | Chứng chỉ điều dưỡng/tiêm chủng đặc thù |

---

### 1.8 Bảng `staff_receptionist` (Lễ tân - Phân hệ chuyên biệt của Staff)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất của bảng lễ tân |
| **staff_id** | `INT` | `FOREIGN KEY` -> `staff_staff(staff_id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với thông tin nhân viên chung |

---

### 1.9 Bảng `appointments_appointment` (Lịch hẹn tiêm chủng)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **appointment_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất của lịch hẹn |
| **candidate_id** | `INT` | `FOREIGN KEY` -> `candidates_candidate(candidate_id)`, `NOT NULL` | Người tiêm thực hiện đặt lịch |
| **center_id** | `INT` | `FOREIGN KEY` -> `appointments_vaccinationcenter(center_id)`, `NULL` | Trung tâm tiêm chủng được chọn |
| **appointment_date** | `DATE` | `NOT NULL` | Ngày hẹn tiêm (Phải lớn hơn thời điểm hiện tại khi đặt lịch) |
| **appointment_time** | `TIME` | `NOT NULL` | Giờ hẹn tiêm cụ thể |
| **notes** | `TEXT` | `NULL` | Ghi chú hoặc yêu cầu đặc biệt của người tiêm |
| **status** | `VARCHAR(20)` | `NOT NULL`, `DEFAULT 'pending'` | Trạng thái lịch hẹn: `pending`, `confirmed`, `waiting_exam`, `waiting_injection`, `waiting_observation`, `waiting_payment`, `cancelled`, `paid` |
| **created_at** | `DATETIME` | `NOT NULL` | Thời điểm đặt lịch trên hệ thống |

---

### 1.10 Bảng `vaccines_vaccine` (Danh mục Vaccine)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **vaccine_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất loại vaccine |
| **name** | `VARCHAR(200)` | `NOT NULL` | Tên vaccine (Ví dụ: Pfizer-BioNTech, Verocell) |
| **manufacturer** | `VARCHAR(200)` | `NOT NULL` | Tên nhà sản xuất (Ví dụ: Pfizer, Sinopharm) |
| **description** | `TEXT` | `NULL` | Thông tin chi tiết, thành phần hoặc chống chỉ định |
| **target_disease** | `VARCHAR(200)` | `NULL` | Tên bệnh phòng ngừa chính |
| **price** | `DECIMAL(12,2)` | `NOT NULL` | Đơn giá vaccine (Ví dụ: `350000.00` VNĐ, miền giá trị >= 0) |
| **required_doses** | `INT` | `NOT NULL`, `DEFAULT 1` | Số lượng mũi tiêm cơ bản cần thiết (miền giá trị >= 1) |
| **image** | `VARCHAR(100)` | `NULL` | Đường dẫn lưu trữ hình ảnh minh họa |
| **created_at** | `DATETIME` | `NOT NULL` | Ngày tạo bản ghi vaccine |

---

### 1.11 Bảng `vaccines_vaccinestock` (Bảng trung gian quản lý Kho Vaccine tại các Trung tâm)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất dòng kho |
| **vaccine_id** | `INT` | `FOREIGN KEY` -> `vaccines_vaccine(vaccine_id)`, `NOT NULL` | Liên kết đến Vaccine |
| **center_id** | `INT` | `FOREIGN KEY` -> `appointments_vaccinationcenter(center_id)`, `NOT NULL` | Liên kết đến Trung tâm tiêm chủng |
| **quantity** | `INT` | `NOT NULL`, `DEFAULT 0` | Số lượng khả dụng hiện có tại trung tâm (Miền giá trị >= 0) |
| **expiry_date** | `DATE` | `NULL` | Hạn sử dụng của lô vaccine hiện tại |
| *Ràng buộc bổ sung* | `UNIQUE(vaccine_id, center_id)` | Ràng buộc duy nhất | Không cho phép trùng lặp 1 loại vaccine tại cùng 1 trung tâm |

---

### 1.12 Bảng `vaccines_vaccineadministration` (Quá trình khám & tiêm thực tế)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **vaccine_administration_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất của lượt tiêm thực tế |
| **appointment_id** | `INT` | `FOREIGN KEY` -> `appointments_appointment(appointment_id)`, `NOT NULL` | Liên kết đến Lịch hẹn tiêm |
| **vaccine_id** | `INT` | `FOREIGN KEY` -> `vaccines_vaccine(vaccine_id)`, `NOT NULL` | Loại vaccine được chỉ định tiêm |
| **doctor_id** | `INT` | `FOREIGN KEY` -> `staff_doctor(id)`, `NULL` | Bác sĩ thực hiện khám sàng lọc |
| **nurse_id** | `INT` | `FOREIGN KEY` -> `staff_nurse(id)`, `NULL` | Y tá thực hiện tiêm thực tế |
| **immunization_hour** | `DATETIME` | `NULL` | Thời gian tiêm chủng thực tế |
| **dose_number** | `INT` | `NOT NULL`, `DEFAULT 1` | Mũi tiêm thứ mấy (Miền giá trị >= 1) |
| **notes** | `TEXT` | `NULL` | Ghi chú y tế của bác sĩ trong quá trình khám sàng lọc |
| **post_vaccination_status** | `TEXT` | `NULL` | Trạng thái/phản ứng sau tiêm (Y tá theo dõi cập nhật) |

---

### 1.13 Bảng `sales_sale` (Hóa đơn thanh toán)

| Tên trường | Kiểu dữ liệu | Ràng buộc | Miền giá trị / Mô tả |
| :--- | :--- | :--- | :--- |
| **sale_id** | `INT` | `PRIMARY KEY`, `AUTO_INCREMENT` | Định danh duy nhất hóa đơn |
| **vaccine_administration_id** | `INT` | `FOREIGN KEY` -> `vaccines_vaccineadministration(vaccine_administration_id)`, `UNIQUE`, `NOT NULL` | Liên kết 1-1 với lượt tiêm thực tế được thanh toán |
| **total_amount** | `DECIMAL(12,2)` | `NOT NULL` | Tổng tiền hóa đơn (VNĐ, tự động lấy giá trị từ đơn giá vaccine, >= 0) |
| **payment_method** | `VARCHAR(20)` | `NOT NULL` | Phương thức thanh toán: `'cash'` (Tiền mặt), `'bank_transfer'` (Chuyển khoản), `'insurance'` (Bảo hiểm y tế) |
| **status** | `VARCHAR(20)` | `NOT NULL`, `DEFAULT 'pending'` | Trạng thái hóa đơn: `'pending'` (Chờ thanh toán), `'paid'` (Đã thanh toán), `'cancelled'` (Đã hủy) |
| **created_at** | `DATETIME` | `NOT NULL` | Thời điểm lập hóa đơn |
| **paid_at** | `DATETIME` | `NULL` | Thời điểm người tiêm thanh toán thực tế |

---

## 2. Kiểm Tra Sự Khớp Nhau & Đầy Đủ Liên Kết Với Sơ Đồ ERD

Dưới đây là đối chiếu chi tiết giữa **Bản thiết kế vật lý hiện tại trong CSDL** và **Sơ đồ ERD (Thực thể liên kết)** do người dùng cung cấp:

### 2.1 Các thực thể (Entities) và Thuộc tính (Attributes)
* **Khớp hoàn toàn**:
  * Các thực thể chính trong ERD (`Candidate`, `Medical Record`, `Vaccination Center`, `Staff`, `Appointment`, `Vaccine`, `VaccineAdministration`, `Sale`) đều được khai báo đầy đủ thành các bảng vật lý.
  * Các trường khóa chính (PK) như `candidate_id`, `record_id`, `center_id`, `staff_id`, `appointment_id`, `vaccine_id`, `vaccine_administration_id`, `sale_id` khớp tuyệt đối với ERD.
  * Các thuộc tính định lượng chi tiết như `height`, `weight`, `blood` (blood_type) trong `Medical Record` hay `quantity_available` (quantity) và `expiry_date` trong mối quan hệ `stocks` đều được định nghĩa chính xác.
* **Mở rộng thêm**:
  * Hệ thống có thêm bảng `accounts_user` để quản lý thông tin đăng nhập tập trung (`username`, `password`, `email`), liên kết 1-1 với `Candidate` và `Staff`. Điều này tối ưu hóa việc phân quyền trong thực tế và tích hợp bảo mật tài khoản.

---

### 2.2 So Sánh Các Liên Kết (Relationships) & Bản Số (Cardinalities)

| Tên Liên Kết trong ERD | Liên Kết Giữa 2 Thực Thể | Bản Số trên ERD | Cấu Trúc Khai Báo trong CSDL Vật Lý | Đánh Giá Khớp Nhau |
| :--- | :--- | :--- | :--- | :--- |
| **has** | Candidate ↔ Medical Record | `1 - 1` | `MedicalRecord.candidate` là `OneToOneField(Candidate)` (tương đương khóa ngoại có ràng buộc `UNIQUE`). | **Khớp hoàn toàn**. Đảm bảo mỗi bệnh nhân chỉ có 1 hồ sơ y tế. |
| **makes** | Candidate ↔ Appointment | `1 - N` | `Appointment.candidate` là `ForeignKey(Candidate)`. | **Khớp hoàn toàn**. Một người tiêm có thể đặt nhiều lịch hẹn. |
| **hosts** | Vaccination Center ↔ Appointment | `1 - N` | `Appointment.center` là `ForeignKey(VaccinationCenter)`. | **Khớp hoàn toàn**. Trung tâm chứa nhiều lịch hẹn tiêm. |
| **employs** | Vaccination Center ↔ Staff | `1 - N` | `Staff.center` là `ForeignKey(VaccinationCenter)`. | **Khớp hoàn toàn**. Trung tâm quản lý nhiều nhân viên làm việc. |
| **stocks** | Vaccination Center ↔ Vaccine | `N - N` | Bảng trung gian `VaccineStock` chứa `ForeignKey(Vaccine)` và `ForeignKey(VaccinationCenter)`. Chứa thuộc tính mối quan hệ `quantity` và `expiry_date`. | **Khớp hoàn toàn**. Một loại vaccine có thể lưu trữ ở nhiều trung tâm và ngược lại. |
| **is a** | Staff ↔ Doctor / Nurse / Receptionist | `ISA` | Ba bảng con `Doctor`, `Nurse`, `Receptionist` đều liên kết 1-1 (`OneToOneField`) kế thừa khóa từ bảng cha `Staff`. | **Khớp hoàn toàn**. Thiết kế phân lớp (specialization) được hiện thực hóa đúng chuẩn quan hệ 1-1. |
| **generates** | Sale ↔ Vaccine Administration | `1 - 1` | `Sale.vaccine_administration` là `OneToOneField(VaccineAdministration)`. | **Khớp hoàn toàn**. Mỗi lượt tiêm chỉ phát sinh tối đa một hóa đơn thanh toán. |
| **creates** | Receptionist ↔ Appointment | `1 - N` | **Không khai báo**. Bảng `appointments_appointment` không có trường nào tham chiếu đến bảng `Receptionist` hoặc `Staff`. | ⚠️ **Lệch (Thiếu liên kết)**. Cơ sở dữ liệu vật lý hiện tại chưa lưu thông tin lễ tân nào đã lập lịch hẹn này. |
| **executes** | Appointment ↔ Vaccine Administration | `1 - 1` | `VaccineAdministration.appointment` là `ForeignKey(Appointment)`. | ⚠️ **Khác biệt về Logic**. CSDL thiết kế là `N - 1` (Một cuộc hẹn có thể có nhiều lượt tiêm thực tế). Thiết kế này linh hoạt hơn (hỗ trợ tiêm nhiều loại vaccine trong cùng một ngày hẹn) nhưng khác với bản số `1-1` của ERD. |
| **examines** | Doctor ↔ Vaccine Administration | `1 - 1` | `VaccineAdministration.doctor` là `ForeignKey(Doctor)`. | ⚠️ **Khác biệt về Logic**. CSDL là `N - 1` (Một bác sĩ có thể khám sàng lọc cho nhiều lượt tiêm). ERD để `1-1` là chưa hợp lý trong thực tế lâm nghiệp vì một bác sĩ không thể chỉ khám cho 1 lượt tiêm duy nhất trong đời. Bản thiết kế CSDL thực tế là tối ưu hơn. |
| **injects** | Nurse ↔ Vaccine Administration | `1 - 1` | `VaccineAdministration.nurse` là `ForeignKey(Nurse)`. | ⚠️ **Khác biệt về Logic**. CSDL là `N - 1` (Một y tá thực hiện tiêm cho nhiều lượt tiêm). ERD để `1-1` tương tự như trường hợp Bác sĩ, CSDL thực tế đã sửa lỗi logic này để tối ưu vận hành. |
| **assigned to** | Vaccine ↔ Vaccine Administration | `N - 1` | `VaccineAdministration.vaccine` là `ForeignKey(Vaccine)`. | ⚠️ **Khác biệt bản số**. Trên sơ đồ ERD ký hiệu `N` ở phía Vaccine và `1` ở phía VaccineAdministration (nghĩa là một vaccine chỉ tiêm cho 1 lượt tiêm, 1 lượt tiêm tiêm nhiều vaccine). Trong thực tế và CSDL, liên kết này ngược lại: Mỗi lượt tiêm tiêm 1 loại vaccine cụ thể (`ForeignKey`), và 1 loại vaccine có thể được sử dụng trong nhiều lượt tiêm khác nhau. Bảng CSDL hiện tại là đúng đắn về mặt nghiệp vụ y tế. |

---

## 3. Tổng Kết Đánh Giá

1. **Về độ đầy đủ các thực thể**: Hệ thống CSDL thực tế đã ánh xạ **đầy đủ 100% các thực thể** từ sơ đồ ERD, đồng thời bổ sung thêm phân hệ Tài khoản đăng nhập (`User`) giúp liên kết nghiệp vụ với người dùng thực tế.
2. **Về các điểm thiếu sót / khác biệt cần lưu ý**:
   * **Thiếu liên kết `creates` (Lễ tân - Lịch hẹn)**: Bảng `Appointment` chưa lưu thông tin nhân viên lễ tân tạo lịch. Nếu nghiệp vụ yêu cầu kiểm toán người tạo lịch hẹn, cần thêm trường `created_by_id` (FK tham chiếu đến `Receptionist` hoặc `Staff`) vào bảng `Appointment`.
   * **Chuẩn hóa quan hệ từ 1-1 sang N-1**: Các mối quan hệ `executes` (lịch hẹn - lượt tiêm), `examines` (bác sĩ - lượt tiêm), `injects` (y tá - lượt tiêm) trên ERD đang để là `1-1`, nhưng trong CSDL thực tế đã chuyển sang `N-1`. Đây là **sự điều chỉnh đúng đắn** để một nhân viên (Bác sĩ, Y tá) có thể thực hiện công việc nhiều lần, tránh việc khóa cứng dữ liệu chỉ cho phép thực hiện 1 lần duy nhất.
   * **Sửa lỗi đảo ngược bản số**: Liên kết `assigned to` giữa `Vaccine` và `VaccineAdministration` bị ký hiệu ngược chiều trên ERD (`Vaccine N - 1 Administration`), CSDL thực tế đã đảo lại chuẩn xác (`Administration N - 1 Vaccine`).
