import random
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import CustomUser, EmailCode, Course, Category, Lesson, CourseStudent
from .serializers import (CustomUserSerializer, EmailUserSerializer, StudentProfileSerializer, TeacherProfileSerializer,
                          AddCourseSerializer, CourseUpdateSerializer, AddLessonSerializer,
                          UpdateTeacherProfileSerializer, EnrollToCourseSerializer, GetStudentCoursesSerializer,
                          LoginUserSerializer)
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
def student_profile(request):
    user = request.user
    print(user)
    profile_info = CustomUser.objects.get(username=user)
    serializer = StudentProfileSerializer(profile_info)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def teacher_profile(request, teacher: int):
    teacher = CustomUser.objects.get(id=teacher)

    if request.user.id == teacher.id:
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


'''@api_view(['GET'])
def get_categories(request):
    categories = Category.objects.get('category_name', 'id')
    return Response(categories, status=status.HTTP_200_OK)'''


@api_view(['GET'])
def get_teacher_courses(request):
    courses = Course.objects.filter(teacher_id=request.user.id).values(
        'id', 'teacher_id_id', 'name', 'description', 'cost'
    )

    return Response(courses, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_course(request, course: int):
    try:
        course = Course.objects.get(id=course)
        print(course)
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
        return Response({'message': 'Profile not found!'}, status=status)


@api_view(['DELETE'])
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
def enroll_to_course(request, student: int):
    student = CustomUser.objects.get(id=student)

    if student.id == request.user.id:
        serializer = EnrollToCourseSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_student_courses(request, student: int):
    #if CourseStudent.student_id == student:
    course_student = Course.objects.filter(id=CourseStudent.course_id).values(id)

    serializer = GetStudentCoursesSerializer(course_student)
    if serializer.is_valid():
        serializer.get_value()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({'message': 'You do not have courses yet!'}, status=status.HTTP_400_BAD_REQUEST)

    #print(course_student)
    #return Response(course_student , status=status.HTTP_200_OK)
    #return Response({'message': 'You do not have course'}, status=status.HTTP_404_NOT_FOUND)

    #courses = Course.objects.filter(id=student_courses).get('course_id', 'name')

    '''if courses:
        return Response(courses, status=status.HTTP_200_OK)
    return Response({'message': "You do not have courses!"}, status=status.HTTP_404_NOT_FOUND)'''





