from django.urls import path
from .views import register_student, register_teacher, login_student, login_teacher, logout, change_password

urlpatterns = [
    path('register-teacher/', register_teacher, name='register-teacher'),
    path('register-student/', register_student, name='register-student'),
    path('login-teacher/', login_teacher, name='login-teacher'),
    path('login-student/', login_student, name='login-student'),
    path('logout/', logout, name='logout'),
    path('change_password/', change_password, name='change-password')
]