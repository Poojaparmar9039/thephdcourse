from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',include('Home.urls')),
    path('dashboard/',include('Admin.urls')),
    path('admin/', admin.site.urls),
    path('user/',include('User.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)