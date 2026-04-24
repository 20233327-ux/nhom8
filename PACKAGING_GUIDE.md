# 📦 Hướng dẫn Đóng gói Ứng dụng

## Các phương pháp đóng gói

### Phương pháp 1: Docker Container (Khuyến nghị) ⭐
Phù hợp nhất cho deployment trên server, cloud platforms.

#### Yêu cầu:
- Docker Desktop (https://www.docker.com/products/docker-desktop)

#### Bước 1: Tạo Dockerfile
Xem file `Dockerfile` trong thư mục gốc.

#### Bước 2: Tạo .dockerignore
```
.git
.gitignore
__pycache__
*.pyc
*.pyo
*.pyd
.Python
env/
.venv
venv/
.env
.env.local
*.egg-info/
dist/
build/
.pytest_cache/
.coverage
htmlcov/
```

#### Bước 3: Build Docker image
```bash
# Build image
docker build -t abc-document-app:latest .

# Chạy container
docker run -p 8000:8000 abc-document-app:latest
```

#### Bước 4: Push lên Docker Hub (tùy chọn)
```bash
# Login to Docker Hub
docker login

# Tag image
docker tag abc-document-app:latest your-username/abc-document-app:latest

# Push
docker push your-username/abc-document-app:latest
```

---

### Phương pháp 2: Executable Launcher (Đơn giản) ⭐⭐
Tạo file .exe để chạy ứng dụng trên Windows dễ dàng.

#### Yêu cầu:
```bash
pip install pyinstaller
```

#### Bước 1: Tạo launcher script
Xem file `run_app.py` và `app_launcher.py`

#### Bước 2: Tạo executable
```bash
# Basic
pyinstaller --onefile --windowed app_launcher.py

# Advanced (với icon)
pyinstaller --onefile --windowed --icon=app_icon.ico app_launcher.py
```

#### Kết quả:
File `.exe` sẽ nằm trong thư mục `dist/`

---

### Phương pháp 3: Standalone Python Package
Đóng gói thành package để phân phối trên PyPI.

#### Bước 1: Tạo setup.py
Xem file `setup.py`

#### Bước 2: Build package
```bash
python setup.py sdist bdist_wheel
```

#### Bước 3: Upload lên PyPI
```bash
pip install twine
twine upload dist/*
```

---

### Phương pháp 4: Cloud Deployment

#### A) Deploy lên Heroku
```bash
# Tạo Procfile
echo "web: gunicorn abc_core.wsgi" > Procfile

# Tạo requirements.txt (đã có)
# Tạo runtime.txt
echo "python-3.11.0" > runtime.txt

# Push code
git init
git add .
git commit -m "Deploy to Heroku"
heroku create your-app-name
git push heroku main
```

#### B) Deploy lên Railway, Render, PythonAnywhere
Tương tự - chỉ cần cung cấp `requirements.txt` và chỉ định command `gunicorn`

---

## 📋 Các file cần chuẩn bị

1. **Dockerfile** - Container image
2. **docker-compose.yml** - Orchestration
3. **.dockerignore** - Files để bỏ qua
4. **app_launcher.py** - Launcher script
5. **setup.py** - Package metadata
6. **requirements.txt** - Dependencies (đã có ✓)

---

## ⚡ Quick Start - Khuyến nghị

### Nếu muốn chạy nhanh trên máy local:
```bash
# 1. Activate venv
.venv\Scripts\activate

# 2. Chạy:
python run_app.py
```

### Nếu muốn deploy trên server:
```bash
# Use Docker
docker build -t abc-app .
docker run -p 8000:8000 abc-app
```

### Nếu muốn tạo .exe cho Windows:
```bash
# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --onefile --windowed app_launcher.py

# Executable nằm tại: dist/app_launcher.exe
```

---

## 🔐 Chuẩn bị Security

Trước khi deploy, hãy:

1. **Tạo file `.env`** với biến môi trường:
```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,your-domain.com
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
```

2. **Disable DEBUG trên production**:
   - Sửa `abc_core/settings.py`: `DEBUG = False`

3. **Generate SECRET_KEY mới**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4. **Chạy collecstatic**:
```bash
python manage.py collectstatic --noinput
```

---

## 🐳 Chi tiết Docker Setup

Docker là cách tốt nhất để đóng gói vì:
- ✅ Chạy được trên bất kỳ máy nào
- ✅ Quản lý dependencies tập trung
- ✅ Dễ scale và update
- ✅ Production-ready

Xem file `Dockerfile` và `docker-compose.yml` trong folder gốc.

---

## 📞 Troubleshooting

**Lỗi port 8000 đã được sử dụng:**
```bash
# Chạy trên port khác
python manage.py runserver 0.0.0.0:3000
```

**Django migrations lỗi:**
```bash
python manage.py migrate --noinput
python manage.py migrate vn_docs
python manage.py migrate vn_users
python manage.py migrate vn_workflow
python manage.py migrate workflow
```

**Celery/Redis issues:**
```bash
# Start Redis (nếu dùng Docker)
docker run -d -p 6379:6379 redis:latest

# Hoặc dùng Redis trên local (Windows)
# Download từ: https://github.com/microsoftarchive/redis/releases
```
