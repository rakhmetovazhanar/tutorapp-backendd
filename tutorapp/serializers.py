from rest_framework import serializers
from .models import CustomUser, EmailCode, Course


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'city', 'experience', 'gender', 'password', 'name',
                  'phone_number', 'surname', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            age=validated_data.pop('age'),
            city=validated_data.pop('city'),
            experience=validated_data.pop('experience', None),
            gender=validated_data.pop('gender', None),
            password=validated_data.pop('password'),
            name=validated_data.pop('name'),
            phone_number=validated_data.pop('phone_number'),
            surname=validated_data.pop('surname'),
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
        fields = ['age', 'city', 'name', 'phone_number', 'surname', 'username', 'role']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'city', 'experience', 'gender', 'name',
                  'phone_number', 'surname', 'username', 'role']


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description', 'level', 'language', 'teacher_id', 'category_id']

    def create(self, validated_data):
        course = Course.objects.create(
            name=validated_data.pop('name'),
            description=validated_data.pop('description'),
            level=validated_data.pop('level'),
            language=validated_data.pop('language'),
        )
        return course

