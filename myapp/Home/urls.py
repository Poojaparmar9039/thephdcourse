from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("checkout/",views.checkout_page,name='checkout_page'),
    path("submit_data/",views.submit_data,name='submit_data'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payment_successful/', views.payment_successful, name='payment_successful'),
    path('payment_failed/', views.payment_failed, name='payment_failed'),
    path('payment-failed-api/', views.payment_failed_api, name='payment_failed_api'),

]


