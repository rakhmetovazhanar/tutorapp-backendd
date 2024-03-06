from rest_framework import serializers
from .models import CustomUser, Teacher, Student

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        role = validated_data.pop('role')
        user = CustomUser.objects.create_user(**validated_data, role=role)
        return user

class TeacherSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'age', 'gender', 'city', 'phone_number', 'experience_year', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = CustomUser.objects.create_user(**user_data)
        teacher = Teacher.objects.create(user=user, **validated_data)
        return teacher

class StudentSerializer(serializers.ModelSerializer):
    #user = CustomUserSerializer()

    class Meta:
        model = Student
        fields = ['age', 'city', 'name', 'password', 'phone_number', 'surname', 'username']

    def create(self, validated_data):
        user_data = {'username': validated_data.pop('username'), 'password': validated_data.pop('password')}
        user = CustomUser.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student
    
class ChangePasswordSerializer (serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)  

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)      

'''class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['course_name', 'course_description', 'course_cost']

        def create(self):
            course = Course.objects.create(**validated_data)
           '''