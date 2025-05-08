from django.urls import path
from . import views

urlpatterns = [
    path('login/',views.login_page,name='login_page'),
    path("email_page/",views.email_page,name='email_page'),
    path("email_verification/",views.email_verification,name='email_verification'),
    path('user_created_password/', views.user_created_password, name='user_created_password'),
    path('login/', views.login_page, name='login_page'),
    path('login/verify/', views.user_login_verification, name='user_login_verification'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('logout/', views.logout_view, name='logout_view'),
    path('course_dashboard/',views.course_dashboard,name='course_dashboard'),
    
]


