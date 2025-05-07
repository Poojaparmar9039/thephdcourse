from django.shortcuts import render
from .models import user_details

# Create your views here.
def dashboard_page(request):
    account_details=user_details.objects.all()
    pending_no=sum(a.status=="Pending" for a in account_details)
    processing_no=sum(a.status=="Processing" for a in account_details)
    completed_no=sum(a.status=="Completed" for a in account_details)
    failed_no=sum(a.status=="Failed" for a in account_details)
    return render(request,'admin.html',
    {
        'account_details':account_details,
        'pending_no':pending_no,
        'processing_no':processing_no,
        'completed_no':completed_no,
        'failed_no':failed_no
    }
    )

def pending_accounts_page(request):
    account_details=user_details.objects.filter(status="Pending")
    return render(request,"admin.html",{'account_details':account_details})

def completed_accounts_page(request):
    account_details=user_details.objects.filter(status="Completed")
    return render(request,"admin.html",{'account_details':account_details})

def failed_accounts_page(request):
    account_details=user_details.objects.filter(status="Failed")
    return render(request,"admin.html",{'account_details':account_details})