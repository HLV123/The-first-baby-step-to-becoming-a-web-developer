# Tập tành làm web python với bước chập chững đầu tiên : Hệ thống Đăng nhập Sinh viên

Web Flask cho phép đăng ký tài khoản, đăng nhập và quản lý thông tin cá nhân an toàn.

## ✨ Tính năng chính



- 🔐 \*\*Xác thực người dùng\*\*: Đăng ký và đăng nhập với JWT

- 🛡️ \*\*Bảo mật cao\*\*: Mã hóa mật khẩu với bcrypt

- 📱 \*\*Giao diện responsive\*\*: Thiết kế đẹp mắt với Bootstrap 5

- ⚡ \*\*Rate limiting\*\*: Giới hạn số lần thử đăng nhập/đăng ký

- 🔄 \*\*Đổi mật khẩu\*\*: Tính năng thay đổi mật khẩu an toàn

- 📧 \*\*Quên mật khẩu\*\*: Tính năng khôi phục mật khẩu (demo)

- 📊 \*\*Dashboard cá nhân\*\*: Hiển thị thông tin người dùng

## 🛠️ Công nghệ sử dụng



- \*\*Backend\*\*: Python Flask

- \*\*Database\*\*: SQLite với SQLAlchemy ORM

- \*\*Authentication\*\*: JWT (JSON Web Tokens)

- \*\*Password Hashing\*\*: Flask-Bcrypt

- \*\*Frontend\*\*: HTML5, CSS3, JavaScript, Bootstrap 5

- \*\*Rate Limiting\*\*: Flask-Limiter

- \*\*Email Validation\*\*: email-validator


## 📋 Yêu cầu hệ thống

- Python 3.7 trở lên

- pip (Python package installer)

```bash

pip install -r requirements.txt

```

```bash

python app.py

```

Ứng dụng sẽ chạy tại: `http://localhost:5000`

## 📁 Cấu trúc thư mục

```

student-login-system/

│
├── app.py                 # File chính của ứng dụng Flask
├── auth.py               # Module xử lý JWT authentication
├── models.py             # Model cơ sở dữ liệu
├── requirements.txt      # Danh sách dependencies
│
├── static/
│   └── style.css         # File CSS tùy chỉnh
│
└── templates/
    ├── index.html        # Trang chủ
    ├── login.html        # Trang đăng nhập
    ├── register.html     # Trang đăng ký
    └── dashboard.html    # Trang dashboard cá nhân

```

## 🎯 API Endpoints

### Trang web

- `GET /` - Trang chủ
- `GET /login` - Trang đăng nhập  
- `GET /register` - Trang đăng ký
- `GET /dashboard` - Trang dashboard (yêu cầu đăng nhập)



### API Routes

- `POST /api/register` - Đăng ký tài khoản mới
- `POST /api/login` - Đăng nhập
- `GET /api/dashboard` - Lấy thông tin dashboard (bảo vệ)
- `POST /api/change\_password` - Đổi mật khẩu (bảo vệ)
- `POST /api/forgot\_password` - Quên mật khẩu (demo)

## 💾 Cơ sở dữ liệu

Ứng dụng sử dụng SQLite với bảng `users`:

```sql

CREATE TABLE users (

&nbsp;   id INTEGER PRIMARY KEY,

&nbsp;   email VARCHAR(120) UNIQUE NOT NULL,

&nbsp;   password\_hash VARCHAR(128) NOT NULL,

&nbsp;   full\_name VARCHAR(120) NOT NULL,

&nbsp;   created\_at DATETIME DEFAULT CURRENT\_TIMESTAMP,

&nbsp;   last\_login DATETIME

);

```

## 🎨 Giao diện người dùng
- \*\*Responsive Design\*\*: Tương thích mọi thiết bị
- \*\*Modern UI\*\*: Sử dụng Bootstrap 5 với custom CSS
- \*\*Animations\*\*: Hiệu ứng hover và transition mượt mà
- \*\*Vietnamese Language\*\*: Giao diện hoàn toàn bằng tiếng Việt


### Version 1.0.0
- ✅ Đăng ký và đăng nhập người dùng
- ✅ JWT authentication
- ✅ Dashboard cá nhân
- ✅ Đổi mật khẩu
- ✅ Giao diện responsive
- ✅ Rate limiting
- ✅ Validation form





