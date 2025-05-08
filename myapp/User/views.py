from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from Admin.models import user_details


def email_page(request):
    return render(request, 'email_verify.html')



def email_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = user_details.objects.filter(email=email).first()
        if not user:
            return render(request, 'email_verify.html', {'message': 'Email not registered'})
        if user.password:
            return render(request, 'login.html', {'message': 'Password already set. Please login.'})
        request.session['verified_email'] = email
        return render(request, 'create_password.html')
    return render(request, 'email_verify.html')



# Handle password creation and save hashed password
def user_created_password(request):
    if request.method == 'POST':
        email = request.session.get('verified_email')
        password = request.POST.get('password')
        if not email:
            return render(request, 'email_verify.html', {'message': 'Session expired. Please verify your email again.'})
        try:
            user = user_details.objects.filter(email=email).first()
            user.password = make_password(password)
            user.save()
            del request.session['verified_email']
            return render(request, 'login.html', {'message': 'Password created successfully. Please login.'})
        except user_details.DoesNotExist:
            return render(request, 'create_password.html', {'message': 'User not found'})
    return render(request, 'create_password.html')



def login_page(request):
    return render(request, 'login.html')



def user_login_verification(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = user_details.objects.filter(email=email).first()
        if user is None:
            return render(request, 'login.html', {'message': 'Email not registered'})
        if user.password is None:
            return render(request, 'login.html', {'message': 'password not registered'})

        if check_password(password, user.password):
            request.session['user_email'] = user.email
            return redirect('user_dashboard')
        else:
            return render(request, 'login.html', {'message': 'Invalid password'})

    return render(request, 'login.html')


def user_dashboard(request):
    email = request.session.get('user_email')
    if not email:
        return redirect('login_page') 
    try:
        user = user_details.objects.get(email=email)
        return render(request, 'user_dashboard.html', {'user': user})
    except user_details.DoesNotExist:
        return redirect('login_page')




def logout_view(request):
    request.session.flush()
    return redirect('login_page')






def course_dashboard(request):
    return render(request,'t.html')