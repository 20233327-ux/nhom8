from django.db import models
from django.conf import settings
from vn_docs.models import Document

class WorkflowDefinition(models.Model):
    name = models.CharField(max_length=100, verbose_name="Tên quy trình")
    description = models.TextField(blank=True, verbose_name="Mô tả")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Quy trình duyệt"
        verbose_name_plural = "Các quy trình duyệt"

class WorkflowStep(models.Model):
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE, related_name='steps')
    order = models.PositiveIntegerField(verbose_name="Thứ tự bước")
    name = models.CharField(max_length=100, verbose_name="Tên bước (ví dụ: Trưởng phòng duyệt)")
    role_required = models.CharField(max_length=20, choices=(
        ('admin', 'Quản trị'),
        ('clerk', 'Văn thư'),
        ('manager', 'Lãnh đạo'),
        ('staff', 'Nhân viên'),
    ), verbose_name="Vai trò yêu cầu")

    def __str__(self):
        return f"{self.workflow.name} - Bước {self.order}: {self.name}"

    class Meta:
        ordering = ['order']
        verbose_name = "Bước quy trình"
        verbose_name_plural = "Các bước quy trình"

class DocumentWorkflow(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Đang chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    )
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='workflows')
    workflow = models.ForeignKey(WorkflowDefinition, on_delete=models.CASCADE)
    current_step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"Duyệt cho: {self.document.doc_number}"

class ApprovalHistory(models.Model):
    doc_workflow = models.ForeignKey(DocumentWorkflow, on_delete=models.CASCADE, related_name='history')
    step = models.ForeignKey(WorkflowStep, on_delete=models.SET_NULL, null=True)
    approver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=(('approve', 'Duyeting'), ('reject', 'Từ chối')))
    comment = models.TextField(blank=True, verbose_name="Ý kiến xử lý")
    signature_data = models.TextField(blank=True, null=True, verbose_name="Dữ liệu ký số")
    timestamp = models.DateTimeField(auto_now_add=True)

