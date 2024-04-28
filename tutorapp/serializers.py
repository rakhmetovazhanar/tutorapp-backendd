import uuid
from rest_framework import serializers
from .models import CustomUser, EmailCode, Course, Category, CourseRating, CourseStudent, Comment, VideoConference
import django.contrib.auth.password_validation as validators
from django.core.exceptions import ValidationError
import datetime


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'city', 'experience', 'gender', 'password', 'first_name',
                  'phone_number', 'last_name', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser.objects.create_user(
            age=validated_data.pop('age'),
            city=validated_data.pop('city'),
            experience=validated_data.pop('experience', None),
            gender=validated_data.pop('gender', None),
            password=password,
            first_name=validated_data.pop('first_name'),
            phone_number=validated_data.pop('phone_number'),
            last_name=validated_data.pop('last_name'),
            username=validated_data.pop('username'),
            role=validated_data.pop('role')
        )
        try:
            validators.validate_password(password=password, user=user)
        except ValidationError as e:
            user.delete()
            raise serializers.ValidationError({'password': e.messages})

        return user


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'age', 'city', 'experience', 'gender', 'password', 'first_name',
                  'phone_number', 'last_name', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            id=validated_data.pop('id'),
            age=validated_data.pop('age'),
            city=validated_data.pop('city'),
            experience=validated_data.pop('experience', None),
            gender=validated_data.pop('gender', None),
            password=validated_data.pop('password'),
            first_name=validated_data.pop('first_name'),
            phone_number=validated_data.pop('phone_number'),
            last_name=validated_data.pop('last_name'),
            username=validated_data.pop('username'),
            role=validated_data.pop('role')
        )
        return user


class EmailUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailCode
        fields = '__all__'

    def create(self, validated_data):
        print(validated_data)
        email_code = EmailCode(
            user=validated_data.pop('user'),
            code=validated_data.pop('code')
        )

        return email_code


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'city', 'first_name', 'phone_number', 'last_name', 'username', 'role', 'profile_picture']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['role', 'first_name', 'last_name', 'username',
                  'phone_number', 'city', 'experience', 'age', 'bio', 'profile_picture']


class UpdateTeacherProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'experience', 'age', 'bio', 'profile_picture']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.phone_number = validated_data.pop('phone_number', instance.phone_number)
        instance.city = validated_data.pop('city', instance.city)
        instance.experience = validated_data.pop('experience', instance.experience)
        instance.age = validated_data.pop('age', instance.age)
        instance.bio = validated_data.pop('bio', instance.bio)
        instance.profile_picture = validated_data.pop('profile_picture', instance.profile_picture)

        instance.save()

        return instance


class UpdateStudentProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'age', 'profile_picture']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.phone_number = validated_data.pop('phone_number', instance.phone_number)
        instance.city = validated_data.pop('city', instance.city)
        instance.age = validated_data.pop('age', instance.age)
        instance.profile_picture = validated_data.pop('profile_picture', instance.profile_picture)

        instance.save()

        return instance


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['teacher_id', 'category_id', 'name', 'description', 'level', 'language', 'cost', 'day_time']

    def create(self, validated_data):
        course = Course.objects.create(
            teacher_id=validated_data.pop('teacher_id'),
            name=validated_data.pop('name'),
            description=validated_data.pop('description'),
            category_id=validated_data.pop('category_id'),
            level=validated_data.pop('level'),
            language=validated_data.pop('language'),
            cost=validated_data.pop('cost'),
            day_time=validated_data.pop('day_time')
        )
        return course


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category_id', 'name', 'description', 'level', 'language', 'cost', 'day_time']

    def update(self, instance, validated_data):
        instance.level = validated_data.pop('level', instance.level)
        instance.language = validated_data.pop('language', instance.language)
        instance.description = validated_data.pop('description', instance.description)
        instance.name = validated_data.pop('name', instance.name)
        instance.category_id = validated_data.pop('category_id', instance.category_id)
        instance.day_time = validated_data.pop('day_time', instance.day_time)
        instance.cost = validated_data['cost']

        instance.save()

        return instance


class EnrollToCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStudent
        fields = ['course_id', 'student_id']


class GetStudentCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'cost', 'day_time', 'avg_rating']


class RateCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseRating
        fields = ['rating', 'course_id', 'user_id']


class StudentCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'name']


class ClientsInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'phone_number']


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['user', 'course', 'comment']


class VideoConferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoConference
        fields = ['course', 'conference']


#payment
def check_expiry_month(value):
    if not 1 <= int(value) <= 12:
        raise serializers.ValidationError("Invalid expiry month")


def check_expiry_year(value):
    today = datetime.datetime.now()
    if not int(value) >= today.year:
        raise serializers.ValidationError("Invalid expiry year")


def check_payment_method(value):
    payment_method = value.lower()
    if payment_method not in ["card"]:
        raise serializers.ValidationError("Invalid method payment")


def check_cvc(value):
    if not 3 <= len(value) <= 4:
        raise serializers.ValidationError("Invalid length of cvc")


class CardInformationSerializer(serializers.Serializer):
    card_number = serializers.CharField(max_length=100, required=True)
    expiry_month = serializers.CharField(max_length=100, required=True, validators=[check_expiry_month])
    expiry_year = serializers.CharField(max_length=100, required=True, validators=[check_expiry_year])
    cvc = serializers.CharField(max_length=100, required=True, validators=[check_cvc])