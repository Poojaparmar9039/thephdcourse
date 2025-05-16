from django.shortcuts import render
from .models import user_details
from datetime import timedelta
from django.utils.timezone import now

def pending_accounts_page(request):
    account_details=user_details.objects.filter(status="Pending")
    account = user_details.objects.all()
    total_accounts = account.count()
    pending_no = sum(a.status == "Pending" for a in account_details)
    processing_no = sum(a.status == "Processing" for a in account_details)
    completed_no = sum(a.status == "Completed" for a in account_details)
    failed_no = sum(a.status == "Failed" for a in account_details)
    return render(request,"admin.html",
    {
        'account_details':account_details,
        'pending_no': pending_no,
        'processing_no': processing_no,
        'completed_no': completed_no,
        'failed_no': failed_no,
        'total_accounts':total_accounts,
    })

def completed_accounts_page(request):
    account_details=user_details.objects.filter(status="Completed")
    account = user_details.objects.all()
    total_accounts = account.count()
    pending_no = sum(a.status == "Pending" for a in account_details)
    processing_no = sum(a.status == "Processing" for a in account_details)
    completed_no = sum(a.status == "Completed" for a in account_details)
    failed_no = sum(a.status == "Failed" for a in account_details)
    return render(request,"admin.html",
    {
        'account_details':account_details,
        'pending_no': pending_no,
        'processing_no': processing_no,
        'completed_no': completed_no,
        'failed_no': failed_no,
        'total_accounts':total_accounts,
    })

def failed_accounts_page(request):
    account_details=user_details.objects.filter(status="Failed")
    account = user_details.objects.all()
    total_accounts = account.count()
    pending_no = sum(a.status == "Pending" for a in account_details)
    processing_no = sum(a.status == "Processing" for a in account_details)
    completed_no = sum(a.status == "Completed" for a in account_details)
    failed_no = sum(a.status == "Failed" for a in account_details)
    return render(request,"admin.html",
    {
        'account_details':account_details,
        'pending_no': pending_no,
        'processing_no': processing_no,
        'completed_no': completed_no,
        'failed_no': failed_no,
        'total_accounts':total_accounts,
    })



def dashboard_page(request):
    filter_value = request.GET.get('date_filter') 
    account_details = user_details.objects.all()
    total_accounts = account_details.count()
    today = now()

    if filter_value == 'today':
        start = today.replace(hour=0, minute=0, second=0, microsecond=0)
        account_details = account_details.filter(created_at__gte=start)

    elif filter_value == 'yesterday':
        start = (today - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        end = start + timedelta(days=1)
        account_details = account_details.filter(created_at__gte=start, created_at__lt=end)

    elif filter_value == 'month':
        start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        account_details = account_details.filter(created_at__gte=start)

    elif filter_value == 'year':
        start = today.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        account_details = account_details.filter(created_at__gte=start)

    
    pending_no = sum(a.status == "Pending" for a in account_details)
    processing_no = sum(a.status == "Processing" for a in account_details)
    completed_no = sum(a.status == "Completed" for a in account_details)
    failed_no = sum(a.status == "Failed" for a in account_details)

    return render(request, 'admin.html', {
        'account_details': account_details,
        'pending_no': pending_no,
        'processing_no': processing_no,
        'completed_no': completed_no,
        'failed_no': failed_no,
        'filter_applied': filter_value,
        'total_accounts':total_accounts,
    })

