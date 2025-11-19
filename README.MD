@"

# 📞 PhoneBook Management System

[![Python](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Hệ thống quản lý danh bạ điện thoại được phát triển bằng Python với đầy đủ tính năng CRUD, quản lý người dùng và sao lưu dữ liệu.

## ✨ Tính năng nổi bật

### 👤 Cho người dùng thông thường

- ✅ **Đăng ký/Đăng nhập** tài khoản
- ✅ **Thêm, sửa, xóa** liên hệ
- ✅ **Tìm kiếm** liên hệ theo nhiều tiêu chí
- ✅ **Quản lý nhóm** liên hệ
- ✅ **Đánh dấu yêu thích** liên hệ
- ✅ **Xuất/nhập** liên hệ từ file TXT
- ✅ **Cập nhật** hồ sơ người dùng

### 👑 Cho quản trị viên

- ✅ **Quản lý người dùng** (kích hoạt/vô hiệu hóa)
- ✅ **Sao lưu hệ thống**
- ✅ **Xem toàn bộ** dữ liệu

## 🛠 Cài đặt và chạy

### Yêu cầu hệ thống

- Python 3.9+
- Không cần thư viện bên ngoài

### Chạy ứng dụng

\`\`\`bash

# Clone repository

git clone https://github.com/your-username/phonebook-management-system.git
cd phonebook-management-system

# Chạy ứng dụng

python main.py
\`\`\`

### Tài khoản mặc định (Admin)

\`\`\`
Email: admin@system.com
Password: admin123
\`\`\`

## 📁 Cấu trúc dự án

\`\`\`
phonebook-management-system/
├── main.py # Điểm khởi chạy chính
├── models.py # Định nghĩa User và Contact
├── system.py # Logic nghiệp vụ chính
├── ui.py # Giao diện người dùng
├── data/ # Thư mục dữ liệu
├── requirements.txt # Danh sách dependencies
├── contacts_import.txt # File import mẫu
├── task_assignment.md # Phân công công việc
├── tools_evidence.md # Bằng chứng công cụ
└── README.md # Tài liệu này
\`\`\`

## 👥 Thành viên phát triển

| Thành viên        | Công việc chính             |
| ----------------- | --------------------------- |
| Nguyễn Hoàng Tú   | Quản lý liên hệ, Models     |
| Huỳnh An          | Đăng nhập, Đăng ký, UI      |
| Trần Việt Đức     | Xóa liên hệ, Reset password |
| Nguyễn Trí Nguyên | Quản lý người dùng, Backup  |

## 🔧 Công cụ phát triển

- **Python 3.9+** - Ngôn ngữ lập trình
- **VS Code** - Môi trường phát triển
- **Git** - Quản lý phiên bản
- **GitHub** - Lưu trữ mã nguồn
