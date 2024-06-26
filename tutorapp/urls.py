from django.urls import path
from .views import *
from .dashboard import *

urlpatterns = [
    #register
    path('register-teacher/', register_teacher, name='register-teacher'),
    path('register-student/', register_student, name='register-student'),
    #login, logout
    path('login-teacher/', login_teacher, name='login-teacher'),
    path('login-student/', login_student, name='login-student'),
    path('logout/', logout, name='logout'),
    #forgot password
    path('forgot-password/', forgot_password, name='forgot-password'),
    path('verify-code/', verify_code, name='verify-code'),
    path('change-password/', change_password, name='change-password'),
    #student profile
    path('student-profile/<int:student>', student_profile, name='student-profile'),
    path('update-student-profile/<int:student>', update_student_profile, name='update-student-profile'),
    path('delete-student-profile/<int:student>', delete_student_profile, name='delete-student-profile'),
    #teacher profile
    path('teacher-profile/<int:teacher>', teacher_profile, name='teacher-profile'),
    path('update-teacher-profile/<int:teacher>', update_teacher_profile, name='update-teacher-profile'),
    path('delete-teacher-profile/<int:teacher>', delete_teacher_profile, name='delete-teacher-profile'),
    path('delete-picture/<int:user>', delete_profile_picture, name='delete-picture'),

    #course
    path('add-course/', add_course, name='add-course'),
    path('course-details/<int:course>', course_details, name='course-detail'),
    path('delete-course/<int:course>', delete_course, name='delete-course'),
    path('update-course/<int:course>', update_course, name='update-course'),
    #teacher, student courses
    path('get-teacher-courses/', get_teacher_courses, name='get-teacher-courses'),
    path('student-courses/<int:student>', get_student_courses, name='student-courses'),
    #enroll
    path('enroll-to-course/<int:course>', enroll_to_course, name='enroll-to-course'),
    #filter
    path('courses-by-category/<int:category>', get_courses_by_category, name='get-courses-by-category'),
    path('search-and-filter/', search_and_filter, name='search-and-filter'),
    #rate
    path('rate-course/<int:course>', rate_course, name='rate-course'),
    #clients
    path('clients/<int:course>', get_teacher_clients, name='teacher-clients'),
    path('delete-client/<int:student>', delete_client, name='delete-client'),
    #delete student course
    path('course-delete/<int:course>', delete_student_course, name='course-delete'),
    #comments
    path('comment/<int:course>', add_comment, name='comment'),
    path('comments/<int:course>', get_comments, name='comments'),

    #video-conference
    path('create-video-conference/<int:course>', create_videoconference, name='create-videoconference'),
    path('join-to-video-conference/<str:url>', join_videoconference, name='join-to-videoconference'),

    #teacher profile info
    path('courses/<int:teacher>', number_of_courses, name='courses'),
    path('students/<int:teacher>', number_of_students, name='students'),
    path('feedback/<int:teacher>', number_of_comments, name='comments'),

    #dashboard
    path('experience-dashboard/', experience_dashboard, name='experience-dashboard'),
    path('age-dashboard/', age_dashboard, name='age-dashboard'),
    path('city-dashboard/', city_dashboard, name='city-dashboard'),
    path('student-dashboard/', count_courses_student_dashboard, name='student-dashboard'),
    path('top-courses-dashboard/', top_courses, name='top-courses-dashboard'),
    path('users-number-dashboard/', number_of_users_dashboard, name='users-number-dashboard'),

    #support
    path('support/', support, name='support'),

    #payment
    path('payment/<int:course>', payment, name='payment'),

    #main page info
    path('top-teacher/', top_three_teachers, name='top-teacher'),
    path('teacher-comments/', comments, name='teacher-comments'),

    path('students-number/', total_students, name='students-number'),
    path('teachers-number/', total_teachers, name='teachers-number'),
    path('courses-number/', total_courses, name='courses-number'),
    path('comments-number/', total_comments, name='comments-number'),

]