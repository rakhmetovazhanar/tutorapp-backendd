from rest_framework import serializers
from .models import CustomUser, EmailCode, Course, Category, Lesson, CourseStudent

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
        instance.experience= validated_data.pop('experience', instance.experience)
        instance.age = validated_data.pop('age', instance.age)
        instance.bio = validated_data.pop('bio'),
        instance.profile_picture = validated_data.pop('profile_picture')

        instance.save()

        return instance


class UpdateStudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'city', 'age', 'profile_picture']

    def update(self, instance, validated_data):
        instance.first_name = validated_data.pop('first_name', instance.first_name)
        instance.last_name = validated_data.pop('last_name', instance.last_name)
        instance.phone_number = validated_data.pop('phone_number', instance.phone_number)
        instance.city = validated_data.pop('city', instance.city)
        instance.age = validated_data.pop('age', instance.age),
        instance.profile_picture = validated_data.pop('profile_picture')

        instance.save()

        return instance


class AddCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['teacher_id', 'category_id', 'name', 'description', 'level', 'language', 'cost']

    def create(self, validated_data):
        course = Course.objects.create(
            teacher_id=validated_data.pop('teacher_id'),
            name=validated_data.pop('name'),
            description=validated_data.pop('description'),
            category_id=validated_data.pop('category_id'),
            level=validated_data.pop('level'),
            language=validated_data.pop('language'),
            cost=validated_data.pop('cost'),
        )
        return course


class CourseUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['category_id', 'name', 'description', 'level', 'language', 'cost']

    def update(self, instance, validated_data):
        instance.level = validated_data.pop('level', instance.level)
        instance.language = validated_data.pop('language', instance.language)
        instance.description = validated_data.pop('description', instance.description)
        instance.name = validated_data.pop('name', instance.name)
        instance.category_id = validated_data.pop('category_id', instance.category_id)
        instance.cost = validated_data['cost']

        instance.save()

        return instance


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


class EnrollToCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseStudent
        fields = ['course', 'student']

    def create(self, validated_data):
        course_student = CourseStudent.objects.create(
            course=validated_data.pop('course'),
            student=validated_data.pop('student')
        )
        return course_student


class GetStudentCoursesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['name', 'description', 'cost']


