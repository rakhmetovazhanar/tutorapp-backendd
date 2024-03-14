import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser, EmailCode, Course, Category
from .serializers import (CustomUserSerializer, EmailUserSerializer, StudentProfileSerializer, TeacherProfileSerializer,
                          AddCourseSerializer, CourseUpdateSerializer)
from rest_framework.permissions import IsAuthenticated
from django.conf.global_settings import EMAIL_HOST_USER


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
                    teacher_data = CustomUserSerializer(user).data
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
                    student_data = CustomUserSerializer(user).data
                    response_data['data'] = student_data

            return Response(response_data)
        else:
            return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    if request.method == 'POST':
        try:
            '''token_key = request.auth.key
            token = Token.objects.get(key=token_key)
            token.delete()'''
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
def student_profile(request):
    user = request.user
    print(user)
    profile_info = CustomUser.objects.get(username=user)
    serializer = StudentProfileSerializer(profile_info)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_profile(request):
    user = request.user

    profile_info = CustomUser.objects.get(username=user)
    serializer = TeacherProfileSerializer(profile_info)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_course(request):
    course = Course.objects.get()


    serializer = AddCourseSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.filter(teacher_id=request.user.id)

    return Response(AddCourseSerializer(courses, many=True).data, status=status.HTTP_200_OK)


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



