from django.db import models
from django.contrib.auth.models import AbstractUser

class Department(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên phòng ban")
    code = models.CharField(max_length=20, unique=True, verbose_name="Mã phòng ban")
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Phòng ban"
        verbose_name_plural = "Phòng ban"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Quản trị hệ thống'),
        ('clerk', 'Văn thư'),
        ('manager', 'Lãnh đạo'),
        ('staff', 'Nhân viên'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff', verbose_name="Vai trò")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Phòng ban")
    phone = models.CharField(max_length=15, blank=True, verbose_name="Số điện thoại")

    class Meta:
        verbose_name = "Người dùng"
        verbose_name_plural = "Người dùng"
from django.db import models

# Create your models here.
