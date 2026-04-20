from django.shortcuts import render
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta
from vn_docs.models import Document

def dashboard(request):
    # Thống kê tổng quan
    total_docs = Document.objects.count()
    pending_docs = Document.objects.filter(status='pending').count()
    signed_docs = Document.objects.filter(status='signed').count()
    
    # Công văn đến trong tháng
    this_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    docs_this_month = Document.objects.filter(date_created__gte=this_month_start).count()
    
    # Thống kê theo loại công văn
    type_stats = Document.objects.values('doc_type').annotate(count=Count('id'))
    
    # Công văn trễ hạn (pending > 7 ngày)
    overdue_limit = timezone.now().date() - timedelta(days=7)
    overdue_docs = Document.objects.filter(status='pending', date_created__lt=overdue_limit)
    
    context = {
        'total_docs': total_docs,
        'pending_docs': pending_docs,
        'signed_docs': signed_docs,
        'docs_this_month': docs_this_month,
        'type_stats': type_stats,
        'overdue_docs': overdue_docs,
    }
    return render(request, 'dashboard/index.html', context)
from django.shortcuts import render

# Create your views here.
