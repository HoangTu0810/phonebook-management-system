# PHÂN CÔNG CÔNG VIỆC - NHÓM 8

## Thành viên và nhiệm vụ

### 1. NGUYỄN HOÀNG TÚ

- **Chức năng**: Quản lý liên hệ cơ bản
- **Công việc**:
  - Class Diagram thiết kế (Giả định)
  - Implement **class User** và **class Contact** (`models.py`)
  - Implement chức năng **Thêm liên hệ** (`PhoneBookSystem.add_contact` & `PhoneBookUI.add_contact`)
  - Implement chức năng **Sửa liên hệ** (`PhoneBookSystem.edit_contact` & `PhoneBookUI.edit_contact`)
  - Implement chức năng **Quản lý nhóm liên hệ** (Filter theo Group trong `PhoneBookSystem.get_contacts_by_group`)
  - Implement chức năng **Đánh dấu/Bỏ đánh dấu liên hệ yêu thích** (Thông qua `Contact.mark_as_favorite`, `Contact.unmark_favorite`, và giao diện `PhoneBookUI.favorite_contacts`)
  - Implement chức năng **Cập nhật hồ sơ người dùng** (`User.update_profile` & `PhoneBookUI.update_profile`)
  - Implement chức năng **Đăng xuất** (`PhoneBookSystem.logout` & `PhoneBookUI.main_menu`)

---

### 2. HUỲNH AN

- **Chức năng**: Đăng ký, đăng nhập, tìm kiếm
- **Công việc**:
  - Use-case Diagram (Giả định)
  - Implement chức năng **Đăng ký tài khoản** (`PhoneBookSystem.register_user` & `PhoneBookUI.register`)
  - Implement chức năng **Đăng nhập** (`PhoneBookSystem.login` & `PhoneBookUI.login`)
  - Implement chức năng **Tìm kiếm liên hệ** (`PhoneBookSystem.search_contacts` & `PhoneBookUI.search_contacts`)
  - Xây dựng **giao diện người dùng (UI)** và **logic điều hướng** cơ bản của hệ thống (`ui.py`)

---

### 3. TRẦN VIỆT ĐỨC

- **Chức năng**: Xóa liên hệ, đặt lại mật khẩu, xuất liên hệ
- **Công việc**:
  - Database Schema (Giả định)
  - Implement chức năng **Xóa liên hệ** (`PhoneBookSystem.delete_contact` & `PhoneBookUI.delete_contact`)
  - Implement chức năng **Đặt lại mật khẩu** (`PhoneBookSystem.request_password_reset`, `PhoneBookSystem.reset_password`, `PhoneBookSystem.validate_reset_token` & giao diện `PhoneBookUI.forgot_password`)
  - Implement chức năng **Xuất liên hệ (CSV)** (`PhoneBookSystem.export_contacts_to_csv` & `PhoneBookUI.import_export_menu`)
  - Implement các phương thức **tải/lưu dữ liệu** cho Users/Contacts (`PhoneBookSystem._load_users`, `_load_contacts`, `_save_users`, `_save_contacts`)

---

### 4. NGUYỄN TRÍ NGUYÊN

- **Chức năng**: Quản lý người dùng, sao lưu hệ thống, nhập liên hệ
- **Công việc**:
  - Non-functional Requirements (Giả định)
  - Data Flow Diagram (Giả định)
  - Implement chức năng **Quản lý người dùng (Admin)** (`PhoneBookSystem.get_all_users`, `PhoneBookSystem.deactivate_user`, `PhoneBookSystem.activate_user` & `PhoneBookUI.user_management`)
  - Implement chức năng **Sao lưu hệ thống** (`PhoneBookSystem.backup_data` & `PhoneBookUI.system_backup`)
  - Implement chức năng **Nhập liên hệ (CSV)** (`PhoneBookSystem.import_contacts_from_csv` & `PhoneBookUI.import_export_menu`)
  - Xây dựng **lớp chính của hệ thống** và quản lý dữ liệu (`PhoneBookSystem.__init__`)

## Tiến độ thực hiện

- ✅ Phân tích yêu cầu và thiết kế hệ thống
- ✅ Implement các chức năng cốt lõi
- ✅ Testing và debug
- ✅ Tài liệu hóa và đóng gói
