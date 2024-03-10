from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICE = (
        ('Женщина', 'Женщина'),
        ('Мужчина', 'Мужчина'),
    )
    EXP_CHOICE = (
        ('От 1 года до 3 лет', 'От 1 года до 3 лет'),
        ('1 год', '1 год'),
        ('Нет опыта', 'Нет опыта'),
    )
    name = models.CharField(max_length=250, blank=False, null=False)
    surname = models.CharField(max_length=250, blank=False, null=False)
    username = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    city = models.CharField(null=False, blank=False)
    role = models.CharField(null=False, blank=False)
    experience = models.CharField(null=True, blank=False, choices=EXP_CHOICE)
    gender = models.CharField(null=True, blank=False, choices=GENDER_CHOICE)
    phone_number = models.CharField(null=False, blank=False, max_length=25)


class EmailCode(models.Model):
    user = models.OneToOneField(CustomUser, max_length=25, blank=False, null=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000, blank=False, unique=True)


'''class Teacher(models.Model):
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
    age = models.IntegerField(blank=False, null=False)'''


class Category(models.Model):
    category_name = models.CharField(max_length=250, blank=False, null=False)
