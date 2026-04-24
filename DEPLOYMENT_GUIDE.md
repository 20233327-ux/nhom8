# 🚀 Deployment Guide - ABC Document Management System

## Quick Start (5 minutes)

### 1. Environment Setup
```bash
# Go to project directory
cd c:\Users\duy\Downloads\python

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser
# Username: admin
# Email: admin@abc.com
# Password: (enter your password)
```

### 3. Run Development Server
```bash
# Start server
python manage.py runserver

# Server will run at http://127.0.0.1:8000/
```

### 4. Access the System
```
Login Page:      http://127.0.0.1:8000/auth/login/
Admin Panel:     http://127.0.0.1:8000/admin/
Documentation:   See *.md files in project root
```

---

## Default Credentials

### Superuser (built-in)
- Username: `admin`
- Password: (from createsuperuser step)
- Access: Full system access

### Test Users (create via admin or shell)
```python
# Run: python manage.py shell

from django.contrib.auth import get_user_model
User = get_user_model()

# Staff user
User.objects.create_user(
    username='staff1',
    email='staff@abc.com',
    password='test123',
    role='staff'
)

# Manager user
User.objects.create_user(
    username='manager1',
    email='manager@abc.com',
    password='test123',
    role='manager'
)

# Clerk user
User.objects.create_user(
    username='clerk1',
    email='clerk@abc.com',
    password='test123',
    role='clerk'
)
```

---

## Project Structure

```
📦 Project Root
│
├── 📂 abc_core/               # Django project config
│   ├── settings.py            # Main Django settings
│   ├── urls.py                # URL routing
│   ├── wsgi.py                # WSGI config
│   ├── celery.py              # Celery config
│   └── __init__.py
│
├── 📂 apps/                   # Django applications
│   ├── vn_users/              # User management
│   │   ├── models.py          # User, Department models
│   │   ├── views.py           # Auth views + dashboards
│   │   ├── urls.py            # Auth routing
│   │   ├── admin.py           # Admin customization
│   │   └── migrations/        # Database migrations
│   │
│   ├── vn_docs/               # Document management
│   │   ├── models.py          # Document model
│   │   ├── views.py           # Dashboard view
│   │   ├── tasks.py           # OCR tasks
│   │   ├── signals.py         # Post-save signals
│   │   ├── signature_utils.py # Digital signatures
│   │   ├── admin.py           # Admin customization
│   │   └── migrations/        # Database migrations
│   │
│   └── vn_workflow/           # Workflow management
│       ├── models.py          # Workflow models
│       ├── admin.py           # Admin customization
│       └── migrations/        # Database migrations
│
├── 📂 templates/              # HTML templates
│   ├── base.html              # Base template
│   ├── 403.html               # Error page
│   ├── auth/
│   │   └── login.html         # Login form
│   └── dashboard/
│       ├── staff.html         # Staff dashboard
│       ├── manager.html       # Manager dashboard
│       └── admin.html         # Admin dashboard
│
├── 📂 static/                 # Static files (CSS, JS, images)
├── 📂 media/                  # Uploaded files
│
├── manage.py                  # Django management
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database
│
└── 📚 Documentation/
    ├── README.md              # Overview
    ├── HUONG_DAN_NHANH.md     # Quick start
    ├── TONG_QUAN_HE_THONG.md  # Architecture
    ├── PHAN_TICH_TANG_DU_LIEU.md # Data analysis
    ├── HUONG_DAN_XU_LY_CONG_VAN.md # User guide
    ├── TONG_KET_HE_THONG.md   # Summary
    └── DANH_SACH_KIEM_TRA.md  # Checklist
```

---

## Key Features

### 1. User Management
- 4 roles: Admin, Manager, Clerk, Staff
- Department-based organization
- Role-based access control
- Secure password hashing

### 2. Document Processing
- 3 document types: IN (Đến), OUT (Đi), INT (Nội bộ)
- Automatic OCR extraction
- File attachment support
- Document metadata tracking

### 3. Workflow Engine
- Multi-step approval workflows
- Customizable approval steps
- Approval history tracking
- Comments and notes

### 4. Dashboard
- Role-specific views
- Real-time statistics
- Document tracking
- Approval management

---

## Operating the System

### Creating Documents
1. Login as Admin or Clerk
2. Go to Admin Panel → Documents → Add Document
3. Fill in:
   - Document number
   - Title/Summary
   - Document type (IN/OUT/INT)
   - Upload file (image/PDF)
4. Click Save
5. OCR processes automatically

