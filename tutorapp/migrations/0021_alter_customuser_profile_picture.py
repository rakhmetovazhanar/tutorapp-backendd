# Generated by Django 5.0.1 on 2024-03-28 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutorapp', '0020_course_day_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='profile_pictures/'),
        ),
    ]