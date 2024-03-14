from rest_framework import serializers
from .models import CustomUser, EmailCode, Course, Category, Lesson


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'city', 'experience', 'gender', 'password', 'first_name',
                  'phone_number', 'last_name', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
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
        fields = ['age', 'city', 'first_name', 'phone_number', 'last_name', 'username', 'role']


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['age', 'city', 'experience', 'gender', 'first_name',
                  'phone_number', 'last_name', 'username', 'role']


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['teacher_id', 'category_id', 'name', 'description', 'level', 'language']

    def create(self, validated_data):
        course = Course.objects.create(
            teacher_id=validated_data.pop('teacher_id'),
            category_id=validated_data.pop('category_id'),
            name=validated_data.pop('name'),
            description=validated_data.pop('description'),
            level=validated_data.pop('level'),
            language=validated_data.pop('language'),
        )
        return course


class AddLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['course_id', 'start_date_time', 'end_date_time']

    def create(self, validated_data):
        lesson = Lesson.objects.create(
            course_id=validated_data.pop('course_id'),
            start_date_time=validated_data.pop('start_date_time'),
            end_date_time=validated_data.pop('end_date_time')
        )
        return lesson


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category_id', 'name', 'description', 'level', 'language']

    def update(self, instance, validated_data):
        instance.level = validated_data.pop('level', instance.level)
        instance.language = validated_data.pop('language', instance.language)
        instance.description = validated_data.pop('description', instance.description)
        instance.name = validated_data.pop('name', instance.name)
        instance.category_id = validated_data.pop('category_id', instance.category_id)

        return instance