### Approving Documents
1. Login as Manager/Leader
2. Go to Dashboard → Approval Tasks
3. View documents waiting for approval
4. Click "Approve" button
5. Add comments if needed
6. Submit approval

### Viewing Statistics
1. Login as Admin
2. Go to Admin Dashboard
3. View system statistics
4. See recent users and documents

---

## Common Tasks

### Add New User
```bash
# Via Admin Panel
1. Login as Admin
2. Go to Users → Add User
3. Fill form and Save

# Via Command Line
python manage.py createsuperuser
```

### Create Workflow
```
1. Login as Admin → Admin Dashboard
2. Go to Workflow Definitions → Add
3. Fill workflow name and description
4. Add steps and assign approval roles
5. Save workflow
```

### View Audit Trail
```
1. Admin Dashboard
2. Go to Approval Histories
3. Filter by document or user
4. View all approval actions
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: Port 8000 already in use
**Solution:**
```bash
python manage.py runserver 8001
```

### Issue: Database errors
**Solution:**
```bash
python manage.py migrate --run-syncdb
```

### Issue: Template not found
**Solution:**
```
Check templates/ folder exists in project root
```

### Issue: Static files not loading
**Solution:**
```bash
python manage.py collectstatic --noinput
```

---

## Performance Tips

### For Better Performance
1. Use PostgreSQL instead of SQLite (production)
2. Enable Redis caching
3. Run Celery workers for OCR
4. Use Nginx as reverse proxy
5. Enable database connection pooling

### Optimization Commands
```bash
# Optimize database
python manage.py dbshell
VACUUM;

# Check system status
python manage.py check

# Monitor Celery tasks
celery -A abc_core worker --loglevel=info
```

---

## Backing Up Data

### Backup Database
```bash
# SQLite
copy db.sqlite3 db.sqlite3.backup

# PostgreSQL (if used)
pg_dump -U postgres databasename > backup.sql
```

### Backup Media Files
```bash
# Windows
xcopy media media.backup /E /I

# Linux/Mac
cp -r media media.backup
```

---

## Scaling for Production

### Recommended Setup
```
Client
  ↓
Nginx (Reverse Proxy) - Load Balancer
  ↓
Gunicorn/uWSGI (App Servers) - Multiple instances
  ↓
PostgreSQL (Database) - Primary + Replicas
Redis (Cache) - Cluster
Celery Workers - Pool
```

### Steps to Deploy
1. Use Docker for containerization
2. Set up nginx configuration
3. Configure PostgreSQL database
4. Set up Redis cache
5. Configure Celery workers
6. Enable SSL/TLS
7. Set up monitoring

---

## Maintenance

### Regular Tasks
- **Daily**: Check error logs
- **Weekly**: Verify database consistency
- **Monthly**: Optimize database, check backups
- **Quarterly**: Review security settings
- **Yearly**: Performance audit, dependency updates

### Monitoring
```bash
# Check Django status
python manage.py check

# Monitor logs
tail -f logs/django.log

# Monitor Celery
celery -A abc_core events
```

---

## Support Resources

### Documentation Files
- **README.md** - Project overview
- **HUONG_DAN_NHANH.md** - Quick start guide
- **TONG_QUAN_HE_THONG.md** - System architecture
- **DANH_SACH_KIEM_TRA.md** - Complete checklist

### Getting Help
1. Check documentation files first
2. Review Django error messages
3. Check logs: `python manage.py runserver` output
4. Contact development team

---

## Checklist Before Going Live

- [ ] Database migrated successfully
- [ ] Superuser created
- [ ] Test users created
- [ ] All templates load without errors
- [ ] Login works for all roles
- [ ] Dashboards display correctly
- [ ] Document upload works
- [ ] OCR processes correctly
- [ ] Approval workflow tested
- [ ] Admin panel functional
- [ ] Error pages configured
- [ ] SSL/TLS certificates (production)
- [ ] Backups configured
- [ ] Monitoring enabled

---

## Final Notes

✅ **System is ready for:**
- Development and testing
- User acceptance testing (UAT)
- Pilot deployment
- Full production deployment (with optimization)

⏳ **Coming in future phases:**
- Email notifications
- Mobile app
- Advanced search
- API endpoints

---

**Last Updated**: 2026  
**Version**: 1.0.0  
**Status**: ✅ READY

🎉 **Hệ thống quản lý công văn ABC sẵn sàng triển khai!**

---

For detailed information, please refer to the documentation files included in this package.
