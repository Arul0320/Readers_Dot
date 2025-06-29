from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('admin_upload/', views.admin_upload, name='admin_upload'),
    path('student/', views.student_access, name='student_access'),
    path('check-answer/', views.check_answer, name='check_answer'),
    path('complete-reading/', views.complete_reading, name='complete_reading'),
    path('results/', views.view_results, name='view_results'),
    path('results/<int:result_id>/', views.result_detail, name='result_detail'),
    
]