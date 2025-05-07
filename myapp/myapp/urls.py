from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',include('Home.urls')),
    path('dashboard/',include('Admin.urls')),
    path('admin/', admin.site.urls),
    path('user/',include('User.urls')),
]
