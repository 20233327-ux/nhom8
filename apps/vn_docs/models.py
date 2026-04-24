from django.db import models
from django.conf import settings

class Document(models.Model):
    DOC_TYPES = (
        ('IN', 'Công văn đến'),
        ('OUT', 'Công văn đi'),
        ('INT', 'Công văn nội bộ'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Dự thảo'),
        ('pending', 'Đang xử lý'),
        ('signed', 'Đã ký/Ban hành'),
        ('archived', 'Đã lưu trữ'),
    )

    doc_number = models.CharField(max_length=50, unique=True, verbose_name="Số hiệu công văn")
    title = models.TextField(verbose_name="Trích yếu nội dung")
    doc_type = models.CharField(max_length=5, choices=DOC_TYPES, verbose_name="Loại công văn")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Trạng thái")
    
    sender_org = models.CharField(max_length=255, verbose_name="Cơ quan ban hành/gửi")
    receiver_org = models.CharField(max_length=255, verbose_name="Cơ quan nhận")
    
    date_issued = models.DateField(verbose_name="Ngày ban hành")
    date_created = models.DateField(auto_now_add=True, verbose_name="Ngày tiếp nhận/tạo")
    
    file_attachment = models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name="Tệp tin đính kèm")
    content_extracted = models.TextField(blank=True, verbose_name="Nội dung trích xuất (OCR)")
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_docs')
    
    def __str__(self):
        return f"{self.doc_number} - {self.title[:50]}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        # Xóa logic OCR trực tiếp trong save() để tránh lỗi 500 trên Windows
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Công văn"
        verbose_name_plural = "Danh sách Công văn"
from django.db import models

# Create your models here.
