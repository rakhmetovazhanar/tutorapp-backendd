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
    user = models.ForeignKey(CustomUser, max_length=25, blank=False, null=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000, blank=False, unique=True)


class Category(models.Model):
    CATEGORY_CHOICE = (
        ('Programming Language', 'Programming Language'),
        ('Math', 'Math'),
        ('Chemistry', 'Chemistry'),
        ('Physics', 'Physics'),
        ('Languages', 'Languages'),
    )
    category_name = models.CharField(max_length=250, blank=False, null=False, choices=CATEGORY_CHOICE)


class Course(models.Model):
    teacher_id = models.ForeignKey(CustomUser, max_length=25, blank=False, null=False, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, max_length=250, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=250, blank=False, null=False)
    level = models.CharField(max_length=250, blank=False, null=False)
    language = models.CharField(max_length=250, blank=False, null=False)




