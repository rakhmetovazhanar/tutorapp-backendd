from django.urls import path
from .views import *

urlpatterns = [
    path('register-teacher/', register_teacher, name='register-teacher'),
    path('register-student/', register_student, name='register-student'),
    path('login-teacher/', login_teacher, name='login-teacher'),
    path('login-student/', login_student, name='login-student'),
    path('logout/', logout, name='logout'),
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('verify-code/', verify_code, name='verify-code'),
    path('change-password/', change_password, name='change-password'),
    path('student-profile/', student_profile, name='student-profile'),
    path('teacher-profile/', teacher_profile, name='teacher-profile'),
    #path('add-course/', add_course, name='add-course'),
]