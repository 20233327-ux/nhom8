from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from vn_docs.models import Document
from vn_workflow.models import DocumentWorkflow, ApprovalHistory
from functools import wraps

def role_required(allowed_roles):
    """Decorator kiểm tra vai trò người dùng"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.role not in allowed_roles:
                return render(request, '403.html', {'message': 'Bạn không có quyền truy cập'}, status=403)
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_staff')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('remember_me')
        
        # Validate input
        if not username or not password:
            messages.error(request, 'Vui lòng nhập tên đăng nhập và mật khẩu')
            return render(request, 'auth/login.html', {'username': username})
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_active:
                login(request, user)
                
                # Handle "Remember me" functionality
                if remember_me:
                    # Session expires in 30 days
                    request.session.set_expiry(30 * 24 * 60 * 60)
                else:
                    # Session expires when browser closes
                    request.session.set_expiry(0)
                
                messages.success(request, f'Chào mừng {user.get_full_name or user.username}!')
                
                # Redirect based on role
                if user.role == 'admin':
                    return redirect('dashboard_admin')
                elif user.role in ['manager', 'clerk']:
                    return redirect('dashboard_manager')
                else:
                    return redirect('dashboard_staff')
            else:
                messages.error(request, 'Tài khoản này đã bị vô hiệu hóa. Vui lòng liên hệ Admin.')
        else:
            messages.error(request, '❌ Tên đăng nhập hoặc mật khẩu không chính xác. Vui lòng thử lại.')
            # Log failed attempt (optional)
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f'Failed login attempt for username: {username}')
    
    return render(request, 'auth/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def forgot_password_view(request):
    """Forgot password page - contact admin to reset"""
    return render(request, 'auth/forgot_password.html')

@login_required(login_url='login')
def dashboard_staff(request):
    """Dashboard cho Nhân viên & Văn thư"""
    my_docs = Document.objects.filter(created_by=request.user).order_by('-date_created')[:10]
    pending_approvals = DocumentWorkflow.objects.filter(status='pending').select_related('document')[:5]
    
    context = {
        'my_docs': my_docs,
        'pending_approvals': pending_approvals,
        'user': request.user,
        'total_docs': Document.objects.count(),
    }
    return render(request, 'dashboard/staff.html', context)

@login_required(login_url='login')
@role_required(['manager', 'admin', 'clerk'])
def dashboard_manager(request):
    """Dashboard cho Lãnh đạo & Văn thư"""
    # Công văn cần duyệt của lãnh đạo
    approval_tasks = ApprovalHistory.objects.filter(
        approver=request.user
    ).select_related('doc_workflow__document').order_by('-timestamp')[:15]
    
    # Thống kê
    total_docs = Document.objects.count()
    pending_docs = Document.objects.filter(status='pending').count()
    signed_docs = Document.objects.filter(status='signed').count()
    
    context = {
        'approval_tasks': approval_tasks,
        'total_docs': total_docs,
        'pending_docs': pending_docs,
        'signed_docs': signed_docs,
        'user': request.user,
    }
    return render(request, 'dashboard/manager.html', context)

@login_required(login_url='login')
@role_required(['admin'])
def dashboard_admin(request):
    """Dashboard cho Quản trị viên"""
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    stats = {
        'total_users': User.objects.count(),
        'total_docs': Document.objects.count(),
        'total_workflows': DocumentWorkflow.objects.count(),
        'pending_approvals': ApprovalHistory.objects.filter(action='approve').count(),
    }
    
    recent_docs = Document.objects.order_by('-date_created')[:10]
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    context = {
        'stats': stats,
        'recent_docs': recent_docs,
        'recent_users': recent_users,
        'user': request.user,
    }
    return render(request, 'dashboard/admin.html', context)
