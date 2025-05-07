from django.urls import path
from . import views

urlpatterns = [
    path("",views.dashboard_page,name='dashboard_page'),
    path("pending_accounts_page/",views.pending_accounts_page,name='pending_accounts_page'),
    path("completed_accounts_page/",views.completed_accounts_page,name='completed_accounts_page'),
    path("failed_accounts_page/",views.failed_accounts_page,name='failed_accounts_page'),

]
