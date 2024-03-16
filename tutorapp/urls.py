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
    path('add-course/', add_course, name='add-course'),
    path('get-teacher-courses/', get_teacher_courses, name='get-teacher-courses'),
    path('delete-course/<int:course>', delete_course, name='delete-course'),
    path('update-course/<int:course>', update_course, name='update-course'),
    path('update-teacher-profile/<int:teacher>', update_teacher_profile, name='update-teacher-profile'),
    path('delete-teacher-profile/<int:teacher>', delete_teacher_profile, name='delete-teacher-profile'),
    path('enroll-to-course/<int:student>', enroll_to_course, name='enroll-to-course'),
    path('student-courses/<int:student>', student_courses, name='student-courses')
]