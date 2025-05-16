from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from Admin.models import user_details,Module
from django.http import JsonResponse
import json


def email_page(request):
    return render(request, 'email_verify.html')


def email_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = user_details.objects.filter(email=email).order_by('-id').first()
        if not user:
            return render(request, 'email_verify.html', {'message': 'Email not registered'})
        if user.password:
            return render(request, 'login.html', {'message': 'Password already set. Please login.'})
        request.session['verified_email'] = email
        return render(request, 'create_password.html')
    return render(request, 'email_verify.html')


def user_created_password(request):
    if request.method == 'POST':
        email = request.session.get('verified_email')
        password = request.POST.get('password')
        if not email:
            return render(request, 'email_verify.html', {'message': 'Session expired. Please verify your email again.'})
        user = user_details.objects.filter(email=email).order_by('-id').first()
        if not user:
            return render(request, 'create_password.html', {'message': 'User not found'})
        user.password = make_password(password)
        user.save()
        del request.session['verified_email']
        return render(request, 'login.html', {'message': 'Password created successfully. Please login.'})
    return render(request, 'create_password.html')


def login_page(request):
    return render(request, 'login.html')


def user_login_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        users_with_password = user_details.objects.filter(email=email, password__isnull=False)

        if not users_with_password.exists():
            if user_details.objects.filter(email=email).exists():
                return render(request, 'login.html', {'message': 'Password not set. Please create one.'})
            else:
                return render(request, 'login.html', {'message': 'Email not registered'})

        for user in users_with_password:
            if check_password(password, user.password):
                request.session['user_email'] = user.email
                return redirect('user_dashboard')

        return render(request, 'login.html', {'message': 'Invalid password'})

    return render(request, 'login.html')


from django.db.models import Max

def user_dashboard(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login_page')

    user = user_details.objects.filter(email=email).order_by('-id').first()
    if not user:
        return redirect('login_page')

    modules = Module.objects.all()
    total_modules = modules.count()
    completed_modules = UserProgress.objects.filter(user=user, completed=True).count()

    # Get last accessed module
    progress_qs = UserProgress.objects.filter(user=user).exclude(last_accessed_on__isnull=True).order_by('-last_accessed_on')
    next_module = progress_qs.first().module if progress_qs.exists() else None
    progress_percent = round((completed_modules / total_modules) * 100) if total_modules > 0 else 0
    in_progress_count = total_modules - completed_modules
    last_accessed = UserProgress.objects.filter(user=user).exclude(last_accessed_on__isnull=True).order_by('-last_accessed_on').first()
    last_accessed_time = last_accessed.last_accessed_on if last_accessed else None

    context = {
    'user': user,
    'total_modules': total_modules,
    'completed_count': completed_modules,  
    'in_progress_count': in_progress_count,
    'progress_percent': progress_percent,
    'next_module': next_module,
    'last_accessed_time': last_accessed_time,
    }
    return render(request, 'user_dashboard.html', context)



def user_dashboard_details(request):
    email = request.session.get('user_email')
    return JsonResponse({'message': 'Not implemented'})


def my_course(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login_page')
    user = user_details.objects.filter(email=email).order_by('-id').first()
    return render(request, 'my_courses.html', {'user': user})


def logout_view(request):
    request.session.flush()
    return redirect('login_page')

from django.shortcuts import render, redirect
from django.http import HttpResponseServerError

def show_orderkey(request):
    try:
        print("show_orderkey view is being called")
        email = request.session.get('user_email')
        if not email:
            print("User not logged in")
            return redirect('login_page')

        user = user_details.objects.filter(email=email).order_by('-id').first()
        if not user:
            print("User not found")
            return render(request, 'orders.html', {'message': 'User not found.'})

        return render(request, 'orders.html', {'user': user})

    except Exception as e:
        print(f"Error in show_orderkey: {e}")
        return HttpResponseServerError("An unexpected error occurred. Please try again later.")


from django.utils import timezone
from Admin.models import user_details, Module, UserProgress

def course_dashboard(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login_page')

    user = user_details.objects.filter(email=email).order_by('-id').first()
    if not user:
        return redirect('login_page')

    chapters = Module.objects.all()
    total_modules = chapters.count()
    completed_modules = UserProgress.objects.filter(user=user, completed=True).count()

    overall_progress = round((completed_modules / total_modules) * 100) if total_modules > 0 else 0

    # Mark last accessed module (optional: pick current module by logic or param)
    if chapters:
        latest_module = chapters.first()  # Example: first module (can be replaced by actual selection)
        user_progress, created = UserProgress.objects.get_or_create(user=user, module=latest_module)
        user_progress.last_accessed_on = timezone.now()
        user_progress.save()

    return render(request, 't.html', {
        'user': user,
        'chapters': chapters,
        'overall_progress': overall_progress
    })











from django.utils import timezone
from django.shortcuts import get_object_or_404
from Admin.models import user_details, Module, UserProgress  # Ensure this is correct

def mark_module_complete(request, module_id):
    email = request.session.get('user_email')  # Get from session
    if not email:
        return JsonResponse({'error': 'User not authenticated'}, status=403)

    user = user_details.objects.filter(email=email).order_by('-id').first()
    if not user:
        return JsonResponse({'error': 'User not found'}, status=404)

    module = get_object_or_404(Module, id=module_id)

    user_progress, created = UserProgress.objects.get_or_create(user=user, module=module)

    if not user_progress.completed:
        user_progress.completed = True
        user_progress.completed_on = timezone.now()
        user_progress.progress_percentage = 100.0
        user_progress.save()

    # Calculate overall progress
    course = module.course
    total_modules = course.module_set.count()
    completed_modules = UserProgress.objects.filter(user=user, module__course=course, completed=True).count()
    overall_progress = (completed_modules / total_modules) * 100

    return JsonResponse({'progress': overall_progress})
