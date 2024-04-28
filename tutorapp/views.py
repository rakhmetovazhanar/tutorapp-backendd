import os
import random

from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .models import CustomUser, EmailCode, Course, Category, CourseRating, CourseStudent, Comment, VideoConference
from .serializers import (CustomUserSerializer, EmailUserSerializer, StudentProfileSerializer, TeacherProfileSerializer,
                          AddCourseSerializer, CourseUpdateSerializer,
                          UpdateTeacherProfileSerializer, EnrollToCourseSerializer, GetStudentCoursesSerializer,
                          LoginUserSerializer, UpdateStudentProfileSerializer, RateCourseSerializer,
                          ClientsInfoSerializer,
                          StudentCoursesSerializer, CommentsSerializer, VideoConferenceSerializer, CardInformationSerializer)
from rest_framework.permissions import IsAuthenticated
from django.conf.global_settings import EMAIL_HOST_USER
import stripe


@api_view(['POST'])
def register_teacher(request):
    if request.method == 'POST':
        request.data['role'] = 'teacher'
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_teacher(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            if user.role == 'teacher':
                if user is not None:
                    teacher_data = LoginUserSerializer(user).data
                    response_data['data'] = teacher_data

            return Response(response_data)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def register_student(request):
    if request.method == 'POST':
        request.data['role'] = 'student'
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_student(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }

            if user.role == 'student':
                if user is not None:
                    student_data = LoginUserSerializer(user).data
                    response_data['data'] = student_data

            return Response(response_data)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            Token.objects.filter(user=request.user).delete()
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({'error': 'User not logged in.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def forgot_password(request):
    username = request.data['username']
    user: CustomUser = CustomUser.objects.get(username=username)
    if user:
        code = random.randint(1000, 9999)

        email_code = EmailCode.objects.get_or_create(user=user, code=code)

        subject = 'Verification code'
        message = f'Code to reset your password: {code}'
        from_email = EMAIL_HOST_USER

        result = send_mail(subject, message, from_email, [user.username])

        if result > 0:
            return Response({'Verification code is sent.'}, status=status.HTTP_200_OK)

    return Response({'message': 'Something went wrong.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def verify_code(request):
    username = request.data['username']
    code = request.data['code']

    user: CustomUser = CustomUser.objects.get(username=username)
    email_code: EmailCode = EmailCode.objects.get(user=user, code=code)

    if email_code and user:
        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        response_data = {
            'token': token.key,
            'username': user.username,
            'role': user.role,
        }

        return Response(response_data, status=status.HTTP_200_OK)

    return Response({'message': 'Invalid code'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    new_password = request.data['new_password']
    confirm_password = request.data['confirm_password']

    if new_password != confirm_password:
        return Response({'message': 'Passwords are not match.'}, status=status.HTTP_400_BAD_REQUEST)

    user = request.user
    user.set_password(new_password)
    user.save()

    return Response({'message': 'Password is successfully changed.'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def student_profile(request, student: int):
    student = CustomUser.objects.get(id=student)

    if student.id == request.user.id:
        serializer = StudentProfileSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_profile(request, teacher: int):
    teacher = CustomUser.objects.get(id=teacher)

    if teacher.id == request.user.id:
        serializer = TeacherProfileSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({'message': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_course(request):
    serializer_add_course = AddCourseSerializer(data=request.data)

    if serializer_add_course.is_valid():
        serializer_add_course.save()
        return Response(serializer_add_course.data, status=status.HTTP_201_CREATED)
    return Response(serializer_add_course.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_teacher_courses(request):
    courses = Course.objects.filter(teacher_id=request.user.id).values(
        'id', 'teacher_id_id', 'name', 'description', 'cost', 'day_time', 'level', 'category_id', 'language',
        'avg_rating'
    )

    return Response(courses, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_course(request, course: int):
    try:
        course = Course.objects.get(id=course)
        if course.teacher_id_id == request.user.id:
            course.delete()
            return Response({'message': 'Course successfully deleted!'}, status=status.HTTP_200_OK)

        return Response({'message': 'Not allowed to delete course'}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_student_course(request, course: int):
    try:
        course = CourseStudent.objects.get(course_id_id=course, student_id_id=request.user.id)
        if course:
            course.delete()
            return Response({'message': 'Course successfully deleted!'}, status=status.HTTP_200_OK)
        return Response({'message': 'Not allowed to delete course'}, status=status.HTTP_400_BAD_REQUEST)
    except CourseStudent.DoesNotExist:
        return Response({'message': 'Course not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
def update_course(request, course: int):
    try:
        course = Course.objects.get(id=course)
        if course.teacher_id_id == request.user.id:
            serializer = CourseUpdateSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Not allowed to update course'}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'message': 'Course not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_teacher_profile(request, teacher: int):
    try:
        teacher = CustomUser.objects.get(id=teacher)

        if teacher.id == request.user.id:
            serializer = UpdateTeacherProfileSerializer(teacher, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Not allowed to update teacher profile'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'message': 'Profile not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_student_profile(request, student: int):
    try:
        student = CustomUser.objects.get(id=student)
        if student.id == request.user.id:
            serializer = UpdateStudentProfileSerializer(student, data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'Not allowed to update student profile'}, status=status.HTTP_400_BAD_REQUEST)
    except CustomUser.DoesNotExist:
        return Response({'message': 'Profile not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_profile_picture(request, user: int):
    user = CustomUser.objects.get(id=user)

    if user.profile_picture:
        user.profile_picture.delete()
        return Response({'message': 'Profile picture is deleted!'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Profile picture is not exists!'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_student_profile(request, student: int):
    try:
        student = CustomUser.objects.get(id=student)

        if student.id == request.user.id:
            student.delete()
            return Response({'message': 'Student profile successfully deleted!'}, status=status.HTTP_200_OK)

        return Response({'message': 'Not allowed to delete profile'}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'message': 'Profile not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_teacher_profile(request, teacher: int):
    try:
        teacher = CustomUser.objects.get(id=teacher)

        if teacher.id == request.user.id:
            teacher.delete()
            return Response({'message': 'Teacher profile successfully deleted!'}, status=status.HTTP_200_OK)

        return Response({'message': 'Not allowed to delete profile'}, status=status.HTTP_400_BAD_REQUEST)
    except Course.DoesNotExist:
        return Response({'message': 'Profile not found!'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_to_course(request, course: int):
    course = Course.objects.get(id=course)
    student = request.user.id

    enrolled_course = CourseStudent.objects.filter(student_id_id=student, course_id_id=course)

    if enrolled_course:
        return Response({'message': 'You are already enrolled to this course'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        serializer = EnrollToCourseSerializer(data={'course_id': course.id, 'student_id': student},
                                              context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_student_courses(request, student: int):
    try:
        courses = CourseStudent.objects.filter(student_id_id=student).values_list('course_id_id', flat=True)

        if courses:
            student_courses = Course.objects.filter(id__in=courses)
            serializer = GetStudentCoursesSerializer(student_courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are not enrolled to this course'}, status=status.HTTP_404_NOT_FOUND)

    except CourseStudent.DoesNotExist:
        return Response({'message': 'No courses found for student!'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'message': 'No match courses!'},
                        status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def course_details(request, course: int):
    course = Course.objects.get(id=course)
    teacher_info = CustomUser.objects.values('first_name', 'last_name', 'profile_picture').get(id=course.teacher_id_id)
    course_info = {
        'id': course.id,
        'name': course.name,
        'description': course.description,
        'category_id_id': course.category_id_id,
        'level': course.level,
        'cost': course.cost,
        'language': course.language,
        'teacher_id_id': course.teacher_id_id,
        'first_name': teacher_info['first_name'],
        'last_name': teacher_info['last_name'],
        'day_time': course.day_time,
        'average_rating': course.avg_rating,
        'profile_picture': teacher_info['profile_picture'],
    }
    return Response(course_info, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_courses_by_category(request, category: int):
    courses_list = Course.objects.filter(category_id_id=category).values(
        'id', 'name', 'description', 'cost', 'day_time', 'avg_rating'
    )
    return Response(courses_list, status=status.HTTP_200_OK)


@api_view(['POST'])
def search_and_filter(request):
    course = request.data.get('course')
    category = request.data.get('category')
    level = request.data.get('level')
    min_cost = request.data.get('min_cost')
    max_cost = request.data.get('max_cost')

    courses = Course.objects.values('id', 'name', 'description', 'cost', 'day_time', 'avg_rating')

    if course:
        courses = courses.filter(name__istartswith=course)

    if category:
        courses = courses.filter(category_id_id=category)

    if level:
        courses = courses.filter(level=level)

    if min_cost and max_cost:
        courses = courses.filter(cost__gte=min_cost, cost__lte=max_cost)

    if courses:
        return Response(courses, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def rate_course(request, course: int):
    rating = request.data.get('rating')
    user = request.user.id

    existing_rating = CourseRating.objects.filter(user_id=request.user.id, course_id=course).first()

    try:
        course = Course.objects.get(id=course).id

        course_rating = Course.objects.filter(id=course).values('avg_rating')
        if course and not existing_rating:
            serializer = RateCourseSerializer(data={'rating': rating, 'course_id': course, 'user_id': user},
                                              context={'request': request})
            if serializer.is_valid():
                serializer.save()
            return Response(course_rating, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You are already rated this course'}, status=status.HTTP_400_BAD_REQUEST)

    except Course.DoesNotExist:
        return Response({'message': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_teacher_clients(request, course: int):
    try:
        students_list = CourseStudent.objects.filter(course_id_id=course).values_list('student_id_id', flat=True)

        if students_list:
            students_info = CustomUser.objects.filter(id__in=students_list)
            student_serializer = ClientsInfoSerializer(students_info, many=True)
            return Response(student_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'You do not have any clients'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        return Response({'message': 'Not found any courses for request teacher'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request, student: int):
    course = request.data.get('course_id')
    student = CourseStudent.objects.filter(student_id_id=student, course_id_id=course)

    if student:
        student.delete()
        return Response({'message': 'Student successfully deleted'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'Student is not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_comment(request, course: int):
    user = request.user.id

    serializer = CommentsSerializer(data={'user': user, 'course': course, 'comment': request.data['comment']})

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_comments(request, course: int):
    try:
        comments = Comment.objects.filter(course_id=course).select_related('user')
        print(comments)

        if comments:
            response_data = []
            for comment in comments:
                user = comment.user
                print(user)
                rating = CourseRating.objects.filter(user_id_id=user, course_id_id=course).first()
                print(rating)
                comment_data = {
                    'profile_picture': user.profile_picture.url if user.profile_picture else None,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'comment': comment.comment,
                    'created': comment.created,
                    'rating': rating.rating,
                }
                response_data.append(comment_data)
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No comments found'}, status=status.HTTP_404_NOT_FOUND)
    except CourseRating.DoesNotExist:
        return Response({'message': 'No rating found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_videoconference(request, course: int):
    course_id = Course.objects.get(id=course)
    print(course)
    if course:
        serializer = VideoConferenceSerializer(data={'course': course_id.id}, context=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'message': 'No course'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_videoconference(request, course: int):
    url_to_conference = request.data['url']
    url = VideoConference.objects.get(conference=url_to_conference, course=course)
    print(url)

    if url:
        return Response({'message': 'You are joined to videoconference!'}, status=status.HTTP_200_OK)
    else:
        return Response({'The url is not correct!'}, status=status.HTTP_404_NOT_FOUND)


support_email = os.getenv('SUPPORT_EMAIL')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def support(request):
    username = request.data['username']
    name = request.data['name']
    message = request.data['message']

    try:
        user: CustomUser = CustomUser.objects.get(username=username)
        print(user)

        if user.username == username:
            print(user.username == username)
            subject = 'Сообщение от "Genius.tech". '
            message = f'Сообщение от {username}, имя: {name}: {message}'
            from_email = EMAIL_HOST_USER
            to_email = support_email
            result = send_mail(subject, message, from_email, [to_email])
            print(result)

            if result > 0:
                subject = 'Техническая поддержка "Genius.tech". '
                message = 'Техническая поддержка получила ваше сообщение, они ответят вам в течении трех рабочих дней.'
                from_email = EMAIL_HOST_USER

                answer = send_mail(subject, message, from_email, [user.username])
                print(answer)

                if answer:
                    return Response({'Answer from support is sent.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Incorrect username'}, status=status.HTTP_404_NOT_FOUND)
    except CustomUser.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def number_of_courses(request, teacher: int):
    courses = Course.objects.filter(teacher_id_id=teacher).count()
    return Response(courses, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def number_of_students(request, teacher: int):
    courses = Course.objects.filter(teacher_id_id=teacher).values_list('id', flat=True)
    students = CourseStudent.objects.filter(course_id__in=courses).count()

    return Response(students, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def number_of_comments(request, teacher: int):
    courses = Course.objects.filter(teacher_id_id=teacher)
    comments = Comment.objects.filter(course_id__in=courses).count()
    return Response(comments, status=status.HTTP_200_OK)



#payment
stripe.api_key = 'sk_test_51P9C4ORuoMQmk41RPNaoCLdLUEKPQbuLB07oU9C70DUKfHeNj89uPVa9a1UwLybCr0JuO4VB7r2sfHAZgM5ZPZxQ00bajRfI7A'


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request, course: int):
    email = request.data['email']
    course = Course.objects.get(id=course)

    serializer = CardInformationSerializer(data=request.data)
    if serializer.is_valid():
        data_dict = serializer.data

    card_details = {
        'email': email,
        'card_number': data_dict['card_number'],
        'expiry_month': data_dict['expiry_month'],
        'expiry_year': data_dict['expiry_year'],
        'cvc': data_dict['cvc'],
    }

    payment_intent = stripe.PaymentIntent.create(
        amount=course.cost,
        currency='usd',
        payment_method_types=['card'],
        receipt_email=email,
        confirm=True
    )

    payment_intent_modified = stripe.PaymentIntent.modify(
        payment_intent['id'],
        payment_method=card_details,
    )
    try:
        payment_confirm = stripe.PaymentIntent.confirm(
            payment_intent['id']
        )
        payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
    except:
        payment_intent_modified = stripe.PaymentIntent.retrieve(payment_intent['id'])
        payment_confirm = {
            "stripe_payment_error": "Failed",
            "code": payment_intent_modified['last_payment_error']['code'],
            "message": payment_intent_modified['last_payment_error']['message'],
            'status': "Failed"
        }
    if payment_intent_modified and payment_intent_modified['status'] == 'succeeded':
        response = {
            'message': "Card Payment Success",
            'status': status.HTTP_200_OK,
            "card_details": card_details,
            "payment_intent": payment_intent_modified,
            "payment_confirm": payment_confirm
        }
        return Response(response, status=status.HTTP_200_OK)
    else:
        response = {
            'message': "Card Payment Failed",
            'status': status.HTTP_400_BAD_REQUEST,
            "card_details": card_details,
            "payment_intent": payment_intent_modified,
            "payment_confirm": payment_confirm
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)




