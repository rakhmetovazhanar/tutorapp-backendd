# Generated by Django 5.0.1 on 2024-03-15 13:57

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0009_customuser_bio'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseStudent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutorapp.course')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
