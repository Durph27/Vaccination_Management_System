# 🗄️ Sơ đồ Quan hệ Cơ sở Dữ liệu (Chỉ gồm PK, FK)

Dưới đây là sơ đồ quan hệ dạng thực thể liên kết (ER Diagram) thể hiện **chỉ các khóa chính (PK) và khóa ngoại (FK)** của các bảng trong cơ sở dữ liệu sau khi đã được cập nhật chính xác theo yêu cầu nghiệp vụ:

```mermaid
erDiagram
    accounts_user {
        int id PK
    }
    candidates_candidate {
        int candidate_id PK
        int user_id FK
    }
    records_medicalrecord {
        int record_id PK
        int candidate_id FK
    }
    appointments_vaccinationcenter {
        int center_id PK
    }
    staff_staff {
        int staff_id PK
        int user_id FK
        int center_id FK
    }
    staff_doctor {
        int id PK
        int staff_id FK
    }
    staff_nurse {
        int id PK
        int staff_id FK
    }
    staff_receptionist {
        int id PK
        int staff_id FK
    }
    appointments_appointment {
        int appointment_id PK
        int candidate_id FK
        int center_id FK
        int created_by_id FK
    }
    vaccines_vaccine {
        int vaccine_id PK
    }
    vaccines_vaccinestock {
        int id PK
        int vaccine_id FK
        int center_id FK
    }
    vaccines_vaccineadministration {
        int vaccine_administration_id PK
        int appointment_id FK
        int doctor_id FK
        int nurse_id FK
    }
    vaccines_vaccineadministration_vaccines {
        int id PK
        int vaccineadministration_id FK
        int vaccine_id FK
    }
    sales_sale {
        int sale_id PK
        int vaccine_administration_id FK
    }

    accounts_user ||--|| candidates_candidate : "1:1 user_id"
    accounts_user ||--|| staff_staff : "1:1 user_id"
    appointments_vaccinationcenter ||--o{ staff_staff : "1:N center_id"
    candidates_candidate ||--|| records_medicalrecord : "1:1 candidate_id"
    candidates_candidate ||--o{ appointments_appointment : "1:N candidate_id"
    appointments_vaccinationcenter ||--o{ appointments_appointment : "1:N center_id"
    staff_receptionist ||--o{ appointments_appointment : "1:N created_by_id"
    staff_staff ||--|| staff_doctor : "1:1 staff_id"
    staff_staff ||--|| staff_nurse : "1:1 staff_id"
    staff_staff ||--|| staff_receptionist : "1:1 staff_id"
    appointments_appointment ||--|| vaccines_vaccineadministration : "1:1 appointment_id"
    staff_doctor ||--o{ vaccines_vaccineadministration : "1:N doctor_id"
    staff_nurse ||--o{ vaccines_vaccineadministration : "1:N nurse_id"
    vaccines_vaccine ||--o{ vaccines_vaccinestock : "1:N vaccine_id"
    appointments_vaccinationcenter ||--o{ vaccines_vaccinestock : "1:N center_id"
    vaccines_vaccineadministration ||--o{ vaccines_vaccineadministration_vaccines : "1:N vaccineadministration_id"
    vaccines_vaccine ||--o{ vaccines_vaccineadministration_vaccines : "1:N vaccine_id"
    vaccines_vaccineadministration ||--|| sales_sale : "1:1 vaccine_administration_id"
```

---

## 🔑 Hướng dẫn Import vào Draw.io
Để đưa sơ đồ này vào phần mềm Draw.io:
1. Sao chép đoạn mã nguồn Mermaid ở trên (từ dòng `erDiagram` đến hết).
2. Truy cập [draw.io](https://app.diagrams.net/).
3. Trên thanh công cụ của Draw.io, chọn **Arrange** (Sắp xếp) -> **Insert** (Chèn) -> **Advanced** (Nâng cao) -> **Mermaid...**.
4. Dán đoạn mã Mermaid vào khung nhập liệu và nhấn **Insert** (Chèn). Draw.io sẽ tự động dựng thành sơ đồ hình học hoàn chỉnh cho bạn!
