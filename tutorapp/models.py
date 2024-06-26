import os
import uuid
from datetime import date

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class CustomUser(AbstractUser):
    GENDER_CHOICE = (
        ('Женщина', 'Женщина'),
        ('Мужчина', 'Мужчина'),
    )
    EXP_CHOICE = (
        ('Больше', 'Больше'),
        ('От 3 до 5 лет', 'От 3 до 5 лет'),
        ('До 3 лет', 'До 3 лет'),
        ('Нет опыта', 'Нет опыта'),
    )

    first_name = models.CharField(max_length=250, blank=False, null=False)
    last_name = models.CharField(max_length=250, blank=False, null=False)
    username = models.EmailField(null=False, blank=False, unique=True)
    password = models.CharField(null=False, blank=False)
    age = models.IntegerField(null=False, blank=False)
    city = models.CharField(null=False, blank=False)
    role = models.CharField(null=False, blank=False)
    experience = models.CharField(null=True, blank=False, choices=EXP_CHOICE)
    gender = models.CharField(null=True, blank=False, choices=GENDER_CHOICE)
    phone_number = models.CharField(null=False, blank=False, max_length=25)
    bio = models.CharField(null=True, blank=True, max_length=500)
    profile_picture = models.ImageField(null=True, default=None, blank=True, upload_to='profile_pictures/')


@receiver(post_delete, sender=CustomUser)
def delete_user_picture(sender, instance, **kwargs):
    if instance.profile_picture:
        path = instance.profile_picture.path
        if os.path.exists(path):
            os.remove(path)


'''file_path = '/media/profile_pictures/'

if os.path.exists(file_path):
    print("Picture exists")
else:
    print("Picture doesnt exist")'''


class EmailCode(models.Model):
    user = models.ForeignKey(CustomUser, max_length=25, blank=False, null=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000, blank=False, unique=True)


class Category(models.Model):
    CATEGORY_CHOICE = (
        ('Programming Language', 'Programming Language'),
        ('Database Management', 'Database Management'),
        ('Graphic Design and Multimedia', 'Graphic Design and Multimedia'),
        ('Finance and Economics', 'Finance and Economics'),
        ('Networking and Security', 'Networking and Security'),
        ('Mathematics and Statistics', 'Mathematics and Statistics'),
        ('Web Development', 'Web Development'),
        ('Shell Scripting and Linux', 'Shell Scripting and Linux'),
        ('Functional Programming', 'Functional Programming'),
        ('Game Development', 'Game Development'),
        ('History and Social Studies', 'History and Social Studies'),
        ('Mobile App Development', 'Mobile App Development'),
    )
    category_name = models.CharField(max_length=250, blank=False, null=False, choices=CATEGORY_CHOICE)


class Course(models.Model):
    LEVEL_CHOICE = (
        ('Легкий', 'Легкий'),
        ('Средний', 'Средний'),
        ('Сложный', 'Сложный'),
    )
    LANGUAGE_CHOICE = (
        ('Казахский', 'Казахский'),
        ('Русский', 'Русский'),
        ('Английский', 'Английский'),
    )
    teacher_id = models.ForeignKey(CustomUser, max_length=25, blank=False, null=False, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, max_length=250, blank=False, null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, blank=False, null=False)
    description = models.CharField(max_length=1000, blank=False, null=False)
    level = models.CharField(max_length=250, blank=False, null=False, choices=LEVEL_CHOICE)
    language = models.CharField(max_length=250, blank=False, null=False, choices=LANGUAGE_CHOICE)
    day_time = models.CharField(max_length=250, blank=False, null=False)
    cost = models.IntegerField(blank=False, null=True, default=0)
    avg_rating = models.FloatField(blank=False, null=True, default=None)


class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    comment = models.CharField(max_length=1000, blank=False, null=False)
    created = models.DateField(auto_now_add=True)


class CourseRating(models.Model):
    RATING_CHOICE = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, choices=RATING_CHOICE)


@receiver(post_save, sender=CourseRating)
def course_avr_rating(sender, instance, **kwargs):
    course = instance.course_id
    ratings_count = CourseRating.objects.filter(course_id=course).count()
    if ratings_count >= 1:
        avg_rating = CourseRating.objects.filter(course_id=course).aggregate(Avg('rating'))['rating__avg']
        avg_rating = round(avg_rating, 1)
        course.avg_rating = avg_rating
        course.save()


class CourseStudent(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)


class VideoConference(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE )
    conference = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
