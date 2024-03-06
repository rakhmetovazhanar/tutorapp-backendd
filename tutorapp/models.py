from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    username = models.EmailField(null=False, blank=False, unique=True)
    role = models.CharField(max_length=20)

class Teacher(models.Model):
    GENDER_CHOICE = (
        ('Женский', 'Женский'), 
        ('Мужской', 'Мужской'),
    )
    EXP_CHOICE = (
        ('От 1 года до 3 лет', 'От 1 года до 3 лет'),
        ('1 год', '1 год'),
        ('Нет опыта', 'Нет опыта'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="teacher_account")
    first_name = models.CharField(max_length=250, blank=False, null=False)
    last_name = models.CharField(max_length=250, blank=False, null=False)
    city = models.CharField(max_length=250, null=False, blank=False)
    age = models.IntegerField(blank=False, null=False)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE, null=False)
    experience_year = models.CharField(max_length=50, choices=EXP_CHOICE)
    phone_number = models.CharField(max_length=250, blank=False, null=False)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="student_account")
    name = models.CharField(max_length=250, blank=False, null=False)
    surname = models.CharField(max_length=250, blank=False, null=False)
    city = models.CharField(max_length=250, null=False, blank=False)
    phone_number = models.CharField(max_length=250, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)

class Category(models.Model):
    category_name = models.CharField(max_length=250, blank=False, null=False)  

class Course(models.Model):
    category_id = models.OneToOneField(Category, on_delete=models.CASCADE, related_name="course_category")
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="teacher_courses")
    course_name = models.CharField(max_length=250, null=False, blank=False)
    course_description = models.CharField(max_length=250, null=False, blank=False)
    course_cost = models.IntegerField(null=False, blank=False)
    
