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

Dưới đây là đối chiếu chi tiết giữa **Bản thiết kế vật lý hiện tại trong CSDL** và **Sơ đồ ERD (Thực thể liên kết)** đã được bạn cập nhật:

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
| **creates** | Receptionist ↔ Appointment | `1 - N` | **Không khai báo**. Bảng `appointments_appointment` không có trường nào tham chiếu đến bảng `Receptionist` hay `Staff`. | ⚠️ **Khác biệt (Hành vi vs Lưu trữ)**. Xem phân tích chi tiết ở Mục 3 về việc có cần thiết kế khóa ngoại trong CSDL hay không. |
| **executes** | Appointment ↔ Vaccine Administration | `1 - 1` | `VaccineAdministration.appointment` là `ForeignKey(Appointment)` (tương đương `N - 1`). | ⚠️ **Khác biệt**. Trên ERD đã cập nhật là `1 - 1` (Một cuộc hẹn chỉ tạo ra đúng 1 lượt tiêm). Tuy nhiên, CSDL vật lý hiện tại đang là `N - 1`. Cần đổi khóa ngoại này thành `OneToOneField` trong code để khớp hoàn toàn với ERD mới. |
| **examines** | Doctor ↔ Vaccine Administration | `1 - N` | `VaccineAdministration.doctor` là `ForeignKey(Doctor)`. | **Khớp hoàn toàn** (sau khi bạn sửa ERD về `1 - N`). Một bác sĩ khám sàng lọc cho nhiều lượt tiêm. |
| **injects** | Nurse ↔ Vaccine Administration | `1 - N` | `VaccineAdministration.nurse` là `ForeignKey(Nurse)`. | **Khớp hoàn toàn** (sau khi bạn sửa ERD về `1 - N`). Một y tá thực hiện tiêm cho nhiều lượt tiêm. |
| **assigned to** | Vaccine ↔ Vaccine Administration | `N - N` | `VaccineAdministration.vaccine` là `ForeignKey(Vaccine)` (tương đương `N - 1`). | ⚠️ **Khác biệt**. Trên ERD đã cập nhật là `N - N` (Một lượt tiêm có thể tiêm nhiều vaccine, và một vaccine có thể dùng trong nhiều lượt tiêm). Để khớp với ERD này, CSDL cần loại bỏ trường `vaccine` trong `VaccineAdministration` và thay bằng bảng trung gian Many-to-Many. |

---

## 3. Tổng Kết Đánh Giá & Giải Quyết Câu Hỏi Thiết Kế

### 3.1 Về mối quan hệ `creates` (Receptionist ↔ Appointment)
Khi lễ tân tạo lịch hẹn (Appointment) cho khách vãng lai, việc **có cần thiết kế mối quan hệ `creates` trong CSDL hay không** phụ thuộc vào yêu cầu quản lý và đối soát:

* **Trường hợp 1: KHÔNG CẦN thiết kế mối quan hệ (Không thêm FK vào CSDL)**
  * *Lý do*: Lễ tân chỉ đóng vai trò là tác nhân (Actor) thực hiện thao tác trên hệ thống (insert dữ liệu vào bảng `Appointment`). Bản thân dữ liệu lịch hẹn chỉ cần quan tâm "Lịch hẹn này của bệnh nhân nào, tại trung tâm nào" mà không cần quan tâm "Lễ tân nào đã bấm nút tạo".
  * *Ưu điểm*: CSDL đơn giản hơn, không cần lưu trữ thông tin thừa nếu không có nhu cầu đối soát. Khách tự đặt online hay lễ tân đặt hộ thì dòng dữ liệu `Appointment` vẫn đồng nhất.
* **Trường hợp 2: CÓ CẦN thiết kế mối quan hệ (Thêm khóa ngoại `created_by` tham chiếu đến `Staff` hoặc `Receptionist`)**
  * *Lý do*: Hệ thống cần ghi nhận vết lịch sử (Audit Log / History) để biết ai là người đã lên lịch hẹn đó nhằm mục đích đối soát lỗi, tính chỉ số KPI hiệu suất làm việc của nhân viên lễ tân.
  * *Cách thiết kế*: Thêm trường `created_by` (cho phép nhận giá trị `NULL` vì nếu khách tự đăng ký online thì trường này sẽ trống).

> [!TIP]
> **Khuyến nghị**: Nếu hệ thống của bạn là một đồ án hoặc ứng dụng quản lý cơ bản không yêu cầu chấm công/đối soát KPI của lễ tân, bạn **không cần thiết kế mối quan hệ này trong CSDL vật lý**. Việc phân quyền hành động sẽ được kiểm soát ở tầng logic ứng dụng (Backend Code) thay vì ràng buộc ở tầng CSDL.

### 3.2 Vấn đề `executes` (1 - 1) và `assigned to` (N - N)
Với các sửa đổi mới nhất trên sơ đồ ERD của bạn:
1. **`executes` là 1 - 1**: Điều này hoàn toàn hợp lý với nghiệp vụ thực tế (Một buổi hẹn đến tiêm chỉ tương ứng với một phiên tiêm chủng duy nhất, y tá chỉ xác nhận giờ tiêm và trạng thái sau tiêm một lần cho cả buổi). Trong CSDL Django hiện tại, trường `appointment` trong `VaccineAdministration` đang là `ForeignKey` (N-1). Để đúng với sơ đồ ERD mới, ta cần chuyển nó thành `OneToOneField`.
2. **`assigned to` là N - N**: Do một lượt tiêm có thể tiêm nhiều loại vaccine cùng lúc. Trong CSDL Django hiện tại, `VaccineAdministration` chỉ có một khóa ngoại `vaccine_id` (chỉ tiêm được 1 loại vaccine). Để đúng với ERD mới, ta cần cấu trúc lại mối quan hệ Many-to-Many giữa `Vaccine` và `VaccineAdministration` thông qua một bảng trung gian.
