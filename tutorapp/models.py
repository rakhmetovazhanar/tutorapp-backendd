from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg


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
    description = models.CharField(max_length=250, blank=False, null=False)
    level = models.CharField(max_length=250, blank=False, null=False, choices=LEVEL_CHOICE)
    language = models.CharField(max_length=250, blank=False, null=False, choices=LANGUAGE_CHOICE)
    day_time = models.CharField(max_length=250, blank=False, null=False)
    cost = models.IntegerField(blank=False, null=True, default=0)
    avg_rating = models.FloatField(blank=False, null=True, default=None)

    def average_rating(self) -> float:
        return CourseRating.objects.filter(course_id=self).aggregate(Avg('rating'))['rating__avg'] or 0


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

    def __str__(self):
        return f"{self.course_id.avg_rating}: {self.rating}"


class Lesson(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, max_length=250, blank=False, null=False)
    start_date_time = models.DateTimeField(max_length=250, blank=False, null=False)
    end_date_time = models.DateTimeField(max_length=250, blank=False, null=False)


class CourseStudent(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

