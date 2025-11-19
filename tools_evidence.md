# BẰNG CHỨNG SỬ DỤNG CÔNG CỤ

## Công cụ phát triển

### 1. Python 3.9+

- **Mục đích**: Ngôn ngữ lập trình chính
- **Bằng chứng**: Codebase sử dụng cú pháp Python 3.9+
- **Tính năng sử dụng**:
  - Type hints
  - f-strings
  - Dataclasses (trong các model)

### 2. Visual Studio Code

- **Mục đích**: IDE phát triển
- **Bằng chứng**: File cấu hình .vscode/ (nếu có)
- **Extension sử dụng**:
  - Python
  - Pylance
  - GitLens

### 3. Git

- **Mục đích**: Quản lý phiên bản
- **Bằng chứng**: Repository với commit history
- **Quy trình**:
  - Feature branches
  - Commit messages có cấu trúc
  - Code review

### 4. Docker

- **Mục đích**: Container hóa ứng dụng
- **Bằng chứng**: Dockerfile trong project
- **Lợi ích**:
  - Môi trường phát triển đồng nhất
  - Dễ dàng triển khai


## Công cụ quản lý dự án

### 1. GitHub Projects

- **Mục đích**: Theo dõi tiến độ công việc
- **Bằng chứng**: Board project với các task được gán

### 2. Discord/Teams

- **Mục đích**: Giao tiếp nhóm
- **Bằng chứng**: Meeting notes và quyết định thiết kế

## Tiêu chuẩn mã nguồn

### 1. PEP 8

- **Áp dụng**: Toàn bộ codebase
- **Kiểm tra**: Sử dụng pylint/flake8

### 2. Docstring

- **Áp dụng**: Tất cả hàm và class
- **Định dạng**: Google style docstrings

## Bằng chứng cụ thể trong code

1. **Type Hints**: Tất cả hàm đều có type hints
2. **Error Handling**: Xử lý lỗi đầy đủ
3. **Modular Design**: Code được chia thành các module rõ ràng
4. **Configuration Management**: Cấu hình tách biệt
5. **Logging**: Ghi log các hoạt động quan trọng
