from rest_framework import serializers
from .models import CustomUser


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


'''class TeacherSerializer(serializers.ModelSerializer):
    # username = CustomUserSerializer()
    # password = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'age', 'gender', 'city', 'phone_number', 'experience_year', 'username',
                  'password']

    def create(self, validated_data):
        user_data = validated_data.pop('username', 'password')
        user = CustomUser.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Student
        fields = ['age', 'city', 'password', 'name', 'password', 'phone_number', 'surname', 'username']

    def create(self, validated_data):
        user_data = validated_data.pop('username', 'password')
        user = CustomUser.objects.create_user(**user_data, role='student')
        student = Student.objects.create(user=user, phone_number=validated_data.pop('phone_number'),
                                         city=validated_data.pop('city'), age=validated_data.pop('age'),
                                         surname=validated_data('surname'))
        return student


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)'''


'''class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'course_description', 'course_cost']

        def create(self):
            course = Course.objects.create(**validated_data)
           '''
