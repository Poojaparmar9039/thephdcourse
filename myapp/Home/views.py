from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import razorpay
from Admin.models import user_details
from django.http import JsonResponse
import json
from django.conf.global_settings import EMAIL_HOST_USER
from django.core.mail import send_mail
import random
import string
from datetime import datetime

# Initialize Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


def home(request):
    return render(request, 'Home.html')


def checkout_page(request):
    return render(request, 'checkout.html')


def submit_data(request):
    if request.method == 'POST':
        fullname = request.POST.get("fullname")
        phone = request.POST.get("phone")
        email = request.POST.get("email")

        # Look up the user by email
        user = user_details.objects.filter(email=email).first()

        if not user:
            # Create a new user if email not found
            user = user_details.objects.create(
                fullname=fullname,
                phone=phone,
                email=email,
                status='Pending',
                purchase_number=0
            )
        else:
           
            user.purchase_number = (user.purchase_number or 0) + 1
            user.created_at=datetime.now()
            user.status = 'Pending'

        user.save()

     
        amount = 100  # in paise (₹1.00)
        currency = 'INR'
        receipt = f"user_{user.id}_purchase_{user.purchase_number}"

        razorpay_order = client.order.create({
            "amount": amount,
            "currency": currency,
            "receipt": receipt,
            "payment_capture": 1,
        })

        user.razorpay_order_id = razorpay_order['id']
        user.save()

        context = {
            'order_id': razorpay_order['id'],
            'amount': amount,
            'fullname': user.fullname,
            'email': user.email,
            'phone': user.phone,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
        }
        return render(request, 'checkout_redirect.html', context)



@csrf_exempt
def payment_success(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        user = user_details.objects.filter(razorpay_order_id=order_id).first()

        try:
            client.utility.verify_payment_signature(params_dict)
            if user:
                user.status = 'Completed'
                user.purchase_number = (user.purchase_number or 0) + 1
                user.save()
                send_email_to_user(user)
                send_email_to_admin(user)
            return redirect('payment_successful')

        except razorpay.errors.SignatureVerificationError:
            if user:
                user.status = 'Failed'
                user.save()
            return redirect('payment_failed')

    return render(request, 'payment_failed.html')



@csrf_exempt
def payment_failed_api(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('order_id')
        user = user_details.objects.filter(razorpay_order_id=order_id).first()
        if user:
            user.status = 'Failed'
            user.save()
        return JsonResponse({'status': 'ok'})


def payment_failed(request):
    return render(request, 'payment_failed.html')


def payment_successful(request):
    # return render(request, 'payment_successful.html')
    return render(request,'login.html')


def send_email_to_user(user):
    orderkey = generate_orderkey(user.id)
    subject = 'Thank you for your purchase!'
    message = f"""Hi {user.fullname},
    Thank you for your payment! We're excited to confirm that your transaction was successful.
    You now have access to your course and can start learning right away. We hope you find the content valuable and enriching.
    If you have any questions or need support, feel free to reach out to us at support@example.com.
    your order key is -{orderkey}
    Best regards,  
    The ResearchphdCourses Team
    """
    email_from = EMAIL_HOST_USER
    recipient_list = [user.email]
    send_mail(subject, message, email_from, recipient_list)

def send_email_to_admin(user):
    subject = "New Purchase Notification - User Payment Successful"
    message = f"""Hello Admin,
            A new purchase has been completed by a user. Here are the details:
            Full Name: {user.fullname}
            Email: {user.email}
            Phone: {user.phone}
            Order ID: {user.razorpay_order_id}
            Purchase Count: {user.purchase_number}
            Status: {user.status}      
            Please log in to the admin panel for more details.  
            Best regards,  
            Your Automated Notification System
            """
    admin_email = 'poojaparmar9753@gmail.com'  
    send_mail(subject, message, EMAIL_HOST_USER, [admin_email])


def generate_orderkey(user_id):
    special_chars = "!@#$?/"
    letters = string.ascii_letters  # a-z + A-Z
    digits = string.digits
    random_part = ''.join(random.choices(letters + digits + special_chars, k=6))
    orderkey=f"{user_id}-{random_part}"
    try:
        user = user_details.objects.get(id=user_id)
        user.orderkey = orderkey
        user.save()
        return orderkey
    except user_details.DoesNotExist:
        return None


     